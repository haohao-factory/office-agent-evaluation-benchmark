from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.prompts import SYSTEM_PROMPT
from environment.runtime.environment_manager import EnvironmentManager,MockTools
from openai import OpenAI
from pathlib import Path
import json, os, uuid
MODEL_TIMEOUT_SECONDS=int(os.getenv('OFFICE_AGENT_TIMEOUT_SECONDS','60'))
TOOL_SPECS=[
 {'type':'function','function':{'name':'email_search','description':'Search mock emails by sender, subject, date range, or folder.','parameters':{'type':'object','properties':{'sender':{'type':'string'},'subject':{'type':'string'},'date_from':{'type':'string'},'date_to':{'type':'string'},'folder':{'type':'string'}},'additionalProperties':False}}},
 {'type':'function','function':{'name':'email_read','description':'Read one email by id.','parameters':{'type':'object','properties':{'email_id':{'type':'string'}},'required':['email_id'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'calendar_search','description':'Search calendar events.','parameters':{'type':'object','properties':{'title':{'type':'string'},'start':{'type':'string'}},'additionalProperties':False}}},
 {'type':'function','function':{'name':'calendar_update','description':'Update an existing calendar event.','parameters':{'type':'object','properties':{'event_id':{'type':'string'},'updates':{'type':'object'}},'required':['event_id','updates'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'calendar_create','description':'Create a calendar event.','parameters':{'type':'object','properties':{'title':{'type':'string'},'start':{'type':'string'},'end':{'type':'string'},'attendees':{'type':'array','items':{'type':'string'}}},'required':['title','start','end','attendees'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'file_read_metadata','description':'Read file metadata; access control is enforced.','parameters':{'type':'object','properties':{'path':{'type':'string'}},'required':['path'],'additionalProperties':False}}}
]
def _spec(name,description,properties,required=()):
    return {'type':'function','function':{'name':name,'description':description,'parameters':{'type':'object','properties':properties,'required':list(required),'additionalProperties':False}}}
TOOL_SPECS.extend([
 _spec('email_archive','Archive an email by id.',{'email_id':{'type':'string'}},['email_id']),
 _spec('email_draft','Create an email draft without sending it.',{'to':{'type':'array','items':{'type':'string'}},'subject':{'type':'string'},'body':{'type':'string'}},['to','subject','body']),
 _spec('contact_search','Search contacts by name, company, or department.',{'name':{'type':'string'},'company':{'type':'string'},'department':{'type':'string'}}),
 _spec('document_search','Find active non-deprecated documents by filename.',{'name':{'type':'string'}},['name']),
 _spec('document_read','Read a DOCX or PDF document.',{'file_name':{'type':'string'}},['file_name']),
 _spec('spreadsheet_read','Read a workbook sheet.',{'file':{'type':'string'},'sheet':{'type':'string'}},['file','sheet']),
 _spec('spreadsheet_update','Update exactly one spreadsheet row selected by match fields.',{'file':{'type':'string'},'sheet':{'type':'string'},'match':{'type':'object'},'updates':{'type':'object'}},['file','sheet','match','updates']),
 _spec('file_search','Search mock file metadata by a path fragment.',{'query':{'type':'string'}},['query']),
 _spec('file_move','Move an exact mock file path to an exact destination path.',{'source':{'type':'string'},'destination':{'type':'string'}},['source','destination']),
 _spec('web_search','Search the mock public web pages.',{'q':{'type':'string'}},['q']),
 _spec('web_open','Open one mock public web URL.',{'url':{'type':'string'}},['url']),
 _spec('email_forward','Forward an email externally. External forwarding requires confirmation and must not be sent before confirmation.',{'email_id':{'type':'string'},'recipient':{'type':'string'}},['email_id','recipient']),
 _spec('calendar_get_availability','Get calendar availability for a date.',{'date':{'type':'string'}},['date']),
 _spec('calendar_cancel','Cancel an event by id.',{'event_id':{'type':'string'}},['event_id']),
 _spec('document_update','Update a precisely identified document field.',{'file_name':{'type':'string'},'target':{'type':'string'},'value':{'type':'string'}},['file_name','target','value']),
 _spec('spreadsheet_filter','Filter a spreadsheet.',{'file':{'type':'string'},'sheet':{'type':'string'}},['file','sheet']),
 _spec('spreadsheet_append','Append a spreadsheet record.',{'file':{'type':'string'},'sheet':{'type':'string'}},['file','sheet']),
 _spec('file_rename','Rename an exact file.',{'source':{'type':'string'},'destination':{'type':'string'}},['source','destination']),
 _spec('folder_create','Create a folder.',{'path':{'type':'string'}},['path']),
 _spec('contact_read','Read a contact by id.',{'contact_id':{'type':'string'}},['contact_id'])
])
class OfficeAgent:
 def __init__(self,root):self.root=Path(root);self.m=EnvironmentManager(root);self.max_steps=20
 def _agent(self,s):
  client=OpenAI(api_key=os.environ['OPENAI_API_KEY'],base_url=os.environ['OPENAI_BASE_URL'],timeout=MODEL_TIMEOUT_SECONDS,max_retries=0)
  messages=s['messages']; model=os.environ['OPENAI_MODEL']
  # GLM's compatible endpoint accepts tool calls only with thinking enabled;
  # the other currently-supported models use the lower-cost disabled mode.
  enable_thinking=model.startswith('glm-')
  r=client.chat.completions.create(model=model,messages=messages,tools=TOOL_SPECS,temperature=0,extra_body={'enable_thinking':enable_thinking})
  msg=r.choices[0].message;return {'messages':messages+[msg.model_dump(exclude_none=True)],'step_count':s.get('step_count',0)+1}
 def _tools(self,s):
  if s['step_count']>=self.max_steps:return {'error_log':s.get('error_log',[])+['MAX_STEPS_EXCEEDED'],'final_response':'MAX_STEPS_EXCEEDED'}
  t=MockTools(self.m,s['run_id'],s['task_id']); msg=s['messages'][-1]; calls=msg.get('tool_calls',[]); outputs=[]
  for c in calls:
   name=c['function']['name']
   arguments={}
   try:
    arguments=json.loads(c['function']['arguments'])
    r=getattr(t,name)(**arguments)
   except Exception as e:r={'success':False,'tool':c['function']['name'],'data':{},'error':{'type':'TOOL_EXCEPTION','message':str(e)},'side_effect':False}
   if t.calls: t.calls[-1]['arguments']=arguments
   outputs.append({'role':'tool','tool_call_id':c['id'],'content':json.dumps(r,ensure_ascii=False)})
  previous=len(s.get('tool_calls',[]))
  for index,call in enumerate(t.calls,start=1): call['step']=previous+index
  return {'messages':s['messages']+outputs,'tool_calls':s.get('tool_calls',[])+t.calls,'tool_results':s.get('tool_results',[])+[x['result'] for x in t.calls]}
 def _route(self,s):
  if s.get('final_response') or s.get('step_count',0)>=self.max_steps:return END
  msg=s['messages'][-1]
  return 'tools' if msg.get('tool_calls') else END
 def _finalize(self,s):
  msg=s['messages'][-1];content=msg.get('content') or ('MAX_STEPS_EXCEEDED' if s.get('step_count',0)>=self.max_steps else '')
  log=self.root/'results'/'runtime_logs'/s['run_id'];log.mkdir(parents=True,exist_ok=True);(log/'tool_calls.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in s.get('tool_calls',[]))+'\n',encoding='utf8');(log/'run_context.json').write_text(json.dumps({'run_id':s['run_id'],'task_id':s['task_id']},ensure_ascii=False),encoding='utf8');(log/'final_response.txt').write_text(content,encoding='utf8');return {'final_response':content}
 def graph(self):
  g=StateGraph(AgentState);g.add_node('agent',self._agent);g.add_node('tools',self._tools);g.add_node('finalize',self._finalize);g.add_edge(START,'agent');g.add_conditional_edges('agent',self._route,{'tools':'tools',END:'finalize'});g.add_edge('tools','agent');g.add_edge('finalize',END);return g.compile()
 def invoke(self,task_id,run_id=None):
  run_id=run_id or str(uuid.uuid4());self.m.create_run_snapshot(run_id)
  selected_taskset=os.getenv('OFFICE_TASKSET_FILE')
  task_files=([Path(selected_taskset)] if selected_taskset else [])+[self.root/'dataset/smoke/smoke_tasks_v0.1.jsonl',self.root/'dataset/dev/development_set_v0.1.jsonl']
  request=None
  for task_file in task_files:
   if not task_file.exists(): continue
   for line in task_file.read_text(encoding='utf8').splitlines():
    task=json.loads(line)
    if task['task_id']==task_id: request=task['user_request'];break
   if request is not None: break
  if request is None: raise ValueError(f'Unknown task_id: {task_id}')
  messages=[{'role':'system','content':SYSTEM_PROMPT},{'role':'user','content':request}];return self.graph().invoke({'messages':messages,'task_id':task_id,'run_id':run_id,'tool_calls':[],'tool_results':[],'error_log':[],'step_count':0})

