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
            # The shim loads before the app scripts and every asset path is relative to the project page.
            self.assertLess(html.index('src="public-demo.js"'), html.index('src="app.js"'))
            self.assertNotIn('src="/', html)
            self.assertNotIn('href="/', html)
            for name in ("orders.json", "policy.json", "scenarios.json", "roles.json"):
                self.assertTrue((out / "data" / name).is_file())
            # Key-entry views stay in the markup but are hidden by the public stylesheet.
            css = (out / "style.css").read_text(encoding="utf-8")
            for selector in ("#view-connection", "#context7Details", "#view-chat"):
                self.assertIn(".public-demo " + selector, css)
            # Public wording replaces the local-workspace and loopback text.
            self.assertIn('data-en="AI IMPLEMENTATION LAB · PUBLIC DEMO">AI IMPLEMENTATION LAB · DEMO PÚBLICA<', html)
            self.assertNotIn("ESPACIO LOCAL", html)
            self.assertIn("Esta demo pública ejecuta las reglas en tu navegador con datos ficticios.", html)
            self.assertNotIn("por loopback", html)
            self.assertIn('<p class="muted" data-en="This public demo runs the rules in your browser with fictional data. '
                          'The local version also includes optional model and MCP connections.">Esta demo pública', html)

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

    def test_workflows_run_verify_before_publishing(self):
        # R30: text checks only (stdlib, no YAML parser); the real run is recorded separately (C144).
        flows = Path(__file__).resolve().parents[1] / ".github/workflows"
        verify = (flows / "verify.yml").read_text(encoding="utf-8")
        for needle in ("push:", "pull_request:", "ubuntu-latest", "windows-latest", "contents: read",
                       "timeout-minutes:", "python scripts/verify.py"):
            self.assertIn(needle, verify)
        self.assertNotIn("secrets.", verify)
        pages = (flows / "pages.yml").read_text(encoding="utf-8")
        # verify.py rewrites evidence; the committed files are restored before the build (D21).
        self.assertLess(pages.index("scripts/verify.py"), pages.index("git checkout -- ."))
        self.assertLess(pages.index("git checkout -- ."), pages.index("scripts/build_pages.py"))

if __name__ == "__main__":
    unittest.main()
