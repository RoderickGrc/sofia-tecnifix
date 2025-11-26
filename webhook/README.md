# Implementación del Webhook - Google Apps Script

Esta carpeta contiene la documentación y código de la implementación del webhook que recibe los datos de las llamadas desde SOF.IA CALL y los guarda en Google Sheets.

## Archivos

- **`google-apps-script-implementation.md`** - Documentación completa de la implementación, incluyendo:
  - Información de la implementación (URL, ID, versión)
  - Código del script
  - Estructura de la hoja de cálculo
  - Flujo de datos
  - Contrato de datos esperado
  - Mapeo de campos
  - Configuración y notas

- **`Code.gs`** - Código fuente del Google Apps Script (listo para copiar/pegar)

- **`sheets-structure.json`** - Estructura JSON de las hojas de Google Sheets

- **`generar-datos-prueba.py`** - Script Python para generar y enviar datos ficticios de llamadas al webhook. Útil para poblar Google Sheets con datos de prueba para análisis en Looker Studio.

- **`servidor-local.ps1`** - Script PowerShell para iniciar un servidor HTTP local y evitar problemas de CORS al usar el simulador-webhook.html

## URL del Webhook

```
https://script.google.com/macros/s/AKfycbwo0m3C-2oeDErTAO9pzLp40B1407SbH3rZPsD9BN1ogQ9X11WT70GgG9iVuWbDaXfv/exec
```

## Uso

1. Configurar este URL en SOF.IA CALL como endpoint para webhooks de llamadas finalizadas
2. El script recibirá automáticamente los datos cuando una llamada termine
3. Los datos se guardarán en la hoja `Encuestas_Base` de Google Sheets

Para más detalles, consulta `google-apps-script-implementation.md`.

## Generar Datos de Prueba

Para poblar Google Sheets con datos ficticios y probar el análisis en Looker Studio:

```powershell
python webhook\generar-datos-prueba.py
```

El script enviará 15 llamadas ficticias (una por cada contacto definido) con datos variados y realistas:
- Calificaciones del 1 al 5
- NPS del 0 al 10
- Diferentes estados de llamada (completada, rechazada, reprogramada, errónea)
- Comentarios variados
- Transcripciones completas y realistas
- Resúmenes generados automáticamente

**Requisitos:**
- Python 3.6 o superior
- Librería `requests` (instalar con: `pip install requests`)

