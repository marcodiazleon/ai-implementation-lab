import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.build_pages import build

class PagesBuildTests(unittest.TestCase):
    def test_public_build_runs_in_browser_without_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            html = (out / "index.html").read_text(encoding="utf-8")
            self.assertLess(html.index('src="public-demo.js"'), html.index('src="cloud.js"'))
            self.assertNotIn('src="/', html)
            self.assertNotIn('href="/', html)
            for name in ("orders.json", "policy.json", "scenarios.json", "roles.json"):
                self.assertTrue((out / "data" / name).is_file())
            css = (out / "style.css").read_text(encoding="utf-8")
            self.assertNotIn(".public-demo #view-chat", css)
            self.assertIn(".public-demo #context7Details", css)
            self.assertIn("AI IMPLEMENTATION LAB · VISTA PÚBLICA", html)
            self.assertNotIn("ESPACIO LOCAL", html)
            self.assertIn("Las conversaciones por API se ejecutan en la versión local.", html)
            self.assertNotIn("por loopback", html)

    def test_public_build_ships_evidence_data_not_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            for name in ("latest.json", "acceptance.csv", "requirements.json"):
                self.assertTrue((out / "data" / name).is_file())
            self.assertFalse(list(out.rglob("spec.md")))
            ids = [r["id"] for r in json.loads((out / "data/requirements.json").read_text(encoding="utf-8"))]
            self.assertIn("R27", ids)
            html = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="view-evidence"', html)
            self.assertIn('src="evidence.js"', html)

    def test_requirement_ids_match_acceptance_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            ids = {r["id"] for r in json.loads((out / "data/requirements.json").read_text(encoding="utf-8"))}
            with (out / "data/acceptance.csv").open(encoding="utf-8", newline="") as h:
                self.assertEqual(ids, {row["requirement_id"] for row in csv.DictReader(h)})
