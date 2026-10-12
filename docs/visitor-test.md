# Visitor test script · Guion de prueba con visitante

Case C170 (R34) and the route review C177 (R37) need a person who does not know the project. This script is what the person running the session says and records. The implementing assistant cannot run it; until someone does, both cases stay NO_PROBADO.

El caso C170 (R34) y la revisión de rutas C177 (R37) necesitan a una persona que no conozca el proyecto. Este guion es lo que dice y registra quien conduce la sesión. El asistente no puede ejecutarlo; hasta que alguien lo haga, ambos casos siguen NO_PROBADO.

## Setup · Preparación

- One visitor who has not seen the repository or the demo. No coaching before or during the test.
- Device and viewport (desktop, or phone at 375 or 390 px). Language chosen by the visitor.
- URL: the published demo, or the local lab (`python run.py serve`). Record which revision: the Evidence view shows it under "File links open revision".
- A timer. The three minutes exclude installation.

- Un visitante que no haya visto el repositorio ni la demo. Sin ayuda antes ni durante.
- Dispositivo y ancho (escritorio, o teléfono a 375 o 390 px). Idioma elegido por el visitante.
- URL: la demo publicada o el laboratorio local (`python run.py serve`). Anota la revisión: la vista Evidencia la muestra en "Los enlaces a archivos abren la revisión".
- Un cronómetro. Los tres minutos no incluyen la instalación.

## 30 seconds (C170) · 30 segundos (C170)

Say only: "Look at this screen for 30 seconds." Then ask, without hints:

Di solo: "Mira esta pantalla durante 30 segundos." Después pregunta, sin pistas:

1. What is this? · ¿Qué es esto?
2. What does Marco do, and what did he not do himself? · ¿Qué hace Marco y qué no hizo él mismo?
3. Name one limit of what you see. · Di un límite de lo que ves.

Expected: purpose (a working lab of an AI implementation method), Marco's contribution separated from the AI-assisted code, and one limit (fictional data, no real refunds, no model in the public demo, or something pending).

Esperado: propósito (un laboratorio de un método de implementación de IA), la aportación de Marco separada del código asistido por IA, y un límite (datos ficticios, sin devoluciones reales, sin modelo en la demo pública, o algo pendiente).

## 3 minutes (C177 route) · 3 minutos (ruta C177)

Say only: "Press the tour button and follow it. Tell me when you are done." Record:

Di solo: "Pulsa el botón del recorrido y síguelo. Avísame cuando termines." Registra:

- Time to the first evidence link opened. · Tiempo hasta abrir el primer enlace a evidencia.
- Which requirement they opened and whether they can say its state (PASS, PARCIAL, PENDIENTE). · Qué requisito abrió y si sabe decir su estado.
- Whether they got back to Session without help. · Si volvió a Sesión sin ayuda.
- Any dead end, unclear word or wrong expectation. · Cualquier callejón sin salida, palabra confusa o expectativa errónea.

## Answer record · Registro de respuestas

Copy this block into `reports/VISITOR_<date>.md`, one per visitor. Do not include the visitor's name or any personal data; use a role (for example "recruiter", "engineer", "client").

Copia este bloque en `reports/VISITOR_<fecha>.md`, uno por visitante. Sin nombre ni datos personales; usa un rol (por ejemplo "reclutador", "ingeniero", "cliente").

```
Date / Fecha:
Visitor role / Rol del visitante:
Device, width, language / Dispositivo, ancho, idioma:
Revision shown in Evidence / Revisión mostrada en Evidencia:
Conducted by / Conducido por:

30 s — Q1 answer / respuesta:
30 s — Q2 answer / respuesta:
30 s — Q3 answer / respuesta:
30 s — result (3 correct = PASS; otherwise FAIL with what was missed) / resultado:

3 min — first evidence link at (mm:ss) / primer enlace a evidencia en:
3 min — requirement opened and state named / requisito abierto y estado nombrado:
3 min — back to Session without help (yes/no) / volvió a Sesión sin ayuda:
3 min — result (route complete without dead ends = PASS) / resultado:

Defects / Defectos (one per line: where, what happened, what was expected):
```

Then update C170 and C177 in `specs/001-support-demo/acceptance.csv` with the observed text, the status, the report file as evidence and the revision as product_version, and run `python scripts/verify.py`.

Después actualiza C170 y C177 en `specs/001-support-demo/acceptance.csv` con lo observado, el estado, el informe como evidencia y la revisión como product_version, y ejecuta `python scripts/verify.py`.
