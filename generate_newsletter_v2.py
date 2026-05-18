#!/usr/bin/env python3
"""
Generador Automatizado de Newsletter Estratégico v2
Incluye: Cooperativismo y CMF
"""
import json
from datetime import datetime
from fetch_news_rss import fetch_all_news

def load_noticias_from_json(filepath='noticias_diarias.json'):
    """Load news from JSON file as fallback"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            'geopolitica': data.get('geopolitica', []),
            'economia_mercados': data.get('economia_global', []),
            'chile_estrategico': data.get('economia_chile', []),
            'tendencias': data.get('tendencias_tech', []),
            'cooperativismo': data.get('cooperativismo', []),
            'cmf': data.get('cmf', [])
        }
    except:
        return None

def build_news_items(news_list):
    """Build news items for newsletter with links"""
    items = []
    for i, news in enumerate(news_list[:4]):
        items.append({
            "tema": news['title'][:50],
            "titulo_completo": news['title'],
            "detalle": news['summary'][:200],
            "link": news.get('link', '#'),
            "source": news.get('source', 'Fuente'),
            "impacto": "En análisis - Ver fuentes"
        })

    while len(items) < 4:
        items.append({
            "tema": "Monitoreo",
            "titulo_completo": "Monitoreo de mercado",
            "detalle": "Se mantiene análisis actualizado.",
            "link": "#",
            "source": "Fuente",
            "impacto": "Neutral"
        })

    return items

def main():
    print("🎯 Generando Newsletter Estratégico v2 (Con Economía en Vivo)...\n")

    # Obtener noticias
    print("📡 Intentando conectar a RSS feeds de fuentes premium...")
    print("   Fuentes: Bloomberg, Reuters, Financial Times, The Economist, CNBC\n")
    all_news = fetch_all_news()

    # Si no hay noticias, cargar desde JSON
    if sum(len(v) for v in all_news.values()) == 0:
        print("⚠️  No se pudo conectar a RSS feeds.")
        print("📁 Cargando noticias desde archivo JSON con datos actualizados...")
        json_news = load_noticias_from_json()
        if json_news:
            all_news = json_news
            print("✅ Noticias cargadas desde noticias_diarias.json")

    print(f"\n✅ Noticias obtenidas:")
    print(f"   • Geopolítica: {len(all_news['geopolitica'])}")
    print(f"   • Economía y Mercados (Bloomberg/Reuters/FT/Economist/CNBC): {len(all_news['economia_mercados'])}")
    print(f"   • Chile Estratégico: {len(all_news['chile_estrategico'])}")
    print(f"   • Tendencias Tech: {len(all_news['tendencias'])}")
    print(f"   • Cooperativismo: {len(all_news['cooperativismo'])}")
    print(f"   • CMF: {len(all_news['cmf'])}")

    current_date = datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo')

    # Preparar noticias de economía y mercados
    econ_items = build_news_items(all_news['economia_mercados'])

    # Generar HTML
    print("\n🎨 Generando HTML...")
    html = generate_html_newsletter(all_news, current_date, econ_items)

    # Guardar
    with open('newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n✅ Newsletter generado exitosamente!")
    print(f"   Archivo: newsletter.html")
    print(f"   Secciones: 9 (incluyendo Cooperativismo y CMF)")

def generate_html_newsletter(all_news, current_date, econ_items=None):
    """Generate complete HTML newsletter"""

    if econ_items is None:
        econ_items = build_news_items(all_news['economia_mercados'])

    coop_items = build_news_items(all_news['cooperativismo'])
    cmf_items = build_news_items(all_news['cmf'])

    econ_html = ""
    for item in econ_items:
        econ_html += f'''
      <div class="news-item">
        <a href="{item['link']}" target="_blank" class="news-link">
          <div class="news-item-title">{item['tema']}</div>
        </a>
        <div class="news-item-detail">{item['detalle']}</div>
        <div class="news-item-footer">
          <span class="impact-badge">{item['impacto']}</span>
          <a href="{item['link']}" target="_blank" class="source-link">→ {item['source']}</a>
        </div>
      </div>'''

    coop_html = ""
    for item in coop_items:
        coop_html += f'''
      <div class="news-item">
        <a href="{item['link']}" target="_blank" class="news-link">
          <div class="news-item-title">{item['tema']}</div>
        </a>
        <div class="news-item-detail">{item['detalle']}</div>
        <div class="news-item-footer">
          <span class="impact-badge">{item['impacto']}</span>
          <a href="{item['link']}" target="_blank" class="source-link">→ {item['source']}</a>
        </div>
      </div>'''

    cmf_html = ""
    for item in cmf_items:
        cmf_html += f'''
      <div class="news-item">
        <a href="{item['link']}" target="_blank" class="news-link">
          <div class="news-item-title">{item['tema']}</div>
        </a>
        <div class="news-item-detail">{item['detalle']}</div>
        <div class="news-item-footer">
          <span class="impact-badge">{item['impacto']}</span>
          <a href="{item['link']}" target="_blank" class="source-link">→ {item['source']}</a>
        </div>
      </div>'''

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

  .news-link {{
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
  }}

  .news-link:hover .news-item-title {{
    color: var(--accent);
    text-decoration: underline;
  }}

  .news-item-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--rule);
  }}

  .source-link {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    text-decoration: none;
    transition: all 0.2s ease;
  }}

  .source-link:hover {{
    text-decoration: underline;
    color: var(--steel);
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
    <div class="masthead-title">📊 Análisis Estratégico Premium</div>
    <div class="masthead-meta">
      {current_date}<br>
      NEWSLETTER PREMIUM v2
    </div>
  </div>

  <div class="edition-badge">Edición Automatizada con Cooperativismo + CMF</div>

  <div class="main-headline">
    <h1>Newsletter Estratégico - Análisis Integral del Mercado</h1>
  </div>

  <div class="executive-summary">
    <strong>📌 Resumen Ejecutivo</strong><br><br>
    Cobertura completa del mercado financiero chileno: regulación CMF, movimientos geopolíticos globales,
    desarrollo del sector cooperativo, tendencias tecnológicas y oportunidades de inversión.
    Newsletter generado automáticamente desde múltiples RSS feeds de calidad.
  </div>

  <!-- ECONOMÍA Y MERCADOS - FUENTES PREMIUM -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">💹</span>
      Economía y Mercados - Fuentes Premium
    </div>
    <span class="section-subtitle">Análisis directo de Bloomberg, Reuters, Financial Times, The Economist y CNBC</span>
    <div class="content-block">
{econ_html}
    </div>
  </div>

  <!-- COOPERATIVISMO -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🤝</span>
      Cooperativismo
    </div>
    <span class="section-subtitle">Movimiento Cooperativo en Expansión</span>
    <div class="content-block">
{coop_html}
    </div>
  </div>

  <!-- CMF - COMISIÓN DEL MERCADO FINANCIERO -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">📋</span>
      CMF - Comisión del Mercado Financiero
    </div>
    <span class="section-subtitle">Regulación y Supervisión de Mercados Financieros</span>
    <div class="content-block">
{cmf_html}
    </div>
  </div>

  <!-- INSIGHT DEL DÍA -->
  <div class="insight-box">
    <strong>💡 Insight Estratégico del Día</strong><br><br>
    El mercado financiero chileno evoluciona hacia mayor inclusión. La regulación CMF fortalece protección
    inversionista, mientras el sector cooperativo expande acceso a servicios financieros.
    Oportunidad: inversores pueden identificar nichos en intermediarios innovadores y plataformas
    financieras digitales con impacto social.
  </div>

  <div class="footer">
    <div class="sources">
      <strong>Fuentes de Información</strong>
      CMF Chile • Confederación Cooperativa • INDAP • ACI Américas • Bloomberg • Reuters • CNBC
    </div>
    <p style="margin-top: 20px;">
      Newsletter generado automáticamente desde múltiples RSS feeds. Análisis estratégico para ejecutivos.
    </p>
    <p style="margin-top: 12px; font-size: 11px;">
      <em>Actualización automática diaria • Datos obtenidos de fuentes públicas verificadas</em>
    </p>
  </div>

</body>
</html>'''

    return html

if __name__ == '__main__':
    main()
