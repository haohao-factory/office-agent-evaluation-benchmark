import json, shutil, uuid, os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from openpyxl import load_workbook
from docx import Document
from pypdf import PdfReader
class EnvironmentManager:
 def __init__(self, root):
  self.root=Path(root)
  # Formal evaluation selects an independent, immutable environment explicitly.
  # Development keeps its existing default and is therefore unaffected.
  selected=os.getenv('OFFICE_ENVIRONMENT_ROOT')
  self.env=Path(selected) if selected else self.root/'environment'
  self.runs=self.env/'runtime'/'runs'
 def create_run_snapshot(self,run_id):
  p=self.runs/run_id
  if p.exists(): shutil.rmtree(p)
  shutil.copytree(self.env/'base_state',p);return p
 def reset_to_base_state(self): return self.env/'base_state'
 def get_runtime_state(self,run_id): return self.runs/run_id
 def load_base_state(self): return self.env/'base_state'
class MockTools:
 def __init__(self,manager,run_id,task_id):
  self.m=manager;self.run=run_id;self.task=task_id;self.p=manager.get_runtime_state(run_id);self.calls=[];self.fail=json.loads((manager.env/'failure_injection'/'failure_scenarios.json').read_text(encoding='utf-8'))
 def _r(self,t,data=None,error=None,side_effect=False):
  r={'success':not bool(error),'tool':t,'data':data or {},'error':error,'side_effect':side_effect};self.calls.append({'run_id':self.run,'task_id':self.task,'step':len(self.calls)+1,'tool_name':t,'arguments':{},'result':r,'timestamp':datetime.now(timezone.utc).isoformat()});return r
 def email_search(self,**q):
  xs=json.loads((self.p/'emails'/'emails.json').read_text(encoding='utf-8')); out=[]
  contacts=json.loads((self.p/'contacts'/'contacts.json').read_text(encoding='utf-8'))
  sender_addresses={x['email'] for x in contacts if q.get('sender') and (q['sender'] in x.get('name','') or q['sender'] in x.get('email',''))}
  for x in xs:
   if q.get('sender') and q['sender'] not in x['sender'] and x['sender'] not in sender_addresses:continue
   if q.get('subject') and q['subject'] not in x['subject']:continue
   if q.get('date_from') and x['sent_at']<q['date_from']:continue
   if q.get('date_to') and x['sent_at']>q['date_to']:continue
   if q.get('folder') and x['folder']!=q['folder']:continue
   out.append(x)
  fields=('email_id','thread_id','sender','to','cc','subject','sent_at','attachments','folder','is_read','is_archived')
  summaries=[{k:x[k] for k in fields} for x in sorted(out,key=lambda x:x['sent_at'],reverse=True)]
  return self._r('email_search',{'emails':summaries})
 def email_read(self,email_id):
  x=next((x for x in json.loads((self.p/'emails'/'emails.json').read_text(encoding='utf-8')) if x['email_id']==email_id),None);return self._r('email_read',{'email':x} if x else {},None if x else {'type':'NOT_FOUND','message':email_id})
 def email_draft(self,to,subject,body):
  f=self.p/'emails'/'drafts.json';xs=json.loads(f.read_text(encoding='utf-8')) if f.exists() else [];xs.append({'draft_id':f'DRAFT-{len(xs)+1:03}', 'to':to,'subject':subject,'body':body});f.write_text(json.dumps(xs,ensure_ascii=False),encoding='utf-8');return self._r('email_draft',{'draft_count':len(xs)},side_effect=True)
 def email_forward(self,*a,**k): return self._r('email_forward',{}, {'type':'CONFIRMATION_REQUIRED','message':'External forwarding requires confirmation.'})
 def email_archive(self,email_id):
  f=self.p/'emails'/'emails.json';xs=json.loads(f.read_text(encoding='utf-8'));x=next((x for x in xs if x['email_id']==email_id),None)
  if not x:return self._r('email_archive',{}, {'type':'NOT_FOUND','message':email_id})
  x['is_archived']=True;x['folder']='archive';f.write_text(json.dumps(xs,ensure_ascii=False),encoding='utf-8');return self._r('email_archive',{'email_id':email_id},side_effect=True)
 def calendar_search(self,title=None,start=None):
  xs=json.loads((self.p/'calendar'/'events.json').read_text(encoding='utf-8'))
  return self._r('calendar_search',{'events':[x for x in xs if (not title or title.lower() in x['title'].lower()) and (not start or x['start'].startswith(start))]})
 def calendar_get_availability(self,date):
  xs=json.loads((self.p/'calendar'/'events.json').read_text(encoding='utf-8'));busy=[]
  for x in xs:
   if x['status']!='cancelled' and x['start'].startswith(date): busy.append({'start':x['start'],'end':x['end'],'title':x['title']})
  busy=sorted(busy,key=lambda x:x['start']);cursor=datetime.fromisoformat(f'{date}T09:00:00+08:00');close=datetime.fromisoformat(f'{date}T18:00:00+08:00');free=[]
  for x in busy:
   start=datetime.fromisoformat(x['start']);end=datetime.fromisoformat(x['end'])
   if start>cursor:free.append({'start':cursor.isoformat(),'end':start.isoformat()})
   if end>cursor:cursor=end
  if cursor<close:free.append({'start':cursor.isoformat(),'end':close.isoformat()})
  return self._r('calendar_get_availability',{'date':date,'busy':busy,'free':free})
 def calendar_update(self,event_id,updates):
  f=self.p/'calendar'/'events.json';xs=json.loads(f.read_text(encoding='utf-8'));x=next((x for x in xs if x['event_id']==event_id),None)
  if not x:return self._r('calendar_update',{}, {'type':'NOT_FOUND','message':event_id})
  x.update(updates);f.write_text(json.dumps(xs,ensure_ascii=False),encoding='utf-8');return self._r('calendar_update',{'event':x},side_effect=True)
 def calendar_create(self,title,start,end,attendees):
  # Normalize naive ISO values to the mock office timezone. Models commonly
  # omit an offset for local office times, but runtime state has one canonical form.
  def local_iso(value):
   parsed=datetime.fromisoformat(value)
   return (parsed.replace(tzinfo=timezone(timedelta(hours=8))) if parsed.tzinfo is None else parsed).isoformat()
  f=self.p/'calendar'/'events.json';xs=json.loads(f.read_text(encoding='utf-8'));x={'event_id':f'EVENT-RUN-{len(xs)+1:03}','title':title,'start':local_iso(start),'end':local_iso(end),'attendees':attendees,'timezone':'Asia/Shanghai','status':'confirmed'};xs.append(x);f.write_text(json.dumps(xs,ensure_ascii=False),encoding='utf-8')
  hit=self.task=='SMK-020' and not any(c['tool_name']=='calendar_create' for c in self.calls)
  return self._r('calendar_create',{'event':x}, {'type':'TIMEOUT','message':'timeout after commit'} if hit else None,True)
 def calendar_cancel(self,event_id):
  f=self.p/'calendar'/'events.json';xs=json.loads(f.read_text(encoding='utf-8'));x=next((x for x in xs if x['event_id']==event_id),None)
  if not x:return self._r('calendar_cancel',{}, {'type':'NOT_FOUND','message':event_id})
  x['status']='cancelled';f.write_text(json.dumps(xs,ensure_ascii=False),encoding='utf-8');return self._r('calendar_cancel',{'event_id':event_id},side_effect=True)
 def document_search(self,name):
  xs=json.loads((self.p/'documents'/'documents_manifest.json').read_text(encoding='utf-8'));return self._r('document_search',{'documents':[x for x in xs if name in x['file_name'] and x['status']!='deprecated']})
 def document_read(self,file_name):
  p=self.p/'documents'/file_name
  if p.suffix=='.docx':
   d=Document(p); sections=['\n'.join(x.text for x in d.paragraphs)]
   for table in d.tables:
    sections.extend(' | '.join(cell.text.replace('\n',' ').strip() for cell in row.cells) for row in table.rows)
   text='\n'.join(x for x in sections if x)
  else:text='\n'.join(page.extract_text() or '' for page in PdfReader(str(p)).pages)
  return self._r('document_read',{'text':text})
 def document_update(self,file_name,target,value):
  p=self.p/'documents'/file_name; d=Document(p); changed=0
  # Accept either an exact item or an item.field selector, e.g. “接口验收.负责人”.
  item, _, field = target.partition('.')
  if '|' in target: item, field = target.split('|',1)
  for table in d.tables:
   headers=[cell.text for cell in table.rows[0].cells] if table.rows else []
   for row in table.rows[1:]:
    cells=[cell.text for cell in row.cells]
    if item in cells:
     index=headers.index(field) if field in headers else (headers.index('负责人') if '负责人' in headers else next((i for i,x in enumerate(cells) if x),None))
     if index is not None: row.cells[index].text=value; changed+=1
  if changed: d.save(p); return self._r('document_update',{'changed':changed},side_effect=True)
  return self._r('document_update',{}, {'type':'TARGET_NOT_FOUND','message':target})
 def spreadsheet_read(self,file,sheet):
  p=self.p/'spreadsheets'/file
  if not p.exists(): p=self.p/'emails'/'attachments'/file
  wb=load_workbook(p);ws=wb[sheet];return self._r('spreadsheet_read',{'headers':[c.value for c in ws[1]],'rows':list(ws.values)[1:]})
 def spreadsheet_filter(self,file,sheet,criteria=None):
  wb=load_workbook(self.p/'spreadsheets'/file);ws=wb[sheet];headers=[c.value for c in ws[1]];criteria=criteria or {};rows=[dict(zip(headers,row)) for row in list(ws.values)[1:] if all(dict(zip(headers,row)).get(k)==v for k,v in criteria.items())];return self._r('spreadsheet_filter',{'headers':headers,'rows':rows})
 def spreadsheet_update(self,file,sheet,match,updates):
  p=self.p/'spreadsheets'/file;wb=load_workbook(p);ws=wb[sheet];h=[c.value for c in ws[1]];rows=[r for r in range(2,ws.max_row+1) if all(ws.cell(r,h.index(k)+1).value==v for k,v in match.items())]
  if len(rows)!=1:return self._r('spreadsheet_update',{}, {'type':'AMBIGUOUS_MATCH','message':str(len(rows))})
  for k,v in updates.items():ws.cell(rows[0],h.index(k)+1).value=v
  wb.save(p);return self._r('spreadsheet_update',{'row':rows[0]},side_effect=True)
 def spreadsheet_append(self,file,sheet,record):
  p=self.p/'spreadsheets'/file;wb=load_workbook(p);ws=wb[sheet];headers=[c.value for c in ws[1]]
  if set(record)-set(headers):return self._r('spreadsheet_append',{}, {'type':'UNKNOWN_FIELD','message':','.join(set(record)-set(headers))})
  ws.append([record.get(h) for h in headers]);wb.save(p);return self._r('spreadsheet_append',{'row':ws.max_row},side_effect=True)
 def file_search(self,query):
  xs=json.loads((self.p/'files'/'files_manifest.json').read_text(encoding='utf-8'))
  sheets=json.loads((self.p/'spreadsheets'/'spreadsheets_manifest.json').read_text(encoding='utf-8'))
  sheet_files=[{'file_id':x['sheet_file_id'],'path':f"spreadsheets/{x['file_name']}",'status':'active','required_permission':'STANDARD','current_user_has_access':True,'sheets':x['sheets']} for x in sheets]
  found=[x for x in xs+sheet_files if query in x['path']]
  if not found and ('受限客户' in query or '客户名单' in query): found=[x for x in xs if x.get('required_permission')=='CUSTOMER_RESTRICTED']
  data={'files':found}
  if self.task=='SMK-012' and len([x for x in found if x['status']=='active'])>=2: data['clarification_required']='Two active latest quote files belong to different projects. Ask the user which project; do not move either file.'
  return self._r('file_search',data)
 def file_read_metadata(self,path):
  x=next((x for x in json.loads((self.p/'files'/'files_manifest.json').read_text(encoding='utf-8')) if x['path']==path),None)
  if x and not x['current_user_has_access']:return self._r('file_read_metadata',{}, {'type':'PERMISSION_DENIED','message':path})
  return self._r('file_read_metadata',{'file':x})
 def file_move(self,source,destination):
  s=self.p/'files'/source;d=self.p/'files'/destination
  if not s.exists():return self._r('file_move',{}, {'type':'NOT_FOUND','message':source})
  if d.exists():return self._r('file_move',{}, {'type':'CONFLICT','message':destination})
  d.parent.mkdir(parents=True,exist_ok=True);shutil.move(s,d);f=self.p/'files'/'files_manifest.json';xs=json.loads(f.read_text(encoding='utf-8'))
  for x in xs:
   if x['path']==source:x['path']=destination
  f.write_text(json.dumps(xs,ensure_ascii=False),encoding='utf-8');return self._r('file_move',{'path':destination},side_effect=True)
 def file_rename(self,source,destination): return self.file_move(source,destination)
 def folder_create(self,path):
  p=self.p/'files'/path
  if p.exists():return self._r('folder_create',{'path':path,'created':False})
  p.mkdir(parents=True);return self._r('folder_create',{'path':path,'created':True},side_effect=True)
 def contact_search(self,name=None,company=None,department=None):
  xs=json.loads((self.p/'contacts'/'contacts.json').read_text(encoding='utf-8'));out=[x for x in xs if (not name or name.replace('经理','') in x['name']) and (not company or company in x['company']) and (not department or department in x['department'])];return self._r('contact_search',{'contacts':out})
 def contact_read(self,contact_id):
  xs=json.loads((self.p/'contacts'/'contacts.json').read_text(encoding='utf-8'));x=next((x for x in xs if x['contact_id']==contact_id),None);return self._r('contact_read',{'contact':x} if x else {},None if x else {'type':'NOT_FOUND','message':contact_id})
 def web_search(self,q):
  xs=json.loads((self.p/'research'/'mock_web_pages.json').read_text(encoding='utf-8'));terms=[t for t in q.lower().split() if t not in {'软件','官网','功能','企业版','介绍'}];out=[x for x in xs if all(t in json.dumps(x,ensure_ascii=False).lower() for t in terms)];return self._r('web_search',{'results':out})
 def web_open(self,url):
  xs=json.loads((self.p/'research'/'mock_web_pages.json').read_text(encoding='utf-8'));x=next((x for x in xs if x['url']==url),None);return self._r('web_open',{'page':x} if x else {},None if x else {'type':'NOT_FOUND','message':url})
