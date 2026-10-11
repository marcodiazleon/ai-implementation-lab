"""R40 / D37: the rule behind the check names that branch protection on main requires.

verify (ubuntu-latest) and verify (windows-latest) are gate jobs. Each one needs every platform job of the
matrix and passes only when all of them succeeded; failure, skipped, cancelled or a missing result fails it.

Usage: python scripts/ci_gate.py CHECK_PLATFORM ubuntu-latest=RESULT windows-latest=RESULT
"""
import sys

# Matrix members per platform; tests/test_u18.py checks them against .github/workflows/verify.yml.
MEMBERS = {"ubuntu-latest": ("3.11", "3.13"), "windows-latest": ("3.13",)}

def gate(check, results):
    """Return (passed, lines). Only the GitHub job result "success" counts as success."""
    lines, passed = [], check in MEMBERS
    for platform, versions in MEMBERS.items():
        result = results.get(platform, "missing")
        passed = passed and result == "success"
        lines.append(f"{platform} (Python {', '.join(versions)}): {result}")
    unknown = sorted(set(results) - set(MEMBERS))
    if unknown:
        passed = False
        lines.append("Unknown platforms: " + ", ".join(unknown))
    lines.append(("PASS" if passed else "FAIL") + f": verify ({check}) requires every matrix member on every platform to succeed")
    return passed, lines

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 2
    results = dict(arg.split("=", 1) for arg in argv[1:] if "=" in arg)
    passed, lines = gate(argv[0], results)
    print("\n".join(lines))
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
