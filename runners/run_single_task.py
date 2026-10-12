import sys,uuid,argparse,json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.graph import OfficeAgent
p=argparse.ArgumentParser();p.add_argument('--task-id',required=True);a=p.parse_args();root=Path(__file__).resolve().parents[1];run_id=str(uuid.uuid4());r=OfficeAgent(root).invoke(a.task_id,run_id);print(r['final_response']);print(f'\n[run_id: {run_id}]')
