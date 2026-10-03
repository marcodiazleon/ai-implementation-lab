"""Read-only local prerequisites; never installs or reads credentials."""
import json
import socket
import sys
from pathlib import Path

def inspect(root=None, port=8765):
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    missing = [name for name in ("run.py", "src/lab/server.py", "src/lab/cloud.py",
                                "web/index.html", "web/cloud.js", "data/scenarios.json")
               if not (root / name).is_file()]
    with socket.socket() as probe:
        probe.settimeout(1)
        occupied = probe.connect_ex(("127.0.0.1", port)) == 0
    return {"python": sys.version.split()[0], "python_supported": sys.version_info >= (3, 10),
            "missing": missing, "port": port, "port_in_use": occupied,
            "api_credentials": "NOT_READ", "destination_runtime": "NOT_TESTED",
            "ready_to_start": sys.version_info >= (3, 10) and not missing and not occupied}

if __name__ == "__main__":
    result = inspect()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ready_to_start"] else 1)
