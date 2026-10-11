"""U17 checks: presentation (R34), tour (R35), evidence status (R36), documentation (R37),
navigation and languages (R38) and the single CI with reproducible evidence (R39)."""
import csv
import http.client
import io
import json
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from html.parser import HTMLParser
from pathlib import Path
from scripts.build_pages import ROOT, build
from scripts import check_evidence
from src.lab import cli
from src.lab.server import make_server

HTML = (ROOT / "web/index.html").read_text(encoding="utf-8")


class Leaves(HTMLParser):
    """Text-bearing leaf elements inside the U17 regions, with their data-en attribute."""
    REGIONS = ("presentation", "tour", "statusRecords", "badge-legend")
    VOID = {"br", "img", "input", "meta", "link"}

    def __init__(self):
        super().__init__()
        self.stack, self.leaves = [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        values = dict(attrs)
        inside = any(r in (values.get("class") or "").split() or values.get("id") == r for r in self.REGIONS)
        if self.stack:
            self.stack[-1]["children"] = True
        self.stack.append({"tag": tag, "attrs": values, "text": "", "children": False,
                           "region": bool(inside or (self.stack and self.stack[-1]["region"]))})

    def handle_data(self, data):
        if self.stack:
            self.stack[-1]["text"] += data

    def handle_endtag(self, tag):
        if tag in self.VOID or not self.stack:
            return
        node = self.stack.pop()
        if node["region"] and not node["children"] and node["text"].strip():
            self.leaves.append(node)


class PresentationTests(unittest.TestCase):
    def test_session_first_screen_presents_marco_before_the_composer(self):
        session = HTML[HTML.index('id="view-chat"'):HTML.index('id="chatForm"')]
        self.assertIn('<h1 id="introName" tabindex="-1">Marco Díaz de León</h1>', session)
        for text in ("ESTRATEGIA E IMPLEMENTACIÓN DE IA", "defino el problema y el alcance, fijo los criterios de aceptación",
                     "El código de este laboratorio se escribió con asistencia de IA.",
                     'href="#method" data-en="Start the three-minute tour"',
                     "Demo pública: sin cuenta, clave ni modelo. Laboratorio local:", "Pendiente: aceptación del dueño"):
            self.assertIn(text, session)
        # One h1 per view: the greeting is now a level-2 heading.
        self.assertEqual(session.count("<h1"), 1)
        self.assertIn('<h2 id="chat-title"', session)

    def test_public_build_keeps_presentation_and_five_destinations(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            html = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="presentation"', html)
            self.assertEqual(re.findall(r'data-view="(\w+)"', html), ["demo", "agents", "mcp", "method", "evidence"])
            self.assertFalse(re.search(r'id="(examplePanel|scenario|propose|execute|receiptCount)"', html))

    def test_readme_order_length_and_screenshot(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for first, second in (("Marco Díaz de León", "The code was written with AI assistance"),
                              ("The code was written with AI assistance", "First action"), ("First action", "## Three routes")):
            self.assertLess(text.index(first), text.index(second))
        body = re.sub(r"```.*?```", "", text, flags=re.S)
        body = "\n".join(line for line in body.splitlines() if not line.lstrip().startswith("|"))
        words = re.findall(r"\S+", re.sub(r"!\[[^\]]*\]\([^)]*\)|\]\([^)]*\)", "", body))
        self.assertLessEqual(len(words), 700)
        image = re.search(r"!\[[^\]]*\]\(([^)]+)\)", text).group(1)
        self.assertEqual(image, "docs/assets/presentation-20261011.jpg")
        self.assertTrue((ROOT / image).is_file())
        links = re.findall(r"\]\(([^)]+)\)", text)
        self.assertEqual(len(links), len(set(links)))
        self.assertNotIn("AI proposes", text)


class TourTests(unittest.TestCase):
    def test_tour_receipts_blocks_and_replay(self):
        result = cli.tour()
        self.assertEqual([s["receipts"] for s in result["steps"]], [0, 0, 0, 0, 1, 1])
        self.assertEqual([s["result"] for s in result["steps"]],
                         ["PENDING_APPROVAL", "APPROVAL_REQUIRED", "APPROVED", "SIMULATED_CONNECTOR_FAILURE", "SIMULATED", "SIMULATED"])
        self.assertIsNotNone(result["steps"][4]["receipt_id"])
        self.assertEqual(result["steps"][4]["receipt_id"], result["steps"][5]["receipt_id"])
        self.assertTrue(result["audit_chain_valid"])
        self.assertEqual((result["model_calls"], result["real_effects"]), (0, 0))
        self.assertEqual(cli.tour(), result)  # a fresh lab each run: same outcome, no state to clear

    def test_tour_text_names_a_simulated_proposal_in_both_languages(self):
        for language, phrase in (("es", "el laboratorio genera una propuesta simulada"), ("en", "the lab generates a simulated proposal")):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                cli.print_tour(language)
            output = buffer.getvalue()
            self.assertIn(phrase, output)
            self.assertNotRegex(output.lower(), r"\b(la ia propone|ai proposes)\b")
            self.assertEqual(output.count("\n   -> "), 6)

    def test_in_app_tour_steps_have_expected_results_and_live_links(self):
        tour = HTML[HTML.index('<section class="tour"'):HTML.index('<h2 class="method-heading"')]
        self.assertEqual(tour.count('<li><span class="tour-time"'), 4)
        self.assertEqual(tour.count('class="tour-expected"'), 4)
        self.assertIn("python run.py tour", tour)
        self.assertIn('href="https://github.com/marcodiazleon"', tour)
        spec = (ROOT / "specs/001-support-demo/spec.md").read_text(encoding="utf-8")
        for requirement in re.findall(r'href="#evidence/(R\d+)"', tour):
            self.assertIn("\n| " + requirement + " |", spec)


NODE_RULES = r"""
const fs = require("fs"), vm = require("vm");
const ctx = {}; ctx.window = ctx; vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"), ctx);
const input = JSON.parse(fs.readFileSync(0, "utf8"));
process.stdout.write(JSON.stringify(input.map(([cases, id]) => [ctx.LabEvidenceRules.badge(cases, id), ctx.LabEvidenceRules.tally(cases, id)])));
"""


class EvidenceRuleTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which("node"):
            self.skipTest("node not available")

    def run_rules(self, calls):
        out = subprocess.run([shutil.which("node"), "-e", NODE_RULES, str(ROOT / "web/evidence-rules.js")],
                             input=json.dumps(calls), capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)

    def test_badge_negatives(self):
        case = lambda status, evidence="evidence/latest.json", observed="x": {
            "requirement_id": "R99", "status": status, "evidence": evidence, "observed": observed}
        table = [
            ([case("PASS"), case("PASS")], "PASS"),
            ([case("PASS"), case("NO_PROBADO", "")], "PARCIAL"),
            ([case("PASS"), case("FAIL")], "FAIL"),
            ([case("PASS"), case("BLOQUEADO")], "BLOQUEADO"),
            ([case("FAIL"), case("BLOQUEADO")], "FAIL"),
            ([case("PASS"), case("NO_APLICA", "", "Superseded by U13")], "PASS"),
            ([case("NO_APLICA", "", "Superseded by U13")], "PENDIENTE"),
            ([case("PASS", "")], "PENDIENTE"),
            ([], "PENDIENTE"),
        ]
        results = self.run_rules([[cases, "R99"] for cases, _ in table])
        self.assertEqual([r[0] for r in results], [expected for _, expected in table])
        self.assertEqual(results[1][1], {"applicable": 2, "passed": 1, "failed": False, "blocked": False})

    def test_committed_cases_with_untested_rows_are_partial(self):
        with (ROOT / "specs/001-support-demo/acceptance.csv").open(encoding="utf-8", newline="") as handle:
            cases = list(csv.DictReader(handle))
        results = self.run_rules([[cases, r] for r in ("R11", "R16", "R17", "R01")])
        self.assertEqual([r[0] for r in results[:3]], ["PARCIAL"] * 3)
        self.assertEqual(results[3][0], "PASS")


class StatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def get(self, path, host=None):
        c = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        c.request("GET", path, headers={"Host": host} if host else {})
        r = c.getresponse(); result = (r.status, r.read()); c.close()
        return result

    def test_status_route_separates_records_and_reports_fingerprint(self):
        status, raw = self.get("/api/status")
        body = json.loads(raw)
        self.assertEqual(status, 200)
        self.assertEqual(body["source_fingerprint"], check_evidence.source_fingerprint())
        self.assertEqual(body["independent_review"]["status"], "LIMITED")
        self.assertEqual(body["acceptance"], "OWNER_ACCEPTANCE_NOT_RECORDED")
        self.assertEqual(set(body["independent_review"]["scope"]), {"es", "en"})
        self.assertTrue({"integration", "deployment"} <= set(body))
        self.assertEqual(self.get("/api/status", host="evil.example")[0], 403)
        self.assertEqual(self.get("/evidence-rules.js")[0], 200)

    def test_public_build_ships_status_and_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            status = json.loads((out / "data/status.json").read_text(encoding="utf-8"))
            self.assertEqual(status["source_fingerprint"], check_evidence.source_fingerprint())
            self.assertIn('"/api/status": "status.json"', (out / "public-demo.js").read_text(encoding="utf-8"))
            html = (out / "index.html").read_text(encoding="utf-8")
            self.assertLess(html.index('src="evidence-rules.js"'), html.index('src="evidence.js"'))
            legend = html[html.index('class="badge-legend"'):]
            for state in ("PASS", "PARCIAL", "PENDIENTE", "BLOQUEADO", "FAIL", "NO_APLICA"):
                self.assertIn("<b>" + state + "</b>", legend)


class EvidenceCheckTests(unittest.TestCase):
    def copy(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "repo"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "_site", ".local"))
        evidence = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
        evidence.update(source_id=check_evidence.source_fingerprint(root), source_sha256=check_evidence.source_hashes(root),
                        record_id=check_evidence.record_fingerprint(root), record_sha256=check_evidence.record_hashes(root), passed=True)
        (root / "evidence/latest.json").write_text(json.dumps(evidence), encoding="utf-8")
        return root

    def test_fingerprint_drift_is_rejected(self):
        root = self.copy()
        self.assertEqual(check_evidence.check_committed(root), [])
        (root / "src/lab/models.py").write_text("# changed\n", encoding="utf-8")
        errors = check_evidence.check_committed(root)
        self.assertEqual(len(errors), 2)
        self.assertIn("src/lab/models.py", errors[1])

    def test_failed_committed_run_and_status_drift_are_rejected(self):
        root = self.copy()
        evidence = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
        evidence["passed"] = False
        (root / "evidence/latest.json").write_text(json.dumps(evidence), encoding="utf-8")
        self.assertIn("Committed evidence is not a passing run", check_evidence.check_committed(root))
        old = {"test_results": [{"test_id": "a", "status": "PASS"}, {"test_id": "b", "status": "PASS"}], "acceptance_states": {"PASS": 2}}
        new = {"test_results": [{"test_id": "a", "status": "PASS"}, {"test_id": "b", "status": "NO_PROBADO"}], "acceptance_states": {"PASS": 1}}
        self.assertEqual(check_evidence.compare_statuses(old, new), ["Status drift: b PASS -> NO_PROBADO", "Acceptance state counts drift"])
        self.assertEqual(check_evidence.compare_statuses(old, old), [])


class CiTests(unittest.TestCase):
    def test_single_reusable_verification_and_least_privilege_deploy(self):
        workflows = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / ".github/workflows").glob("*.yml")}
        self.assertEqual(set(workflows), {"verify.yml", "pages.yml"})
        verify, pages = workflows["verify.yml"], workflows["pages.yml"]
        self.assertEqual([name for name, text in workflows.items() if "python scripts/verify.py" in text], ["verify.yml"])
        for trigger in ("push:", "pull_request:", "workflow_dispatch:", "workflow_call:"):
            self.assertIn(trigger, verify)
        for combo in ('{ os: ubuntu-latest, python: "3.11" }', '{ os: ubuntu-latest, python: "3.13" }', '{ os: windows-latest, python: "3.13" }'):
            self.assertIn(combo, verify)
        steps = [line.strip() for line in verify[:verify.index("  verify-windows:")].splitlines() if line.strip().startswith("- run:")]
        self.assertLess(steps.index("- run: python scripts/check_evidence.py"), steps.index("- run: python scripts/verify.py"))
        self.assertLess(steps.index("- run: python scripts/verify.py"),
                        steps.index("- run: python scripts/check_evidence.py --against committed-latest.json"))
        self.assertIn("uses: ./.github/workflows/verify.yml", pages)
        self.assertEqual(pages.count("pages: write"), 1)
        self.assertLess(pages.index("deploy:"), pages.index("pages: write"))
        self.assertNotIn("pages: write", verify)
        self.assertIn("persist-credentials: false", verify)


class LanguageAndDocsTests(unittest.TestCase):
    def test_new_copy_has_english_text(self):
        parser = Leaves(); parser.feed(HTML)
        technical = re.compile(r"^(R\d+|PASS|PARCIAL|PENDIENTE|BLOQUEADO|FAIL|NO_APLICA|python run\.py tour|Marco Díaz de León|\d+"
                               r"|(PENDING_APPROVAL|APPROVAL_REQUIRED|APPROVED|SIMULATED_CONNECTOR_FAILURE|SIMULATED)( · SIM-[0-9a-f]+)?)$")
        missing = [n["text"].strip() for n in parser.leaves if "data-en" not in n["attrs"] and not technical.match(n["text"].strip())]
        self.assertEqual(missing, [])
        self.assertGreater(len(parser.leaves), 40)

    def test_skip_link_targets_an_existing_element_and_rail_has_labels(self):
        target = re.search(r'class="skip-link" href="#([\w-]+)"', HTML).group(1)
        self.assertIn('id="' + target + '"', HTML)
        css = (ROOT / "web/style.css").read_text(encoding="utf-8")
        self.assertIn("body.sidebar-collapsed .sidebar nav a .nav-label{display:block", css)
        # The router would move focus to the view heading; the skip link handler keeps it in the message box.
        studio = (ROOT / "web/studio.js").read_text(encoding="utf-8")
        self.assertIn("document.querySelector('.skip-link').addEventListener('click'", studio)
        self.assertIn("el('question').focus()", studio)
        for gray in ("#666672", "#72727e", "color:#777;"):
            self.assertNotIn(gray, css)

    def test_index_routes_history_and_traceability_example(self):
        index = (ROOT / "docs/INDEX.md").read_text(encoding="utf-8")
        for heading in ("## Three routes", "## Technical review", "## One requirement from need to evidence", "## Historical documents"):
            self.assertIn(heading, index)
        history = index[index.index("## Historical documents"):]
        for report in (ROOT / "reports").glob("*.md"):
            self.assertIn(report.name, history)
        for link in ("R03", "T02", "Lab.execute", "test_execute_requires_approval", "C018", "81dfced59cc85231e25732137859923b39a2beed"):
            self.assertIn(link, index)
        capabilities = (ROOT / "docs/capabilities.md").read_text(encoding="utf-8")
        self.assertIn("| Area | Public demo, no account or key | Local lab | Pending | Limit |", capabilities)

    def test_startup_and_verify_warn_about_rewritten_evidence(self):
        from scripts.check_environment import inspect
        self.assertIn("rewrites evidence/latest.json", inspect()["note"])
        self.assertIn("this run rewrote evidence/latest.json", (ROOT / "scripts/verify.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
