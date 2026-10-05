"""Build the public static demo for GitHub Pages into _site/.

The refund workflow runs in the visitor's browser (web/public-demo.js). Model, API-key and
MCP connections are hidden: the public page asks for no credentials and stores no visitor data.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.sdd_check import requirement_rows
DATA = ["data/orders.json", "data/policy.json", "data/scenarios.json", "agents/roles.json",
        "evidence/latest.json", "specs/001-support-demo/acceptance.csv"]
NOTE = ('<p class="public-note" data-en="Public demo: everything runs in your browser with fictional data. '
        'No keys, accounts or personal data. Reloading the page resets it.">Demo pública: todo corre en tu '
        'navegador con datos ficticios. Sin claves, cuentas ni datos personales. Recargar la página la reinicia.</p>')
REPLACEMENTS = [
    ('<script src="i18n.js"', '<script src="public-demo.js"></script>\n  <script src="i18n.js"'),
    ('<div id="view-demo" data-panel="demo">', '<div id="view-demo" data-panel="demo">' + NOTE),
    ('<details id="examplePanel" class="example-panel">', '<details id="examplePanel" class="example-panel" open>'),
    ('Guardados en este repositorio en esta computadora.', 'Se guardan solo en esta pestaña y se borran al recargar.'),
    ('data-en="Saved in this repository on this computer.', 'data-en="Kept only in this tab and cleared on reload.'),
    ('Sesión en memoria · Reiniciar el servidor restablece los escenarios · Uso local',
     'Demo pública · Datos ficticios · Recargar la página restablece los escenarios'),
    ('<p class="sidebar-note" data-en="AI IMPLEMENTATION LAB · LOCAL WORKSPACE">AI IMPLEMENTATION LAB · ESPACIO LOCAL</p>',
     '<p class="sidebar-note" data-en="AI IMPLEMENTATION LAB · PUBLIC DEMO">AI IMPLEMENTATION LAB · DEMO PÚBLICA</p>'),
    ('<p class="muted">La conversación API es independiente del ejercicio de devoluciones. El servidor está diseñado para ejecutarse en tu equipo por loopback.</p>',
     '<p class="muted" data-en="This public demo runs the rules in your browser with fictional data. The local version also includes optional model and MCP connections.">'
     'Esta demo pública ejecuta las reglas en tu navegador con datos ficticios. La versión local incluye además conexión opcional a modelos y MCP.</p>'),
]

def build(out=ROOT / "_site"):
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(ROOT / "web", out)
    (out / "data").mkdir()
    for name in DATA:
        shutil.copy(ROOT / name, out / "data" / Path(name).name)
    # Requirements are published as generated JSON, not the spec itself (decision D21).
    spec = (ROOT / "specs/001-support-demo/spec.md").read_text(encoding="utf-8")
    (out / "data" / "requirements.json").write_text(json.dumps(requirement_rows(spec), ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    html = (out / "index.html").read_text(encoding="utf-8")
    # Project Pages live under /<repo>/, so root-absolute asset paths must become relative.
    html = re.sub(r'(src|href)="/(?=[a-z])', r'\1="', html).replace('href="/"', 'href="./"')
    for old, new in REPLACEMENTS:
        if old not in html:
            raise SystemExit("build_pages: expected markup not found: " + old[:60])
        html = html.replace(old, new)
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    return out

if __name__ == "__main__":
    print("Built", build())
