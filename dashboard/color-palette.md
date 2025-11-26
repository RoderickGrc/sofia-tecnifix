# Paleta de Colores - Dashboard TecniFix

Paleta monocromática minimalista (blanco/negro/grises) para el dashboard de análisis de satisfacción.

---

## Variables CSS Principales

```css
--bg: #f5f5f5
--card: #ffffff
--border: #e4e4e7
--border-soft: #f0f0f0
--text-main: #111827
--text-soft: #6b7280
--text-muted: #9ca3af
--accent: #111827
```

---

## Colores de Fondo

| Color | Hex | Uso |
|-------|-----|-----|
| **Fondo principal** | `#f5f5f5` | Fondo general del dashboard |
| **Fondo de tarjetas** | `#ffffff` | Paneles y tarjetas KPI |
| **Fondo suave** | `#fafafa` | Tarjetas KPI secundarias |
| **Gradiente body** | `#f9fafb` → `#f3f4f6` → `#e5e7eb` | Fondo degradado radial del body |
| **Gradiente shell** | `#fdfdfd` → `#f5f5f5` | Fondo degradado del contenedor principal |
| **Fondo de gráficos** | `#f3f4f6` | Barras de progreso, fondos de gráficos |

---

## Colores de Texto

| Color | Hex | Uso |
|-------|-----|-----|
| **Texto principal** | `#111827` | Títulos, valores importantes, texto principal |
| **Texto secundario** | `#6b7280` | Subtítulos, etiquetas, texto secundario |
| **Texto atenuado** | `#9ca3af` | Metadatos, texto de ayuda, leyendas |
| **Texto en acentos** | `#4b5563` | Texto en elementos destacados |
| **Texto en elementos** | `#374151` | Texto en tablas, elementos interactivos |

---

## Colores de Bordes y Separadores

| Color | Hex | Uso |
|-------|-----|-----|
| **Borde principal** | `#e4e4e7` | Bordes de paneles, filtros |
| **Borde suave** | `#f0f0f0` | Bordes sutiles, separadores |
| **Borde destacado** | `#e5e7eb` | Bordes de contenedores principales |
| **Borde de gráficos** | `#d4d4d8` | Bordes de placeholders de gráficos |
| **Borde de badges** | `#d1d5db` | Bordes de badges y etiquetas |

---

## Colores de Acento (Negro)

| Color | Hex | Uso |
|-------|-----|-----|
| **Acento principal** | `#111827` | Botones primarios, valores destacados, barras de gráficos, elementos activos |
| **Acento en badges** | `#111827` | Badges destacados, etiquetas importantes |
| **Texto sobre acento** | `#f9fafb` | Texto blanco sobre fondo negro |

---

## Colores Semánticos (Uso Limitado)

### Verde (Solo para tendencias positivas)
| Color | Hex | Uso |
|-------|-----|-----|
| **Verde positivo** | `#16a34a` | Tendencias positivas, mejoras |
| **Verde estado** | `#22c55e` | Indicadores de estado activo/operativo |

### Rojo (Solo para alertas)
| Color | Hex | Uso |
|-------|-----|-----|
| **Rojo alerta** | `#dc2626` | Alertas, errores, valores críticos |

---

## Escala de Grises para Diagramas de Pastel

Para los diagramas de pastel de "Demora por tipo de problema":

| Categoría | Color | Hex | Uso |
|-----------|-------|-----|-----|
| **Bueno** | Negro | `#111827` | Porción "bueno" en pastel |
| **Regular** | Gris medio | `#6b7280` | Porción "regular" en pastel |
| **Malo** | Gris claro | `#d1d5db` | Porción "malo" en pastel |

---

## Sombras

| Sombra | Valor | Uso |
|--------|-------|-----|
| **Sombra suave** | `0 12px 30px rgba(15, 23, 42, 0.12)` | Sombras de paneles principales |
| **Sombra de grid** | `rgba(0, 0, 0, 0.03)` | Líneas de grid en gráficos |

---

## Uso en Looker Studio

### Para gráficos y visualizaciones:

1. **Barras de gráficos**: Usar `#111827` (negro) para valores principales
2. **Fondos de gráficos**: Usar `#f3f4f6` o `#ffffff` según el contexto
3. **Líneas de gráficos**: Usar `#111827` con opacidad 0.4-0.8
4. **Texto de ejes**: Usar `#6b7280` (texto secundario)
5. **Leyendas**: Usar `#9ca3af` (texto atenuado)

### Para diagramas de pastel:

- **Bueno**: `#111827` (negro)
- **Regular**: `#6b7280` (gris medio)
- **Malo**: `#d1d5db` (gris claro)

### Para formato condicional:

- **Valores positivos/mejoras**: `#16a34a` (verde)
- **Valores negativos/alertas**: `#dc2626` (rojo)
- **Valores neutros**: Escala de grises según importancia

---

## Principios de Diseño

1. **Monocromático**: Predominio de blanco, negro y grises
2. **Minimalismo**: Colores solo donde aportan significado
3. **Contraste**: Texto principal siempre en `#111827` sobre fondos claros
4. **Jerarquía**: Diferentes tonos de gris para establecer jerarquía visual
5. **Uso limitado de color**: Verde y rojo solo para indicar estados específicos (tendencias, alertas)

---

**Última actualización**: 23 de noviembre de 2025



