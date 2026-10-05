"""Build the public static demo for GitHub Pages into _site/.

The refund workflow runs in the visitor's browser (web/public-demo.js). Model, API-key and
MCP connections are hidden: the public page asks for no credentials and stores no visitor data.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ["data/orders.json", "data/policy.json", "data/scenarios.json", "agents/roles.json"]
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
    # ponytail: Spanish only; the original paragraph has no data-en and the public build adds no new i18n key.
    ('La conversación API es independiente del ejercicio de devoluciones. El servidor está diseñado para ejecutarse en tu equipo por loopback.',
     'Esta demo pública ejecuta las reglas en tu navegador con datos ficticios. La versión local incluye además conexión opcional a modelos y MCP.'),
]

def build(out=ROOT / "_site"):
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(ROOT / "web", out)
    (out / "data").mkdir()
    for name in DATA:
        shutil.copy(ROOT / name, out / "data" / Path(name).name)
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
