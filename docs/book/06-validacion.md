# 6 Validación: CI, revisión independiente, aceptación, integración y publicación

[Índice del libro](README.md) · Código descrito: `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be` (PR #9).

## 6.1 Cinco registros que nadie infiere de otro

La vista Evidencia muestra cinco filas y la constitución exige que ninguna se deduzca de otra (regla 4; README: "none is implied by another"). A la fecha de este libro, con las palabras exactas de [project-status.json](../project-status.json) y de `evidence/latest.json`:

| Registro | Qué significa | Quién lo produce | Estado de la revisión descrita | Fuente |
|---|---|---|---|---|
| Verificación | `verify.py` corrió sobre estas fuentes y la evidencia comprometida las describe | La máquina (CI y la corrida comprometida) | Evidencia comprometida en `a16a4e6`: `passed: true`, 216 pruebas, 7 escenarios, casos PASS 267 / NO_PROBADO 9 / FAIL 0, `source_id` `0a2c32a9bd84…`. La entrega del libro añade tres casos y regenera la evidencia en su propia revisión (ver el PR) | `evidence/latest.json` (no se copia a project-status, R42c) |
| Revisión independiente | Codex leyó fuentes, CI y registros y emitió una nota | Codex | Registro vigente: "COMPLETED" sobre `fb7ecf6` (PR #7). Las revisiones de PR #8 y PR #9 están en la bitácora y en los cuerpos de los PR; la cuarta de PR #9 sobre `a16a4e6` dio 8.5/10 provisional, sin 9 acreditado ni visto bueno para fusionar, sin ejecutar el candidato (bitácora, entrada U22) | `independent_review`; [notebook.md](../notebook.md) |
| Aceptación del dueño | Marco aceptó un contenido concreto (árbol) | Marco | "OWNER_ACCEPTED" para `fb7ecf62…` (U17–U19, PR #7); "It does not cover changes after that revision" | `acceptance` |
| Integración | La revisión está contenida en main | Git | "INTEGRATED": main `166ea91…`, PR 7. `a16a4e6` **no** está integrada | `integration`; `scripts/revision.py:113-123` |
| Despliegue | Pages sirve esa revisión | Workflow `pages.yml` en main | "DEPLOYED": `166ea91…`, run 38190865149. La demo pública **no** muestra el código descrito aquí | `deployment` |

Por qué se separan (registrado): CU07, "A commit is not owner acceptance"; R56e, "CI results never authorize publication"; D41 nació de un fallo real: tras fusionar PR #7, main siguió sirviendo estados escritos a mano, así que ahora cada registro nombra su revisión y Git calcula contenido y contención; D43 añadió que un checkout con cambios sin confirmar nunca se lee como aceptado.

## 6.2 CI: qué corre y qué no autoriza

`.github/workflows/verify.yml` corre en cada push y pull request, con permisos `contents: read`, solo en este repositorio y para PR del mismo repositorio. Matriz: Ubuntu con Python 3.11 y 3.13, Windows con 3.13. Cada trabajo ejecuta en orden `security_check.py`, `check_evidence.py`, `check_evidence.py --save`, `verify.py`, `check_evidence.py --against`, `build_pages.py` y `node --check` sobre seis archivos JS; sube los tres archivos de evidencia como artefacto. Dos trabajos gate con nombres fijos, `verify (ubuntu-latest)` y `verify (windows-latest)`, agregan la matriz con `if: always()` (D37; `scripts/ci_gate.py`). `pages.yml` reutiliza `verify.yml` y despliega **solo** desde `main`, en push o `workflow_dispatch`, tras verificar (`pages.yml:5-7,16-18,36-38`). Las siete acciones están fijadas por SHA completo ([supply-chain.md](../supply-chain.md)).

Lo que CI no es: ni aceptación, ni revisión, ni publicación de una rama. Un check verde en un PR en borrador no cambia ningún registro.

## 6.3 El corredor aislado

Desde U21, las corridas que ejecutan código del repositorio en el entorno del implementador pasan por `scripts/sandbox/run_isolated.sh` (R58e, R58f; D50, D54, D57): raíz mínima por `pivot_root` con la cadena de herramientas de solo lectura y un `/etc` sintético, namespaces de usuario, montaje, red y PID con `/proc` privado, cgroups de procesos y memoria obligatorios, límites de CPU, tamaño de archivo y reloj, entorno vacío con lista blanca, loopback aislado. Tres etapas con tres niveles de confianza: la etapa que posee el directorio de resultados vive fuera del PID namespace del payload; el supervisor no es dumpable y no tiene descriptores de host; el payload corre en un namespace anidado con los flags de solo lectura bloqueados por el kernel y `no_new_privs`; la promoción de resultados (`scripts/sandbox/promote.py`) solo empieza cuando el namespace murió y valida nombres, tipo, enlaces y tamaños antes de escribir nada. Once líneas `CONTROL … OK` preceden al payload o la corrida aborta.

Lo que el corredor no es: no corre en CI (CI usa los runners de GitHub), no sustituye la reproducción de Codex (registrada como pendiente) y el kernel es el del host.

## 6.4 Las rondas de revisión independiente

Regla aplicada en cada ronda: registrar primero (requisito enmendado, tarea, decisión, casos), después corregir, después regenerar evidencia, en commits separados; lo anterior se conserva como "reported and superseded".

| PR | Revisión de Codex | Hallazgos | Cierre registrado |
|---|---|---|---|
| #7 (U17–U19) | `f0f088b`: 7.5/10, no listo | Nombres de gate, tour con cp1252, manifiestos, enlaces fijados, pie bilingüe, resultado del recorrido | R40–R45, D37–D39, fix `f15562d` |
| #7 | `5c4292d`: 8/10 como presentación, no listo | Comprobación incondicional del digest, ruta de candidato, `#evidence/<ID>` | R46–R48, D40, fix `e4981e5` |
| #7 | `fb7ecf6`: COMPLETED (140 pruebas, 7 escenarios, Windows 3.13 y Node 24, 10 checks verdes) | — | Marco aceptó; merge `166ea91`; publicado |
| #8 (U20) | `3f2c7ea`: no todas las áreas a 9 | Payload de forma inválida mostraba PASS; checkout sucio heredaba estados; lista de código vacía pasaba; `-X utf8` anidado | R49e–f, R51d, R53c, T79, D43–D44, C260–C268 en `2b645e4` |
| #8 | `2b645e4`: un residual | Estado fuera de la enumeración | R49e enmendado, C269 en `86051b5` |
| #9 (U21) | `26fb88d`: 7.5 provisional | F1 corredor sin confinar; F2 tope tras el hilo y goteo; F3 guardas de interfaz solo con prefijos; F4 directorios ocultos omitidos | D50–D53, T86, C307–C312 |
| #9 | `ebd38ed`: 7.5 provisional | S1 `/etc` del host y ruta escribible; S2 deadline armado una vez; S3 guardas solo sobre la serialización | D54–D56, T87, C313–C317 |
| #9 | `8a079ea`: 8/10 provisional | V1 descriptor del supervisor alcanzable por `/proc`, remount posible, promoción insegura | D57, R58f, T88, C318–C321 |
| #9 | `a16a4e6`: 8.5/10 provisional, sin 9 ni visto bueno | Sin nuevo P1 o P2 confirmado en el delta (bitácora, U22); reproducción independiente pendiente | Pendientes externos en 6.5 |

Entre rondas, dos carreras de CI en C284 (Windows: reset antes de leer; Ubuntu 3.11: slot keep-alive liberado un instante después) se cerraron en `968c72f` y `8a079ea`, documentadas en el [informe](../../reports/U21_SECURITY_2026-10-12.md) y no ocultadas.

## 6.5 Lo que sigue pendiente y no lo cierra esta documentación

- Evidencia del propietario (SC-15, C304): MFA, protección de rama, reporte privado de vulnerabilidades, escaneo de secretos, ajustes de Pages. Nada lo habilita el implementador (R58c).
- Análisis externo en CI: SAST, auditoría de dependencias, ruff; NO_PROBADO hasta una decisión de dependencia de Marco (D48).
- Un canal privado de reporte operativo (R58a).
- Pruebas humanas y de dispositivo: C170 (visitante nuevo), C176, C177, lector de pantalla, llamada real a un proveedor, otro PC. Casos NO_PROBADO en `a16a4e6` (nueve en el conteo de la evidencia): C045, C066, C067, C120, C151, C152, C170, C176, C177, C260, C296 y C304 figuran así en acceptance.csv; tres de ellos (C260, C296 y C120) tienen una prueba que los deja NO_PROBADO con motivo registrado.
- Decisión de Marco sobre D35 y la conciliación de los PR #4–#6.
- SC-16 (corredor) es VERIFICADO por casos ejecutados por el implementador; no es un PASS independiente de Codex.

## Summary in English

Five records, never inferred from one another: verification (machine), independent review (Codex, latest record on `fb7ecf6`; the fourth review of PR #9 at `a16a4e6` gave 8.5/10 provisional, no 9, no go, without executing the candidate), owner acceptance (`fb7ecf6`, bounded to that tree), integration (main `166ea91`) and deployment (Pages serves `166ea91`, not the code described here). CI runs on every push and PR across Linux 3.11/3.13 and Windows 3.13 with two gate jobs and SHA-pinned actions, and deploys only from main; it authorizes nothing. Since U21 the implementer's runs go through a three-stage isolated runner that is not CI and not Codex's reproduction. Each review round was closed in the order records, fix, evidence, with earlier runs kept as superseded. Owner evidence, external analysis in CI, a private reporting channel, the human and device tests and the owner's decisions on D35 and PRs #4–#6 remain open, and this book closes none of them.
