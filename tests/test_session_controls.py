import json,threading,unittest
from unittest.mock import patch
from src.lab.cloud import CloudSessions,CloudError,OpenAITransport,AnthropicTransport
from src.lab.model_catalog import catalog

class Fake:
 def __init__(self):self.calls=[]
 def check(self,key,model):self.calls.append(('check',key,model))
 def answer(self,key,model,messages,limit,effort='default'):
  self.calls.append(('answer',model,messages,limit,effort));return {'text':'Text only','usage':{}}

class SessionControlTests(unittest.TestCase):
 def connect(self,cloud,**extra):
  return cloud.connect({'provider':'openai','api_key':'fixture-key-with-enough-length','model':'gpt-6.1-sol','effort':'medium','max_output_tokens':4096,'consent':True,**extra})['session_id']
 def test_native_effort_payloads(self):
  for transport,model,payload,field in [
   (OpenAITransport(),'gpt-6.1-sol',{'output':[{'type':'message','content':[{'type':'output_text','text':'ok'}]}]},'reasoning'),
   (AnthropicTransport(),'claude-opus-5-5',{'content':[{'type':'text','text':'ok'}],'stop_reason':'end_turn'},'output_config')]:
   with patch.object(transport,'request',return_value=payload) as request:
    transport.answer('fixture',model,[{'role':'user','content':'Hello'}],4096,effort='high')
    self.assertEqual(request.call_args.args[3][field],{'effort':'high'})
    self.assertNotIn('service_tier',request.call_args.args[3])
 def test_unsupported_effort_rejected_before_provider(self):
  fake=Fake();cloud=CloudSessions(transports={'openai':fake,'anthropic':fake})
  for kwargs in ({'effort':'ultra'},{'model':'unverified-model','effort':'high'},{'provider':'anthropic','model':'claude-haiku-4-5-20251001','effort':'medium'},{'effort':{}}):
   with self.assertRaisesRegex(CloudError,'EFFORT_UNSUPPORTED'):self.connect(cloud,**kwargs)
  self.assertEqual(fake.calls,[])
 def test_same_provider_model_change_is_transactional(self):
  fake=Fake();cloud=CloudSessions(fake);token=self.connect(cloud)
  cloud.ask({'session_id':token,'message':'old context'});row=cloud.sessions[token]
  with patch.object(fake,'check',side_effect=CloudError('MODEL_UNAVAILABLE',502)):
   with self.assertRaises(CloudError):cloud.configure({'session_id':token,'model':'gpt-6-astra','effort':'high'})
  self.assertEqual(row['model'],'gpt-6.1-sol');self.assertEqual(len(row['history']),2);self.assertFalse(row['busy'])
  result=cloud.configure({'session_id':token,'model':'gpt-6-astra','effort':'high'})
  self.assertTrue(result['history_cleared']);self.assertEqual(row['history'],[]);self.assertEqual(row['requests'],1)
  cloud.ask({'session_id':token,'message':'new context'});self.assertEqual(fake.calls[-1][-1],'high');self.assertNotIn('old context',json.dumps(fake.calls[-1]))
 def test_effort_change_preserves_history_and_budget(self):
  fake=Fake();cloud=CloudSessions(fake);token=self.connect(cloud);cloud.ask({'session_id':token,'message':'keep context'})
  count=len(fake.calls);result=cloud.configure({'session_id':token,'model':'gpt-6.1-sol','effort':'low'})
  self.assertFalse(result['history_cleared']);self.assertEqual(len(fake.calls),count);self.assertEqual(cloud.sessions[token]['requests'],1)
  cloud.ask({'session_id':token,'message':'follow-up'});self.assertEqual(len(fake.calls[-1][2]),3);self.assertEqual(fake.calls[-1][-1],'low')
 def test_configuration_cannot_switch_provider_or_bypass_busy(self):
  fake=Fake();cloud=CloudSessions(fake);token=self.connect(cloud)
  with self.assertRaises(CloudError):cloud.configure({'session_id':token,'provider':'anthropic','model':'claude-opus-5-5','effort':'high'})
  cloud.sessions[token]['busy']=True
  with self.assertRaisesRegex(CloudError,'REQUEST_IN_PROGRESS'):cloud.configure({'session_id':token,'model':'gpt-6-astra','effort':'high'})
  self.assertEqual(len(fake.calls),1)
 def test_disconnect_during_access_check_does_not_restore_session(self):
  fake=Fake();cloud=CloudSessions(fake);token=self.connect(cloud)
  with patch.object(fake,'check',side_effect=lambda *_:cloud.disconnect({'session_id':token})):
   with self.assertRaisesRegex(CloudError,'SESSION_EXPIRED'):cloud.configure({'session_id':token,'model':'gpt-6-astra','effort':'high'})
  self.assertNotIn(token,cloud.sessions)
 def test_catalog_is_reference_copy_not_account_claim(self):
  first=catalog();self.assertEqual(first['kind'],'documented_reference');self.assertEqual(len(first['models']),7)
  first['models'][0]['efforts'].clear();self.assertTrue(catalog()['models'][0]['efforts'])
  self.assertNotIn('api_key',json.dumps(first));self.assertTrue(all(x['source'].startswith('https://') for x in first['models']))
