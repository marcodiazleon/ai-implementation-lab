# Empieza aquí

Soy Marco Díaz de León. Ayudo a definir qué necesita un negocio, qué sistemas hay que conectar y cómo organizar su implementación.

Este repositorio muestra mi trabajo de definición, selección de herramientas y coordinación de una integración. El ejemplo funciona con pedidos ficticios y el código se desarrolló con asistencia de IA.

## Cómo revisar mi forma de trabajar

| Paso | Qué puedes revisar | Documento |
|---|---|---|
| 1. Entender la necesidad | Audiencia, resultado esperado, alcance y fuentes | [Especificación: fuentes, casos de uso y requisitos](../specs/001-support-demo/spec.md) |
| 2. Conocer las reglas | Responsables, datos permitidos y decisiones pendientes | [Constitución](constitution.md) y [decisiones](decisions.md) |
| 3. Elegir herramientas | Para qué uso cada herramienta, acceso, coste, versión y comprobación | [Registro de herramientas](tools-and-capabilities.md) |
| 4. Organizar la construcción | Componentes, contratos, errores y recuperación | [Plan](../specs/001-support-demo/plan.md) y [arquitectura](architecture.md) |
| 5. Ejecutar por incrementos | Requisito, entregable, dependencia, responsable y cierre | [Tareas actuales](../specs/001-support-demo/tasks.md) |
| 6. Comprobar el resultado | Condición, acción, resultado esperado y observado por caso | [Matriz de aceptación](../specs/001-support-demo/acceptance.csv) |
| 7. Entregar y continuar | Evidencia, estado de cada registro, límites, siguiente tarea y mantenimiento | [Evidencia de esta revisión](../evidence/latest.json), [estado del proyecto](project-status.json), [operación](operations.md) y [bitácora](notebook.md). La [revisión del método del 2026-10-03](../reports/SDD_REVIEW.md) es histórica |

El [mapa del método](sdd-adoption.md) explica cómo se aplica cada área del libro de ingeniería a este proyecto. El [estado actual](project-status.json) identifica la especificación activa.

## Un recorrido concreto

Abre la [demo pública](https://marcodiazleon.github.io/ai-implementation-lab/). La entrada es **Sesión**, una conversación: arriba está quién soy, qué aporto y qué está pendiente. La URL pública sirve la revisión de main indicada en [project-status.json](project-status.json) (`deployment`); la vista Evidencia de cualquier versión dice si tiene el mismo contenido que la publicada y que la aceptada por el dueño.

En **Cómo está construido**, el recorrido de 3 minutos sigue **R03**: una devolución necesita una decisión previa. Los casos **CU04 y CU05** describen el flujo; la tarea **T02** corresponde a sus transiciones; **C013 y C018** comprueban que ejecutar antes de aprobar se bloquea. Cada control del recorrido abre su requisito en **Evidencia**, con sus casos, pruebas y estado. El recorrido termina con el resultado de `python run.py tour`: seis pasos con 0, 0, 0, 0, 1 y 1 recibos simulados.

Si tienes una copia del repositorio y Python 3.11 o superior, ejecuta `python run.py tour` (añade `--lang en` para inglés). Clonar e instalar no forma parte de los tres minutos. Comandos completos en el [README](../README.md).

**Revisar un candidato.** Un clon por defecto queda en main. Para revisar una rama aún no publicada, trae la rama, compara el commit con el SHA informado en su pull request y arranca el laboratorio:

```sh
git fetch origin <rama>
git checkout --detach FETCH_HEAD
git rev-parse HEAD        # debe coincidir con el SHA informado; si no: git checkout --detach <SHA informado>
python scripts/check_evidence.py
python run.py serve
```

Después abre http://127.0.0.1:8765. Si algo falla: Python 3.11 o superior, puerto 8765 libre (o `--port 8766`), y recuerda que `scripts/verify.py` reescribe cuatro archivos generados (`evidence/latest.json`, `evidence/sdd-check.json`, `specs/001-support-demo/acceptance.csv` y `docs/requirements-matrix.md`); para descartar solo esos, `git checkout -- evidence/latest.json evidence/sdd-check.json specs/001-support-demo/acceptance.csv docs/requirements-matrix.md`, nunca un reset de todo el árbol. Una consola que no pueda codificar un carácter (página de códigos ASCII; cp1252 sí imprime las tildes) muestra `?` en su lugar; `python -X utf8 run.py tour` lo imprime todo.

| Dónde | Qué funciona | Qué no |
|---|---|---|
| Demo pública | Presentación, recorrido, evidencia, creación de agentes en la pestaña y exploración de modelos | Conversar con un modelo o enviar una clave |
| Versión local | Lo anterior, `python run.py tour` y conversación con tu propia clave de OpenAI o Anthropic | Pagos, integraciones reales y autenticación del revisor |
| Pendiente | Prueba con una persona nueva (C170), lector de pantalla, API real y otra PC registrados por separado | — |

Todos los datos son ficticios. El recibo es local y simulado. El estado se pierde al reiniciar el servidor.

**Histórico.** Hasta U13 (2026-10-05) la web incluía un ejercicio visible de devoluciones: seleccionar el pedido, analizar, aprobar, simular el fallo y reintentar. U13 lo retiró de la interfaz; sus pasos quedan en el [guion histórico](demo-script.md) y el mismo caso se ejecuta hoy con `python run.py tour`.

## Cómo están organizadas las piezas

- **specs/** contiene el alcance, casos de uso, requisitos, plan, tareas y aceptación de cada incremento.
- **src/** separa datos, coordinación, hooks e interfaces; **web/** contiene la vista.
- **data/** contiene pedidos, política y escenarios ficticios.
- **.agents/skills/** guarda procedimientos concretos; **AGENTS.md** indica cuándo utilizarlos.
- **.githooks/** inspecciona el contenido preparado para un commit. Los hooks de la aplicación registran momentos del flujo.
- **tests/** comprueba las reglas; **scripts/** permite repetir las comprobaciones.
- **evidence/** contiene los resultados de ejecución y sus versiones; **reports/** explica su alcance.
- **docs/** conserva decisiones, herramientas, operación y continuidad.

**MVC** organiza datos, coordinación y pantalla. **MCP** expone herramientas mediante un protocolo: aquí son dos consultas de datos ficticios. Una **skill** define un procedimiento; su archivo por sí solo no demuestra que un ejecutor lo haya cargado.

## Qué sigue

Las [diez incorporaciones y diez mejoras](roadmap.md) tienen requisito, prioridad, dependencias, responsable y criterio de cierre. Su implementación se sigue en [S02](../specs/002-expansion/tasks.md).

La versión actual permite examinar el proceso y ejecutar el ejemplo. Las integraciones reales, autenticación, persistencia y evaluación de modelos tienen tareas propias. La aceptación de un visitante se registra cuando ese recorrido ocurra.
