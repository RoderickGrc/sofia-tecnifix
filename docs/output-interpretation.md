# Interpretación de Salidas - Campaña TecniFix Solutions

## Propósito
Este documento define cómo interpretar y procesar las variables de salida de cada llamada realizada por el agente "Karla de TecniFix" en SOF.IA CALL, específicamente la variable `{{estado_llamada}}` y sus acciones asociadas.

---

## Variable Clave: `{{estado_llamada}}`

Esta variable determina el **destino y procesamiento** de cada registro de llamada. Es el campo principal para la lógica de flujo post-llamada.

### Valores Posibles

| Valor | Descripción | Acción Post-Llamada |
|-------|-------------|---------------------|
| `completada` | Encuesta completada exitosamente con todos los datos recopilados. | ✅ **Procesar datos** → Enviar a Google Sheets → Incluir en dashboard. |
| `reprogramada` | Cliente solicitó reprogramar la llamada para otro momento. | 🔄 **Reagendar** → Usar `{{fecha_reprogramacion}}` y `{{hora_reprogramacion}}` para nueva llamada. |
| `rechazada` | Cliente rechazó participar y no quiere reprogramar. | ❌ **Marcar como finalizado** → NO volver a llamar. |
| `contacto_erroneo` | Número equivocado, persona incorrecta, fallecida, etc. | ❌ **Marcar como inválido** → NO volver a llamar. |

---

## Flujos de Procesamiento por Estado

### 1. Estado: `completada`

**Condición:** `{{estado_llamada}} = "completada"`

**Variables Esperadas (Todas deben tener valor):**
- `{{calificacion_servicio}}` (1-10)
- `{{tiempo_atencion}}` (Bueno/Regular/Malo)
- `{{amabilidad_tecnico}}` (Buena/Regular/Mala)
- `{{problema}}` (texto libre o "Ninguno")
- `{{nps}}` (0-10)
- `{{opinion_cliente}}` (texto libre)

**Acciones:**
1. ✅ Validar que todas las variables de encuesta estén presentes.
2. ✅ Enviar registro completo al webhook → Google Sheets.
3. ✅ Incluir en análisis y dashboard.
4. ✅ Marcar contacto como "Encuestado" en la base de contactos.
5. ❌ **NO volver a llamar** a este contacto.

**Ejemplo de Registro:**
```json
{
  "id_llamada": "LL-001",
  "nombre_cliente": "Carlos Pérez",
  "estado_llamada": "completada",
  "calificacion_servicio": 9,
  "tiempo_atencion": "Bueno",
  "amabilidad_tecnico": "Buena",
  "problema": "Ninguno",
  "nps": 8,
  "opinion_cliente": "Todo excelente, muy profesional."
}
```

---

### 2. Estado: `reprogramada`

**Condición:** `{{estado_llamada}} = "reprogramada"`

**Variables Esperadas:**
- `{{fecha_reprogramacion}}` (DD-MM-YY, ej: "26-11-22")
- `{{hora_reprogramacion}}` (HH:MM, ej: "14:30")

**Acciones:**
1. 🔄 Extraer `{{fecha_reprogramacion}}` y `{{hora_reprogramacion}}`.
2. 🔄 Convertir a formato datetime estándar para el sistema de campañas.
3. 🔄 **Reagendar la llamada** en SOF.IA CALL para la fecha/hora especificada.
4. 🔄 Mantener el contacto en estado "Pendiente de reprogramación".
5. ⚠️ **NO enviar a Google Sheets** aún (no hay datos de encuesta).

**Validación:**
- Si `{{fecha_reprogramacion}}` o `{{hora_reprogramacion}}` están vacíos → Marcar como error y no reprogramar.

**Ejemplo de Registro:**
```json
{
  "id_llamada": "LL-002",
  "nombre_cliente": "María González",
  "estado_llamada": "reprogramada",
  "fecha_reprogramacion": "26-11-22",
  "hora_reprogramacion": "15:00"
}
```

**Lógica de Reagendamiento:**
- El sistema de campañas debe leer estos campos y crear una nueva tarea de llamada programada.
- Si la fecha/hora ya pasó al momento de procesar, marcar como "reprogramación vencida" y ofrecer nueva fecha o marcar como "rechazada".

---

### 3. Estado: `rechazada`

**Condición:** `{{estado_llamada}} = "rechazada"`

**Variables Esperadas:**
- Ninguna variable de encuesta (o todas vacías).

**Acciones:**
1. ❌ Marcar contacto como "Rechazado - No volver a llamar".
2. ❌ Registrar en log de rechazos (opcional, para análisis de tasa de rechazo).
3. ❌ **NO enviar a Google Sheets** (no hay datos útiles).
4. ❌ **NO volver a llamar** a este contacto en futuras campañas.

**Ejemplo de Registro:**
```json
{
  "id_llamada": "LL-003",
  "nombre_cliente": "Juan López",
  "estado_llamada": "rechazada"
}
```

**Nota:** Este estado se usa cuando el cliente explícitamente rechaza participar después del intento de persuasión y también rechaza reprogramar.

---

### 4. Estado: `contacto_erroneo`

**Condición:** `{{estado_llamada}} = "contacto_erroneo"`

**Variables Esperadas:**
- Ninguna variable de encuesta (o todas vacías).

**Acciones:**
1. ❌ Marcar contacto como "Contacto Inválido" en la base de datos.
2. ❌ Registrar motivo (número equivocado, persona incorrecta, fallecida, etc.) si está disponible en logs.
3. ❌ **NO enviar a Google Sheets**.
4. ❌ **NO volver a llamar** a este número.
5. ⚠️ Considerar actualizar/limpiar la base de contactos si hay muchos casos de este tipo.

**Ejemplo de Registro:**
```json
{
  "id_llamada": "LL-004",
  "nombre_cliente": "Pedro Martínez",
  "estado_llamada": "contacto_erroneo"
}
```

**Casos Comunes:**
- "No soy esa persona"
- "Número equivocado"
- "Esa persona ya no vive aquí"
- "Línea desconectada"
- "Persona fallecida"

---

## Matriz de Decisión Rápida

| Estado | ¿Enviar a Sheets? | ¿Reagendar? | ¿Volver a Llamar? | ¿Incluir en Dashboard? |
|--------|------------------|-------------|-------------------|------------------------|
| `completada` | ✅ Sí | ❌ No | ❌ No | ✅ Sí |
| `reprogramada` | ❌ No | ✅ Sí | ✅ Sí (en fecha programada) | ❌ No (hasta completar) |
| `rechazada` | ❌ No | ❌ No | ❌ No | ❌ No |
| `contacto_erroneo` | ❌ No | ❌ No | ❌ No | ❌ No |

---

## Implementación Técnica Sugerida

### En el Webhook (Google Apps Script o Backend)

```javascript
// Pseudocódigo de lógica de procesamiento
function procesarLlamada(datos) {
  const estado = datos.estado_llamada;
  
  switch(estado) {
    case "completada":
      // Validar que todas las variables de encuesta estén presentes
      if (validarDatosCompletos(datos)) {
        insertarEnGoogleSheets(datos); // Incluir en análisis
        marcarContactoComo("encuestado", datos.nombre_cliente);
      }
      break;
      
    case "reprogramada":
      // Extraer fecha y hora
      const fecha = datos.fecha_reprogramacion; // DD-MM-YY
      const hora = datos.hora_reprogramacion;   // HH:MM
      
      if (fecha && hora) {
        reagendarLlamada(datos.nombre_cliente, fecha, hora);
        marcarContactoComo("pendiente_reprogramacion", datos.nombre_cliente);
      } else {
        // Error: falta fecha/hora
        logError("Reprogramación sin fecha/hora", datos);
      }
      break;
      
    case "rechazada":
      marcarContactoComo("rechazado", datos.nombre_cliente);
      // NO hacer nada más
      break;
      
    case "contacto_erroneo":
      marcarContactoComo("invalido", datos.nombre_cliente);
      // NO hacer nada más
      break;
  }
}
```

### En el Sistema de Campañas (SOF.IA CALL o similar)

1. **Filtro de Contactos para Nueva Campaña:**
   - Excluir contactos con estado: "encuestado", "rechazado", "invalido".
   - Incluir solo: "pendiente" y "pendiente_reprogramacion" (con fecha/hora cumplida).

2. **Procesamiento de Reprogramaciones:**
   - Leer registros con `estado_llamada = "reprogramada"`.
   - Convertir `fecha_reprogramacion` y `hora_reprogramacion` a datetime del sistema.
   - Crear tarea programada para esa fecha/hora.
   - Si la fecha ya pasó, marcar como "reprogramación vencida" y ofrecer nueva fecha o marcar como "rechazada".

---

## Métricas de Seguimiento Recomendadas

1. **Tasa de Completación:** `(completadas / total_llamadas) × 100`
2. **Tasa de Reprogramación:** `(reprogramadas / total_llamadas) × 100`
3. **Tasa de Rechazo:** `(rechazadas / total_llamadas) × 100`
4. **Tasa de Contactos Erróneos:** `(contacto_erroneo / total_llamadas) × 100`

Estas métricas ayudan a identificar:
- Calidad de la base de contactos.
- Efectividad del agente en persuasión.
- Necesidad de limpieza de datos.

---

## Notas Finales

- **Prioridad:** Siempre procesar `estado_llamada` primero antes de cualquier otra lógica.
- **Validación:** Validar que `estado_llamada` siempre tenga uno de los 4 valores permitidos.
- **Logs:** Registrar todos los estados para auditoría y análisis de tendencias.
- **Actualización:** Este documento debe actualizarse si se añaden nuevos estados o se modifican las reglas de negocio.

---

**Documento generado:** 2025-11-22  
**Versión:** 1.0  
**Responsable:** Equipo de Calidad TecniFix Solutions





