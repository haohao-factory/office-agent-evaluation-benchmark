import json, shutil, unittest, uuid
from pathlib import Path
from graders.formal_grader import grade, error_type
ROOT=Path(__file__).resolve().parents[1]
TASK_FILE=ROOT/'dataset/formal/formal_tasks_v1.0.jsonl'
class FormalGraderTests(unittest.TestCase):
 def setUp(self):
  self.run='formal-grader-'+uuid.uuid4().hex;self.log=ROOT/'results/runtime_logs'/self.run;self.log.mkdir(parents=True)
  (self.log/'run_context.json').write_text(json.dumps({'task_id':'FORMAL-001'}),encoding='utf8')
  (self.log/'final_response.txt').write_text('已读取周报并汇报阻塞。',encoding='utf8')
 def tearDown(self): shutil.rmtree(self.log,ignore_errors=True)
 def write_calls(self, rows): (self.log/'tool_calls.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows),encoding='utf8')
 def test_success_record_with_null_error_is_gradable(self):
  self.write_calls([{'tool_name':'email_read','result':{'success':True,'error':None,'side_effect':False}}])
  result=grade(ROOT,self.run,TASK_FILE)
  self.assertEqual(result['verdict'],'PASS')
  self.assertFalse(result['critical_failure'])
 def test_error_object_is_read_safely(self):
  row={'tool_name':'file_read_metadata','result':{'success':False,'error':{'type':'PERMISSION_DENIED'},'side_effect':False}}
  self.write_calls([row]);self.assertEqual(error_type(row),'PERMISSION_DENIED');self.assertIn(grade(ROOT,self.run,TASK_FILE)['verdict'],{'PASS','PARTIAL','FAIL'})
 def test_missing_tool_log_is_gradable(self):
  result=grade(ROOT,self.run,TASK_FILE)
  self.assertEqual(result['verdict'],'FAIL')
if __name__=='__main__': unittest.main()
