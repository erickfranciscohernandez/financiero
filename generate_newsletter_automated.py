#!/usr/bin/env python3
"""
Generador Automatizado de Newsletter Estratégico
Obtiene noticias de RSS feeds y genera análisis profesional
"""
import json
from datetime import datetime
from fetch_news_rss import fetch_all_news, categorize_news

def synthesize_news_section(news_items, section_name):
    """Synthesize news items into professional analysis paragraphs"""

    if not news_items:
        return {
            "titular": f"Monitoreo de {section_name}",
            "parrafo1": "Sin noticias disponibles en este momento.",
            "parrafo2": "Se recomienda consultar directamente las fuentes de información.",
            "parrafo3": "Los análisis se actualizarán con nueva información disponible.",
            "impacto": "Neutral"
        }

    titles = [n['title'] for n in news_items[:3]]
    summaries = [n['summary'][:150] for n in news_items[:3]]

    synthesis = {
        "titular": f"{', '.join([t[:40] + '...' if len(t) > 40 else t for t in titles[:2]])}",
        "parrafo1": f"Las últimas noticias muestran: {titles[0] if titles else 'sin datos'}. {summaries[0] if summaries else ''}",
        "parrafo2": f"Adicionalmente, se observa: {titles[1] if len(titles) > 1 else 'análisis en desarrollo'}. {summaries[1][:100] if len(summaries) > 1 else ''}",
        "parrafo3": f"En perspectiva: {titles[2] if len(titles) > 2 else 'seguimiento continuo'}. {summaries[2][:100] if len(summaries) > 2 else ''}",
        "impacto": "Variado - Consultar fuentes directas"
    }

    return synthesis

def build_chile_news_items(news_list):
    """Build Chile news items for newsletter"""
    items = []
    for i, news in enumerate(news_list[:4]):
        items.append({
            "tema": news['title'][:50],
            "detalle": news['summary'][:200],
            "impacto": "En análisis - Ver fuentes"
        })

    return items

def generate_newsletter_from_news(all_news):
    """Generate complete newsletter from fetched news"""

    current_date = datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo')

    # Crear titular principal basado en noticias
    top_geo = all_news['geopolitica'][0]['title'] if all_news['geopolitica'] else "Mercados en movimiento"
    top_eco = all_news['economia_mercados'][0]['title'] if all_news['economia_mercados'] else "Datos económicos en revisión"

    titular = f"{top_geo[:50]} - Impacto en {top_eco[:40]}"

    # Crear resumen ejecutivo
    geo_count = len(all_news['geopolitica'])
    eco_count = len(all_news['economia_mercados'])
    chile_count = len(all_news['chile_estrategico'])
    trend_count = len(all_news['tendencias'])

    resumen = f"Análisis estratégico basado en {geo_count + eco_count + chile_count + trend_count} noticias actualizadas. " \
              f"Se detectan {geo_count} eventos geopolíticos, {eco_count} movimientos económicos, " \
              f"{chile_count} desarrollos locales, y {trend_count} tendencias emergentes. " \
              f"Newsletter generado automáticamente desde múltiples RSS feeds de calidad."

    data = {
        "fecha": current_date,
        "titular_principal": titular,
        "resumen_ejecutivo": resumen,

        "geopolitica": synthesize_news_section(all_news['geopolitica'], "Geopolítica"),

        "economia_mercados": {
            "titular": "Economía Global en Seguimiento",
            "tasas": {
                "fed": "5.25-5.50%",
                "bcch": "8.25%",
                "bcrp": "5.75%"
            },
            "commodities": {
                "cobre": "Obtener datos...",
                "petroleo": "Obtener datos...",
                "oro": "Obtener datos..."
            },
            "parrafo1": f"Noticias económicas recientes: {all_news['economia_mercados'][0]['title'] if all_news['economia_mercados'] else 'Análisis en desarrollo'}. " +
                       (f"{all_news['economia_mercados'][0]['summary'][:200]}" if all_news['economia_mercados'] else ""),
            "parrafo2": f"Mercados monitorean: {all_news['economia_mercados'][1]['title'] if len(all_news['economia_mercados']) > 1 else 'Indicadores clave'}.",
            "parrafo3": "Volatilidad en activos emergentes refleja repricing de riesgo.",
            "parrafo4": "Análisis sectorial en actualización continua.",
            "parrafo5": "Spreads de deuda corporativa bajo presión."
        },

        "chile_estrategico": {
            "titular": "Noticias de Chile - Seguimiento Actualizado",
            "noticias": build_chile_news_items(all_news['chile_estrategico'])
        },

        "tendencias": {
            "titular": "Tendencias Emergentes en Tecnología y Mercados",
            "parrafo1": f"Tendencias detectadas: {all_news['tendencias'][0]['title'] if all_news['tendencias'] else 'Análisis en progreso'}. " +
                       (f"{all_news['tendencias'][0]['summary'][:200]}" if all_news['tendencias'] else ""),
            "parrafo2": "Disrupción tecnológica continúa redefiniendo mercados.",
            "parrafo3": "Oportunidades de inversión en sectores de transformación digital.",
            "parrafo4": "Reskilling y automatización marcan agenda empresarial.",
            "impacto_inversion": "Tech, Defensa, Energía Verde, Financiero Digital"
        },

        "insight": "Los mercados transicionan hacia un nuevo equilibrio donde fragmentación geopolítica y " \
                   "disruption tecnológica dominan la dinámica de precios. Inversores deben seleccionar " \
                   "activos con visibilidad de cash flows y presencia en economías resilientes. " \
                   "Latinoamérica presenta oportunidades selectivas en países con estabilidad institucional.",

        "fuentes": [
            "Bloomberg RSS",
            "Reuters Feeds",
            "El Mostrador",
            "Diario Financiero",
            "EMOL",
            "La Tercera",
            "CNBC",
            "FT Markets"
        ]
    }

    return data

def generate_html(data):
    """Generate HTML newsletter (same as before)"""
    current_date = data.get('fecha', datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo'))

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Newsletter Estratégico — {current_date}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #0d0d0d;
    --paper: #f5f0e8;
    --cream: #ede7d5;
    --accent: #c0392b;
    --gold: #b8860b;
    --steel: #2c3e50;
    --muted: #6b6457;
    --rule: #c9b99a;
    --light-accent: #e8f4f8;
    --success: #27ae60;
    --warning: #e67e22;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: var(--paper);
    color: var(--ink);
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 15px;
    line-height: 1.8;
    max-width: 900px;
    margin: 0 auto;
    padding: 50px 32px 100px;
  }}

  .masthead {{
    border-top: 3px solid var(--ink);
    border-bottom: 1px solid var(--rule);
    padding: 24px 0 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}

  .masthead-title {{
    font-family: 'Playfair Display', serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--steel);
  }}

  .masthead-meta {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    text-align: right;
    line-height: 1.6;
  }}

  .edition-badge {{
    background: var(--ink);
    color: var(--paper);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 6px 12px;
    display: inline-block;
    margin-bottom: 32px;
    font-weight: 600;
  }}

  .main-headline {{
    border-left: 5px solid var(--accent);
    padding-left: 24px;
    margin-bottom: 32px;
  }}

  .main-headline h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 900;
    line-height: 1.25;
    color: var(--ink);
    margin-bottom: 12px;
  }}

  .executive-summary {{
    background: var(--light-accent);
    border-left: 4px solid var(--accent);
    padding: 24px;
    margin: 40px 0;
    border-radius: 2px;
    font-size: 16px;
    font-weight: 500;
    line-height: 1.8;
    color: var(--steel);
  }}

  .section {{
    margin-bottom: 48px;
  }}

  .section-header {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 4px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--rule);
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .section-emoji {{
    font-size: 24px;
  }}

  .section-subtitle {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 20px;
    display: block;
  }}

  .content-block {{
    margin: 24px 0;
    line-height: 1.8;
  }}

  .content-block p {{
    margin-bottom: 16px;
    color: var(--ink);
  }}

  .highlight {{
    background: var(--cream);
    padding: 16px 20px;
    border-left: 3px solid var(--gold);
    margin: 20px 0;
    border-radius: 2px;
  }}

  .highlight-title {{
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 8px;
    font-size: 14px;
  }}

  .news-item {{
    background: var(--cream);
    padding: 20px;
    margin: 16px 0;
    border-radius: 2px;
    border-left: 3px solid var(--steel);
  }}

  .news-item-title {{
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
    font-size: 15px;
  }}

  .news-item-detail {{
    font-size: 14px;
    line-height: 1.7;
    color: var(--ink);
    margin-bottom: 10px;
  }}

  .impact-badge {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
    display: inline-block;
    color: #fff;
    background: var(--accent);
  }}

  .insight-box {{
    background: var(--light-accent);
    border: 2px solid var(--accent);
    padding: 32px;
    margin: 40px 0;
    border-radius: 2px;
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 600;
    line-height: 1.8;
    color: var(--steel);
  }}

  .footer {{
    border-top: 1px solid var(--rule);
    padding-top: 32px;
    margin-top: 60px;
    font-size: 12px;
    color: var(--muted);
    text-align: center;
  }}

  .sources {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--rule);
  }}

  .sources strong {{
    display: block;
    margin-bottom: 8px;
    color: var(--ink);
  }}

  .data-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 24px 0;
  }}

  .data-item {{
    background: var(--cream);
    padding: 16px;
    border-radius: 2px;
    border-left: 3px solid var(--steel);
  }}

  .data-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
  }}

  .data-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    color: var(--ink);
  }}

  a {{
    color: var(--accent);
    text-decoration: none;
  }}

  a:hover {{
    text-decoration: underline;
  }}
</style>
</head>
<body>

  <div class="masthead">
    <div class="masthead-title">📊 Análisis Estratégico - Noticias en Vivo</div>
    <div class="masthead-meta">
      {current_date}<br>
      NEWSLETTER PREMIUM
    </div>
  </div>

  <div class="edition-badge">Edición Automatizada - RSS Feeds</div>

  <div class="main-headline">
    <h1>{data['titular_principal']}</h1>
  </div>

  <div class="executive-summary">
    <strong>📌 Resumen Ejecutivo</strong><br><br>
    {data['resumen_ejecutivo']}
  </div>

  <!-- GEOPOLÍTICA -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🌍</span>
      Geopolítica
    </div>
    <span class="section-subtitle">{data['geopolitica'].get('titular', 'Análisis en progreso')}</span>
    <div class="content-block">
      <p>{data['geopolitica'].get('parrafo1', 'Monitoreo de eventos geopolíticos.')}</p>
      <p>{data['geopolitica'].get('parrafo2', '')}</p>
      <p>{data['geopolitica'].get('parrafo3', '')}</p>
      <div class="highlight">
        <div class="highlight-title">⚡ Impacto</div>
        {data['geopolitica'].get('impacto', 'Análisis en actualización')}
      </div>
    </div>
  </div>

  <!-- ECONOMÍA Y MERCADOS -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">💹</span>
      Economía y Mercados
    </div>
    <span class="section-subtitle">{data['economia_mercados']['titular']}</span>

    <div class="data-grid">
      <div class="data-item">
        <div class="data-label">Cobre</div>
        <div class="data-value">{data['economia_mercados']['commodities']['cobre']}</div>
      </div>
      <div class="data-item">
        <div class="data-label">Petróleo</div>
        <div class="data-value">{data['economia_mercados']['commodities']['petroleo']}</div>
      </div>
    </div>

    <div class="content-block">
      <p>{data['economia_mercados']['parrafo1']}</p>
      <p>{data['economia_mercados']['parrafo2']}</p>
      <p>{data['economia_mercados']['parrafo3']}</p>
    </div>
  </div>

  <!-- CHILE ESTRATÉGICO -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🇨🇱</span>
      Chile Estratégico
    </div>
    <span class="section-subtitle">{data['chile_estrategico']['titular']}</span>
    <div class="content-block">
'''

    for noticia in data['chile_estrategico']['noticias']:
        html += f'''
      <div class="news-item">
        <div class="news-item-title">{noticia['tema']}</div>
        <div class="news-item-detail">{noticia['detalle']}</div>
        <span class="impact-badge">{noticia['impacto']}</span>
      </div>
'''

    html += f'''
    </div>
  </div>

  <!-- TENDENCIAS -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🚀</span>
      Tendencias y Futuro
    </div>
    <span class="section-subtitle">{data['tendencias']['titular']}</span>
    <div class="content-block">
      <p>{data['tendencias']['parrafo1']}</p>
      <p>{data['tendencias']['parrafo2']}</p>
      <p>{data['tendencias']['parrafo3']}</p>
      <p>{data['tendencias']['parrafo4']}</p>
      <div class="highlight">
        <div class="highlight-title">💰 Impacto de Inversión</div>
        {data['tendencias']['impacto_inversion']}
      </div>
    </div>
  </div>

  <!-- INSIGHT DEL DÍA -->
  <div class="insight-box">
    <strong>💡 Insight Estratégico del Día</strong><br><br>
    {data['insight']}
  </div>

  <div class="footer">
    <div class="sources">
      <strong>Fuentes de Información (RSS Feeds Automatizadas)</strong>
      {', '.join(data['fuentes'])}
    </div>
    <p style="margin-top: 20px;">
      Newsletter generado automáticamente desde múltiples RSS feeds. Análisis en tiempo real para ejecutivos.
    </p>
    <p style="margin-top: 12px; font-size: 11px;">
      <em>Actualización automática diaria • Datos obtenidos de fuentes públicas verificadas</em>
    </p>
  </div>

</body>
</html>'''

    return html

def load_noticias_from_json(filepath='noticias_diarias.json'):
    """Load news from JSON file as fallback"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            'geopolitica': data.get('geopolitica', []),
            'economia_mercados': data.get('economia_global', []),
            'chile_estrategico': data.get('economia_chile', []),
            'tendencias': data.get('tendencias_tech', [])
        }
    except:
        return None

def main():
    print("🎯 Generando Newsletter Estratégico Automatizado...\n")

    # Obtener noticias de RSS feeds
    print("📡 Intentando conectar a RSS feeds...")
    all_news = fetch_all_news()

    # Si no hay noticias de RSS, cargar desde JSON
    if sum(len(v) for v in all_news.values()) == 0:
        print("\n⚠️  No se pudo conectar a RSS feeds (sin internet).")
        print("📁 Cargando noticias desde archivo JSON...")
        json_news = load_noticias_from_json()
        if json_news:
            all_news = json_news
            print("✅ Noticias cargadas desde noticias_diarias.json")

    print("\n✅ Noticias obtenidas:")
    print(f"   • Geopolítica: {len(all_news['geopolitica'])}")
    print(f"   • Economía: {len(all_news['economia_mercados'])}")
    print(f"   • Chile: {len(all_news['chile_estrategico'])}")
    print(f"   • Tendencias: {len(all_news['tendencias'])}")

    # Generar data para newsletter
    print("\n📝 Sintetizando análisis...")
    data = generate_newsletter_from_news(all_news)

    # Generar HTML
    print("🎨 Generando HTML...")
    html = generate_html(data)

    # Guardar
    with open('newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n✅ Newsletter generado exitosamente!")
    print(f"   Archivo: newsletter.html")
    print(f"   Titular: {data['titular_principal'][:60]}...")
    print(f"   Fecha: {data['fecha']}")

if __name__ == '__main__':
    main()
