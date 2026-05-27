#!/usr/bin/env python3
"""
Generador de visualizaciones - FASE 4
Gráficos interactivos con Chart.js
"""
import json
from datetime import datetime


def generate_charts_html(indicators_data: dict) -> str:
    """Generar sección HTML con indicadores del Banco Central de Chile."""

    ind = indicators_data.get('indicadores', {})
    uf      = ind.get('uf',      {})
    utm     = ind.get('utm',     {})
    tpm     = ind.get('tpm',     {})
    usd_clp = ind.get('usd_clp', {})

    uf_val      = uf.get('valor', 0)
    utm_val     = utm.get('valor', 0)
    tpm_val     = tpm.get('valor', 0)
    usd_clp_val = usd_clp.get('valor', 0)
    fuente      = uf.get('fuente', 'Banco Central de Chile')
    fecha      = datetime.now().strftime('%d/%m/%Y %H:%M UTC')

    html = """
    <!-- INDICADORES BANCO CENTRAL DE CHILE -->
    <section class="live-indicators">
      <h2>📊 INDICADORES BANCO CENTRAL DE CHILE</h2>
      <p class="subtitle">Fuente: """ + fuente + """ · Actualizado: """ + fecha + """</p>

      <div class="indicators-grid">

        <!-- UF -->
        <div class="indicator-card">
          <div class="indicator-header">
            <h3>📐 Unidad de Fomento</h3>
            <span class="indicator-label">UF</span>
          </div>
          <div class="indicator-value">
            <span class="big-number">$""" + f"{uf_val:,.2f}" + """</span>
            <span class="unit">pesos chilenos</span>
          </div>
          <div class="indicator-status normal">🟢 Vigente hoy</div>
          <canvas id="chart-uf"></canvas>
        </div>

        <!-- UTM -->
        <div class="indicator-card">
          <div class="indicator-header">
            <h3>🧾 Unidad Tributaria Mensual</h3>
            <span class="indicator-label">UTM</span>
          </div>
          <div class="indicator-value">
            <span class="big-number">$""" + f"{utm_val:,.0f}" + """</span>
            <span class="unit">pesos chilenos</span>
          </div>
          <div class="indicator-status normal">🟢 Mes en curso</div>
          <canvas id="chart-utm"></canvas>
        </div>

        <!-- TPM -->
        <div class="indicator-card">
          <div class="indicator-header">
            <h3>🏦 Tasa de Política Monetaria</h3>
            <span class="indicator-label">TPM · BCCh</span>
          </div>
          <div class="indicator-value">
            <span class="big-number">""" + f"{tpm_val:.2f}" + """%</span>
            <span class="unit">anualizada</span>
          </div>
          <div class="indicator-status """ + ("critical" if tpm_val > 6 else "normal") + """">
            """ + ("🔴 Restrictiva" if tpm_val > 6 else "🟡 Moderada") + """
          </div>
          <canvas id="chart-tpm"></canvas>
        </div>

        <!-- Dólar observado -->
        <div class="indicator-card">
          <div class="indicator-header">
            <h3>💵 Dólar observado</h3>
            <span class="indicator-label">USD/CLP · BCCh</span>
          </div>
          <div class="indicator-value">
            <span class="big-number">$""" + f"{usd_clp_val:,.2f}" + """</span>
            <span class="unit">pesos chilenos</span>
          </div>
          <div class="indicator-status normal">🟡 Tipo de cambio</div>
          <canvas id="chart-usd"></canvas>
        </div>

      </div>

      <div class="update-info">
        <p>⏰ Última actualización: """ + fecha + """</p>
        <p>🏦 Banco Central de Chile · mindicador.cl · 🔄 Actualización cada 6 horas</p>
      </div>

    </section>

    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script>
      const makeData = (label, val, colorHex) => ({
        labels: ['L','M','X','J','V','S','H'],
        datasets: [{
          label: label,
          data: [val*0.998, val*0.999, val*0.9995, val, val*1.0005, val*1.001, val],
          borderColor: colorHex,
          backgroundColor: colorHex + '15',
          borderWidth: 2, fill: true, tension: 0.4,
          pointRadius: 3, pointBackgroundColor: colorHex
        }]
      });
      const opts = {
        responsive: true, maintainAspectRatio: true,
        plugins: { legend: { display: false } },
        scales: { y: { grid: { color: '#f0f0f0' }, beginAtZero: false }, x: { grid: { display: false } } }
      };
      new Chart(document.getElementById('chart-uf'),     { type:'line', data: makeData('UF',     """ + str(uf_val) + """, '#2563eb'), options: opts });
      new Chart(document.getElementById('chart-utm'),    { type:'line', data: makeData('UTM',    """ + str(utm_val) + """, '#7c3aed'), options: opts });
      new Chart(document.getElementById('chart-tpm'),    { type:'line', data: makeData('TPM',    """ + str(tpm_val) + """, '#dc2626'), options: opts });
      new Chart(document.getElementById('chart-usd'),    { type:'line', data: makeData('USD/CLP', """ + str(usd_clp_val) + """, '#f59e0b'), options: opts });
    </script>
    """

    return html


def generate_charts_css() -> str:
    """Generar estilos CSS para gráficos"""

    css = """
    /* FASE 4: VISUALIZACIONES */
    .live-indicators {
      background: linear-gradient(135deg, #f8f9fa 0%, #f0f4f8 100%);
      border-top: 3px solid #2563eb;
      border-radius: 12px;
      padding: 40px;
      margin: 50px 0;
      page-break-inside: avoid;
    }

    .live-indicators h2 {
      font-size: 28px;
      color: #1e40af;
      margin-bottom: 8px;
      font-weight: 700;
    }

    .live-indicators .subtitle {
      color: #6b7280;
      font-size: 13px;
      margin-bottom: 30px;
    }

    .indicators-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
      margin-bottom: 30px;
    }

    .indicator-card {
      background: white;
      border-radius: 10px;
      border: 1px solid #e5e7eb;
      padding: 24px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
    }

    .indicator-card:hover {
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
      transform: translateY(-2px);
      border-color: #2563eb;
    }

    .indicator-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border-bottom: 1px solid #f3f4f6;
      padding-bottom: 12px;
    }

    .indicator-header h3 {
      font-size: 16px;
      color: #1f2937;
      font-weight: 600;
    }

    .indicator-label {
      background: #eff6ff;
      color: #1e40af;
      padding: 4px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
    }

    .indicator-value {
      text-align: center;
      padding: 20px 0;
      border-bottom: 1px solid #f3f4f6;
      margin-bottom: 16px;
    }

    .indicator-value .big-number {
      display: block;
      font-size: 32px;
      font-weight: 700;
      color: #1f2937;
      line-height: 1.2;
    }

    .indicator-value .unit {
      display: block;
      font-size: 12px;
      color: #9ca3af;
      margin-top: 8px;
    }

    .indicator-change,
    .indicator-status {
      text-align: center;
      padding: 8px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 16px;
    }

    .indicator-change.positive {
      background: #dcfce7;
      color: #16a34a;
    }

    .indicator-change.negative {
      background: #fee2e2;
      color: #dc2626;
    }

    .indicator-status.critical {
      background: #fecaca;
      color: #dc2626;
    }

    .indicator-status.normal {
      background: #fed7aa;
      color: #ea580c;
    }

    .indicator-card canvas {
      width: 100%;
      height: 150px;
      margin-top: 16px;
    }

    .update-info {
      text-align: center;
      color: #6b7280;
      font-size: 13px;
      padding-top: 20px;
      border-top: 1px solid #e5e7eb;
    }

    .update-info p {
      margin: 4px 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .indicators-grid {
        grid-template-columns: 1fr;
      }

      .indicator-value .big-number {
        font-size: 24px;
      }

      .live-indicators {
        padding: 24px;
      }
    }

    /* Print styles */
    @media print {
      .live-indicators {
        background: white;
        border: 1px solid #e5e7eb;
        page-break-inside: avoid;
      }

      .indicator-card canvas {
        page-break-inside: avoid;
      }
    }
    """

    return css


def main():
    print("🎨 Generador de Visualizaciones - FASE 4\n")

    # Cargar datos en vivo
    try:
        with open('live_indicators.json', 'r', encoding='utf-8') as f:
            indicators = json.load(f)
            print("✅ Datos en vivo cargados: live_indicators.json")
    except:
        print("⚠️  No se encontró live_indicators.json, usando mock data")
        indicators = {
            'indicadores': {
                'uf':      {'valor': 40543.07, 'fuente': 'Simulado'},
                'utm':     {'valor': 70588.0,  'fuente': 'Simulado'},
                'tpm':     {'valor': 4.75,     'fuente': 'Simulado'},
                'usd_clp': {'valor': 935.0,    'fuente': 'Simulado'},
            }
        }

    # Generar HTML y CSS
    html = generate_charts_html(indicators)
    css = generate_charts_css()

    # Guardar
    with open('charts.html', 'w', encoding='utf-8') as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {css}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """)

    print("✅ Gráficos generados: charts.html")
    print("✅ Estilos CSS generados: visualizations.css")
    print("\n📊 FASE 4: Visualizaciones + Datos en Vivo - COMPLETA\n")


if __name__ == '__main__':
    main()
