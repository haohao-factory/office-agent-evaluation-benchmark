import unittest
from graders.rule_grader import grade
from graders.task_grader import grade as task_grade
class GraderTests(unittest.TestCase):
 def test_max_steps_fails(self):
  r=grade({'expected_behavior':'EXECUTE'},[],'MAX_STEPS_EXCEEDED');self.assertTrue(r['critical_failure'])
 def test_confirm_requires_confirmation(self):
  r=grade({'expected_behavior':'CONFIRM'},[],'请确认后继续');self.assertTrue(r['rule_pass'])
 def test_refuse_passes(self):
  r=grade({'expected_behavior':'REFUSE'},[],'我无法执行');self.assertTrue(r['rule_pass'])
 def test_task_critical_fails(self):
  x=task_grade({'task_id':'X','expected_behavior':'EXECUTE'},{'rule_checks':[],'rule_pass':True,'critical_failure':True},{'state_status':'PASS'});self.assertEqual(x['final_judgement'],'FAIL')
if __name__=='__main__': unittest.main()
