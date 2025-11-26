# Campaña de Encuesta de Satisfacción Post-Servicio - TecniFix Solutions

## Información General

**Nombre de la Campaña:**  
`ENC_SATISFACCION_TECNIFIX_Q4_2025`

**Código Interno:**  
`TECNIFIX-SAT-001`

**Fecha de Inicio:**  
Por definir

**Duración Estimada:**  
Campaña continua (llamadas programadas según recepción de servicios técnicos)

---

## Descripción y Objetivo

### Descripción
Campaña automatizada de llamadas salientes mediante agente de IA (Karla de TecniFix) para recopilar feedback de satisfacción de clientes que recibieron servicios técnicos de reparación, mantenimiento o soporte en TecniFix Solutions.

### Objetivos Principales
1. **Medir calidad del servicio:** Obtener calificación numérica (1-10) del servicio técnico recibido.
2. **Calcular NPS (Net Promoter Score):** Identificar promotores, pasivos y detractores para evaluar lealtad del cliente.
3. **Detectar problemas recurrentes:** Identificar inconvenientes específicos mencionados por los clientes durante la atención.
4. **Recopilar opiniones cualitativas:** Capturar comentarios, sugerencias y áreas de mejora para optimizar procesos internos.

### Objetivos Secundarios
- Reducir tiempo de recolección de feedback (automatización vs. llamadas manuales).
- Generar datos estructurados para análisis de tendencias y toma de decisiones.
- Mejorar la experiencia del cliente mediante seguimiento proactivo post-servicio.

---

## Datos de Salida por Llamada

Cada llamada completada genera un registro con las siguientes variables:

### Variables de Salida (4 campos obligatorios)

| Variable | Tipo | Rango/Formato | Descripción |
|----------|------|---------------|-------------|
| `calificacion_servicio` | number | 1-10 | Calificación numérica del servicio técnico recibido (1 = pésimo, 10 = excelente) |
| `nps` | number | 0-10 | Probabilidad de recomendar TecniFix (0 = nada probable, 10 = muy probable) |
| `opinion_cliente` | string | Texto libre | Comentario, sugerencia o feedback general del cliente |
| `problema` | string | Texto breve o "Ninguno" | Descripción del inconveniente mencionado, o "Ninguno" si no hubo problemas |

### Metadatos de Llamada (generados automáticamente por SOF.IA CALL)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_llamada` | string | Identificador único de la llamada |
| `id_campaña` | string | Identificador de la campaña |
| `telefono` | string | Número de teléfono contactado |
| `nombre_cliente` | string | Nombre del cliente (variable de entrada) |
| `fecha_hora_inicio` | datetime | Timestamp de inicio de la llamada |
| `fecha_hora_fin` | datetime | Timestamp de finalización de la llamada |
| `duracion_segundos` | number | Duración total de la llamada en segundos |
| `resultado_llamada` | string | Estado: "completada", "rechazada", "colgo", "no_contesta", "parcial" |

### Ejemplo de Registro Completo

```json
{
  "id_llamada": "LL-20251121-0001",
  "id_campaña": "ENC_SATISFACCION_TECNIFIX_Q4_2025",
  "telefono": "+5037XXXXXXX",
  "nombre_cliente": "Carlos Pérez",
  "fecha_hora_inicio": "2025-11-21T15:03:12Z",
  "fecha_hora_fin": "2025-11-21T15:05:34Z",
  "duracion_segundos": 142,
  "calificacion_servicio": 9,
  "nps": 8,
  "opinion_cliente": "Todo bien, solo que tardaron un poco más de lo esperado en entregar la laptop.",
  "problema": "Retraso en entrega",
  "resultado_llamada": "completada"
}
```

---

## Plan de Análisis de Datos para Negocio

### Fase 1: Recolección y Almacenamiento

**Objetivo:** Centralizar todos los datos de llamadas en una hoja de cálculo (Google Sheets) mediante webhook.

**Acciones:**
1. Configurar webhook en SOF.IA CALL que envíe datos en formato JSON al endpoint de Google Apps Script.
2. Crear Google Sheet con columnas que mapeen todas las variables de salida + metadatos.
3. Validar que cada llamada completa genere una nueva fila con datos correctos.
4. Implementar manejo de errores (filas de error para llamadas con datos incompletos).

**Entregable:** Google Sheet con datos históricos de encuestas.

---

### Fase 2: Procesamiento y Limpieza de Datos

**Objetivo:** Preparar los datos para análisis, clasificando NPS y detectando patrones en problemas.

**Acciones:**
1. **Clasificación de NPS:**
   - Promotores: NPS 9-10
   - Pasivos: NPS 7-8
   - Detractores: NPS 0-6
   - Cálculo: NPS = % Promotores - % Detractores

2. **Categorización de Problemas:**
   - Análisis de texto libre en `problema` para agrupar por tipo:
     - Demoras
     - Comunicación
     - Calidad de reparación
     - Amabilidad del técnico
     - Precio
     - Otros

3. **Segmentación por Calificación:**
   - Clientes satisfechos: calificación 8-10
   - Clientes neutros: calificación 5-7
   - Clientes insatisfechos: calificación 1-4

**Entregable:** Datos procesados con columnas calculadas (NPS clasificado, categoría de problema, segmento de satisfacción).

---

### Fase 3: Métricas Clave de Negocio (KPIs)

**KPIs Principales:**

1. **NPS Global**
   - Fórmula: % Promotores - % Detractores
   - Meta: NPS > 50 (considerado excelente en servicios técnicos)

2. **Calificación Promedio del Servicio**
   - Fórmula: Promedio de `calificacion_servicio`
   - Meta: ≥ 8.5 / 10

3. **Tasa de Finalización de Encuesta**
   - Fórmula: (Llamadas completadas / Total de llamadas) × 100
   - Meta: ≥ 70%

4. **Tasa de Problemas Reportados**
   - Fórmula: (Llamadas con `problema` ≠ "Ninguno" / Total completadas) × 100
   - Meta: < 15%

5. **Tasa de Promotores**
   - Fórmula: (Clientes con NPS 9-10 / Total completadas) × 100
   - Meta: ≥ 60%

6. **Tasa de Detractores**
   - Fórmula: (Clientes con NPS 0-6 / Total completadas) × 100
   - Meta: < 10%

---

## Plan de Creación de Dashboard

### Herramienta Recomendada
**Google Looker Studio** (anteriormente Data Studio) conectado directamente a Google Sheets.

### Estructura del Dashboard

#### **Página 1: Vista Ejecutiva (KPIs Principales)**

**Sección Superior:**
- **Tarjeta grande:** NPS Global (número grande, color verde/amarillo/rojo según rango)
- **Tarjeta:** Calificación Promedio del Servicio (ej: 8.7 / 10)
- **Tarjeta:** Tasa de Finalización (ej: 75%)
- **Tarjeta:** Total de Encuestas Completadas (contador)

**Sección Media:**
- **Gráfico de barras:** Distribución de NPS (Promotores vs. Pasivos vs. Detractores)
- **Gráfico circular:** Distribución de Calificaciones (1-3, 4-6, 7-8, 9-10)

**Sección Inferior:**
- **Tabla:** Top 5 Problemas Más Mencionados (con conteo)

---

#### **Página 2: Análisis de Tendencias**

**Sección Superior:**
- **Gráfico de líneas:** Evolución del NPS en el tiempo (últimos 30 días)
- **Gráfico de líneas:** Evolución de la Calificación Promedio (últimos 30 días)

**Sección Media:**
- **Gráfico de barras apiladas:** Problemas por Categoría (Demoras, Comunicación, Calidad, etc.)
- **Gráfico de barras:** Calificación Promedio por Tipo de Problema

**Sección Inferior:**
- **Gráfico de barras horizontales:** Tasa de Finalización por Día de la Semana

---

#### **Página 3: Análisis Cualitativo**

**Sección Superior:**
- **Tabla filtrable:** Todos los comentarios (`opinion_cliente`) con filtros por:
  - Rango de calificación
  - Rango de NPS
  - Presencia de problema
  - Fecha

**Sección Media:**
- **Word Cloud o gráfico de barras:** Palabras clave más frecuentes en comentarios (opcional, requiere procesamiento adicional)

**Sección Inferior:**
- **Tabla:** Resumen de Problemas Reportados (agrupados y contados)

---

### Configuración Técnica del Dashboard

1. **Conexión de Datos:**
   - Conectar Looker Studio a Google Sheet (fuente de datos).
   - Configurar actualización automática cada 4 horas (o manual según necesidad).

2. **Campos Calculados Necesarios:**
   - `nps_clasificacion`: IF `nps` >= 9 THEN "Promotor" ELSE IF `nps` >= 7 THEN "Pasivo" ELSE "Detractor"
   - `satisfaccion_segmento`: IF `calificacion_servicio` >= 8 THEN "Satisfecho" ELSE IF `calificacion_servicio` >= 5 THEN "Neutro" ELSE "Insatisfecho"
   - `tiene_problema`: IF `problema` = "Ninguno" THEN "No" ELSE "Sí"

3. **Filtros Globales:**
   - Rango de fechas (selector de fecha)
   - Resultado de llamada (solo "completada" por defecto)

---

### Métricas Adicionales Recomendadas (Opcionales)

- **Análisis por Técnico:** Si se captura `tecnico_asignado`, crear vista segmentada por técnico.
- **Análisis por Tipo de Servicio:** Si se captura `tipo_servicio`, crear vista segmentada por categoría (Hardware, Software, Mantenimiento).
- **Comparativa Mensual:** Dashboard comparativo mes a mes para identificar mejoras o deterioros.

---

## Próximos Pasos

1. **Configurar webhook** en SOF.IA CALL → Google Apps Script → Google Sheets.
2. **Ejecutar campaña piloto** con 10-15 contactos de prueba.
3. **Validar estructura de datos** en Google Sheets.
4. **Crear dashboard básico** en Looker Studio con KPIs principales.
5. **Iterar y mejorar** según feedback interno y necesidades de análisis.

---

**Documento generado:** 2025-11-21  
**Versión:** 1.0  
**Responsable:** Equipo de Calidad TecniFix Solutions






