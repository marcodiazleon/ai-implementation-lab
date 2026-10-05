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
        for p in (ROOT / "docs/assets").glob("*.jpg"):
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

    def test_version_header_mismatch_is_rejected(self):
        plan = self.root / "specs/001-support-demo/plan.md"
        text = plan.read_text(encoding="utf-8")
        plan.write_text(text.replace("Version ", "Version 9", 1), encoding="utf-8")
        self.assertTrue(any("Version mismatch" in e for e in validate(self.root)))
