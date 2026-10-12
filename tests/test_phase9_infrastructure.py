from pathlib import Path
import json, unittest, uuid, shutil
from agent.graph import MODEL_TIMEOUT_SECONDS
from environment.runtime.environment_manager import EnvironmentManager, MockTools
ROOT=Path(__file__).resolve().parents[1]
class Phase9InfrastructureTests(unittest.TestCase):
 def test_model_timeout_allows_slow_provider_responses(self): self.assertGreaterEqual(MODEL_TIMEOUT_SECONDS,60)
 def test_referenced_infrastructure_objects_exist(self):
  base=ROOT/'environment/base_state'; emails=json.loads((base/'emails/emails.json').read_text(encoding='utf-8'));self.assertIn('DEV-EMAIL-005',{x['email_id'] for x in emails})
  files=json.loads((base/'files/files_manifest.json').read_text(encoding='utf-8'));paths={x['path'] for x in files}
  for path in ('项目C/待整理/项目C方案_v1.docx','项目C/发布/项目C方案_final.docx','项目C/发布/项目C发布清单_final.pdf'):self.assertIn(path,paths)
  events=json.loads((base/'calendar/events.json').read_text(encoding='utf-8'));self.assertTrue(any(x['event_id']=='DEV-EVENT-002' and 'client@customer.example' in x['attendees'] for x in events))
  self.assertTrue((base/'emails/attachments/项目C预算_final.xlsx').exists())
 def test_web_search_does_not_return_unmatched_official_pages(self):
  run_id=f'search-{uuid.uuid4()}';manager=EnvironmentManager(ROOT);manager.create_run_snapshot(run_id)
  try:self.assertNotIn('DEV-WEB-001',[x['page_id'] for x in MockTools(manager,run_id,'SMK-013').web_search('Nebula Work 软件')['data']['results']])
  finally:shutil.rmtree(manager.get_runtime_state(run_id),ignore_errors=True)
if __name__=='__main__':unittest.main()

