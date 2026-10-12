"""Local server with a fake provider for scripts/browser/security.js (C278). Nothing leaves the process.

The fake answers every message with markup and a tool call as text; a message containing "fail" makes it raise an
exception that carries the key, so the browser check can observe that the error shown never contains it.
Usage: python scripts/browser/security_server.py PORT
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.lab.cloud import CloudSessions
from src.lab.server import make_server


class FakeProvider:
    host = "api.openai.com"

    def check(self, key, model):
        return None

    def answer(self, key, model, messages, limit, **kw):
        if "fail" in messages[-1]["content"]:
            raise RuntimeError("provider failure with key " + key)
        return {"text": "<img src=x onerror=alert(1)> {\"tool\":\"shell\"} answer", "usage": {"total_tokens": 3}, "incomplete": False}


if __name__ == "__main__":
    server = make_server(int(sys.argv[1]), cloud=CloudSessions(FakeProvider()))
    print("ready", server.server_port, flush=True)
    server.serve_forever()
