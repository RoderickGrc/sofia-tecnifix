# Entregables - Proyecto TecniFix Solutions

## Estado del Proyecto

✅ **Completado**

---

## Entregables

### 1. Agente de IA (Karla)
- **Estado**: ✅ Listo
- **Ubicación**: `prompts/sofiacall_agent_prompt.md`
- **Descripción**: Agente de llamadas IA configurado para realizar encuestas de satisfacción post-servicio técnico

### 2. Campaña de Llamadas
- **Estado**: ✅ Lista
- **Ubicación**: `docs/campaign-plan.md`
- **Descripción**: Campaña configurada para ejecutar encuestas de satisfacción a clientes recientes

### 3. Dashboard de Análisis (Looker Studio)
- **Estado**: ✅ Implementado
- **URL**: https://lookerstudio.google.com/u/0/reporting/576fba1f-d80b-443d-be4e-9c7392c737e9/page/JZXgF/edit
- **Descripción**: Dashboard de Business Intelligence con análisis de satisfacción, NPS, CSAT y métricas por tipo de problema
- **Mockup de referencia**: `dashboard/dashboard-mockup.html`
- **Paleta de colores**: `dashboard/color-palette.md`

---

## Componentes Técnicos

### Webhook (Google Apps Script)
- **URL**: https://script.google.com/macros/s/AKfycbwo0m3C-2oeDErTAO9pzLp40B1407SbH3rZPsD9BN1ogQ9X11WT70GgG9iVuWbDaXfv/exec
- **Documentación**: `webhook/google-apps-script-implementation.md`
- **Código**: `webhook/Code.gs`
- **Función**: Recibe datos de llamadas finalizadas y los guarda en Google Sheets

### Google Sheets
- **Hoja principal**: `Encuestas_Base`
- **Estructura**: `webhook/sheets-structure.json`
- **Función**: Almacena datos de encuestas para análisis en Looker Studio

### Simulador de Webhook
- **Archivo**: `simulador-webhook.html`
- **Función**: Permite simular envíos de webhook parseando HTML de llamadas de prueba

### Generador de Datos de Prueba
- **Archivo**: `webhook/generar-datos-prueba.py`
- **Función**: Genera y envía datos ficticios al webhook para poblar Google Sheets con datos de prueba

---

## Flujo Completo

1. **Campaña ejecutada** → SOF.IA CALL realiza llamadas a contactos
2. **Llamada finalizada** → Webhook recibe datos (transcript, summary, analysis)
3. **Datos guardados** → Google Apps Script guarda en Google Sheets
4. **Análisis visualizado** → Looker Studio muestra métricas y análisis

---

**Fecha de entrega**: 23 de noviembre de 2025



