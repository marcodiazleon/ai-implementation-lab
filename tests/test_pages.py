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

if __name__ == "__main__":
    unittest.main()
