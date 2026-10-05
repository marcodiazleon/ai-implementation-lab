"""Regression checks for U12: conversation-only Session and truthful static preview."""
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from scripts.build_pages import ROOT, build
from src.lab.model_catalog import catalog

class PageElements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.views = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("data-view"):
            self.views.append(values["data-view"])

class SessionShellTests(unittest.TestCase):
    def test_session_has_chat_and_five_destinations_without_refund_exercise(self):
        page = PageElements()
        html = (ROOT / "web/index.html").read_text(encoding="utf-8")
        page.feed(html)
        self.assertEqual(page.views, ["demo", "agents", "mcp", "method", "evidence"])
        self.assertTrue({"view-chat", "question", "messages", "sessionProvider",
                         "sessionModel", "sessionEffort", "chatAgent", "connectionDialog"} <= page.ids)
        self.assertFalse({"examplePanel", "scenario", "propose", "execute", "trace", "receiptCount"} & page.ids)
        self.assertNotIn('src="/app.js"', html)
        self.assertNotIn('data-panel="connection"', html)

    def test_public_catalog_matches_local_catalog_without_enabling_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            public = json.loads((out / "data/model-catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(public, catalog())
            self.assertEqual({m["provider"] for m in public["models"]}, {"openai", "anthropic"})
            self.assertIn('"/api/model-catalog": "model-catalog.json"',
                          (out / "public-demo.js").read_text(encoding="utf-8"))
            cloud = (out / "cloud.js").read_text(encoding="utf-8")
            self.assertIn("if(publicPreview||busy||session)return", cloud)
            self.assertIn("el('connectApi').disabled=publicPreview", cloud)

    def test_legacy_connection_hash_opens_dialog_and_never_targets_removed_exercise(self):
        studio = (ROOT / "web/studio.js").read_text(encoding="utf-8")
        self.assertIn("if(hash==='connection')window.LabCloud?.openConnection()", studio)
        self.assertNotIn("el('examplePanel')", studio)
        cloud = (ROOT / "web/cloud.js").read_text(encoding="utf-8")
        self.assertIn("el('openConnection').onclick=openConnection", cloud)
        self.assertIn("el('connectionDialog').close()", cloud)
