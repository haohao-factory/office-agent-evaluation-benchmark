import json, os, shutil, tempfile, unittest
from pathlib import Path
from environment.runtime.environment_manager import EnvironmentManager
ROOT=Path(__file__).resolve().parents[1]
class FormalPreflightTests(unittest.TestCase):
 def setUp(self): self.tasks=[json.loads(x) for x in (ROOT/'dataset/formal/formal_tasks_v1.0.jsonl').read_text(encoding='utf8').splitlines()]
 def test_distribution(self):
  def counts(key):return {v:sum(t[key]==v for t in self.tasks) for v in set(t[key] for t in self.tasks)}
  self.assertEqual(len(self.tasks),100);self.assertEqual(counts('category'),{'Email':12,'Calendar':10,'Document':10,'Spreadsheet':10,'File / Drive':10,'Contacts':6,'Research':7,'Cross-tool Workflow':25,'Safety / Clarification / Failure':10});self.assertEqual(counts('difficulty'),{'L1':10,'L2':25,'L3':40,'L4':25});self.assertEqual(counts('expected_behavior'),{'EXECUTE':46,'REPORT':22,'CLARIFY':10,'CONFIRM':12,'REFUSE':10});self.assertEqual(counts('risk_level'),{'LOW':25,'MEDIUM':45,'HIGH':30});self.assertEqual({v:sum(t['cross_tool_depth']==v for t in self.tasks) for v in (1,2,3)},{1:35,2:35,3:30})
 def test_unique_formal_ids_and_no_legacy_names(self):
  ids=[t['task_id'] for t in self.tasks];self.assertEqual(ids,[f'FORMAL-{i:03d}' for i in range(1,101)]);self.assertFalse(any(any(x in t['user_request'] for x in ('项目A','项目C','SMK-','DEV-')) for t in self.tasks))
 def test_independent_isolated_environment(self):
  old=os.environ.get('OFFICE_ENVIRONMENT_ROOT');os.environ['OFFICE_ENVIRONMENT_ROOT']=str(ROOT/'environment/formal_v1')
  try:
   m=EnvironmentManager(ROOT);run='formal-preflight';p=m.create_run_snapshot(run);self.assertTrue((p/'emails/emails.json').exists());self.assertTrue((ROOT/'environment/formal_v1/manifest.json').exists());self.assertNotEqual(m.env,ROOT/'environment');shutil.rmtree(p)
  finally:
   if old is None:os.environ.pop('OFFICE_ENVIRONMENT_ROOT',None)
   else:os.environ['OFFICE_ENVIRONMENT_ROOT']=old
if __name__=='__main__':unittest.main()
