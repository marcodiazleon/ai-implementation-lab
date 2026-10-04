import http.client,json,threading,unittest
from src.lab.server import make_server
from src.lab.context7 import Context7Sessions
from tests.test_context7 import FakeMcp

class WorkbenchHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mcp=Context7Sessions(FakeMcp());cls.server=make_server(0,mcp=cls.mcp)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def request(self,path,body=None,origin=None):
        c=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        c.request('GET' if body is None else 'POST',path,None if body is None else json.dumps(body),headers)
        r=c.getresponse();status=r.status;raw=r.read();c.close();return status,raw
    def test_contracts_run_and_assets(self):
        status,raw=self.request('/api/agents');self.assertEqual(status,200);self.assertEqual(len(json.loads(raw)),4)
        body={'agent':'implementer','mode':'local','brief':'Create a review flow for public demo support requests.'}
        status,raw=self.request('/api/agents/run',body);self.assertEqual(status,200);self.assertEqual(json.loads(raw)['agent'],'implementer')
        self.assertEqual(self.request('/workbench.js')[0],200)
    def test_origin_body_and_provider_boundaries(self):
        self.assertEqual(self.request('/api/agents/run',{},'https://outside.example')[0],403)
        c=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        c.request('POST','/api/agents/run',headers={'Content-Type':'application/json','Content-Length':'100001'})
        response=c.getresponse();self.assertEqual(response.status,413);response.read();c.close()
        self.assertEqual(self.request('/api/mcp/connect',{'api_key':'','consent':False})[0],400)
    def test_mcp_endpoints(self):
        status,raw=self.request('/api/mcp/connect',{'api_key':'','consent':True});self.assertEqual(status,200)
        token=json.loads(raw)['session_id']
        status,raw=self.request('/api/mcp/call',{'session_id':token,'tool':'resolve-library-id','arguments':{'libraryName':'Python','query':'JSON'},'consent':True})
        self.assertEqual(status,200);self.assertIn(b'Public fixture docs',raw)
        self.assertEqual(self.request('/api/mcp/disconnect',{'session_id':token})[0],200)
