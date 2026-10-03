import json
import os
import sys
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.publication_check import inspect, check
from scripts.validate_data import validate
from src.lab.controller import ROOT

class GuardTests(unittest.TestCase):
    def test_fixture_contract(self):
        self.assertEqual(validate(), [])

    def test_data_rejects_real_currency(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "data", root / "data")
            policy = json.loads((root / "data/policy.json").read_text())
            policy["currency"] = "USD"
            (root / "data/policy.json").write_text(json.dumps(policy))
            self.assertTrue(validate(root))

    def test_private_key_pattern(self):
        data = ("-----BEGIN " + "PRIVATE KEY-----").encode()
        self.assertTrue(inspect("sample.txt", data))

    def test_env_file_rejected(self):
        self.assertTrue(inspect(".env", b"placeholder"))
        self.assertFalse(inspect(".env.example", b"placeholder"))

    def test_token_pattern(self):
        self.assertTrue(inspect("sample.txt", ("ghp_" + "a" * 36).encode()))

    def test_staged_bytes_not_clean_worktree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            p = root / "sample.txt"
            p.write_text("ghp_" + "a" * 36)
            subprocess.run(["git", "-C", str(root), "add", "sample.txt"], check=True, capture_output=True)
            p.write_text("now harmless")
            self.assertTrue(check(root, staged=True))
            self.assertFalse(check(root, staged=False))

    def test_actual_precommit_hook_blocks_then_accepts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            shutil.copytree(ROOT / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / ".githooks", root / ".githooks")
            subprocess.run(["git", "-C", str(root), "config", "--local", "core.hooksPath", ".githooks"], check=True)
            sample = root / "sample.txt"
            sample.write_text("ghp_" + "a" * 36)
            subprocess.run(["git", "-C", str(root), "add", "sample.txt"], check=True)
            env = dict(os.environ, PYTHON=sys.executable)
            command = ["git", "-C", str(root), "-c", "user.name=Fixture", "-c",
                       "user.email=fixture@example.invalid", "commit", "-m", "Synthetic hook test"]
            blocked = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("GitHub token", blocked.stdout + blocked.stderr)
            sample.write_text("synthetic harmless sample")
            subprocess.run(["git", "-C", str(root), "add", "sample.txt"], check=True)
            accepted = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
