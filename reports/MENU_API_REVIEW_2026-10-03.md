# Menú, conversación y traslado — revisión del 3 de octubre de 2026

Alcance U05, S01 0.4, R15–R17. Revisión realizada por el mismo ejecutor; no es revisión independiente ni aceptación de Marco.

## Observado
- 57 pruebas automatizadas y siete escenarios sintéticos: PASS en evidence/latest.json. Validación estructural SDD sin hallazgos.
- Navegador local, instancia nueva en 8766: menú abre Conexión API y Cómo está construido; Enter activa el enlace y Atrás recupera la vista anterior. El foco pasa al título.
- Elegir otro caso oculta la decisión de la propuesta anterior. Se conserva el comportamiento del controlador.
- Instancia de prueba 8767 con transporte simulado inyectado: conexión con clave ficticia, pregunta, respuesta, contador, vaciado y desconexión funcionaron. La respuesta mostraba explícitamente PRUEBA LOCAL SIMULADA.
- Una cadena con etiquetas script se mostró como texto; cero elementos script dentro del registro. Tras desconectar, envío y entrada quedaron deshabilitados.
- Captura de la pantalla de conexión sin credenciales: docs/assets/menu-api-20261003.jpg.
- Vista observada a 1280 px sin desbordamiento horizontal. La nueva comprobación a 390 px no quedó acreditada: el navegador devolvió 1280 px pese al ajuste solicitado. No se declara PASS móvil para este incremento.

## Pendiente
C045: comprensión y aceptación de un visitante. C066: respuesta con API real. C067: arranque en el segundo equipo.
No se leyó ninguna clave real ni se contactó al proveedor durante las pruebas. No se verificaron latencia, disponibilidad o coste real. El transporte hace la llamada real únicamente cuando el operador configura su clave y envía una pregunta.

La copia de proyectos a otro disco es una operación distinta de la aceptación de producto. Se requiere comparar archivos tras terminar la copia y revisar dependencias del destino. No se acredita portabilidad de bases de datos o sesiones.
