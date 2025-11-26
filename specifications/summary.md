### 1. Resumen del caso (qué tienes que lograr)

Para **TecniFix Solutions** debes montar, en SOF.IA CALL, una campaña donde la IA llame automáticamente a clientes recientes para hacer una **encuesta de satisfacción post-servicio técnico** y luego:

1. **Agente IA**

   * Configurado con tono *formal, amable y orientado al servicio*.
   * Personalización: saluda por nombre.
   * Hace una encuesta de **3 a 5 preguntas** clave (calidad, tiempos, amabilidad, NPS, comentario). 

2. **Campaña de llamadas**

   * Subes al menos **10 contactos simulados**.
   * Ejecutas las llamadas desde SOF.IA CALL.
   * Verificas que las **respuestas queden correctamente registradas** en la plataforma. 

3. **Webhook → Google Sheets/Excel** (obligatorio)

   * Crear un **endpoint con Google Apps Script**.
   * Configurar SOF.IA CALL para mandar los datos de cada llamada en **JSON** al webhook.
   * Cada llamada debe generar una **nueva fila** con todos los datos de la encuesta. 

4. **Dashboard de Business Intelligence (Looker Studio/Data Studio)**

   * Estilo de reporte empresarial real.
   * Debe mostrar al menos:

     * **NPS promedio**
     * **Calificación promedio**
     * **Tendencias por tipo de problema**
     * **3+ gráficos y KPIs principales**. 

5. **Datos mínimos a capturar por llamada** 

   * Nombre del cliente
   * Calificación del servicio (1–5)
   * Tiempo de atención (bueno / regular / malo)
   * Amabilidad del técnico (buena / regular / mala)
   * Comentario del cliente (texto libre)
   * NPS (0–10)
   * Resultado de la llamada (ej. completada, colgó, no contesta)
   * Nota resumen (síntesis de la IA / analista)

6. **Entregables** 

   * Agente configurado
   * Campaña creada y ejecutada
   * Webhook funcionando
   * Dashboard profesional
   * Informe breve

---

### 2. Checklist para empezar a idear (paso a paso)

#### A. Definir el flujo lógico de la encuesta

* [ ] Definir **objetivo principal**: ¿qué quieres priorizar? (ej. medir NPS y detectar problemas recurrentes en el soporte técnico).

* [ ] Redactar un **guion base** de llamada:

  * [ ] Presentación de la empresa y del agente IA.
  * [ ] Saludo personalizado: “Hola, [Nombre del cliente]…”
  * [ ] Explicar que es una **encuesta corta de satisfacción** (tiempo estimado).
  * [ ] Cierre y agradecimiento.

* [ ] Definir las **3–5 preguntas** concretas:

  * [ ] Calificación general del servicio (1–5).
  * [ ] Percepción del **tiempo de atención** (bueno/regular/malo).
  * [ ] Percepción de la **amabilidad del técnico** (buena/regular/mala).
  * [ ] Pregunta de **NPS**: “En una escala de 0 a 10, ¿qué probabilidad hay de que recomiende TecniFix a un amigo o colega?”.
  * [ ] Comentario abierto: “¿Hay algo que quiera comentarnos sobre el servicio recibido?”.

* [ ] Definir **ramas básicas** del flujo si:

  * [ ] El cliente no quiere responder.
  * [ ] El cliente cuelga a mitad de la encuesta.
  * [ ] El cliente responde con algo que no encaja (ej. responde texto libre donde debe ir un número).

---

#### B. Diseñar el prompt del agente IA en SOF.IA CALL

* [ ] Definir el **tono**: formal, amable, enfocado en servicio al cliente.
* [ ] Incluir en el prompt:

  * [ ] Quién es el agente (“representante virtual de TecniFix Solutions”).
  * [ ] Contexto: llamada post-servicio técnico para encuesta corta.
  * [ ] Instrucciones claras de **flujo**:

    * [ ] Presentarse y confirmar identidad del cliente por nombre.
    * [ ] Pedir permiso para continuar con la encuesta.
    * [ ] Hacer las preguntas en orden.
    * [ ] Validar rango de respuestas (ej. si pide 1–5 o 0–10).
    * [ ] Si la respuesta no es válida, pedirla de nuevo.
    * [ ] Terminar agradeciendo.
  * [ ] Formato interno de datos que el agente debe “tener listo” para el webhook (ej. campos JSON).
  * [ ] Pedir que el agente genere una **nota resumen** de 1–2 líneas de la llamada.

*(Más adelante puedo ayudarte a redactar el prompt completo ya listo para pegar.)*

---

#### C. Plan de estructura de datos (JSON → Sheet/Excel)

* [ ] Definir la estructura JSON que se va a enviar desde SOF.IA CALL, por ejemplo:

```json
{
  "nombre_cliente": "",
  "telefono": "",
  "calificacion_servicio": 0,
  "tiempo_atencion": "",
  "amabilidad_tecnico": "",
  "comentario": "",
  "nps": 0,
  "resultado_llamada": "",
  "nota_resumen": "",
  "tipo_problema": "",
  "fecha_llamada": ""
}
```

* [ ] Ver qué campos SOF.IA CALL **ya genera por defecto** (id de llamada, duración, etc.) y si conviene agregarlos.
* [ ] Asegurarse de que **todos los campos del caso** están mapeados a columnas de Excel/Google Sheets.

---

#### D. Diseño del Webhook (Google Apps Script + Sheets/Excel)

* [ ] Crear un **Google Sheet** base (será tu “base de datos” de encuestas).

* [ ] Diseñar las **columnas** que coincidan con el JSON del webhook.

* [ ] En Google Apps Script:

  * [ ] Crear un **script web app** que reciba peticiones POST.
  * [ ] Parsear el cuerpo JSON.
  * [ ] Insertar cada llamada como **nueva fila**.
  * [ ] Devolver un `status: ok` para que SOF.IA CALL sepa que se registró bien.

* [ ] Probar el endpoint con **datos de prueba** (Postman, curl o herramienta similar).

* [ ] Configurar en SOF.IA CALL la **URL del webhook** y el formato JSON.

* [ ] Ejecutar una llamada de prueba y confirmar que:

  * [ ] Llega la fila al Sheet.
  * [ ] Los campos se posicionan en las columnas correctas.

*(Si prefieres Excel, la idea es similar, pero más sencillo quedarte en Google Sheets porque se integra directo con Looker Studio.)*

---

#### E. Diseño del Dashboard de BI (Looker Studio / Data Studio)

* [ ] Conectar Looker Studio a tu **Google Sheet**.

* [ ] Definir los KPIs principales:

  * [ ] NPS promedio.
  * [ ] Calificación promedio del servicio.
  * [ ] Porcentaje de “bueno/regular/malo” en tiempo de atención.
  * [ ] Porcentaje de “buena/regular/mala” en amabilidad.

* [ ] Definir gráficos:

  * [ ] Gráfico de barras para **tipo de problema vs calificación promedio**.
  * [ ] Gráfico de líneas para **tendencia del NPS en el tiempo**.
  * [ ] Gráfico circular o barras apiladas para **distribución del tiempo de atención**.

* [ ] Crear secciones visuales:

  * [ ] Encabezado con logo de TecniFix Solutions y texto breve del objetivo del reporte.
  * [ ] Sección de KPIs grandes (NPS, calificación promedio, % de clientes promotores vs detractores).
  * [ ] Sección de análisis (gráficos por tipo de problema).
  * [ ] Sección de notas o insights (donde luego puedes añadir conclusiones).

---

#### F. Checklist de pruebas finales

* [ ] Ejecutar campaña con **10 contactos simulados**.

* [ ] Confirmar que:

  * [ ] El tono del agente es coherente y profesional.
  * [ ] Personaliza correctamente el nombre.
  * [ ] Hace todas las preguntas sin saltarse ninguna.
  * [ ] Las respuestas quedan almacenadas en SOF.IA CALL.
  * [ ] El webhook recibe cada llamada y genera una fila en el Sheet.
  * [ ] No hay filas con campos desfasados o vacíos sin razón.
  * [ ] El dashboard se actualiza correctamente con los nuevos datos.

* [ ] Preparar un **informe breve**:

  * [ ] Explicar la lógica del flujo.
  * [ ] Explicar cómo se configuró el webhook.
  * [ ] Describir el dashboard y sus métricas.
  * [ ] Incluir capturas de pantalla (agente, campaña, Sheet, dashboard).
