# Empieza aquí

Soy Marco Díaz de León. Ayudo a definir qué necesita un negocio, qué sistemas hay que conectar y cómo organizar su implementación.

Este repositorio contiene un ejemplo de atención posventa con pedidos ficticios. Puedes consultar los requisitos, probar la aplicación y revisar sus resultados. El código se desarrolló con asistencia de IA.

## En dos minutos
1. Lee el problema en [la especificación](../specs/001-support-demo/spec.md).
2. Observa [la captura](assets/demo.jpg): solicitud, decisión y rastro de acciones.
3. Lee [las decisiones](decisions.md): qué se hizo, por qué y qué falta.

## En diez minutos
Ejecuta los comandos del README. En la web, selecciona el pedido elegible, analiza y pulsa ejecutar antes de aprobar: debe bloquearse. Después aprueba, activa el fallo simulado, ejecuta y comprueba que no hay recibo. Desactiva el fallo, reintenta y comprueba un único recibo.

No introduzcas claves, contraseñas ni datos de clientes. Todos los pedidos ya están incluidos.

## Qué significa cada pieza
- **Spec:** acuerdo de lo que debe ocurrir y cómo comprobarlo.
- **MVC:** separación entre datos, coordinación y pantalla.
- **Hook:** función que se ejecuta en un momento del flujo; aquí registra antes y después.
- **Skill:** procedimiento pequeño y reutilizable; su archivo no lo convierte en un control automático.
- **MCP:** contrato para que un cliente invoque herramientas. Aquí permite dos consultas de datos ficticios.
- **Evidencia:** resultado de una comprobación con el código al que corresponde.

El motor toma decisiones con reglas explícitas. Una futura integración con un modelo deberá demostrar su propia calidad; esta versión no la da por probada.
