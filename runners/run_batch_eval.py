"""Development-only Smoke batch runner; never a formal baseline runner."""
import argparse,json,uuid,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.graph import OfficeAgent
from graders.state_grader import grade

def main():
 root=Path(__file__).resolve().parents[1]; p=argparse.ArgumentParser();p.add_argument('--dataset',default='smoke');p.add_argument('--limit',type=int);p.add_argument('--task-ids',nargs='*');p.add_argument('--batch-id');p.add_argument('--resume',action='store_true');a=p.parse_args()
 dataset_file=(root/'dataset/dev/development_set_v0.1.jsonl') if a.dataset=='development' else (root/'dataset'/a.dataset/'smoke_tasks_v0.1.jsonl')
 tasks=[json.loads(x) for x in dataset_file.read_text(encoding='utf-8').splitlines()]
 if a.task_ids: tasks=[x for x in tasks if x['task_id'] in a.task_ids]
 if a.limit: tasks=tasks[:a.limit]
 batch_id=a.batch_id or 'dev-smoke-'+uuid.uuid4().hex; out=root/'results'/'development_runs'/batch_id
 if out.exists() and not a.resume: raise SystemExit(f'Batch already exists: {out}. Use --resume to continue it.')
 out.mkdir(parents=True,exist_ok=True)
 agent=OfficeAgent(root); results=[]
 for task in tasks:
  saved=out/f"{task['task_id']}.json"
  if a.resume and saved.exists():
   results.append(json.loads(saved.read_text(encoding='utf-8'))); continue
  run_id=str(uuid.uuid4())
  quota_exhausted=False
  try:
   agent.invoke(task['task_id'],run_id); result=grade(root,run_id)
  except Exception as exc:
   quota_exhausted='insufficient_quota' in str(exc)
   # A pre-tool transport failure is safe to retry once in a fresh snapshot.
   # Never retry a run that recorded any tool call, because a write may exist.
   log=root/'results'/'runtime_logs'/run_id/'tool_calls.jsonl'
   pre_tool_failure=not log.exists() or not log.read_text(encoding='utf-8').strip()
   if not quota_exhausted and pre_tool_failure:
    retry_id=str(uuid.uuid4())
    try:
     agent.invoke(task['task_id'],retry_id); result=grade(root,retry_id); result['retried_after_pre_tool_failure']=True
    except Exception as retry_exc:
     quota_exhausted='insufficient_quota' in str(retry_exc)
     result={'run_id':retry_id,'task_id':task['task_id'],'verdict':'FAIL','tool_call_count':0,'reasons':['QUOTA_EXHAUSTED' if quota_exhausted else 'RUNNER_EXCEPTION',str(retry_exc),'retry_after_pre_tool_failure']}
   else:
    result={'run_id':run_id,'task_id':task['task_id'],'verdict':'FAIL','tool_call_count':0,'reasons':['QUOTA_EXHAUSTED' if quota_exhausted else 'RUNNER_EXCEPTION',str(exc)]}
  result.update({'model':os.getenv('OPENAI_MODEL'),'environment_version':json.loads((root/'environment/manifest.json').read_text(encoding='utf-8'))['environment_version'],'dataset_version':'smoke_v0.1'});results.append(result)
  saved.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  write_summary(out,batch_id,results,complete=False)
  if quota_exhausted: break
 write_summary(out,batch_id,results,complete=True)
def write_summary(out,batch_id,results,complete):
 summary={'batch_id':batch_id,'kind':'development_smoke','complete':complete,'model':os.getenv('OPENAI_MODEL'),'total':len(results),'counts':{x:sum(r['verdict']==x for r in results) for x in ['PASS','PARTIAL','FAIL']},'results':results}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary['counts'],ensure_ascii=False))
if __name__=='__main__':main()
