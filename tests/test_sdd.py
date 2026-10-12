import csv
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.sdd_check import ROOT, validate

class SddTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "sample"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.jpg", ".venv"))
        # Link checks need the image paths, not the binary contents.
        for p in ROOT.rglob("*.jpg"):
            if ".git" in p.relative_to(ROOT).parts:
                continue
            target = self.root / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.touch()

    def edit_cases(self, change):
        path = self.root / "specs/001-support-demo/acceptance.csv"
        with path.open(encoding="utf-8", newline="") as h:
            reader = csv.DictReader(h)
            fields = reader.fieldnames
            rows = list(reader)
        change(rows)
        with path.open("w", encoding="utf-8", newline="") as h:
            writer = csv.DictWriter(h, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_valid_project(self):
        self.assertEqual(validate(self.root), [])

    def test_unknown_test_reference_is_rejected(self):
        self.edit_cases(lambda rows: rows[0].update(test_id="test_missing.No.test_nothing"))
        self.assertTrue(any("Unknown test" in e for e in validate(self.root)))

    def test_empty_expected_result_is_rejected(self):
        self.edit_cases(lambda rows: rows[0].update(expected=""))
        self.assertTrue(any("Missing expected" in e for e in validate(self.root)))

    def test_duplicate_case_is_rejected(self):
        self.edit_cases(lambda rows: rows.append(dict(rows[0])))
        self.assertTrue(any("Duplicate" in e for e in validate(self.root)))

    def edit(self, name, old, new):
        path = self.root / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    # U17 / R36c negatives: each edit must produce its specific error and nothing passes silently.
    def test_version_header_mismatch_is_rejected(self):
        self.edit("specs/001-support-demo/plan.md", "Version 1.1.", "Version 1.0.")
        self.assertIn("Version mismatch: plan.md 1.0 != 1.1", validate(self.root))

    def test_outdated_guide_version_is_rejected_but_provenance_is_allowed(self):
        self.edit("docs/WORKBENCH.md", "introduced in S01 0.8", "S01 0.8")
        self.assertIn("Outdated S01 version in docs/WORKBENCH.md: 0.8", validate(self.root))
        self.edit("docs/WORKBENCH.md", "S01 0.8", "introduced in S01 0.8")
        self.assertEqual(validate(self.root), [])

    def test_id_reserved_by_another_pull_request_is_rejected(self):
        # R30 stays reserved for PR #4 (docs/id-registry.json); defining it here must fail.
        self.edit("specs/001-support-demo/spec.md", "| R34 |", "| R30 |")
        errors = validate(self.root)
        self.assertIn("ID reserved by another open pull request: R30", errors)
        self.assertIn("Unexpected core requirement set", errors)

    def test_duplicated_task_and_decision_ids_are_rejected(self):
        self.edit("specs/001-support-demo/tasks.md", "| T58 |", "| T57 |")
        self.edit("docs/decisions.md", "## D33 ", "## D32 ")
        errors = validate(self.root)
        self.assertIn("Duplicated ID in specs/001-support-demo/tasks.md: T57", errors)
        self.assertIn("Duplicated ID in docs/decisions.md: D32", errors)

    def test_no_aplica_requires_a_reason(self):
        def case(rows):
            return next(r for r in rows if r["case_id"] == "C177")
        self.edit_cases(lambda rows: case(rows).update(status="NO_APLICA", observed="Not executed for this revision"))
        self.assertIn("NO_APLICA without reason: C177", validate(self.root))
        self.edit_cases(lambda rows: case(rows).update(observed="Superseded by U13: no visible exercise to test"))
        self.assertEqual(validate(self.root), [])
