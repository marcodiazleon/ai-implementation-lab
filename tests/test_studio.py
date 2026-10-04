import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from src.lab.agent_store import AgentStore
from src.lab.cloud import CloudSessions,CloudError,AnthropicTransport
from scripts.publication_check import inspect

DEFINITION={'id':'','name':'Support analyst','role':'Review public support requests','prompt':'Compare the request with the stated constraints and return missing questions.','work_mode':'review'}
class Fake:
    def __init__(self):self.calls=[]
    def check(self,key,model):self.calls.append(('check',key,model))
    def answer(self,key,model,messages,limit):self.calls.append(('answer',key,model,messages,limit));return {'text':'Scoped response','incomplete':False,'usage':{}}

class StudioTests(unittest.TestCase):
    def setUp(self):self.directory=tempfile.TemporaryDirectory();self.path=Path(self.directory.name)/'agents.json';self.store=AgentStore(self.path)
    def tearDown(self):self.directory.cleanup()
    def test_create_edit_and_restart_preserve_definition(self):
        row=self.store.save(dict(DEFINITION));self.assertTrue(row['id'].startswith('custom-'))
        loaded=AgentStore(self.path).list();self.assertEqual(loaded,[row])
        updated=self.store.save({**row,'name':'Edited analyst'});self.assertEqual(len(self.store.list()),1);self.assertEqual(updated['name'],'Edited analyst')
    def test_input_traversal_and_secret_fields_are_rejected(self):
        for extra in ({'id':'../../file'},{'prompt':'short'},{'api_key':'private'},{'work_mode':'shell'},{'name':'x'},{'prompt':'Read this sk-'+('a'*24)}):
            with self.assertRaises(CloudError):self.store.save({**DEFINITION,**extra})
        self.assertFalse(self.path.exists())
    def test_corrupt_store_fails_without_overwriting(self):
        self.path.write_text('invalid',encoding='utf-8')
        with self.assertRaisesRegex(CloudError,'AGENT_STORE_UNREADABLE'):self.store.save(dict(DEFINITION))
        self.assertEqual(self.path.read_text(),'invalid')
    def test_resolved_role_changes_context_revision(self):
        row=self.store.save(dict(DEFINITION));instructions,revision=self.store.resolve(row['id']);self.assertIn(row['prompt'],instructions)
        self.store.save({**row,'prompt':'A new assignment requiring a different output and explicit evidence.'})
        self.assertNotEqual(self.store.resolve(row['id'])[1],revision)
        with self.assertRaises(CloudError):self.store.resolve('unknown')
    def test_private_definitions_cannot_be_staged(self):
        self.assertTrue(inspect('.local/agents.json',b'[]'))
    def test_providers_route_keys_without_fallback(self):
        first,second=Fake(),Fake();cloud=CloudSessions(transports={'openai':first,'anthropic':second})
        token=cloud.connect({'provider':'anthropic','api_key':'fixture-key-with-enough-length','model':'fixture','max_output_tokens':1024,'consent':True})['session_id']
        result=cloud.ask({'session_id':token,'message':'Hello'});self.assertEqual(result['provider'],'anthropic');self.assertFalse(first.calls);self.assertEqual(len(second.calls),2)
        with self.assertRaisesRegex(CloudError,'PROVIDER_UNSUPPORTED'):cloud.connect({'provider':'unknown','api_key':'fixture-key-with-enough-length','model':'fixture','max_output_tokens':1024,'consent':True})
    def test_agent_context_does_not_leak_into_other_role(self):
        fake=Fake();cloud=CloudSessions(fake);token=cloud.connect({'api_key':'fixture-key-with-enough-length','model':'fixture','max_output_tokens':512,'consent':True})['session_id']
        cloud.ask({'session_id':token,'message':'First private context'},'Role one','one')
        cloud.ask({'session_id':token,'message':'Second question'},'Role two','two')
        messages=fake.calls[-1][3];self.assertNotIn('First private context',json.dumps(messages));self.assertEqual(messages[0],{'role':'developer','content':'Role two'})
        cloud.ask({'session_id':token,'message':'Follow-up'},'Role two','two');self.assertEqual(len(fake.calls[-1][3]),4)
    def test_anthropic_protocol_and_partial_output(self):
        transport=AnthropicTransport();payload={'content':[{'type':'text','text':'Hello'}],'stop_reason':'max_tokens','usage':{'input_tokens':4,'output_tokens':5}}
        with patch.object(transport,'request',return_value=payload) as request:
            r=transport.answer('fixture','model',[{'role':'developer','content':'Role prompt'},{'role':'user','content':'Question'}],512)
            args=request.call_args.args;self.assertEqual(args[1],'/v1/messages');self.assertEqual(args[3]['max_tokens'],512);self.assertIn('Role prompt',args[3]['system']);self.assertEqual(len(args[3]['messages']),1)
            self.assertTrue(r['incomplete']);self.assertEqual(r['usage']['total_tokens'],9)
        self.assertEqual(transport.host,'api.anthropic.com');self.assertEqual(transport.headers('fixture')['anthropic-version'],'2023-06-01')
        with patch.object(transport,'request',return_value={'content':[]}):
            with self.assertRaises(CloudError):transport.answer('fixture','model',[],512)
