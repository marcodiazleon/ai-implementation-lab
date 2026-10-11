"""Build the static Session preview; live provider connections use the local backend."""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.sdd_check import requirement_rows
from scripts.revision import status_payload
from src.lab.model_catalog import catalog

DATA = ["data/orders.json", "data/policy.json", "data/scenarios.json", "agents/roles.json",
        "evidence/latest.json", "specs/001-support-demo/acceptance.csv"]
REPLACEMENTS = [
    ('<script src="i18n.js"', '<script src="public-demo.js"></script>\n  <script src="i18n.js"'),
    ('Guardados en este repositorio en esta computadora.', 'Se guardan solo en esta pestaña y se borran al recargar.'),
    ('data-en="Saved in this repository on this computer.', 'data-en="Kept only in this tab and cleared on reload.'),
    # R44a: whole elements, so the English text changes with the Spanish one.
    ('<small id="footerScope" data-en="In-memory session · Optional API · Local use">Sesión en memoria · API opcional · Uso local</small>',
     '<small id="footerScope" data-en="Public preview · Agents in this tab · API in the local version">Vista pública · Agentes en esta pestaña · API en versión local</small>'),
    ('<p class="sidebar-note" data-en="AI IMPLEMENTATION LAB · LOCAL WORKSPACE">AI IMPLEMENTATION LAB · ESPACIO LOCAL</p>',
     '<p class="sidebar-note" data-en="AI IMPLEMENTATION LAB · PUBLIC PREVIEW">AI IMPLEMENTATION LAB · VISTA PÚBLICA</p>'),
    ('<p class="muted">La conversación API es independiente del ejercicio de devoluciones. El servidor está diseñado para ejecutarse en tu equipo por loopback.</p>',
     '<p class="muted" data-en="Session is the conversation workspace. The public version previews its interface; '
     'the local backend connects to providers with your own API key.">Sesión es el espacio de conversación. '
     'La versión pública muestra su interfaz; el backend local conecta con los proveedores mediante tu propia clave API.</p>'),
]

def build(out=ROOT / "_site"):
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(ROOT / "web", out)
    (out / "data").mkdir()
    for name in DATA:
        shutil.copy(ROOT / name, out / "data" / Path(name).name)
    spec = (ROOT / "specs/001-support-demo/spec.md").read_text(encoding="utf-8")
    (out / "data/requirements.json").write_text(
        json.dumps(requirement_rows(spec), ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    # R36b, R42, R43a: the project records, the fingerprints and the Git revision this site was built from.
    status = status_payload()
    (out / "data/status.json").write_text(json.dumps(status, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8", newline="\n")
    (out / "data/model-catalog.json").write_text(
        json.dumps(catalog(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    html = (out / "index.html").read_text(encoding="utf-8")
    html = re.sub(r'(src|href)="/(?=[a-z])', r'\1="', html).replace('href="/"', 'href="./"')
    for old, new in REPLACEMENTS:
        if old not in html:
            raise SystemExit("build_pages: expected markup not found: " + old[:60])
        html = html.replace(old, new)
    # R43a: repository links open the revision this site is built from (live main only without Git).
    if status["revision"]:
        html = re.sub(r'href="(https://github\.com/marcodiazleon/ai-implementation-lab/(?:blob|tree))/main/([^"]+)" data-repo-path="\2"',
                      lambda m: f'href="{m.group(1)}/{status["revision"]}/{m.group(2)}" data-repo-path="{m.group(2)}"', html)
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    return out

if __name__ == "__main__":
    print("Built", build())
