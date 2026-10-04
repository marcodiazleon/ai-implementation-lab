import json
import threading
import unittest
from unittest.mock import patch
from src.lab.cloud import CloudError
from src.lab.context7 import Context7Sessions, Context7Transport, VERSION

class FakeMcp:
    def __init__(self):self.calls=[];self.fail=False;self.missing=False
    def exchange(self,payload,key,session,version):
        self.calls.append(payload)
        method=payload['method']
        if method=='initialize':return {'protocolVersion':VERSION},'fixture-session'
        if method=='notifications/initialized':return None,session
        if method=='tools/list':return {'tools':[{'name':x} for x in ([] if self.missing else ['resolve-library-id','query-docs','unexpected-tool'])]},session
        return {'isError':self.fail,'content':[{'type':'text','text':'Public fixture docs'}]},session

class McpTests(unittest.TestCase):
    def setUp(self):
        self.now=0;self.transport=FakeMcp();self.manager=Context7Sessions(self.transport,lambda:self.now)
        self.token=self.manager.connect({'api_key':'','consent':True})['session_id']
    def call(self,**extra):return self.manager.call({'session_id':self.token,'tool':'query-docs','arguments':{'libraryId':'/python/cpython','query':'JSON validation'},'consent':True,**extra})
    def test_handshake_discovery_and_explicit_query(self):
        self.assertEqual([r['method'] for r in self.transport.calls],['initialize','notifications/initialized','tools/list'])
        self.assertNotIn('id',self.transport.calls[1])
        r=self.call();self.assertEqual(r['text'],'Public fixture docs');self.assertEqual(r['requests_used'],1)
    def test_unlisted_tool_and_unconsented_query_blocked(self):
        for changes in ({'tool':'unexpected-tool'},{'consent':False},{'arguments':{'libraryId':'https://evil.example','query':'x'}}):
            with self.assertRaises(CloudError):self.call(**changes)
        self.assertEqual(len(self.transport.calls),3)
    def test_missing_tools_do_not_connect(self):
        self.transport.missing=True
        with self.assertRaises(CloudError):self.manager.connect({'api_key':'','consent':True})
        self.assertEqual(len(self.manager.sessions),1);self.assertEqual(self.manager.connecting,0)
    def test_expiry_disconnect_and_limit(self):
        self.manager.sessions[self.token]['requests']=20
        with self.assertRaises(CloudError):self.call()
        self.now=1801
        with self.assertRaises(CloudError):self.call()
        self.assertFalse(self.manager.sessions)
        token=self.manager.connect({'api_key':'fixture-key','consent':True})['session_id']
        row=self.manager.sessions[token];self.manager.disconnect({'session_id':token})
        self.assertEqual(row['key'],'')
    def test_remote_error_releases_busy_and_is_sanitized(self):
        self.transport.fail=True
        with self.assertRaises(CloudError) as ex:self.call()
        self.assertEqual(ex.exception.code,'MCP_TOOL_FAILED');self.assertFalse(self.manager.sessions[self.token]['busy'])
    def test_disconnect_during_query_discards_result(self):
        old=self.transport.exchange
        def revoke(payload,*args):
            if payload['method']=='tools/call':self.manager.disconnect({'session_id':self.token})
            return old(payload,*args)
        self.transport.exchange=revoke
        with self.assertRaises(CloudError) as ex:self.call()
        self.assertEqual(ex.exception.code,'MCP_SESSION_EXPIRED')
    def test_transport_json_sse_and_wrong_id(self):
        class Response:
            status=200
            def read(self,size):return self.raw
            def getheader(self,name):return self.mime if name=='Content-Type' else None
        class Connection:
            def request(self,*args):self.request_args=args
            def getresponse(self):return response
            def close(self):pass
        response=Response();connection=Connection();transport=Context7Transport();payload={'jsonrpc':'2.0','id':'one','method':'tools/list'}
        with patch('src.lab.context7.http.client.HTTPSConnection',return_value=connection) as host:
            for mime in ('application/json','text/event-stream'):
                response.mime=mime;data=json.dumps({'jsonrpc':'2.0','id':'one','result':{'tools':[]}})
                response.raw=(data if mime=='application/json' else 'event: message\ndata: '+data+'\n\n').encode()
                self.assertEqual(transport.exchange(payload)[0],{'tools':[]})
            host.assert_called_with('mcp.context7.com',timeout=25)
            self.assertEqual(connection.request_args[1],'/mcp')
            response.raw=b'data: {"jsonrpc":"2.0","id":"wrong","result":{}}\n\n'
            with self.assertRaises(CloudError):transport.exchange(payload)

