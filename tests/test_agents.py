import hashlib
import json
import unittest
from src.lab.agents import contracts, run_agent
from src.lab.cloud import CloudError, CloudSessions

class Transport:
    def __init__(self):self.calls=[];self.bad=False;self.incomplete=False
    def check(self,*args):pass
    def answer(self,key,model,messages,limit):
        self.calls.append(messages)
        data={"summary":"Scoped response","deliverables":["A technical proposal"],"open_questions":[],"checks":["No execution"],"sources":[]}
        return {"text":"invalid" if self.bad else json.dumps(data),"usage":{"total_tokens":50},"incomplete":self.incomplete}

class AgentTests(unittest.TestCase):
    def setUp(self):
        self.transport=Transport();self.cloud=CloudSessions(self.transport)
        self.token=self.cloud.connect({"api_key":"x"*24,"model":"fixture","max_output_tokens":1024,"consent":True})["session_id"]
        self.body={"agent":"manager","mode":"local","brief":"Design a support request review tool for a small business.","language":"en"}
    def run_body(self,**extra):return run_agent({**self.body,**extra},self.cloud)
    def assert_code(self,code,**extra):
        with self.assertRaises(CloudError) as exc:self.run_body(**extra)
        self.assertEqual(exc.exception.code,code)
    def test_all_roles_produce_hashed_bilingual_templates(self):
        self.assertEqual(len(contracts()),4)
        for role in ("manager","researcher","implementer","reviewer"):
            for lang in ("es","en"):
                r=self.run_body(agent=role,language=lang)
                self.assertEqual(r["artifact_sha256"],hashlib.sha256(r["text"].encode()).hexdigest())
                self.assertEqual(len(r["hooks"]),4);self.assertEqual(r["product_tests"],"NOT_EXECUTED")
                self.assertFalse(r["release_approval"])
        self.assertEqual(self.transport.calls,[])
    def test_stale_brief_context_blocked(self):
        r=self.run_body();a={k:r[k] for k in ("agent","brief_hash","text")}
        self.assert_code("AGENT_STALE_CONTEXT",brief="This is a different customer brief that must not reuse context.",artifacts=[a])
    def test_context_size_and_secret_guards(self):
        self.assert_code("AGENT_SENSITIVE_INPUT",brief="Do something with sk-"+"x"*25)
        self.assert_code("AGENT_INVALID_INPUT",documentation="a"*12001)
        self.assert_code("AGENT_INVALID_INPUT",agent=[])
    def test_openai_requires_consent_before_call(self):
        self.assert_code("AGENT_CONSENT_REQUIRED",mode="openai",session_id=self.token)
        self.assertFalse(self.transport.calls)
    def test_model_task_isolated_from_chat_and_bounded(self):
        self.cloud.ask({"session_id":self.token,"message":"Private chat context"})
        before=list(self.cloud.sessions[self.token]["history"])
        r=self.run_body(mode="openai",session_id=self.token,consent=True)
        self.assertNotIn("Private chat context",json.dumps(self.transport.calls[-1]))
        self.assertEqual(self.cloud.sessions[self.token]["history"],before)
        self.assertEqual(self.cloud.sessions[self.token]["requests"],2)
        self.assertEqual(r["usage"]["total_tokens"],50)
    def test_invalid_or_truncated_model_output_fails(self):
        self.transport.bad=True
        self.assert_code("AGENT_INVALID_OUTPUT",mode="openai",session_id=self.token,consent=True)
        self.transport.bad=False;self.transport.incomplete=True
        self.assert_code("AGENT_INCOMPLETE_OUTPUT",mode="openai",session_id=self.token,consent=True)
        self.assertFalse(self.cloud.sessions[self.token]["busy"])
    def test_shared_budget_and_revocation(self):
        self.cloud.sessions[self.token]["requests"]=20
        self.assert_code("SESSION_REQUEST_LIMIT",mode="openai",session_id=self.token,consent=True)
        self.cloud.disconnect({"session_id":self.token})
        self.assert_code("SESSION_EXPIRED",mode="openai",session_id=self.token,consent=True)
    def test_reviewer_reports_missing_artifacts(self):
        r=self.run_body(agent="reviewer")
        self.assertIn("manager, researcher, implementer",r["text"])

