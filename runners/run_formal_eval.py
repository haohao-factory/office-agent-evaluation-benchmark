"""One-shot formal runner. It records every attempted task and never resumes a completed formal run."""
import argparse, json, os, sys, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.graph import OfficeAgent
from graders.formal_grader import grade

def main():
 p=argparse.ArgumentParser();p.add_argument('--batch-id',required=True);p.add_argument('--dataset-file',default=str(ROOT/'dataset/formal/formal_tasks_v1.0.jsonl'));p.add_argument('--environment-root',default=str(ROOT/'environment/formal_v1'));a=p.parse_args()
 dataset=Path(a.dataset_file);env=Path(a.environment_root);out=ROOT/'results/formal_runs'/a.batch_id
 if out.exists():raise SystemExit('Formal batch already exists; rerun is forbidden.')
 out.mkdir(parents=True); tasks=[json.loads(x) for x in dataset.read_text(encoding='utf8').splitlines() if x.strip()]
 os.environ['OFFICE_ENVIRONMENT_ROOT']=str(env);os.environ['OFFICE_TASKSET_FILE']=str(dataset)
 agent=OfficeAgent(ROOT);results=[]
 for task in tasks:
  run_id=str(uuid.uuid4());runtime_error=None
  try:
   agent.invoke(task['task_id'],run_id)
  except Exception as exc:
   runtime_error=str(exc);r={'run_id':run_id,'task_id':task['task_id'],'verdict':'FAIL','tool_call_count':0,'tool_names':[],'side_effect':False,'safety_failure':False,'critical_failure':False,'expected_behavior':task['expected_behavior'],'risk_level':task['risk_level'],'difficulty':task['difficulty'],'category':task['category'],'tool_depth':task['cross_tool_depth'],'final_response':'','reasons':['AGENT_RUNTIME_EXCEPTION',runtime_error]}
  else:
   try:
    r=grade(ROOT,run_id,dataset)
   except Exception as exc:
    runtime_error=str(exc);r={'run_id':run_id,'task_id':task['task_id'],'verdict':'FAIL','tool_call_count':0,'tool_names':[],'side_effect':False,'safety_failure':False,'critical_failure':False,'expected_behavior':task['expected_behavior'],'risk_level':task['risk_level'],'difficulty':task['difficulty'],'category':task['category'],'tool_depth':task['cross_tool_depth'],'final_response':'','reasons':['GRADER_EXCEPTION',runtime_error]}
  r['runtime_error']=runtime_error;r['model']=os.getenv('OPENAI_MODEL');results.append(r);(out/f"{task['task_id']}.json").write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
  write(out,a.batch_id,results,False)
 write(out,a.batch_id,results,True)
def write(out,batch_id,results,complete):
 counts={v:sum(x['verdict']==v for x in results) for v in ('PASS','PARTIAL','FAIL')}
 summary={'batch_id':batch_id,'kind':'formal_blind_evaluation','complete':complete,'model':os.getenv('OPENAI_MODEL'),'total':len(results),'counts':counts,'runtime_errors':sum(bool(x.get('runtime_error')) for x in results),'safety_failures':sum(x.get('safety_failure',False) for x in results),'critical_failures':sum(x.get('critical_failure',False) for x in results),'results':results}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({**counts,'attempted':len(results)},ensure_ascii=False))
if __name__=='__main__':main()
