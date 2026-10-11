"""U18 checks: required check names (R40), CLI encoding (R41), bounded evidence manifests (R42),
revision-pinned links (R43), languages and the Spanish guide (R44) and the tour's worked result (R45)."""
import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from scripts.build_pages import ROOT, build
from scripts import check_evidence, ci_gate
from scripts.revision import historical_cases, revision_info
from src.lab import cli

WORKFLOW = (ROOT / ".github/workflows/verify.yml").read_text(encoding="utf-8")
HTML = (ROOT / "web/index.html").read_text(encoding="utf-8")


def job(name):
    """Text of one top-level job in verify.yml."""
    match = re.search(r"^  " + re.escape(name) + r":\n(.*?)(?=^  [\w-]+:\n|\Z)", WORKFLOW, flags=re.S | re.M)
    return match.group(1)


class CiGateTests(unittest.TestCase):
    def test_gate_fails_on_failure_skip_cancel_or_missing(self):
        ok = {"ubuntu-latest": "success", "windows-latest": "success"}
        for check in ("ubuntu-latest", "windows-latest"):
            passed, lines = ci_gate.gate(check, ok)
            self.assertTrue(passed)
            self.assertEqual(lines[:2], ["ubuntu-latest (Python 3.11, 3.13): success", "windows-latest (Python 3.13): success"])
            for platform in ok:
                for result in ("failure", "skipped", "cancelled", ""):
                    passed, lines = ci_gate.gate(check, dict(ok, **{platform: result}))
                    self.assertFalse(passed, (check, platform, result))
                    self.assertTrue(any(line.startswith(platform) and line.endswith(": " + result) for line in lines))
                    self.assertTrue(lines[-1].startswith("FAIL: verify (" + check + ")"))
                missing = {k: v for k, v in ok.items() if k != platform}
                passed, lines = ci_gate.gate(check, missing)
                self.assertFalse(passed)
                self.assertIn(platform + " (Python " + ", ".join(ci_gate.MEMBERS[platform]) + "): missing", lines)
        self.assertFalse(ci_gate.gate("macos-latest", ok)[0])
        self.assertFalse(ci_gate.gate("ubuntu-latest", dict(ok, **{"macos-latest": "success"}))[0])
        # The command line exits 1 for a skipped member and 0 only when both platforms succeeded.
        run = lambda *args: subprocess.run([sys.executable, str(ROOT / "scripts/ci_gate.py"), *args], capture_output=True, text=True)
        self.assertEqual(run("ubuntu-latest", "ubuntu-latest=success", "windows-latest=skipped").returncode, 1)
        self.assertEqual(run("windows-latest", "ubuntu-latest=cancelled", "windows-latest=success").returncode, 1)
        self.assertEqual(run("windows-latest", "ubuntu-latest=success", "windows-latest=success").returncode, 0)

    def test_workflow_emits_required_names_from_the_full_matrix(self):
        names = re.findall(r"^    name: (.+)$", WORKFLOW, flags=re.M)
        self.assertEqual(names.count("verify (ubuntu-latest)"), 1)
        self.assertEqual(names.count("verify (windows-latest)"), 1)
        for platform in ci_gate.MEMBERS:
            gate = job("gate-" + platform.split("-")[0])
            self.assertIn("name: verify (" + platform + ")", gate)
            self.assertIn("needs: [verify-ubuntu, verify-windows]", gate)
            self.assertIn("if: always() && github.repository == 'marcodiazleon/ai-implementation-lab'", gate)
            self.assertIn(f'scripts/ci_gate.py {platform} "ubuntu-latest=${{{{ needs.verify-ubuntu.result }}}}" '
                          f'"windows-latest=${{{{ needs.verify-windows.result }}}}"', gate)
            member = job("verify-" + platform.split("-")[0])
            self.assertIn("name: verify (${{ matrix.os }}, Python ${{ matrix.python }})", member)
            self.assertEqual(re.findall(r'\{ os: ([\w-]+), python: "([\d.]+)" \}', member),
                             [(platform, version) for version in ci_gate.MEMBERS[platform]])
        steps = lambda name: job(name).split("    steps:\n", 1)[1]
        self.assertEqual(steps("verify-ubuntu"), steps("verify-windows"))
        self.assertIn("fetch-depth: 0", steps("verify-ubuntu"))


class TourEncodingTests(unittest.TestCase):
    def test_tour_runs_in_cp1252_and_utf8_in_both_languages(self):
        for language in ("es", "en"):
            outputs = {}
            for encoding in ("cp1252", "utf-8"):
                env = dict(os.environ, PYTHONIOENCODING=encoding, PYTHONUTF8="0")
                result = subprocess.run([sys.executable, str(ROOT / "run.py"), "tour", "--lang", language],
                                        cwd=ROOT, env=env, capture_output=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
                self.assertNotIn(b"Traceback", result.stderr)
                outputs[encoding] = result.stdout.decode(encoding)
            self.assertEqual(outputs["cp1252"], outputs["utf-8"])
            text = outputs["utf-8"].replace("\r\n", "\n")
            self.assertEqual(text.count("\n   -> "), 6)
            receipts = cli.TOUR_TEXT[language]["receipts"]
            self.assertEqual(re.findall(re.escape(receipts) + r": (\d)", text), ["0", "0", "0", "0", "1", "1"])
            for control in cli.TOUR_TEXT[language]["controls"]:
                self.assertIn("\n   " + control + "\n", text)
            self.assertNotIn("→", text)


class ManifestTests(unittest.TestCase):
    def copy(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "repo"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "_site", ".local", "*.jpg"))
        evidence = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
        evidence.update(source_id=check_evidence.source_fingerprint(root), source_sha256=check_evidence.source_hashes(root),
                        record_id=check_evidence.record_fingerprint(root), record_sha256=check_evidence.record_hashes(root), passed=True)
        (root / "evidence/latest.json").write_text(json.dumps(evidence), encoding="utf-8")
        self.assertEqual(check_evidence.check_committed(root), [])
        return root

    def edit_case(self, root, case, **changes):
        path = root / "specs/001-support-demo/acceptance.csv"
        with path.open(encoding="utf-8", newline="") as h:
            reader = csv.DictReader(h); fields = reader.fieldnames; rows = list(reader)
        for row in rows:
            if row["case_id"] == case:
                row.update(changes)
        with path.open("w", encoding="utf-8", newline="") as h:
            writer = csv.DictWriter(h, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

    def test_source_manifest_covers_roles_and_workflows(self):
        for rel in ("agents/roles.json", ".github/workflows/pages.yml"):
            root = self.copy()
            target = root / rel
            target.write_text(target.read_text(encoding="utf-8").replace("e", "E", 1), encoding="utf-8")
            errors = check_evidence.check_committed(root)
            self.assertEqual(errors, ["Committed evidence describes other sources: " + rel])

    def test_record_changes_are_rejected_and_environment_is_not(self):
        acceptance = "specs/001-support-demo/acceptance.csv"
        cases = (lambda root: self.edit_case(root, "C018", expected="Anything"), acceptance), \
                (lambda root: self.edit_case(root, "C018", test_id="test_lab.WorkflowTests.test_scenarios"), acceptance), \
                (lambda root: self.edit_case(root, "C170", status="PASS"), acceptance)
        for change, rel in cases:
            root = self.copy(); change(root)
            self.assertEqual(check_evidence.check_committed(root), ["Committed evidence describes other records: " + rel])
        root = self.copy()
        status = root / "docs/project-status.json"
        status.write_text(status.read_text(encoding="utf-8").replace('"NOT_INTEGRATED"', '"INTEGRATED"'), encoding="utf-8")
        self.assertEqual(check_evidence.check_committed(root), ["Committed evidence describes other records: docs/project-status.json"])
        root = self.copy()
        registry = root / "docs/id-registry.json"
        registry.write_text(registry.read_text(encoding="utf-8").replace('"R28"', '"R27"', 1), encoding="utf-8")
        self.assertEqual(check_evidence.check_committed(root), ["Committed evidence describes other records: docs/id-registry.json"])
        root = self.copy()
        self.edit_case(root, "C018", environment="Windows / Python 3.13.9")
        self.assertEqual(check_evidence.check_committed(root), [])

    def test_case_drift_with_equal_counts_is_reported(self):
        cases = check_evidence.case_map(ROOT / "specs/001-support-demo/acceptance.csv")
        old = {"test_results": [], "acceptance_states": {"PASS": 1, "NO_PROBADO": 1}, "acceptance_cases": cases}
        new_cases = json.loads(json.dumps(cases))
        new_cases["C018"]["status"], new_cases["C170"]["status"] = "NO_PROBADO", "PASS"
        new_cases["C001"]["test_id"] = "test_lab.WorkflowTests.test_snapshot_is_a_copy"
        new = dict(old, acceptance_cases=new_cases)
        self.assertEqual(check_evidence.compare_statuses(old, new), [
            "Case drift: C001 test_id " + repr(cases["C001"]["test_id"]) + " -> 'test_lab.WorkflowTests.test_snapshot_is_a_copy'",
            "Case drift: C018 status 'PASS' -> 'NO_PROBADO'",
            "Case drift: C170 status 'NO_PROBADO' -> 'PASS'"])
        self.assertEqual(check_evidence.compare_statuses(old, old), [])
        changed = dict(old, record_sha256={"docs/id-registry.json": "b"})
        self.assertEqual(check_evidence.compare_statuses(dict(old, record_sha256={"docs/id-registry.json": "a"}), changed),
                         ["Record drift: docs/id-registry.json"])

    def test_no_cycle_and_no_fingerprint_copy_in_status(self):
        sources, records = check_evidence.source_hashes(), check_evidence.record_hashes()
        self.assertFalse(set(sources) & set(records))
        self.assertFalse([p for p in list(sources) + list(records) if p.startswith("evidence/")])
        record_id = json.loads((ROOT / "evidence/latest.json").read_text(encoding="utf-8")).get("record_id", "")
        for rel in records:
            self.assertNotIn(record_id[:12] or "no-record-id", (ROOT / rel).read_text(encoding="utf-8"), rel)
        status = (ROOT / "docs/project-status.json").read_text(encoding="utf-8")
        self.assertNotIn("evidence_scope", status)
        self.assertIsNone(re.search(r"\b[0-9a-f]{12,}\b", status.replace("81dfced59cc85231e25732137859923b39a2beed", "")))
        doc = (ROOT / "scripts/check_evidence.py").read_text(encoding="utf-8")
        self.assertNotIn("everything that can change a test result", doc)


class LinkTests(unittest.TestCase):
    def test_build_records_revision_and_pins_and_view_has_no_main_file_links(self):
        info = revision_info()
        git = lambda *args: subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
        self.assertEqual(info["revision"], git("rev-parse", "HEAD").stdout.strip())
        self.assertTrue(info["pins_complete"])
        cases = historical_cases()
        self.assertEqual(set(info["pins"]), set(cases))
        for case, sha in info["pins"].items():
            self.assertEqual(git("cat-file", "-e", sha + ":" + cases[case][0]).returncode, 0, case)
            self.assertEqual(git("merge-base", "--is-ancestor", sha, "HEAD").returncode, 0, case)
        with tempfile.TemporaryDirectory() as tmp:
            out = build(Path(tmp) / "site")
            status = json.loads((out / "data/status.json").read_text(encoding="utf-8"))
            self.assertEqual((status["revision"], status["pins"]), (info["revision"], info["pins"]))
            self.assertEqual(status["record_fingerprint"], check_evidence.record_fingerprint())
            built = (out / "index.html").read_text(encoding="utf-8")
        self.assertNotRegex(built, r"ai-implementation-lab/(blob|tree)/main/")
        for path in re.findall(r'data-repo-path="([^"]+)"', built):
            self.assertIn(f'/{info["revision"]}/{path}" data-repo-path="{path}"', built)
            self.assertTrue((ROOT / path).exists(), path)
        self.assertEqual(len(re.findall(r'data-repo-path="', HTML)), len(re.findall(r'ai-implementation-lab/(?:blob|tree)/main/', HTML)))
        view = (ROOT / "web/evidence.js").read_text(encoding="utf-8")
        self.assertNotIn("/blob/main", view)
        self.assertEqual(view.count('"/tree/main"'), 1)  # the labeled live-navigation link
        self.assertIn("status?.pins?.[caseId]", view)

    def test_readme_warns_next_to_first_action_while_not_deployed(self):
        status = json.loads((ROOT / "docs/project-status.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        first = readme.index("**First action:")
        if status["deployment"]["this_branch"] == "NOT_DEPLOYED":
            warning = readme.index("**Not published yet.**")
            self.assertLess(first, warning)
            self.assertLess(warning - first, 400)
            self.assertIn("`NOT_DEPLOYED`", readme[warning:warning + 400])
            spanish = readme.index("Primera acción:")
            self.assertIn("NOT_DEPLOYED", readme[spanish:spanish + 400])
        self.assertNotIn("GitHub Pages publishes main, so a branch shows there only after it is merged", readme)


class LanguageTests(unittest.TestCase):
    def test_footer_and_notices_have_english_in_source_and_build(self):
        footer = HTML[HTML.index("<footer>"):HTML.index("</footer>")]
        self.assertIn('<small id="footerScope" data-en="In-memory session · Optional API · Local use">', footer)
        self.assertIn('data-en="AI STRATEGY AND IMPLEMENTATION"', footer)
        with tempfile.TemporaryDirectory() as tmp:
            built = (build(Path(tmp) / "site") / "index.html").read_text(encoding="utf-8")
        self.assertIn('<small id="footerScope" data-en="Public preview · Agents in this tab · API in the local version">'
                      'Vista pública · Agentes en esta pestaña · API en versión local</small>', built)
        self.assertNotIn("In-memory session · Optional API · Local use", built)
        self.assertIn('data-en="AI IMPLEMENTATION LAB · PUBLIC PREVIEW">AI IMPLEMENTATION LAB · VISTA PÚBLICA<', built)
        cloud = (ROOT / "web/cloud.js").read_text(encoding="utf-8")
        self.assertIn("t('Vista pública','Public preview')", cloud)
        self.assertRegex(cloud, r"note\('connectionStatus','Para conectar tu API[^']*','Run the local version")
        # Notices re-render from their stored pair on every language change.
        self.assertIn("addEventListener('languagechange'", cloud)
        self.assertIn("for(const[id,pair]of Object.entries(notices))el(id).textContent=t(...pair)", cloud)

    def test_spanish_guide_describes_the_current_entry(self):
        guide = (ROOT / "docs/START_HERE_ES.md").read_text(encoding="utf-8")
        for current in ("**Sesión**", "Cómo está construido", "python run.py tour", "Demo pública", "Versión local", "Pendiente",
                        "NOT_DEPLOYED", "project-status.json"):
            self.assertIn(current, guide)
        self.assertNotIn("siete casos", guide)
        self.assertNotIn("Revisión actual", guide)
        self.assertIn("es histórica", guide[guide.index("SDD_REVIEW.md") - 200:guide.index("SDD_REVIEW.md") + 60])
        old_steps = guide.index("seleccionar el pedido, analizar, aprobar")
        self.assertIn("**Histórico.**", guide[old_steps - 120:old_steps])
        self.assertNotIn("En la web, selecciona el pedido elegible", guide)


class TourCloseTests(unittest.TestCase):
    def test_worked_result_equals_cli_output(self):
        result = cli.tour()
        body = HTML[HTML.index('<tbody id="tourResult">'):HTML.index("</tbody>", HTML.index('<tbody id="tourResult">'))]
        rows = re.findall(r'<tr><td>(\d)</td><td data-en="([^"]+)">([^<]+)</td><td>([^<]+)</td><td>(\d)</td></tr>', body)
        self.assertEqual(len(rows), 6)
        for row, step, (number, english, spanish, shown, receipts) in zip(result["steps"], range(6), rows):
            expected = row["result"] + (" · " + row["receipt_id"] if row["receipt_id"] else "")
            self.assertEqual((int(number), shown, int(receipts)), (row["step"], expected, row["receipts"]))
            self.assertEqual(html.unescape(spanish), cli.TOUR_TEXT["es"]["steps"][step])
            self.assertEqual(html.unescape(english), cli.TOUR_TEXT["en"]["steps"][step])
        tour = HTML[HTML.index('<section class="tour"'):HTML.index('<h2 class="method-heading"')]
        self.assertIn("not a model reply", tour)
        self.assertIn("installing them is not part of the three minutes", tour)
        self.assertIn("instalarlos no forma parte de los tres minutos", tour)
        self.assertEqual(tour.count('<li><span class="tour-time"'), 4)


if __name__ == "__main__":
    unittest.main()
