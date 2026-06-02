#!/usr/bin/env python3
"""
Newsletter Estratégico v4 - FASE 4
Incluye: Análisis inteligente + Visualizaciones + Datos en Vivo + Agenda
"""
import json
import sys
from datetime import datetime
from fetch_news_rss import fetch_all_news
from fetch_live_data import LiveDataFetcher, generate_chart_data
from visualizations import generate_charts_html, generate_charts_css
from generate_agenda import generate_agenda_html, get_agenda_css
from generate_ai_analysis import run_ai_analysis
from fetch_cmf_normativa import generate_normativa_html, get_normativa_css


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
    score = 5

    for keyword in high_impact_keywords:
        if keyword in text:
            score += 3

    for keyword in medium_keywords:
        if keyword in text:
            score += 1

    return min(score, 10)


def build_news_items_advanced(news_list):
    """Build news items with importance scoring"""
    items = []

    # Mostrar todas las noticias disponibles (máximo 4)
    for i, news in enumerate(news_list[:4]):
        importance = analyze_news_importance(news['title'], news['summary'])

        if importance >= 8:
            impact_level = "🔴 Crítico"
        elif importance >= 6:
            impact_level = "🟠 Alto"
        elif importance >= 4:
            impact_level = "🟡 Medio"
        else:
            impact_level = "🟢 Bajo"

        items.append({
            "titulo_completo": news['title'],
            "detalle": news['summary'][:200],
            "link": news.get('link', '#'),
            "source": news.get('source', 'Fuente'),
            "impacto": impact_level,
            "score": importance
        })

    return items


def generate_alerts(all_news):
    """Generate critical alerts from news"""
    alerts = []

    for section, news_list in all_news.items():
        for news in news_list:
            score = analyze_news_importance(news['title'], news['summary'])
            if score >= 8:
                alerts.append({
                    'section': section,
                    'title': news['title'],
                    'summary': news['summary'][:150],
                    'score': score,
                    'source': news.get('source', 'Fuente'),
                    'link': news.get('link', '#')
                })

    return sorted(alerts, key=lambda x: x['score'], reverse=True)[:5]


def fetch_live_indicators():
    """Fetch live economic indicators"""
    print("📊 Obteniendo indicadores macro en vivo...")
    fetcher = LiveDataFetcher()
    indicators = fetcher.get_all_indicators()
    return indicators


def integrate_visualizations_html(indicators_data):
    """Integrate live data visualization into HTML"""
    return generate_charts_html(indicators_data)


def get_visualization_css():
    """Get CSS for visualizations"""
    return generate_charts_css()


def main():
    print("🎯 FASE 4: Newsletter Estratégico v4 (Análisis + Visualizaciones)\n")

    # Step 1: Fetch live data
    print("="*60)
    print("PASO 1: Obteniendo datos en vivo")
    print("="*60)
    indicators = fetch_live_indicators()
    print()

    # Step 2: Fetch news
    print("="*60)
    print("PASO 2: Obteniendo noticias")
    print("="*60)
    print("📡 Intentando conectar a RSS feeds...")
    all_news = fetch_all_news()

    # Complementar con JSON para categorías vacías
    print("📁 Complementando con noticias del JSON...")
    json_news = load_noticias_from_json()
    if json_news:
        for key, items in json_news.items():
            if len(all_news.get(key, [])) < 2:
                all_news[key] = items

    # Respaldo: garantizar mínimo 2 noticias en cada categoría
    try:
        from generate_mock_news import generate_dynamic_news
        mock_news = generate_dynamic_news()
        mock_key_map = {
            'cooperativismo': 'cooperativismo',
            'cmf': 'cmf',
            'noticias_economicas_actuales': 'noticias_economicas',
            'inteligencia_artificial': 'ia',
            'economia_global': 'economia_mercados',
            'economia_chile': 'chile_estrategico',
            'tendencias_tech': 'tendencias',
            'geopolitica': 'geopolitica',
        }
        for mock_key, target_key in mock_key_map.items():
            if len(all_news.get(target_key, [])) < 2 and mock_news.get(mock_key):
                all_news[target_key] = mock_news[mock_key]
                print(f"   ✅ {target_key}: respaldo activado ({len(mock_news[mock_key])} noticias)")
    except Exception as e:
        print(f"   ⚠️  Sin datos de respaldo: {e}")

    print("✅ Noticias listas\n")

    # Step 3: Generate alerts
    print("="*60)
    print("PASO 3: Analizando importancia de noticias")
    print("="*60)
    print("🚨 Analizando...")
    alerts = generate_alerts(all_news)
    print(f"✅ {len(alerts)} alertas críticas detectadas\n")

    # Step 4: Prepare news items
    print("="*60)
    print("PASO 4: Preparando análisis")
    print("="*60)
    econ_items = build_news_items_advanced(all_news.get('economia_mercados', []))
    econ_actuales = build_news_items_advanced(all_news.get('noticias_economicas', []))
    ia_items = build_news_items_advanced(all_news.get('ia', []))
    coop_items = build_news_items_advanced(all_news.get('cooperativismo', []))
    cmf_items = build_news_items_advanced(all_news.get('cmf', []))
    geo_items = build_news_items_advanced(all_news.get('geopolitica', []))
    chile_items = build_news_items_advanced(all_news.get('chile_estrategico', []))
    print("✅ Análisis completo\n")

    # Step 5: Generate HTML with visualizations
    print("="*60)
    print("PASO 5: Generando HTML con visualizaciones")
    print("="*60)

    current_date = datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo')

    # Generate visualizations section
    viz_html = integrate_visualizations_html(indicators)
    viz_css = get_visualization_css()

    # Generate agenda section
    agenda_html = generate_agenda_html()
    agenda_css = get_agenda_css()

    # Generate CMF normativa section
    print('\n🏛️  Obteniendo normativa CMF en consulta...')
    normativa_html = generate_normativa_html()
    normativa_css  = get_normativa_css()

    # Generate old HTML (from v3)
    tendencias_items = build_news_items_advanced(all_news.get('tendencias', []))
    ai_analyses = run_ai_analysis(all_news)
    html_v3 = generate_html_advanced_v4(
        all_news, current_date,
        econ_items, econ_actuales, ia_items,
        coop_items, cmf_items, geo_items, chile_items,
        tendencias_items, alerts, viz_html, viz_css, agenda_html, agenda_css,
        normativa_html=normativa_html, normativa_css=normativa_css,
        ai_analyses=ai_analyses
    )

    with open('newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html_v3)

    # Also save v4-specific version
    with open('newsletter_v4.html', 'w', encoding='utf-8') as f:
        f.write(html_v3)

    print("✅ HTML generado\n")

    # Summary
    print("="*60)
    print("✅ FASE 4 COMPLETADA - Newsletter v4")
    print("="*60)
    print(f"📊 Indicadores macro: 5 visualizaciones")
    print(f"📰 Noticias analizadas: {sum(len(v) for v in all_news.values())}")
    print(f"🚨 Alertas críticas: {len(alerts)}")
    print(f"📈 Scoring de impacto: Activado")
    print(f"📊 Gráficos interactivos: Incluidos")
    print(f"💱 Datos en vivo: Actualizándose cada 4h")
    print("\n📄 Archivos generados:")
    print("   • newsletter.html (versión completa)")
    print("   • newsletter_v4.html (alternativa)")
    print("   • live_indicators.json (datos macro)")


def generate_html_advanced_v4(all_news, current_date, econ_items, econ_actuales, ia_items,
                               coop_items, cmf_items, geo_items, chile_items, tendencias_items, alerts,
                               viz_html, viz_css, agenda_html, agenda_css,
                               normativa_html='', normativa_css='', ai_analyses=None):
    """Generate advanced HTML v4 with visualizations, agenda and Claude AI analysis"""

    def items_to_html(items):
        html = ""
        for item in items:
            html += f'''
      <div class="news-item" data-score="{item['score']}" data-title="{item['titulo_completo'].lower()}">
        <div class="score-badge" title="Score de importancia: {item['score']}/10">{item['score']}/10</div>
        <a href="{item['link']}" target="_blank" class="news-link">
          <div class="news-item-title">{item['titulo_completo']}</div>
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
    tendencias_html = items_to_html(tendencias_items)

    # Alerts section
    alerts_html = ""
    for alert in alerts:
        alerts_html += f'''
    <div class="alert-item" data-score="{alert['score']}">
      <strong>🚨 {alert['title'][:60]}...</strong>
      <p>{alert['summary']}</p>
      <small>Score: {alert['score']}/10 | {alert['source']}</small>
    </div>'''

    html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Estratégico Premium v4</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
      :root {{
        --ink: #1a1a1a;
        --muted: #888;
        --rule: #e0e0e0;
        --cream: #f8f8f4;
        --steel: #455;
        --accent: #8b1a1a;
        --paper: #fff;
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
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--muted);
      }}

      .masthead-date {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        color: var(--muted);
      }}

      .title {{
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        color: var(--ink);
        margin: 40px 0 8px;
      }}

      .subtitle {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 13px;
        color: var(--muted);
        margin-bottom: 40px;
      }}

      /* ALERTS SECTION */
      .alerts-section {{
        background: #fff5f7;
        border: 2px solid var(--accent);
        border-radius: 4px;
        padding: 24px;
        margin-bottom: 40px;
        page-break-inside: avoid;
      }}

      .alerts-section h3 {{
        color: var(--accent);
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 20px;
      }}

      .alert-item {{
        background: white;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid var(--accent);
        border-radius: 2px;
      }}

      .alert-item strong {{
        display: block;
        margin-bottom: 8px;
        color: var(--ink);
      }}

      .alert-item p {{
        margin-bottom: 8px;
        font-size: 14px;
      }}

      .alert-item small {{
        color: var(--muted);
        font-size: 12px;
      }}

      /* SEARCH BOX */
      .search-box {{
        background: var(--cream);
        padding: 24px;
        border-radius: 4px;
        margin: 40px 0;
        display: flex;
        gap: 12px;
      }}

      .search-box input {{
        flex: 1;
        padding: 12px 16px;
        border: 1px solid var(--rule);
        border-radius: 2px;
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 14px;
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
        background: #555;
        color: #fff;
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
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 3px solid var(--accent);
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

      .footer {{
        border-top: 1px solid var(--rule);
        padding-top: 32px;
        margin-top: 60px;
        font-size: 12px;
        color: var(--muted);
        text-align: center;
      }}

      /* VISUALIZACIONES CSS */
      {viz_css}

      /* AGENDA CSS */
      {agenda_css}

      /* NORMATIVA CMF CSS */
      {normativa_css}

      @media print {{
        body {{ padding: 20px; }}
        .search-box {{ display: none; }}
        .alerts-section {{ page-break-inside: avoid; }}
        .live-indicators {{ page-break-inside: avoid; }}
      }}
    </style>
</head>
<body>
    <div class="masthead">
        <span class="masthead-title">Newsletter Estratégico Premium</span>
        <span class="masthead-date">{current_date}</span>
    </div>

    <h1 class="title">Análisis Estratégico</h1>
    <p class="subtitle">Inteligencia de mercados · Análisis automatizado · Datos en vivo</p>

    <!-- BÚSQUEDA -->
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="Busca noticias por palabra clave..." onkeyup="searchNews()">
        <button class="search-button" onclick="sortByScore()">Ordenar por Score</button>
        <button class="search-button" onclick="filterByScore(8)">Críticas</button>
    </div>

    <!-- ALERTAS CRÍTICAS -->
    <div class="alerts-section">
        <h3>🚨 ALERTAS CRÍTICAS - TOP 5</h3>
        {alerts_html}
    </div>

    <!-- VISUALIZACIONES + DATOS EN VIVO -->
    {viz_html}

    <!-- ECONOMÍA Y MERCADOS -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">💱</span>
            Economía y Mercados
        </h2>
        <span class="section-subtitle">Bloomberg · Reuters · WSJ · The Economist</span>
        {econ_html}
    </div>

    <!-- NOTICIAS ECONÓMICAS ACTUALES -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">📊</span>
            Noticias Económicas Actuales
        </h2>
        <span class="section-subtitle">INE · BCCh · ICARE · Banco Mundial</span>
        {econ_actuales_html}
    </div>

    <!-- INTELIGENCIA ARTIFICIAL -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">🤖</span>
            Inteligencia Artificial
        </h2>
        <span class="section-subtitle">OpenAI · Anthropic · Google DeepMind · TLDR AI</span>
        {ia_html}
    </div>

    <!-- GEOPOLÍTICA -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">🌍</span>
            Geopolítica
        </h2>
        <span class="section-subtitle">Reuters · FT · Bloomberg · The Economist</span>
        {geo_html}
    </div>

    <!-- CHILE ESTRATÉGICO -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">🇨🇱</span>
            Chile Estratégico
        </h2>
        <span class="section-subtitle">Codelco · BCCh · CMF · Gobierno</span>
        {chile_html}
    </div>

    <!-- COOPERATIVISMO -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">🤝</span>
            Cooperativismo
        </h2>
        <span class="section-subtitle">CONFECOOP · Coopeuch · ACI Américas · BID</span>
        {coop_html}
    </div>

    <!-- CMF -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">📋</span>
            CMF
        </h2>
        <span class="section-subtitle">Regulación · Fintech · Banca · Mercado de Capitales</span>
        {cmf_html}
    </div>

    <!-- NORMATIVA CMF EN CONSULTA -->
    {normativa_html}

    <!-- TENDENCIAS TECH -->
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">💻</span>
            Tendencias Tech
        </h2>
        <span class="section-subtitle">TechCrunch · The Verge · MIT Tech Review</span>
        {tendencias_html}
    </div>

    <!-- AGENDA DE ACTIVIDADES -->
    {agenda_html}

    <div class="footer">
        <strong>Newsletter Estratégico Premium v4 - FASE 4: Visualizaciones + Datos en Vivo + Agenda</strong>
        <p>Generado automáticamente · Análisis inteligente · Datos en vivo · Agenda de eventos · Publicado en GitHub Pages</p>
    </div>

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

      function sortByScore() {{
        const container = document.querySelector('body');
        const newsItems = Array.from(document.querySelectorAll('.news-item'));
        newsItems.sort((a, b) => b.getAttribute('data-score') - a.getAttribute('data-score'));
        newsItems.forEach(item => item.parentElement.appendChild(item));
      }}

      function filterByScore(minScore) {{
        const newsItems = document.querySelectorAll('.news-item');
        newsItems.forEach(item => {{
          const score = parseInt(item.getAttribute('data-score'));
          item.style.display = score >= minScore ? 'block' : 'none';
        }});
      }}
    </script>
</body>
</html>
'''

    return html


if __name__ == '__main__':
    main()
