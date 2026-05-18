# 📊 FASE 4: Visualizaciones + Datos en Vivo

## ¿QUÉ ES NUEVA EN FASE 4?

### **Indicadores Macro en Vivo**
- 📊 **5 gráficos interactivos** con datos macro clave
- 💱 **USD/CLP** - Tipo de cambio en tiempo real
- 📈 **Inflación Anual** - CPI desde Federal Reserve
- 🏦 **Tasa de Fondos Fed** - Política monetaria USA
- 🔴 **Precio del Cobre** - Commodity principal de Chile
- 📈 **S&P 500** - Índice accionario global

### **Gráficos Interactivos**
- Visualizaciones con **Chart.js** (biblioteca JavaScript)
- Líneas de tendencia con últimos 7 días
- Hover interactivo con detalles
- Responsive design (móvil + desktop)
- Optimizado para impresión

## 📁 ARCHIVOS NUEVOS

```
📁 financiero/
├── fetch_live_data.py        # Obtiene datos macro en vivo
├── visualizations.py          # Genera gráficos HTML + CSS
├── generate_newsletter_v4.py  # Newsletter con visualizaciones
├── live_indicators.json       # Datos macro actualizados
└── charts.html               # Preview de gráficos
```

## 🚀 CÓMO FUNCIONA

### **Paso 1: Obtener Datos en Vivo**
```python
# fetch_live_data.py
fetcher = LiveDataFetcher()
indicators = fetcher.get_all_indicators()
```

**APIs Soportadas:**
- **Alpha Vantage** - USD/CLP, Cobre, S&P 500 (gratis con límites)
- **Federal Reserve FRED** - Inflación, Tasa Fed (gratis, sin límites)
- **Mock Data** - Fallback automático si las APIs no responden

### **Paso 2: Generar Gráficos**
```python
# visualizations.py
html = generate_charts_html(indicators)
css = generate_charts_css()
```

Genera sección HTML con 5 indicadores en tarjetas diseñadas profesionalmente.

### **Paso 3: Integrar en Newsletter**
```python
# generate_newsletter_v4.py
viz_html = integrate_visualizations_html(indicators)
# Inserta gráficos entre alertas y noticias
```

## 🔌 CONFIGURACIÓN DE APIs (PRODUCCIÓN)

### **Alpha Vantage** (para USD/CLP, Cobre, S&P 500)

1. Obtener API key:
   - Ir a: https://www.alphavantage.co/
   - Registrarse gratis
   - Copiar API key

2. Actualizar `fetch_live_data.py`:
```python
CONFIG = {
    'alpha_vantage_key': 'tu_api_key_aqui',  # Cambiar
    'fred_key': 'tu_fred_key_aqui',          # Ver abajo
    'use_mock': False  # Usar datos reales en lugar de mock
}
```

3. Límites gratis:
   - 500 llamadas/día
   - 5 llamadas/minuto
   - Suficiente para newsletter diaria

### **Federal Reserve FRED** (para Inflación, Tasa Fed)

1. Obtener API key:
   - Ir a: https://fred.stlouisfed.org/
   - Registrarse (gratis)
   - Crear API key en "Account" → "API Keys"

2. Actualizar `fetch_live_data.py`:
```python
CONFIG = {
    'fred_key': 'tu_fred_api_key'  # Cambiar
}
```

3. Ventajas:
   - ✅ Gratis sin límites de uso
   - ✅ Datos oficiales del Banco Central USA
   - ✅ Histórico disponible

### **GitHub Secrets** (para CI/CD)

Si usas GitHub Actions, guardar credenciales de forma segura:

```yaml
# .github/workflows/generate-newsletter.yml
- name: Fetch live data
  env:
    ALPHA_VANTAGE_KEY: ${{ secrets.ALPHA_VANTAGE_KEY }}
    FRED_KEY: ${{ secrets.FRED_KEY }}
  run: python fetch_live_data.py
```

En GitHub → Settings → Secrets → crear:
- `ALPHA_VANTAGE_KEY`
- `FRED_KEY`

## 📊 INDICADORES INCLUIDOS

### **1. USD/CLP (Tipo de Cambio)**
- Fuente: Alpha Vantage
- Frecuencia: Tiempo real
- Relevancia: Crítica para economía chilena
- Impacto: Inversiones, exportaciones, deuda externa

### **2. Inflación Anual (CPI)**
- Fuente: Federal Reserve
- Indicador: Consumer Price Index (CPI-U)
- Frecuencia: Mensual
- Relevancia: Política monetaria, poder de compra

### **3. Tasa de Fondos Fed**
- Fuente: Federal Reserve
- Rango actual: 4.50% (simulado)
- Impacto: Tasas de interés global, ciclos económicos

### **4. Precio del Cobre**
- Fuente: Alpha Vantage (commodities)
- Unidad: USD por libra
- Relevancia: Exportación #1 de Chile
- Sensible a: Demanda global, política monetaria China

### **5. Índice S&P 500**
- Fuente: Alpha Vantage
- Símbolo: ^GSPC (Global Quote)
- Frecuencia: Mercados USA
- Indicador: Sentimiento riesgo-apetito global

## 🎨 VISUALIZACIÓN HTML/CSS

### **Tarjetas de Indicadores**
```html
<div class="indicator-card">
  <h3>💱 Tipo de Cambio</h3>
  <span class="big-number">825.50 pesos</span>
  <canvas id="chart-usd-clp"></canvas>
</div>
```

Características:
- ✅ Número grande y legible
- ✅ Etiqueta descriptiva
- ✅ Gráfico de tendencia
- ✅ Estado actual (color)
- ✅ Responsive grid (auto-ajusta cantidad de columnas)

### **Gráficos Chart.js**
```javascript
new Chart(canvas, {
  type: 'line',
  data: {
    labels: ['L', 'M', 'X', 'J', 'V', 'S', 'H'],  // 7 últimos días
    datasets: [{
      data: [825, 826, 825.5, 827, ...],
      borderColor: '#2563eb',
      fill: true
    }]
  }
});
```

## 📈 DATOS MOCK (PARA SANDBOX)

Como estamos en ambiente sandbox sin acceso a internet, el sistema usa automáticamente **datos mock realistas**:

```json
{
  "usd_clp": {
    "tipo": "USD/CLP (simulado)",
    "precio": 808.50,
    "cambio": 16.50,
    "mock": true
  },
  "inflacion": {
    "tipo": "Inflación Anual (simulada)",
    "porcentaje": 3.2,
    "mock": true
  },
  ...
}
```

Cuando tengas credenciales reales de APIs, cambia `use_mock: False` para datos actuales.

## 🔄 AUTOMATIZACIÓN

### **Ejecución Diaria**
```yaml
# .github/workflows/generate-newsletter.yml
schedule:
  - cron: '0 9 * * *'  # 09:00 UTC diariamente
```

### **Orden de Ejecución**
1. `fetch_live_data.py` → Obtiene indicadores macro
2. `generate_newsletter_v4.py` → Genera HTML con gráficos
3. `export_newsletter.py` → Exporta PDF, JSON, CSV
4. `alerts_system.py` → Detecta eventos críticos
5. Git commit → Pushea cambios
6. GitHub Pages → Publica en web

## 📱 RESPONSIVE DESIGN

### **Desktop (>768px)**
```
5 columnas de indicadores
Gráficos grandes y claros
Información completa visible
```

### **Móvil (<768px)**
```
1 columna stacked
Gráficos adaptados
Scroll vertical
Touch-friendly
```

### **Impresión**
```
CSS de print
Saltos de página optimizados
Colores B&W
Sin elementos interactivos
```

## 🎯 CASOS DE USO

### **Para Ejecutivos**
- Dashboard visual de macro en 5 segundos
- Alertas críticas + contexto de datos
- PDF para presentaciones

### **Para Analistas**
- Datos estructurados en live_indicators.json
- Fácil integración con BI tools (Power BI, Tableau)
- Histórico guardado diariamente

### **Para Comunicación**
- Gráficos profesionales listos para incluir en reportes
- Newsletter visual + interactiva
- PDF imprimible

## 🔧 TROUBLESHOOTING

### **Los gráficos no aparecen**
1. Verificar que `live_indicators.json` exista
2. Revisar consola de navegador (F12 → Console)
3. Asegurar que Chart.js CDN está disponible

### **Las APIs no conectan**
- Normal en sandbox
- Sistema fallback a datos mock automáticamente
- Para producción: configurar credenciales en `fetch_live_data.py`

### **Datos desactualizados**
- Verificar que el workflow se ejecutó (GitHub Actions)
- Check logs: Repository → Actions → última ejecución
- Ejecutar manualmente: `workflow_dispatch`

## 📊 ARCHIVO live_indicators.json

```json
{
  "fecha": "2026-05-18T10:30:00",
  "version": "v4",
  "datos": {
    "usd_clp": {
      "tipo": "USD/CLP",
      "precio": 825.50,
      "cambio": 1.2
    },
    "inflacion": {
      "tipo": "Inflación Anual",
      "porcentaje": 3.2
    },
    "fed_rate": {
      "tipo": "Tasa Fed",
      "porcentaje": 4.50
    },
    "cobre": {
      "tipo": "Cobre (USD/lb)",
      "precio": 4.12
    },
    "sp500": {
      "tipo": "S&P 500",
      "precio": 5243.88,
      "cambio": 12.5
    }
  }
}
```

## 🚀 PRÓXIMAS MEJORAS (FASE 5+)

- [ ] Dashboard web interactivo con histórico
- [ ] Alertas automáticas en Slack/Teams
- [ ] Análisis predictivo con ML
- [ ] Integración Bloomberg Terminal API
- [ ] Comparativas día-a-día
- [ ] Exportar gráficos como PNG/SVG

## 📞 CONFIGURACIÓN RÁPIDA

Para producción con APIs reales:

```bash
# 1. Obtener keys (alphavantage.co, fred.stlouisfed.org)
# 2. Editar fetch_live_data.py
nano fetch_live_data.py
# Cambiar: 
# - alpha_vantage_key = 'tu_key'
# - fred_key = 'tu_key'
# - use_mock = False

# 3. Guardar en GitHub Secrets (si usas CI/CD)
# 4. Ejecutar
python generate_newsletter_v4.py

# 5. Ver resultado
open newsletter.html
```

---

**Estado:** ✅ Operacional  
**Versión:** v4 (FASE 4)  
**Última actualización:** 18 de Mayo, 2026
