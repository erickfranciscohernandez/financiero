#!/usr/bin/env python3
"""
Newsletter Estratégico Avanzado v3
Incluye: Análisis inteligente, visualizaciones, dashboard, alertas
"""
import json
from datetime import datetime
from fetch_news_rss import fetch_all_news

def load_noticias_from_json(filepath='noticias_diarias.json'):
    """Load news from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            'geopolitica': data.get('geopolitica', []),
            'economia_mercados': data.get('economia_global', []),
            'chile_estrategico': data.get('economia_chile', []),
            'tendencias': data.get('tendencias_tech', []),
            'cooperativismo': data.get('cooperativismo', []),
            'cmf': data.get('cmf', []),
            'noticias_economicas': data.get('noticias_economicas_actuales', []),
            'ia': data.get('inteligencia_artificial', [])
        }
    except:
        return None

def analyze_news_importance(title, summary):
    """Analyze importance/impact score of news (1-10)"""
    high_impact_keywords = [
        'crisis', 'colapso', 'récord', 'máximo', 'mínimo', 'emergencia',
        'regulación', 'sanciones', 'reforma', 'inversión masiva', 'acuerdo histórico',
        'advertencia', 'riesgo', 'oportunidad', 'revolución', 'transformación',
        'china', 'ee.uu', 'fed', 'bce', 'bcrp', 'bcch', 'cobre', 'litio'
    ]

    medium_keywords = [
        'cambio', 'aumenta', 'disminuye', 'sube', 'baja', 'variación',
        'analista', 'experto', 'estimación', 'proyección', 'crecimiento'
    ]

    text = (title + ' ' + summary).lower()

    score = 5  # Base score

    # High impact keywords +3
    for keyword in high_impact_keywords:
        if keyword in text:
            score += 3

    # Medium impact keywords +1
    for keyword in medium_keywords:
        if keyword in text:
            score += 1

    # Cap at 10
    return min(score, 10)

def build_news_items_advanced(news_list):
    """Build news items with importance scoring"""
    items = []
    for i, news in enumerate(news_list[:4]):
        importance = analyze_news_importance(news['title'], news['summary'])

        # Determine impact badge color
        if importance >= 8:
            impact_level = "🔴 Crítico"
        elif importance >= 6:
            impact_level = "🟠 Alto"
        elif importance >= 4:
            impact_level = "🟡 Medio"
        else:
            impact_level = "🟢 Bajo"

        items.append({
            "tema": news['title'][:50],
            "titulo_completo": news['title'],
            "detalle": news['summary'][:200],
            "link": news.get('link', '#'),
            "source": news.get('source', 'Fuente'),
            "impacto": impact_level,
            "score": importance
        })

    while len(items) < 4:
        items.append({
            "tema": "Monitoreo",
            "titulo_completo": "Monitoreo de mercado",
            "detalle": "Se mantiene análisis actualizado.",
            "link": "#",
            "source": "Fuente",
            "impacto": "🟢 Bajo",
            "score": 3
        })

    return items

def generate_alerts(all_news):
    """Generate critical alerts from news"""
    alerts = []

    for section, news_list in all_news.items():
        for news in news_list[:2]:  # Check top 2 per section
            score = analyze_news_importance(news['title'], news['summary'])
            if score >= 8:
                alerts.append({
                    'section': section,
                    'title': news['title'],
                    'score': score,
                    'link': news.get('link', '#')
                })

    return sorted(alerts, key=lambda x: x['score'], reverse=True)[:5]

def main():
    print("🎯 Generando Newsletter Estratégico v3 (Análisis Inteligente)...\n")

    print("📡 Intentando conectar a RSS feeds...")
    all_news = fetch_all_news()

    if sum(len(v) for v in all_news.values()) == 0:
        print("⚠️  No se pudo conectar a RSS feeds.")
        print("📁 Cargando noticias desde JSON...")
        json_news = load_noticias_from_json()
        if json_news:
            all_news = json_news
            print("✅ Noticias cargadas\n")

    # Generar alertas críticas
    print("🚨 Analizando importancia de noticias...")
    alerts = generate_alerts(all_news)
    print(f"✅ {len(alerts)} alertas críticas detectadas\n")

    # Preparar todos los items con scoring
    print("📊 Preparando análisis...\n")

    econ_items = build_news_items_advanced(all_news['economia_mercados'])
    econ_actuales = build_news_items_advanced(all_news.get('noticias_economicas', []))
    ia_items = build_news_items_advanced(all_news.get('ia', []))
    coop_items = build_news_items_advanced(all_news['cooperativismo'])
    cmf_items = build_news_items_advanced(all_news['cmf'])
    geo_items = build_news_items_advanced(all_news['geopolitica'])
    chile_items = build_news_items_advanced(all_news['chile_estrategico'])

    current_date = datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo')

    print("🎨 Generando HTML avanzado...")
    html = generate_html_advanced(
        all_news, current_date,
        econ_items, econ_actuales, ia_items,
        coop_items, cmf_items, geo_items, chile_items,
        alerts
    )

    with open('newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n✅ Newsletter v3 generado exitosamente!")
    print(f"   • Secciones: 11+")
    print(f"   • Noticias analizadas: {sum(len(v) for v in all_news.values())}")
    print(f"   • Alertas críticas: {len(alerts)}")
    print(f"   • Scoring de impacto: Activado")
    print(f"   • Dashboard: Incluido")
    print(f"   • Búsqueda: Interactiva")

def generate_html_advanced(all_news, current_date, econ_items, econ_actuales, ia_items,
                           coop_items, cmf_items, geo_items, chile_items, alerts):
    """Generate advanced HTML with all features"""

    # Generar HTML de items
    def items_to_html(items):
        html = ""
        for item in items:
            html += f'''
      <div class="news-item" data-score="{item['score']}" data-title="{item['titulo_completo'].lower()}">
        <div class="score-badge" title="Score de importancia: {item['score']}/10">{item['score']}/10</div>
        <a href="{item['link']}" target="_blank" class="news-link">
          <div class="news-item-title">{item['tema']}</div>
        </a>
        <div class="news-item-detail">{item['detalle']}</div>
        <div class="news-item-footer">
          <span class="impact-badge">{item['impacto']}</span>
          <a href="{item['link']}" target="_blank" class="source-link">→ {item['source']}</a>
        </div>
      </div>'''
        return html

    econ_html = items_to_html(econ_items)
    econ_actuales_html = items_to_html(econ_actuales)
    ia_html = items_to_html(ia_items)
    coop_html = items_to_html(coop_items)
    cmf_html = items_to_html(cmf_items)
    geo_html = items_to_html(geo_items)
    chile_html = items_to_html(chile_items)

    # Generar alertas HTML
    alerts_html = ""
    if alerts:
        for alert in alerts[:5]:
            alerts_html += f'''
    <div class="alert-item alert-critical">
      <div class="alert-score">⚠️ {alert['score']}/10</div>
      <a href="{alert['link']}" target="_blank" class="alert-link">
        {alert['title'][:70]}...
      </a>
    </div>'''

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Newsletter Estratégico Premium v3 — {current_date}</title>
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
    --critical: #d32f2f;
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

  .v3-badge {{
    background: linear-gradient(135deg, var(--accent) 0%, var(--warning) 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 20px;
    font-size: 12px;
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

  /* ALERTS SECTION */
  .alerts-section {{
    background: #ffebee;
    border: 2px solid var(--critical);
    border-radius: 2px;
    padding: 24px;
    margin: 40px 0;
  }}

  .alerts-header {{
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--critical);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .alert-item {{
    background: white;
    border-left: 4px solid var(--critical);
    padding: 12px 16px;
    margin-bottom: 8px;
    border-radius: 2px;
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .alert-score {{
    font-weight: 700;
    color: var(--critical);
    font-size: 14px;
    min-width: 50px;
  }}

  .alert-link {{
    color: var(--critical);
    text-decoration: none;
    font-weight: 600;
    flex: 1;
  }}

  .alert-link:hover {{
    text-decoration: underline;
  }}

  /* SEARCH BOX */
  .search-box {{
    background: var(--cream);
    border: 2px solid var(--rule);
    border-radius: 2px;
    padding: 16px;
    margin: 32px 0;
    display: flex;
    gap: 10px;
  }}

  .search-input {{
    flex: 1;
    padding: 10px 12px;
    border: 1px solid var(--rule);
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
  }}

  .search-input:focus {{
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(192, 57, 43, 0.1);
  }}

  .search-button {{
    background: var(--accent);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 2px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
  }}

  .search-button:hover {{
    background: #a02f23;
  }}

  /* SCORE BADGE */
  .score-badge {{
    background: linear-gradient(135deg, #ffeb3b 0%, #ffc107 100%);
    color: #333;
    font-weight: 700;
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace;
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
    transition: all 0.2s;
  }}

  .news-item:hover {{
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateX(4px);
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

  .news-item-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--rule);
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

  @media print {{
    body {{ padding: 20px; }}
    .search-box {{ display: none; }}
    .alerts-section {{ page-break-inside: avoid; }}
  }}
</style>
<script>
function searchNews() {{
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  const newsItems = document.querySelectorAll('.news-item');

  newsItems.forEach(item => {{
    const title = item.getAttribute('data-title');
    if (searchTerm === '' || title.includes(searchTerm)) {{
      item.style.display = 'block';
    }} else {{
      item.style.display = 'none';
    }}
  }});
}}

function filterByScore(minScore) {{
  const newsItems = document.querySelectorAll('.news-item');
  newsItems.forEach(item => {{
    const score = parseInt(item.getAttribute('data-score'));
    if (score >= minScore) {{
      item.style.display = 'block';
    }} else {{
      item.style.display = 'none';
    }}
  }});
}}

function sortByScore(order = 'desc') {{
  const container = document.querySelector('.content-block');
  const items = Array.from(document.querySelectorAll('.news-item'));

  items.sort((a, b) => {{
    const scoreA = parseInt(a.getAttribute('data-score'));
    const scoreB = parseInt(b.getAttribute('data-score'));
    return order === 'desc' ? scoreB - scoreA : scoreA - scoreB;
  }});

  items.forEach(item => container.appendChild(item));
}}
</script>
</head>
<body>

  <div class="masthead">
    <div class="masthead-title">📊 Newsletter Premium v3</div>
    <div class="masthead-meta">
      {current_date}<br>
      ANÁLISIS INTELIGENTE
    </div>
  </div>

  <div class="v3-badge">✨ Versión 3.0 - Análisis Inteligente + Dashboard</div>

  <div class="main-headline">
    <h1>Newsletter Estratégico Premium - Análisis en Vivo</h1>
  </div>

  <div class="executive-summary">
    <strong>📌 Resumen Ejecutivo v3</strong><br><br>
    Análisis inteligente con scoring de impacto. Dashboard ejecutivo con alertas críticas.
    Búsqueda interactiva y filtrado por importancia. Noticias categorizadas por relevancia estratégica.
    Sistema completo de inteligencia para tomadores de decisión.
  </div>

  <!-- ALERTAS CRÍTICAS -->
  <div class="alerts-section">
    <div class="alerts-header">
      🚨 ALERTAS CRÍTICAS ({len(alerts)} detectadas)
    </div>
    {alerts_html}
  </div>

  <!-- BUSCADOR -->
  <div class="search-box">
    <input type="text" id="searchInput" class="search-input" placeholder="🔍 Buscar noticias..." onkeyup="searchNews()">
    <button class="search-button" onclick="filterByScore(8)">🔴 Crítico</button>
    <button class="search-button" onclick="filterByScore(6)">🟠 Alto</button>
    <button class="search-button" onclick="sortByScore('desc')">📊 Ordenar</button>
  </div>

  <!-- ECONOMÍA Y MERCADOS -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">💹</span>
      Economía y Mercados - Fuentes Premium
    </div>
    <span class="section-subtitle">Bloomberg, Reuters, Financial Times, The Economist, CNBC</span>
    <div class="content-block">
{econ_html}
    </div>
  </div>

  <!-- NOTICIAS ECONÓMICAS ACTUALES -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">📰</span>
      Noticias Económicas Actuales
    </div>
    <span class="section-subtitle">Indicadores clave y desarrollos económicos</span>
    <div class="content-block">
{econ_actuales_html}
    </div>
  </div>

  <!-- INTELIGENCIA ARTIFICIAL -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🤖</span>
      Inteligencia Artificial - Tendencias
    </div>
    <span class="section-subtitle">TLDR AI, Ben's Bites, The Rundown AI</span>
    <div class="content-block">
{ia_html}
    </div>
  </div>

  <!-- GEOPOLÍTICA -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🌍</span>
      Geopolítica
    </div>
    <span class="section-subtitle">Conflictos, relaciones internacionales, tensiones comerciales</span>
    <div class="content-block">
{geo_html}
    </div>
  </div>

  <!-- CHILE ESTRATÉGICO -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🇨🇱</span>
      Chile Estratégico
    </div>
    <span class="section-subtitle">Gobierno, reformas, empresas, minería, energía</span>
    <div class="content-block">
{chile_html}
    </div>
  </div>

  <!-- COOPERATIVISMO -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">🤝</span>
      Cooperativismo
    </div>
    <span class="section-subtitle">Movimiento cooperativo en expansión</span>
    <div class="content-block">
{coop_html}
    </div>
  </div>

  <!-- CMF -->
  <div class="section">
    <div class="section-header">
      <span class="section-emoji">📋</span>
      CMF - Comisión del Mercado Financiero
    </div>
    <span class="section-subtitle">Regulación y supervisión de mercados financieros</span>
    <div class="content-block">
{cmf_html}
    </div>
  </div>

  <!-- INSIGHT -->
  <div class="insight-box">
    <strong>💡 Insight Estratégico del Día</strong><br><br>
    Mercados operan bajo tensión geopolítica creciente. Sistema de scoring detecta
    {len(alerts)} eventos críticos hoy. Recomendación: concentrar atención en alertas rojas.
    Oportunidades en selectividad sectorial y timing de entrada en activos castigados.
  </div>

  <div class="footer">
    <p style="margin-top: 20px;">
      <strong>Newsletter Estratégico Premium v3</strong> - Análisis automático + Dashboard + Alertas
    </p>
    <p style="margin-top: 12px; font-size: 11px;">
      <em>Actualización automática • Scoring de impacto • Sistema de alertas • Búsqueda interactiva</em>
    </p>
    <div class="sources">
      <strong>Fuentes de Información</strong>
      Bloomberg • Reuters • FT • The Economist • CNBC • CMF Chile • CEPAL • TLDR AI • Ben's Bites • The Rundown AI
    </div>
  </div>

</body>
</html>'''

    return html

if __name__ == '__main__':
    main()
