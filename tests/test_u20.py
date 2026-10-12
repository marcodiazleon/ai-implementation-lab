"""U20 checks: records computed against this build (R49), interface structure and bilingual validation (R50),
the semantic requirement matrix and the fail-closed demonstration (R51), documentation (R52) and the
behavior-level cases the matrix asked for (R17, R39–R43)."""
import csv
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from scripts.build_pages import ROOT, build
from scripts import check_evidence, ci_gate, requirement_matrix, revision
from scripts.sdd_check import validate as validate_sdd
from src.lab.server import make_server

HTML = (ROOT / "web/index.html").read_text(encoding="utf-8")
NODE = shutil.which("node")
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="lab", GIT_AUTHOR_EMAIL="lab@example.invalid",
               GIT_COMMITTER_NAME="lab", GIT_COMMITTER_EMAIL="lab@example.invalid")


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, env=GIT_ENV, check=True).stdout.strip()


def copy_repo(testcase):
    temp = tempfile.TemporaryDirectory(); testcase.addCleanup(temp.cleanup)
    root = Path(temp.name) / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "_site", ".local", "*.jpg", "node_modules"))
    return root


NODE_ROWS = r"""
const fs = require("fs"), vm = require("vm");
const ctx = {}; ctx.window = ctx; vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"), ctx);
const input = JSON.parse(fs.readFileSync(0, "utf8"));
process.stdout.write(JSON.stringify(input.map(([status, evidence, lang]) => ctx.LabEvidenceRules.statusRows(status, evidence, lang))));
"""

NODE_I18N = r"""
// Minimal document so web/i18n.js can load without a browser; only validityMessage is exercised.
const fs = require("fs"), vm = require("vm");
const lang = process.argv[2];
const noop = () => {};
const element = { addEventListener: noop, setAttribute: noop, getAttribute: () => null, value: "", textContent: "" };
const document = { body: {}, documentElement: {}, createTreeWalker: () => ({ nextNode: () => false }), querySelectorAll: () => [],
  getElementById: () => element, addEventListener: noop };
const ctx = { document, localStorage: { getItem: () => lang, setItem: noop }, console, NodeFilter: { SHOW_TEXT: 4 } };
ctx.window = ctx; ctx.Event = class {}; ctx.dispatchEvent = noop; ctx.addEventListener = noop;
vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"), ctx);
const cases = [{ validity: { valueMissing: true } }, { validity: { tooShort: true }, minLength: 20 }, { validity: { valid: true } }, { validity: { typeMismatch: true } }];
process.stdout.write(JSON.stringify(cases.map((f) => ctx.LabI18n.validityMessage(f))));
"""


class RecordTests(unittest.TestCase):
    def synthetic_repo(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        git(root, "init", "-q", "-b", "main")
        (root / "file.txt").write_text("base\n", encoding="utf-8")
        git(root, "add", "file.txt"); git(root, "commit", "-q", "-m", "base")
        (root / "file.txt").write_text("accepted\n", encoding="utf-8")
        git(root, "commit", "-q", "-am", "accepted"); accepted = git(root, "rev-parse", "HEAD")
        git(root, "commit", "-q", "--allow-empty", "-m", "merge with the same content"); merge = git(root, "rev-parse", "HEAD")
        (root / "file.txt").write_text("later\n", encoding="utf-8")
        git(root, "commit", "-q", "-am", "later"); later = git(root, "rev-parse", "HEAD")
        return root, accepted, merge, later

    def test_git_states_on_a_synthetic_repository(self):
        root, accepted, merge, later = self.synthetic_repo()
        status = {"independent_review": {"revision": accepted}, "acceptance": {"revision": accepted},
                  "integration": {"main": merge}, "deployment": {"revision": merge}}
        at_merge = revision.build_states(status, root, merge)
        self.assertEqual({k: at_merge[k] for k in ("independent_review", "acceptance", "integration", "deployment")},
                         {"independent_review": True, "acceptance": True, "integration": True, "deployment": True})
        at_later = revision.build_states(status, root, later)
        self.assertEqual({k: at_later[k] for k in ("acceptance", "integration", "deployment")},
                         {"acceptance": False, "integration": False, "deployment": False})
        unknown = revision.build_states(dict(status, acceptance={"revision": "0" * 40}), root, merge)
        self.assertIsNone(unknown["acceptance"])
        self.assertIn("not in this checkout's history", unknown["reasons"]["acceptance"])
        missing = revision.build_states({"acceptance": {}, "integration": {}}, root, merge)
        self.assertEqual((missing["acceptance"], missing["deployment"], missing["integration"]), (None, None, None))
        self.assertEqual(missing["reasons"]["integration"], "no main revision recorded")
        with tempfile.TemporaryDirectory() as empty:
            none = revision.build_states(status, Path(empty))
            self.assertFalse(none["git"])
            self.assertEqual(none["reasons"]["acceptance"], "Git unavailable")

    @unittest.skipUnless(NODE, "node is required")
    def test_status_view_model_states_and_negatives(self):
        status = json.loads((ROOT / "docs/project-status.json").read_text(encoding="utf-8"))
        evidence = {"passed": True, "tests": {"run": 3}, "generated_utc": "2026-10-12T00:00:00", "input_revision": "a" * 40}
        covered = dict(status, build_states={"git": True, "reasons": {}, "independent_review": True, "acceptance": True, "integration": True, "deployment": True})
        candidate = dict(status, build_states={"git": True, "reasons": {}, "independent_review": False, "acceptance": False, "integration": False, "deployment": False})
        unknown = dict(status, build_states={"git": False, "reasons": {"acceptance": "Git unavailable", "integration": "Git unavailable", "deployment": "Git unavailable", "independent_review": "Git unavailable"}})
        absent = {k: v for k, v in status.items() if k not in ("acceptance", "deployment")}
        absent["build_states"] = {"git": True, "reasons": {"acceptance": "no revision recorded", "deployment": "no revision recorded"}, "integration": True, "independent_review": True}
        out = subprocess.run([NODE, "-e", NODE_ROWS, str(ROOT / "web/evidence-rules.js")], capture_output=True, text=True, check=True,
                             input=json.dumps([[covered, evidence, "en"], [candidate, evidence, "es"], [unknown, evidence, "en"], [absent, evidence, "en"],
                                               [None, evidence, "en"], [status, {"tests": {}}, "es"], [status, "text", "en"]]))
        results = json.loads(out.stdout)
        rows = results[0]["rows"]
        self.assertEqual([r["key"] for r in rows], ["verification", "review", "acceptance", "integration", "deployment"])
        self.assertEqual([r["state"] for r in rows], ["PASS", "COVERED", "COVERED", "CONTAINED", "COVERED"])
        self.assertIn("covers this build", rows[2]["value"]); self.assertIn("revision fb7ecf6", rows[2]["value"])
        cand = results[1]["rows"]
        self.assertEqual([r["state"] for r in cand][1:], ["OTHER_REVISION", "OTHER_REVISION", "NOT_CONTAINED", "OTHER_REVISION"])
        self.assertIn("esta revisión no está aceptada", cand[2]["value"]); self.assertIn("Pages publica 166ea91", cand[4]["value"])
        self.assertIn("esta revisión no está publicada", cand[4]["value"])
        self.assertTrue(all(r["state"] == "UNKNOWN" for r in results[2]["rows"][1:]))
        self.assertIn("undetermined (Git unavailable)", results[2]["rows"][2]["value"])
        absent_rows = results[3]["rows"]
        self.assertEqual((absent_rows[2]["state"], absent_rows[2]["value"]), ("NOT_RECORDED", "Not recorded"))
        self.assertEqual(absent_rows[4]["state"], "NOT_RECORDED")
        for bad in results[4:]:
            self.assertTrue(bad["error"]); self.assertEqual(bad["rows"], [])

    def test_sdd_check_rejects_bad_or_missing_record_revisions(self):
        root = copy_repo(self)
        status_path = root / "docs/project-status.json"
        original = json.loads(status_path.read_text(encoding="utf-8"))
        short = json.loads(json.dumps(original)); short["acceptance"]["revision"] = "fb7ecf6"
        status_path.write_text(json.dumps(short), encoding="utf-8")
        self.assertIn("Record acceptance.revision is not a 40-character revision", validate_sdd(root))
        missing = {k: v for k, v in original.items() if k != "deployment"}
        status_path.write_text(json.dumps(missing), encoding="utf-8")
        self.assertIn("Missing record object: deployment", validate_sdd(root))
        status_path.write_text(json.dumps(original), encoding="utf-8")
        self.assertEqual([e for e in validate_sdd(root) if e.startswith("Record") or e.startswith("Missing record")], [])
        # With a Git history that does not contain the recorded revisions, every record is rejected.
        git(root, "init", "-q", "-b", "main"); git(root, "add", "-A"); git(root, "commit", "-q", "-m", "copy")
        errors = [e for e in validate_sdd(root) if "is not in the history of this checkout" in e]
        self.assertEqual(len(errors), 5, errors)

    def test_build_and_server_payload_agree_with_git(self):
        head = git(ROOT, "rev-parse", "HEAD"); head_tree = git(ROOT, "rev-parse", head + "^{tree}")
        status = json.loads((ROOT / "docs/project-status.json").read_text(encoding="utf-8"))
        expected = {}
        for key in ("independent_review", "acceptance", "deployment"):
            expected[key] = git(ROOT, "rev-parse", status[key]["revision"] + "^{tree}") == head_tree
        expected["integration"] = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", head, status["integration"]["main"]], capture_output=True).returncode == 0
        for key in ("independent_review", "acceptance", "deployment"):
            self.assertRegex(status[key]["revision"], r"^[0-9a-f]{40}$")
        self.assertRegex(status["integration"]["main"], r"^[0-9a-f]{40}$")
        server = make_server(0); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            c = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5); c.request("GET", "/api/status"); body = json.loads(c.getresponse().read()); c.close()
        finally:
            server.shutdown(); server.server_close(); thread.join()
        with tempfile.TemporaryDirectory() as tmp:
            built = json.loads((build(Path(tmp) / "site") / "data/status.json").read_text(encoding="utf-8"))
        for payload in (body, built):
            self.assertEqual(payload["revision"], head)
            self.assertEqual({k: payload["build_states"][k] for k in expected}, expected)
            self.assertTrue(payload["build_states"]["git"])

    def test_evidence_markup_has_error_state_and_no_hand_written_states(self):
        self.assertIn('<button id="evidenceRetry" type="button" hidden data-en="Retry loading the evidence">', HTML)
        view = (ROOT / "web/evidence.js").read_text(encoding="utf-8")
        self.assertIn("LabEvidenceRules.statusRows(status, evidence, LabI18n.language)", view)
        for literal in ("NOT_DEPLOYED", "NOT_INTEGRATED", "OWNER_ACCEPTANCE_NOT_RECORDED", "this_branch", "pages_source"):
            self.assertNotIn(literal, view)
        self.assertIn('el("evidenceRetry").addEventListener("click", load)', view)
        status = (ROOT / "docs/project-status.json").read_text(encoding="utf-8")
        for stale in ("NOT_DEPLOYED", "NOT_INTEGRATED", "OWNER_ACCEPTANCE_NOT_RECORDED", "evidence_scope"):
            self.assertNotIn(stale, status)


class InterfaceTests(unittest.TestCase):
    @unittest.skipUnless(NODE, "node is required")
    def test_validation_and_mcp_notices_are_bilingual(self):
        messages = {}
        for lang in ("es", "en"):
            out = subprocess.run([NODE, "-e", NODE_I18N, str(ROOT / "web/i18n.js"), lang], capture_output=True, text=True, check=True)
            messages[lang] = json.loads(out.stdout)
        self.assertEqual(messages["es"], ["Completa este campo.", "Escribe al menos 20 caracteres.", "", "Revisa el formato de este campo."])
        self.assertEqual(messages["en"], ["Fill in this field.", "Enter at least 20 characters.", "", "Check the format of this field."])
        i18n = (ROOT / "web/i18n.js").read_text(encoding="utf-8")
        workbench = (ROOT / "web/workbench.js").read_text(encoding="utf-8")
        notices = re.findall(r'(?:bind\("mcpStatus",|[A-Z_]+:)"([^"]+)"', workbench)
        self.assertGreater(len(notices), 4)
        for notice in notices:
            self.assertIn(json.dumps(notice, ensure_ascii=False) + ":", i18n, notice)

    def test_identity_tokens_and_attribution(self):
        css = (ROOT / "web/style.css").read_text(encoding="utf-8")
        tokens = dict(re.findall(r"--(ink|paper|muted|line):\s*([^;]+);", css))
        self.assertEqual(set(tokens), {"ink", "paper", "muted", "line"})
        self.assertRegex(css, r"--bg:\s*#0[0-9a-f]{5};")
        self.assertRegex(css, r"--ink:\s*#f[0-9a-f]{5};")
        self.assertIn('class="attribution" data-en="The code in this lab was written with AI assistance.', HTML)
        self.assertIn("se escribió con asistencia de IA", HTML)

    def test_routes_and_legacy_hashes(self):
        nav = HTML[HTML.index('<nav id="mainNav"'):HTML.index("</nav>")]
        self.assertEqual(re.findall(r'href="#(\w+)" data-view="(\w+)"', nav),
                         [("session", "demo"), ("agents", "agents"), ("mcp", "mcp"), ("method", "method"), ("evidence", "evidence")])
        studio = (ROOT / "web/studio.js").read_text(encoding="utf-8")
        self.assertIn("['chat','session'].includes(hash)?'demo'", studio)
        self.assertIn("if(hash==='connection')window.LabCloud?.openConnection()", studio)

    def test_menu_landmarks_and_language_options(self):
        self.assertIn('<button id="toggleSidebar" aria-controls="mainNav" aria-expanded="true" aria-label="Contraer menú">', HTML)
        self.assertIn('<nav id="mainNav" aria-label="Secciones">', HTML)
        picker = HTML[HTML.index('<select id="language"'):]
        picker = picker[:picker.index("</select>")]
        self.assertEqual(re.findall(r'value="(\w+)"', picker), ["es", "en"])

    def test_mcp_guide_fields_and_export_shape(self):
        form = HTML[HTML.index('<form id="mcpGuideForm"'):HTML.index("</form>", HTML.index('<form id="mcpGuideForm"'))]
        for field in ("mcpProfileName", "mcpTransport", "mcpUrl", "mcpCommand"):
            self.assertIn('id="' + field + '"', form)
        self.assertIn("pattern=", form)
        studio = (ROOT / "web/studio.js").read_text(encoding="utf-8")
        self.assertIn("mcpServers", studio)
        self.assertNotIn("child_process", studio)

    def test_composer_label_and_motion_rules(self):
        self.assertIn('<label for="question" class="sr-only" data-en="Message">Mensaje</label>', HTML)
        self.assertIn('<span id="animatedGreeting" aria-hidden="true">', HTML)
        css = (ROOT / "web/style.css").read_text(encoding="utf-8")
        self.assertIn("@media(prefers-reduced-motion:reduce){.typing-cursor{animation:none;display:none}", css)
        self.assertIn(".session .composer:has(textarea:focus-visible){outline:2px solid", css)
        self.assertIn('<script src="/orientation.js"></script>', HTML)


class CodeTests(unittest.TestCase):
    def test_environment_check_reports_a_complete_repository(self):
        from scripts.check_environment import inspect
        report = inspect(ROOT, port=0)
        self.assertEqual(report["missing"], [])
        self.assertRegex(report["python"], r"^\d+\.\d+")
        self.assertEqual(report["api_credentials"], "NOT_READ")
        self.assertNotIn("sk-", json.dumps(report))

    def test_matching_evidence_and_identical_runs_pass(self):
        # Sources and records of this checkout are the ones the committed evidence describes. Whether that run
        # passed is a separate claim (C194); checking it here would make the first run after a change circular.
        self.assertEqual([e for e in check_evidence.check_committed(ROOT) if "not a passing run" not in e], [])
        latest = json.loads((ROOT / "evidence/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(check_evidence.compare_statuses(latest, latest), [])

    def test_gate_passes_when_every_member_succeeded(self):
        for platform in ci_gate.MEMBERS:
            run = subprocess.run([sys.executable, str(ROOT / "scripts/ci_gate.py"), platform, "ubuntu-latest=success", "windows-latest=success"],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout)
            self.assertIn(f"PASS: verify ({platform})", run.stdout)

    def test_tour_on_an_ascii_stream_replaces_instead_of_raising(self):
        env = dict(os.environ, PYTHONIOENCODING="ascii", PYTHONUTF8="0")
        run = subprocess.run([sys.executable, str(ROOT / "run.py"), "tour", "--lang", "es"], cwd=ROOT, env=env, capture_output=True, timeout=60)
        self.assertEqual(run.returncode, 0, run.stderr.decode("ascii", "replace"))
        self.assertNotIn(b"Traceback", run.stderr)
        text = run.stdout.decode("ascii")
        self.assertIn("devoluci?n", text)
        self.assertEqual(text.count("\n   -> "), 6)

    def test_record_fingerprint_ignores_the_run_environment(self):
        root = copy_repo(self)
        before = check_evidence.record_fingerprint(root)
        path = root / "specs/001-support-demo/acceptance.csv"
        with path.open(encoding="utf-8", newline="") as h:
            reader = csv.DictReader(h); fields = reader.fieldnames; rows = list(reader)
        for row in rows:
            row["environment"] = "Windows / Python 3.13.9"
        with path.open("w", encoding="utf-8", newline="") as h:
            writer = csv.DictWriter(h, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
        self.assertEqual(check_evidence.record_fingerprint(root), before)
        self.assertEqual(before, check_evidence.record_fingerprint(ROOT))

    def test_revision_info_without_git_is_explicit(self):
        root = copy_repo(self)
        info = revision.revision_info(root)
        self.assertEqual(info, {"revision": None, "revision_dirty": None, "pins": {}, "pins_complete": False})
        payload = revision.status_payload(root)
        self.assertIsNone(payload["revision"])
        self.assertFalse(payload["build_states"]["git"])


class MatrixTests(unittest.TestCase):
    def test_matrix_passes_on_the_records(self):
        self.assertEqual(requirement_matrix.validate(ROOT), [])
        document = requirement_matrix.render(ROOT)
        cases, kinds, requirements = requirement_matrix.load(ROOT)
        for req in requirements:
            self.assertIn("## " + req["id"] + " —", document)
        self.assertIn("| C018 | behavior | negative |", document)
        self.assertEqual(len(kinds["cases"]), len(cases))
        committed = (ROOT / "docs/requirements-matrix.md").read_text(encoding="utf-8")
        self.assertEqual(committed.strip(), document.strip(), "docs/requirements-matrix.md is stale: run python scripts/requirement_matrix.py --write")

    def test_matrix_rejects_gaps(self):
        root = copy_repo(self)
        path = root / "specs/001-support-demo/case-kinds.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        def with_change(change):
            kinds = json.loads(json.dumps(original)); change(kinds)
            path.write_text(json.dumps(kinds), encoding="utf-8")
            return requirement_matrix.validate(root)
        def no_negative(k):
            for case, entry in k["cases"].items():
                if entry["polarity"] != "positive" and any(r["requirement_id"] == "R03" for r in requirement_matrix.load(root)[0] if r["case_id"] == case):
                    entry["polarity"] = "positive"
        self.assertIn("Requirement R03 (code) has no behavior-level negative or limit case", with_change(no_negative))
        self.assertIn("Classified case does not exist: C999", with_change(lambda k: k["cases"].__setitem__("C999", {"kind": "behavior", "polarity": "positive"})))
        self.assertIn("Requirement R35 (code) has no behavior-level positive case", with_change(lambda k: k["cases"]["C186"].__setitem__("kind", "structure")))
        self.assertIn("Requirement R03 cites code that does not exist: src/lab/controller.py::def vanish",
                      with_change(lambda k: k["requirements"]["R03"].__setitem__("code", ["src/lab/controller.py::def vanish"])))
        self.assertIn("Unclassified case: C018", with_change(lambda k: k["cases"].pop("C018")))

    def test_injected_defect_fails_closed(self):
        if os.environ.get("LAB_SKIP_NESTED"):
            self.skipTest("nested fail-closed run")
        root = copy_repo(self)
        controller = root / "src/lab/controller.py"
        source = controller.read_text(encoding="utf-8")
        defect = source.replace('                if proposal.status != "APPROVED":\n                    raise RuleError("APPROVAL_REQUIRED")\n', "")
        self.assertNotEqual(defect, source)
        controller.write_text(defect, encoding="utf-8")
        committed = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
        run = subprocess.run([sys.executable, str(root / "scripts/verify.py")], cwd=root, capture_output=True, text=True, timeout=600,
                             env=dict(os.environ, LAB_SKIP_NESTED="1"))
        self.assertEqual(run.returncode, 1, run.stdout[-2000:])
        latest = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
        self.assertFalse(latest["passed"])
        self.assertEqual(latest["acceptance_cases"]["C018"]["status"], "FAIL")
        with (root / "specs/001-support-demo/acceptance.csv").open(encoding="utf-8", newline="") as h:
            recorded = {r["case_id"]: r["status"] for r in csv.DictReader(h)}
        self.assertEqual(recorded["C018"], "FAIL")
        self.assertIn("Committed evidence is not a passing run", check_evidence.check_committed(root))
        drift = check_evidence.compare_statuses(committed, latest)
        self.assertIn("Status drift: test_lab.WorkflowTests.test_execute_requires_approval PASS -> FAIL", drift)
        self.assertIn("Case drift: C018 status 'PASS' -> 'FAIL'", drift)


class DocsTests(unittest.TestCase):
    DOCS = ("README.md", "docs/INDEX.md", "docs/START_HERE_ES.md")

    def test_routes_stay_true_on_main_and_branch(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for stale in ("Not published yet", "While `NOT_DEPLOYED`", "NOT_DEPLOYED"):
            self.assertNotIn(stale, readme)
        section = readme[readme.index("## Published or candidate"):readme.index("## Run locally")]
        for text in ("project-status.json", "git rev-parse HEAD", "git fetch origin", "git checkout --detach", "Evidence"):
            self.assertIn(text, section)
        self.assertIsNone(re.search(r"\b[0-9a-f]{40}\b", section))
        trouble = readme[readme.index("## Troubleshooting"):readme.index("## Limits")]
        for item in ("Python 3.11", "port", "verify.py", "cp1252"):
            self.assertIn(item, trouble)
        index = (ROOT / "docs/INDEX.md").read_text(encoding="utf-8")
        self.assertNotIn("NOT_DEPLOYED", index); self.assertIn("project-status.json", index[:index.index("## Technical review")])
        guide = (ROOT / "docs/START_HERE_ES.md").read_text(encoding="utf-8")
        self.assertNotIn("NOT_DEPLOYED", guide); self.assertIn("git rev-parse HEAD", guide)
        visitor = (ROOT / "docs/visitor-test.md").read_text(encoding="utf-8")
        for heading in ("## 30 seconds (C170)", "## 3 minutes (C177 route)", "## Answer record"):
            self.assertIn(heading, visitor)
        self.assertIn("Sin nombre ni datos personales", visitor)

    def test_scope_line_is_not_stale(self):
        line = re.search(r'<p class="scope-line" data-en="([^"]+)">([^<]+)</p>', HTML)
        english, spanish = line.group(1), line.group(2)
        status = json.loads((ROOT / "docs/project-status.json").read_text(encoding="utf-8"))
        if status["acceptance"].get("status") == "OWNER_ACCEPTED":
            self.assertNotIn("Pending: owner acceptance", english); self.assertNotIn("Pendiente: aceptación del dueño", spanish)
        self.assertIn("Evidence", english); self.assertIn("Evidencia", spanish)
        self.assertIn("new visitor", english); self.assertIn("visitante nuevo", spanish)

    def test_relative_links_resolve_and_startup_commands_exist(self):
        def slug(text):
            return re.sub(r"[^\w\- ]", "", text.lower().replace("·", "")).strip().replace(" ", "-")
        for name in self.DOCS:
            path = ROOT / name; text = path.read_text(encoding="utf-8")
            headings = {slug(h) for h in re.findall(r"^#+ (.+)$", text, flags=re.M)}
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                file_part, _, anchor = target.partition("#")
                resolved = (path.parent / file_part).resolve() if file_part else path
                self.assertTrue(resolved.exists(), f"{name}: {target}")
                if anchor and resolved.suffix == ".md":
                    target_text = resolved.read_text(encoding="utf-8")
                    target_headings = {slug(h) for h in re.findall(r"^#+ (.+)$", target_text, flags=re.M)}
                    self.assertIn(anchor, target_headings, f"{name}: {target}")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for command in ("python scripts/check_environment.py", "python run.py tour", "python run.py serve"):
            self.assertIn(command, readme)


if __name__ == "__main__":
    unittest.main()
