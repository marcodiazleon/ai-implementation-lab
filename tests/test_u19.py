"""U19 checks: fingerprint digests checked on their own (R46), candidate review route (R47) and
requirement selection kept across language changes (R48)."""
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.build_pages import ROOT
from scripts import check_evidence



class DigestTests(unittest.TestCase):
    def copy(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "repo"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "_site", ".local", "*.jpg"))
        evidence = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
        evidence.update(source_id=check_evidence.source_fingerprint(root), source_sha256=check_evidence.source_hashes(root),
                        record_id=check_evidence.record_fingerprint(root), record_sha256=check_evidence.record_hashes(root), passed=True)
        return root, evidence

    def write(self, root, evidence):
        (root / "evidence/latest.json").write_text(json.dumps(evidence), encoding="utf-8")
        return check_evidence.check_committed(root)

    def test_corrupt_invalid_or_missing_digest_is_rejected_with_correct_maps(self):
        root, evidence = self.copy()
        for field in ("source_id", "record_id"):
            label = "sources" if field == "source_id" else "records"
            errors = self.write(root, dict(evidence, **{field: "0" * 64}))
            self.assertEqual(len(errors), 1, errors)
            self.assertTrue(errors[0].startswith(f"Committed evidence {field} 000000000000 does not match the checked-out {label} "))
            for bad in ("0" * 63, "Z" * 64, evidence[field].upper(), 7, ""):
                self.assertEqual(self.write(root, dict(evidence, **{field: bad})), [f"Committed evidence {field} is not a SHA-256 digest"])
            self.assertEqual(self.write(root, {k: v for k, v in evidence.items() if k != field}), [f"Committed evidence has no {field}"])

    def test_intact_evidence_passes_and_file_list_accompanies_the_digest_error(self):
        root, evidence = self.copy()
        self.assertEqual(self.write(root, evidence), [])
        (root / "src/lab/models.py").write_text("# changed\n", encoding="utf-8")
        errors = check_evidence.check_committed(root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(errors[0].startswith("Committed evidence source_id "))
        self.assertEqual(errors[1], "Committed evidence describes other sources: src/lab/models.py")


class CandidateRouteTests(unittest.TestCase):
    def test_readme_separates_published_and_candidate_review(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        section = readme[readme.index("## Published or candidate"):readme.index("## Run locally")]
        self.assertIn("project-status.json", section)
        for command in ("git fetch origin", "git checkout --detach FETCH_HEAD", "git rev-parse HEAD", "python scripts/check_evidence.py"):
            self.assertIn(command, section)
        self.assertLess(section.index("git checkout --detach FETCH_HEAD"), section.index("python run.py serve"))
        self.assertIn("reported SHA", section)
        self.assertIsNone(re.search(r"\b[0-9a-f]{40}\b", section))
        spanish = readme[readme.index("Primera acción:"):]
        self.assertIn("Published or candidate", spanish[:700])

    def test_index_and_spanish_guide_carry_the_candidate_route(self):
        index = (ROOT / "docs/INDEX.md").read_text(encoding="utf-8")
        note = index[index.index("| Technical review |"):index.index("## Technical review")]
        for text in ("**Published or candidate.**", "project-status.json", "../README.md#published-or-candidate", "git rev-parse HEAD"):
            self.assertIn(text, note)
        guide = (ROOT / "docs/START_HERE_ES.md").read_text(encoding="utf-8")
        section = guide[guide.index("**Revisar un candidato.**"):guide.index("**Histórico.**")]
        for command in ("git fetch origin", "git checkout --detach FETCH_HEAD", "git rev-parse HEAD", "python scripts/check_evidence.py"):
            self.assertIn(command, section)
        self.assertIn("SHA informado", section)
        self.assertIsNone(re.search(r"\b[0-9a-f]{40}\b", section))


class SelectionTests(unittest.TestCase):
    def test_choosing_a_requirement_updates_the_address(self):
        view = (ROOT / "web/evidence.js").read_text(encoding="utf-8")
        handler = view[view.index('el("reqPicker").addEventListener("change"'):]
        handler = handler[:handler.index("});") + 3]
        self.assertLess(handler.index('history.replaceState(null, "", "#evidence/" + el("reqPicker").value)'), handler.index("renderCases()"))
        # render() reads the address first; with the address updated, a language change keeps the choice.
        self.assertIn('location.hash.match(/^#evidence\\/(R\\d+)$/)', view)
        self.assertIn('window.addEventListener("languagechange", render)', view)


if __name__ == "__main__":
    unittest.main()
