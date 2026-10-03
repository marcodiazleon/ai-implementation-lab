# Investigación de expansión — AI Implementation Lab

Fecha: 2026-10-03. Estado: investigación integrada al backlog S02; sus propuestas no equivalen a implementación.
Base revisada: commit b7206c67918c9b70635d107615aa9ebf1873f59f.

## Conclusión

El proyecto ya ofrece una muestra reproducible de control de operaciones. Para posicionar mejor a su autor como estratega de implementación, conviene reforzar tres cosas: experiencia de entrada, decisiones de negocio y una integración real acotada. Aumentar el número de agentes o documentos por sí solo no demuestra mayor valor.

Las recomendaciones siguientes son juicio de diseño aplicado a la inspección del código y a fuentes primarias. Las fuentes apoyan mecanismos concretos; no certifican el repositorio ni garantizan resultados comerciales.

## Base observada

Inspección de README, constitution, capabilities, roadmap, controller, server, hooks, MCP, interfaz, tests, scripts y matriz de aceptación. El árbol estaba limpio al comenzar.

- evidence/latest.json registra 42 tests y 7 escenarios aprobados el 3 de octubre. Esta investigación leyó ese registro; no volvió a ejecutar las pruebas.
- El controlador usa diccionarios en memoria para propuestas y recibos.
- El endpoint de decisión entrega el literal human_reviewer al controlador, sin autenticar al solicitante.
- El fallo simulado ocurre antes de crear el recibo. El registro after ocurre después de modificar estado.
- Los eventos no incorporan hora, duración ni identificador independiente de ejecución.
- El adaptador MCP limita sus herramientas a dos consultas y su evidencia corresponde al protocolo por stdio, no a un cliente de IA real.
- La web requiere servidor local; no hay una versión pública ejecutable sin instalación.
- La interfaz mantiene la propuesta anterior cuando solo cambia la selección del escenario; todavía exige pulsar analizar para reemplazarla.
- El scanner contiene un grupo limitado de patrones. No hay workflow de CI versionado en el repositorio.
- La evidencia resume el total de tests y hashes; no guarda cada resultado individual ni plataforma, versión de Python o commit del run.

## Diez capacidades para agregar

Prioridad: P1 = siguiente entrega orientada a mostrar valor; P2 = después de cerrar esa entrega; P3 = ampliar cuando la base sea comprensible. No son fechas ni presupuestos.

| ID | Capacidad nueva | Entrega mínima y utilidad | Cierre verificable | Prioridad |
|---|---|---|---|---|
| A01 | Demo pública sin instalación | Showroom estático, separado del servidor Python, que reproduzca casos con datos ficticios en el navegador. Facilita la entrada desde el perfil profesional. | Otra persona completa un caso desde una URL sin Python, cuenta ni claves; los resultados coinciden con fixtures de contrato. | P1 |
| A02 | Diagnóstico guiado de una oportunidad | Formulario sobre problema, usuario, sistema actual, frecuencia, restricciones y éxito esperado. Produce un brief editable y marca información faltante. | Dos casos ficticios generan briefs diferentes y una respuesta incompleta no se presenta como requisito confirmado. | P1 |
| A03 | Simulador de beneficio y coste | Volumen, tiempo manual, tiempo asistido, tasa de revisión, implantación y operación; escenarios conservador/base/optimista. Hace visible el criterio de negocio. | Fórmulas visibles, sensibilidad reproducible, unidades claras y todos los supuestos identificados; cero ahorro presentado como obtenido. | P1 |
| A04 | Planificador con modelo real opcional | Una única integración intercambiable con el motor determinista. El modelo propone; el controlador conserva la decisión sobre acciones permitidas. | Evaluación separada de lenguaje, herramienta, estado final y seguridad; repetir casos para medir variabilidad; coste/límites visibles, cancelación y modo offline conservado. | P2 |
| A05 | Consulta de documentación con citas | Pequeño conjunto original de políticas ficticias, búsqueda y respuestas que señalen documento y fragmento. Puede empezar sin LLM. | Preguntas conocidas recuperan la fuente correcta; sin evidencia se responde que falta información; contenido recuperado no altera permisos. | P2 |
| A06 | Integración externa real de solo lectura | Consultar incidencias públicas de un repositorio de demostración controlado por el autor; mostrar transformación de datos y errores. | Evidencia de una lectura real con fecha, límites y resultados; tratamiento de timeout y rate limit; ninguna escritura externa. | P2 |
| A07 | Segundo caso operativo | Clasificar y derivar solicitudes internas ficticias, con revisión humana. Comprueba que el método sirve más allá de devoluciones. | Una solicitud ambigua se deriva a una persona; ambos casos reutilizan contratos y controles sin copiar toda la aplicación. | P3 |
| A08 | Explorador visual de requisitos y evidencia | Pantalla navegable problema → requisito → decisión → prueba → resultado. Convierte la matriz existente en una herramienta para el visitante. | Cada vínculo resuelve a una evidencia real; un requisito sin prueba aparece pendiente, nunca aprobado por defecto. | P1 |
| A09 | Comparador de estrategias | Simulador de construir, integrar, comprar o mantener un proceso manual, con criterios y pesos editables. Muestra cuándo no conviene usar IA. | Cambiar costes, restricciones o pesos cambia la comparación de forma explicable; el resultado es apoyo a decisión, no recomendación universal. | P2 |
| A10 | Kit de piloto y adopción | Evaluador guiado de responsables, capacitación, indicador inicial, condiciones de avance, parada y reversión. Exporta un plan pequeño. | Un responsable o criterio crítico ausente produce pendiente; incluye una práctica de operador y una revisión de comprensión. | P2 |

A01 requiere trabajo distinto al simple despliegue de los archivos actuales: GitHub Pages sirve HTML/CSS/JavaScript estático, y la UI actual llama a un backend Python. Una reproducción estática debe identificarse como tal y mantener pruebas de equivalencia. [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

A02, A03 y A09 aplican a esta muestra la recomendación de establecer una línea base, explorar alternativas y contrastar supuestos. A10 incorpora la medición y aprendizaje en el piloto. Son propuestas propias; no existen beneficios medidos de clientes. [GOV.UK: beneficios](https://www.gov.uk/service-manual/measuring-success/measuring-service-benefits), [métricas](https://www.gov.uk/service-manual/measuring-success/how-to-set-performance-metrics-for-your-service).

A06 puede basarse en la API de incidencias públicas de GitHub. Hay que gestionar su contrato y distinguir incidencias de pull requests cuando corresponda, sin incorporar datos de proyectos privados. [GitHub REST Issues](https://docs.github.com/en/rest/issues/issues#list-repository-issues).

## Diez mejoras a lo existente

| ID | Situación observada | Mejora propuesta | Cierre verificable | Prioridad |
|---|---|---|---|---|
| M01 | El README explica ingeniería, pero el visitante aún debe deducir algunas decisiones del autor. | Presentar problema → alternativas → decisión → resultado observable → próximo paso. Añadir un vídeo corto narrado por el autor con transcripción. | Un lector identifica qué decidió el autor y qué se simuló; sin experiencia o resultados comerciales inventados. | P1 |
| M02 | La UI conserva la propuesta previa al cambiar el selector y el reinicio exige parar el servidor. | Limpiar o identificar inequívocamente la propuesta al cambiar de caso; pasos activos, estado de espera y reinicio explícito de una sesión de muestra. Completar idioma español/inglés. | Cambiar escenario no permite actuar accidentalmente sobre el anterior; reiniciar pide confirmar la pérdida de estado y permite exportar antes. | P1 |
| M03 | Hay etiquetas y región de estado, pero no una evaluación formal de accesibilidad. | Revisar teclado, foco, contraste, zoom, móvil, mensajes y lector de pantalla. | Recorrido básico por teclado y a 200% de zoom documentado; fallos corregidos. No declarar conformidad completa por pasar checks iniciales. | P1 |
| M04 | La aprobación HTTP asigna un rol fijo. | Identidad real para una variante de piloto, roles separados, permisos por operación y expiración/revocación de decisiones. | Un solicitante sin rol no puede aprobar por API; se comprueba autorización en el servidor en cada operación. | P2, antes de piloto real |
| M05 | Los recibos desaparecen al reiniciar y el fallo probado es solo previo al efecto. | Persistencia transaccional, clave de idempotencia duradera y estado de resultado desconocido con reconciliación. | Reiniciar no duplica; un timeout posterior al efecto no dispara otra acción ciega; falla del hook posterior no deja estado ambiguo sin recuperación. | P2, antes de efectos reales |
| M06 | La traza solo tiene secuencia, acción y resultado. | Añadir ID de ejecución, hora, duración, fase, causa y métricas; anonimizar/redactar antes de exportar. | Seguir un caso de principio a fin y distinguir intento, fallo y reintento sin exponer contenido sensible. | P2 |
| M07 | Evidencia local resumida; no CI versionado. | Guardar resultados individuales, versión de entorno, commit y estado del árbol; automatizar checks acotados en Windows/Linux y navegador. | Un defecto introducido en una rama de prueba falla el check correspondiente; evidencia distingue omitido, fallido y aprobado. | P1 |
| M08 | El hook de publicación detecta pocos patrones y puede omitirse. | Combinar revisión de material publicable, scanner mantenido y controles de GitHub, verificando disponibilidad antes de configurarlos. | Fixtures artificiales para distintos tipos de secreto se detectan; se documentan exclusiones y bypass, sin afirmar cobertura total. | P1 |
| M09 | MCP implementado a mano y probado por stdio. | Verificar el cliente objetivo, esquema de mensajes, negociación, entradas malformadas y límites antes de cargar mensajes completos. Valorar SDK oficial según compatibilidad. | Un cliente real usa ambas herramientas, una operación fuera de alcance se bloquea y una entrada malformada no termina el proceso. | P2 |
| M10 | El controlador mezcla datos de fixture, reglas y almacenamiento; CSS y HTML están muy compactados. | Interfaces pequeñas para repositorio de datos, política, planificador y conector; formatear código y fijar herramientas sin crear capas innecesarias. | Sustituir almacenamiento o conector de prueba sin tocar las reglas ni la UI; mantener los contratos y resultados existentes. | P2 |

Para M03: WCAG 2.2 incluye requisitos sobre foco y objetivos de interacción. Los checks iniciales de WAI ayudan a detectar problemas, pero no sustituyen una evaluación completa. [W3C WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/), [WAI Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/).

Para M05: SQLite aporta transacciones locales; por sí solo no garantiza idempotencia frente a servicios externos ni atomicidad entre base de datos y un pago. Es una pieza candidata, no la solución completa. [SQLite transactional](https://www.sqlite.org/transactional.html).

Para M07: GitHub documenta matrices de Python y sistemas operativos para construir y probar. Propongo un workflow pequeño con permisos mínimos y sin usar claves de modelos. No se activó CI en esta investigación. [GitHub Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).


Para A04, la evaluación debe medir el conjunto modelo + herramientas + control de ejecución, con varias repeticiones por caso y resultados finales verificables. La cantidad inicial de casos será una decisión de alcance, no un umbral de calidad universal. Para A05, añadir documentos sintéticos que intenten cambiar reglas; observar llamadas y efectos, no solo lo que dice la respuesta. El caso actual de herramienta prohibida no es evidencia de defensa contra prompt injection. [Anthropic: evals de agentes](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [OWASP: prompt injection](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).

Para M04, comprobar permisos por petición y por recurso, con denegación por defecto. Para M05, un proveedor puede haber realizado la operación antes de perder su respuesta; la recuperación necesita identidad de operación y consulta de estado. [OWASP: autorización](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [AWS: reintentos e idempotencia](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/).

Para M06, las trazas relacionan operaciones y tiempos; empezar con exportación local y campos mínimos. Para M07 y M08, limitar permisos del workflow y verificar la protección de publicación efectiva, sin dar por activadas funciones de la cuenta. [OpenTelemetry: traces](https://opentelemetry.io/docs/concepts/signals/traces/), [GitHub Actions: uso seguro](https://docs.github.com/en/actions/reference/security/secure-use), [GitHub: push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection).

Para M09, utilizar un cliente independiente como Inspector y luego el cliente de IA elegido; Inspector por sí solo no demuestra compatibilidad con todos los clientes. La documentación actual describe también otras versiones del protocolo; validar primero la versión fijada 2025-11-25 y decidir después si conviene migrar. [MCP Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector).

## Secuencia recomendada

1. **Muestra que cualquiera entiende:** M01, M02, M03 y A01. Cierre: visitante externo termina el recorrido y explica el caso.
2. **Estrategia visible:** A02 y A03. Cierre: una oportunidad ficticia tiene brief, alternativas y números con supuestos.
3. **Evidencia fácil de revisar:** M07, M08 y A08. Cierre: un visitante llega del requisito al check concreto.
4. **Integración acotada:** A06 y M09. Cierre: consulta real y herramientas probadas con cliente, sin efectos externos.
5. **IA evaluada:** A04 y después A05, usando M06. Cierre: comparación con baseline, límites de uso y fallos registrados.
6. **Variante de piloto:** M04, M05, M10 y A10. Cierre: identidad, recuperación y operación antes de efectos reales.
7. **Amplitud de muestra:** A07 y A09 cuando la primera historia ya sea convincente.

No recomiendo comenzar por multiagentes, una bóveda propia, chat multicanal ni un IDE completo. Son otros productos o capas de complejidad y diluirían el objetivo de esta muestra. No se descartan en otros proyectos; quedan fuera de este incremento.

## Qué cambió con esta investigación

En el corte de investigación solo se prepararon propuestas. En la entrega SDD posterior, por solicitud del propietario, este informe se integra al repositorio y los 20 puntos se convierten en requisitos y tareas en specs/002-expansion. No se habilitaron proveedores ni conectores; el estado vigente de implementación está en ese backlog.
