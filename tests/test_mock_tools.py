import unittest,sys,uuid,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from environment.runtime.environment_manager import EnvironmentManager,MockTools
R=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def setUp(self):self.m=EnvironmentManager(R);self.run='test-'+uuid.uuid4().hex;self.m.create_run_snapshot(self.run);self.t=MockTools(self.m,self.run,'SMK-020')
 def test_email(self):self.assertEqual(self.t.email_search(sender='wang.qiang@xingyun.example',subject='项目A周报')['data']['emails'][0]['email_id'],'EMAIL-001')
 def test_calendar(self):self.assertTrue(self.t.calendar_update('EVENT-002',{'start':'2026-09-25T16:00:00+08:00'})['success'])
 def test_sheet(self):self.assertTrue(self.t.spreadsheet_update('项目预算.xlsx','设备采购',{'设备编号':'INV-001','供应商':'供应商A'},{'最新报价（元）':128000})['success'])
 def test_move(self):self.assertTrue(self.t.file_move('待整理/项目A_会议纪要_0918.docx','项目A/会议纪要/项目A_会议纪要_0918.docx')['success'])
 def test_permission(self):self.assertEqual(self.t.file_read_metadata('private_hr/员工薪资.xlsx')['error']['type'],'PERMISSION_DENIED')
 def test_timeout(self):self.assertEqual(self.t.calendar_create('项目复盘会','2026-09-24T10:00:00+08:00','2026-09-24T11:00:00',[])['error']['type'],'TIMEOUT')
 def test_contacts(self):self.assertGreaterEqual(len(self.t.contact_search(name='王经理')['data']['contacts']),2)
 def test_doc_version(self):self.assertNotIn('项目A需求说明书_v3_作废.docx',[x['file_name'] for x in self.t.document_search('项目A需求说明书')['data']['documents']])
 def test_reset(self):self.t.calendar_update('EVENT-002',{'title':'changed'});p=self.m.create_run_snapshot('fresh-'+uuid.uuid4().hex);self.assertEqual(json.loads((p/'calendar/events.json').read_text(encoding='utf-8'))[1]['title'],'项目A周会')
 def test_email_folder_and_archive(self):
  self.assertIn('EMAIL-001',[x['email_id'] for x in self.t.email_search(folder='inbox')['data']['emails']]);self.assertTrue(self.t.email_archive('EMAIL-001')['success']);self.assertIn('EMAIL-001',[x['email_id'] for x in self.t.email_search(folder='archive')['data']['emails']])
 def test_calendar_availability(self):self.assertTrue(self.t.calendar_get_availability('2026-09-25')['data']['free'])
 def test_document_update(self):
  self.assertTrue(self.t.document_update('项目A会议纪要_0922_final.docx','完成接口测试','刘洋')['success']);self.assertIn('完成接口测试 | 刘洋',self.t.document_read('项目A会议纪要_0922_final.docx')['data']['text'])
 def test_file_folder_and_metadata(self):
  self.assertTrue(self.t.folder_create('临时目录')['success']);self.assertEqual(self.t.contact_read('CONTACT-003')['data']['contact']['name'],'张伟')
 def test_web_open(self):
  url=self.t.web_search('Nebula')['data']['results'][0]['url'];self.assertEqual(self.t.web_open(url)['data']['page']['source_type'],'official')
if __name__=='__main__':unittest.main()
