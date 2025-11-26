# Implementación del Webhook - Google Apps Script

## Información de la Implementación

**Versión:** 1  
**Fecha de implementación:** 23 de noviembre de 2025, 12:35 p.m.  
**ID de implementación:** `AKfycbwo0m3C-2oeDErTAO9pzLp40B1407SbH3rZPsD9BN1ogQ9X11WT70GgG9iVuWbDaXfv`

**URL del webhook (App web):**  
```
https://script.google.com/macros/s/AKfycbwo0m3C-2oeDErTAO9pzLp40B1407SbH3rZPsD9BN1ogQ9X11WT70GgG9iVuWbDaXfv/exec
```

---

## Código del Google Apps Script

```javascript
function doPost(e) {
  const body = JSON.parse(e.postData.contents);
  const call = body.call;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Encuestas_Base');

  // transcript para fecha/hora/duración
  const transcript = call.transcript || [];
  let fecha = '';
  let hora = '';
  let duracionSegundos = '';

  if (transcript.length > 0) {
    const first = new Date(transcript[0].created_at);
    const last = new Date(transcript[transcript.length - 1].created_at);
    fecha = Utilities.formatDate(last, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    hora  = Utilities.formatDate(last, Session.getScriptTimeZone(), 'HH:mm:ss');
    const diffMs = last.getTime() - first.getTime();
    duracionSegundos = Math.round(diffMs / 1000);
  }

  const analysis = call.analysis || {};
  const row = [
    call.id,
    call.to,
    call.from,
    fecha,
    hora,
    analysis.calificacion_servicio,
    analysis.nps,
    analysis.tiempo_atencion,
    analysis.amabilidad_tecnico,
    analysis.opinion_cliente,
    analysis.estado_llamada_completada_rechazada_reprogramada_o_erronea,
    call.summary,
    duracionSegundos,
    call.credits
  ];

  sheet.appendRow(row);

  return ContentService
    .createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

---

## Estructura de la Hoja de Cálculo (Google Sheets)

### Hoja: `Encuestas_Base`

**Columnas (en orden):**

1. `call_id` - ID único de la llamada
2. `telefono_cliente_to` - Número de teléfono del cliente (destinatario)
3. `telefono_origen_from` - Número de teléfono origen (desde donde se llama)
4. `fecha_hora` - Fecha de la llamada (formato: yyyy-MM-dd)
5. `canal` - *(Reservado para uso futuro)*
6. `agente` - *(Reservado para uso futuro)*
7. `nombre_cliente` - *(Reservado para uso futuro)*
8. `motivo_llamada` - *(Reservado para uso futuro)*
9. `sub_motivo` - *(Reservado para uso futuro)*
10. `cliente_calificacion` - Calificación del servicio (1-5)
11. `cliente_comentario` - Comentario del cliente (texto libre)
12. `estado_llamada` - Estado de la llamada (completada, rechazada, reprogramada, errónea)
13. `resumen_llamada` - Resumen generado por la IA
14. `duracion_segundos` - Duración de la llamada en segundos
15. `credits` - Créditos consumidos en la llamada

**Nota:** Las columnas 5-9 están definidas en la estructura pero no se están poblando actualmente. Están reservadas para integraciones futuras o datos adicionales que puedan venir del CRM.

### Hoja: `CRM_Contactos`

**Columnas:**

1. `telefono` - Número de teléfono del contacto
2. `nombre` - Nombre del contacto
3. `problema` - Tipo de problema reportado

**Nota:** Esta hoja está preparada para almacenar información de contactos del CRM, pero actualmente no se está utilizando en el flujo del webhook.

---

## Flujo de Datos

1. **Recepción del webhook:** El script recibe un `POST` con el payload JSON del contrato de llamada.

2. **Extracción de datos:**
   - Se parsea el cuerpo de la petición
   - Se extrae el objeto `call` que contiene toda la información de la llamada
   - Se procesa el `transcript` para calcular fecha, hora y duración

3. **Cálculo de duración:**
   - Se toma el primer mensaje del transcript como inicio
   - Se toma el último mensaje del transcript como fin
   - Se calcula la diferencia en milisegundos y se convierte a segundos

4. **Formateo de fecha y hora:**
   - Fecha: formato `yyyy-MM-dd`
   - Hora: formato `HH:mm:ss`
   - Se usa la zona horaria del script

5. **Construcción de la fila:**
   - Se mapean los datos del `call` y `analysis` a las columnas correspondientes
   - Se respeta el orden definido en la estructura de la hoja

6. **Guardado:**
   - Se agrega la fila a la hoja `Encuestas_Base` usando `appendRow()`

7. **Respuesta:**
   - Se retorna un JSON con `{ success: true }` para confirmar el procesamiento

---

## Contrato de Datos Esperado

El webhook espera recibir un JSON con la siguiente estructura:

```json
{
  "successful": true,
  "call": {
    "id": 987654321,
    "from": "+12025550123",
    "to": "+5493510001111",
    "credits": 333,
    "transcript": [
      {
        "id": "m1",
        "created_at": "2025-11-23T16:11:21.360Z",
        "text": "Hola, ¿hablo con Pedro?",
        "user": "bot"
      }
    ],
    "summary": "Resumen de la llamada...",
    "is_completed": true,
    "analysis_schema": {
      "calificacion_servicio": "number",
      "nps": "number",
      "tiempo_atencion": "string",
      "amabilidad_tecnico": "string",
      "opinion_cliente": "string",
      "estado_llamada_completada_rechazada_reprogramada_o_erronea": "string"
    },
    "analysis": {
      "calificacion_servicio": 5,
      "nps": 10,
      "tiempo_atencion": "bueno",
      "amabilidad_tecnico": "regular",
      "opinion_cliente": "Pongan aire acondicionado en el local.",
      "estado_llamada_completada_rechazada_reprogramada_o_erronea": "completada"
    }
  }
}
```

---

## Mapeo de Campos

| Campo en el Webhook | Columna en Sheets | Tipo | Notas |
|---------------------|-------------------|------|-------|
| `call.id` | `call_id` | number | ID único de la llamada |
| `call.to` | `telefono_cliente_to` | string | Número del cliente |
| `call.from` | `telefono_origen_from` | string | Número origen |
| Calculado del transcript | `fecha_hora` | string | Fecha (yyyy-MM-dd) |
| Calculado del transcript | `hora` | string | Hora (HH:mm:ss) |
| *(Reservado)* | `canal` | - | No se usa actualmente |
| *(Reservado)* | `agente` | - | No se usa actualmente |
| *(Reservado)* | `nombre_cliente` | - | No se usa actualmente |
| *(Reservado)* | `motivo_llamada` | - | No se usa actualmente |
| *(Reservado)* | `sub_motivo` | - | No se usa actualmente |
| `analysis.calificacion_servicio` | `cliente_calificacion` | number | 1-5 |
| `analysis.opinion_cliente` | `cliente_comentario` | string | Texto libre |
| `analysis.estado_llamada_completada_rechazada_reprogramada_o_erronea` | `estado_llamada` | string | completada/rechazada/etc. |
| `call.summary` | `resumen_llamada` | string | Resumen generado por IA |
| Calculado del transcript | `duracion_segundos` | number | Duración en segundos |
| `call.credits` | `credits` | number | Créditos consumidos |

**Nota:** Los campos `analysis.nps`, `analysis.tiempo_atencion` y `analysis.amabilidad_tecnico` se están guardando pero no tienen columnas asignadas en la estructura actual. Esto puede requerir ajustes futuros.

---

## Configuración del Script

1. **Permisos necesarios:**
   - Acceso a Google Sheets (lectura/escritura)
   - Ejecución como usuario autenticado

2. **Despliegue:**
   - Tipo: Aplicación web
   - Ejecutar como: Yo (usuario autenticado)
   - Quién tiene acceso: Cualquiera (para permitir llamadas desde SOF.IA CALL)

3. **URL del webhook:**
   - Se debe configurar en SOF.IA CALL como el endpoint para recibir los datos de las llamadas finalizadas

---

## Notas de Implementación

- El script calcula la duración basándose en el primer y último mensaje del transcript
- La fecha y hora se toman del último mensaje del transcript
- Si el transcript está vacío, los campos de fecha, hora y duración quedarán vacíos
- El script maneja casos donde `analysis` o `transcript` pueden estar vacíos usando el operador `||`
- La respuesta siempre es JSON con `{ success: true }` independientemente del resultado

---

## Próximos Pasos / Mejoras Futuras

1. **Validación de datos:** Agregar validación de campos requeridos antes de guardar
2. **Manejo de errores:** Implementar logging de errores y respuestas de error más descriptivas
3. **Mapeo completo:** Ajustar el mapeo para incluir todos los campos de `analysis` (NPS, tiempo_atencion, amabilidad_tecnico)
4. **Integración con CRM:** Poblar las columnas reservadas con datos del CRM usando el número de teléfono como clave
5. **Deduplicación:** Implementar lógica para evitar duplicados basándose en `call.id`

---

**Última actualización:** 23 de noviembre de 2025



