# Empieza aquí

Soy Marco Díaz de León. Ayudo a definir qué necesita un negocio, qué sistemas hay que conectar y cómo organizar su implementación.

Este repositorio muestra mi trabajo de definición, selección de herramientas y coordinación de una integración. El ejemplo funciona con pedidos ficticios y el código se desarrolló con asistencia de IA.

## Cómo revisar mi forma de trabajar

| Paso | Qué puedes revisar | Documento |
|---|---|---|
| 1. Entender la necesidad | Audiencia, resultado esperado, alcance y fuentes | [Especificación: necesidad y siete casos de uso](../specs/001-support-demo/spec.md) |
| 2. Conocer las reglas | Responsables, datos permitidos y decisiones pendientes | [Constitución](constitution.md) y [decisiones](decisions.md) |
| 3. Elegir herramientas | Para qué uso cada herramienta, acceso, coste, versión y comprobación | [Registro de herramientas](tools-and-capabilities.md) |
| 4. Organizar la construcción | Componentes, contratos, errores y recuperación | [Plan](../specs/001-support-demo/plan.md) y [arquitectura](architecture.md) |
| 5. Ejecutar por incrementos | Requisito, entregable, dependencia, responsable y cierre | [Tareas actuales](../specs/001-support-demo/tasks.md) |
| 6. Comprobar el resultado | Condición, acción, resultado esperado y observado por caso | [Matriz de aceptación](../specs/001-support-demo/acceptance.csv) |
| 7. Entregar y continuar | Evidencia, límites, siguiente tarea y mantenimiento | [Revisión actual](../reports/SDD_REVIEW.md), [operación](operations.md) y [bitácora](notebook.md) |

El [mapa del método](sdd-adoption.md) explica cómo se aplica cada área del libro de ingeniería a este proyecto. El [estado actual](project-status.json) identifica la especificación activa.

## Un recorrido concreto

Sigue **R03**: una devolución necesita una decisión previa. Los casos **CU04 y CU05** describen el flujo; la tarea **T02** corresponde a sus transiciones; **C013 y C018** comprueban que ejecutar antes de aprobar se bloquea. La matriz enlaza las pruebas y sus resultados.

En la web, selecciona el pedido elegible y analiza. Ejecutar antes de aprobar debe bloquearse. Después aprueba, activa el fallo simulado y ejecuta: no debe producir recibo. Desactiva el fallo, reintenta y comprueba un único recibo. Sigue los [pasos completos](demo-script.md) y los comandos del [README](../README.md).

Todos los datos necesarios están incluidos. El resultado es un recibo local simulado. El estado se pierde al reiniciar el servidor.

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
