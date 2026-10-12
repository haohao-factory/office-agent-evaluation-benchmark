import json, os, shutil, unittest
from pathlib import Path
from environment.runtime.environment_manager import EnvironmentManager
ROOT=Path(__file__).resolve().parents[1]
class CertificationFormalV2Tests(unittest.TestCase):
 def setUp(self):self.tasks=[json.loads(x) for x in (ROOT/'dataset/formal_v2/certification_tasks_v2.0.jsonl').read_text(encoding='utf8').splitlines()]
 def test_exact_distribution(self):
  c=lambda key:{v:sum(t[key]==v for t in self.tasks) for v in set(t[key] for t in self.tasks)}
  self.assertEqual(len(self.tasks),100);self.assertEqual(c('category'),{'Email':12,'Calendar':10,'Document':10,'Spreadsheet':10,'File / Drive':10,'Contacts':6,'Research':7,'Cross-tool Workflow':25,'Safety / Clarification / Failure':10});self.assertEqual(c('difficulty'),{'L1':10,'L2':25,'L3':40,'L4':25});self.assertEqual(c('expected_behavior'),{'EXECUTE':46,'REPORT':22,'CLARIFY':10,'CONFIRM':12,'REFUSE':10});self.assertEqual(c('risk_level'),{'LOW':25,'MEDIUM':45,'HIGH':30});self.assertEqual({d:sum(t['cross_tool_depth']==d for t in self.tasks) for d in (1,2,3)},{1:35,2:35,3:30})
 def test_v2_is_independent_and_executable(self):
  self.assertTrue(all('北辰' not in t['user_request'] and '项目A' not in t['user_request'] and '项目C' not in t['user_request'] for t in self.tasks))
  old=os.environ.get('OFFICE_ENVIRONMENT_ROOT');os.environ['OFFICE_ENVIRONMENT_ROOT']=str(ROOT/'environment/formal_v2')
  try:
   m=EnvironmentManager(ROOT);p=m.create_run_snapshot('certification-v2-preflight');self.assertTrue((p/'documents/曙光计划行动清单.docx').exists());self.assertTrue((p/'files/曙光/归档').exists());shutil.rmtree(p)
  finally:
   if old is None:os.environ.pop('OFFICE_ENVIRONMENT_ROOT',None)
   else:os.environ['OFFICE_ENVIRONMENT_ROOT']=old
if __name__=='__main__':unittest.main()
