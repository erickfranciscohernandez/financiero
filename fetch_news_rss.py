#!/usr/bin/env python3
"""
Fetcher de Noticias - NewsAPI + RSS Feeds
Prioriza NewsAPI (noticias reales) con fallback a RSS ampliado
"""
import os
import json
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser

NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY', '')
NEWSAPI_URL = 'https://newsapi.org/v2/everything'

CHOCALE_FEEDS = [
    'https://www.chocale.cl/feed/',
    'https://www.chocale.cl/feed/rss/',
    'https://www.chocale.cl/rss.xml',
]

NEWSAPI_QUERIES = {
    'geopolitica': 'geopolitica OR guerra OR sanciones OR OTAN OR diplomacia',
    'economia_mercados': 'economia global OR fed reserva federal OR banco central OR inflacion mercados',
    'chile_estrategico': 'Chile economia OR codelco OR peso chileno OR litio chile OR gobierno chile',
    'tendencias': 'tecnologia innovacion OR startup latinoamerica OR transformacion digital',
    'cooperativismo': 'cooperativa OR cooperativismo OR economia solidaria',
    'cmf': 'CMF Chile OR regulacion financiera Chile OR superintendencia valores',
    'noticias_economicas': 'bolsa latinoamerica OR dolar peso OR commodities OR cobre precio',
    'ia': 'inteligencia artificial OR ChatGPT OR OpenAI OR IA generativa',
    'microsoft': 'Microsoft Copilot OR Microsoft AI OR Microsoft Azure OR Microsoft 365',
}

RSS_FEEDS = {
    'geopolitica': [
        'https://feeds.reuters.com/reuters/worldNews',
        'https://feeds.bloomberg.com/politics/news.rss',
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    ],
    'chile_estrategico': [
        'https://www.chocale.cl/feed/',
        'https://www.chocale.cl/feed/rss/',
        'https://www.diariofinanciero.com/feed',
        'https://www.emol.com/rss/economia.xml',
        'https://www.latercera.com/feed/',
        'https://www.elmostrador.cl/feed/',
    ],
    'economia_mercados': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.bloomberg.com/markets/commodities.rss',
        'https://feeds.bloomberg.com/markets/currencies.rss',
        'https://feeds.cnbc.com/id/100003114/rss.xml',
        'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
        'https://www.economist.com/finance-and-economics/rss.xml',
    ],
    'tendencias': [
        'https://feeds.bloomberg.com/technology/news.rss',
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
    ],
    'ia': [
        'https://techcrunch.com/tag/artificial-intelligence/feed/',
        'https://venturebeat.com/category/ai/feed/',
        'https://www.artificialintelligence-news.com/feed/',
    ],
    'noticias_economicas': [
        'https://www.ine.gob.cl/rss/estadisticas',
        'https://feeds.reuters.com/reuters/businessNews',
        'https://feeds.cnbc.com/id/10000664/rss.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
        'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml',
    ],
    'cooperativismo': [
        'https://www.chocale.cl/feed/',
        'https://www.elmostrador.cl/feed/',
        'https://www.latercera.com/feed/',
    ],
    'cmf': [
        'https://www.diariofinanciero.com/feed',
        'https://www.emol.com/rss/economia.xml',
    ],
    'microsoft': [
        'https://www.microsoft.com/en-us/research/feed/',
        'https://www.microsoft.com/en-us/microsoft-365/blog/feed/',
        'https://www.microsoft.com/en-us/security/blog/feed/',
    ],
}


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text).strip()


def strip_html(html):
    if not html:
        return ''
    s = MLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except Exception:
        return html[:300]


def fetch_newsapi(category, query, max_results=4):
    """Fetch news from NewsAPI for a given category query."""
    if not NEWSAPI_KEY:
        return []

    params = urllib.parse.urlencode({
        'q': query,
        'language': 'es',
        'sortBy': 'publishedAt',
        'pageSize': max_results,
        'apiKey': NEWSAPI_KEY,
    })
    url = f'{NEWSAPI_URL}?{params}'

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'FinancieroNewsletter/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        articles = []
        for art in data.get('articles', []):
            title = (art.get('title') or '').strip()
            description = strip_html(art.get('description') or art.get('content') or '')
            source = art.get('source', {}).get('name', 'NewsAPI')
            link = art.get('url', '#')
            if title and title != '[Removed]':
                articles.append({
                    'title': title,
                    'summary': description[:300],
                    'source': source,
                    'link': link,
                    'date': art.get('publishedAt', datetime.now().isoformat()),
                })
        return articles

    except Exception:
        return []


OFFOPIC_KEYWORDS = [
    # Gastronomía
    'receta', 'marinada', 'pollo', 'cocina', 'gastronomía', 'restaurante',
    'ingredientes', 'preparación', 'horno', 'fritura', 'ensalada', 'postre',
    'bebida', 'vino', 'cerveza', 'cocktail', 'recetas', 'jugosas', 'sabrosas',
    'pechuga', 'filete', 'carne',
    # Moda y entretenimiento
    'moda', 'belleza', 'maquillaje', 'horóscopo', 'celebrities', 'farándula',
    # Deportes y política no financiera
    'deporte', 'fútbol', 'tenis', 'boicot', 'genocidio', 'partido político',
    'manifestación', 'protesta',
]

OFFOPIC_DOMAINS = [
    'directoalpaladar.com', 'hogarmania.com', 'pequerecetas.com',
    'huffingtonpost.es', 'huffpost.com',
]


def is_relevant(title, link=''):
    """Retorna False si el artículo es claramente off-topic para un boletín financiero."""
    title_lower = title.lower()
    if any(kw in title_lower for kw in OFFOPIC_KEYWORDS):
        return False
    if any(domain in link for domain in OFFOPIC_DOMAINS):
        return False
    return True


def fetch_rss_feed(url, timeout=5):
    """Fetch and parse a single RSS feed."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            root = ET.fromstring(data)
            ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
            articles = []
            for item in root.findall('.//item'):
                try:
                    title = item.findtext('title', '').strip()
                    link = item.findtext('link', '').strip()
                    description = item.findtext('description', '')
                    content = item.findtext('content:encoded', '', ns)
                    text = strip_html(content if content else description)[:300]
                    if title and link and is_relevant(title, link):
                        articles.append({
                            'title': title,
                            'link': link,
                            'summary': text,
                            'source': url.split('/')[2],
                            'date': item.findtext('pubDate', ''),
                        })
                except Exception:
                    continue
            return articles
    except Exception:
        return []


# Mantener alias para compatibilidad con código antiguo
fetch_feed = fetch_rss_feed


def fetch_chocale_news(max_results=4):
    """Siempre intenta obtener noticias desde chocale.cl."""
    for url in CHOCALE_FEEDS:
        articles = fetch_rss_feed(url)
        if articles:
            print(f'   chocale.cl: ✅ {len(articles[:max_results])} noticias')
            return articles[:max_results]
    print('   chocale.cl: ❌ sin datos')
    return []


def fetch_all_news():
    """Fetch news: NewsAPI first, RSS fallback para categorías sin resultados.
    Chocale.cl se incorpora siempre a chile_estrategico."""
    all_news = {key: [] for key in RSS_FEEDS}

    if NEWSAPI_KEY:
        print('🌐 Obteniendo noticias desde NewsAPI...')
        for category, query in NEWSAPI_QUERIES.items():
            articles = fetch_newsapi(category, query, max_results=4)
            all_news[category] = articles
            status = f'✅ {len(articles)} noticias' if articles else '⚠️  sin resultados'
            print(f'   {category}: {status}')
        total = sum(len(v) for v in all_news.values())
        if total > 0:
            print(f'✅ NewsAPI: {total} noticias obtenidas\n')

    # Chocale.cl: fuente nacional siempre activa
    print('📡 Obteniendo noticias desde chocale.cl...')
    chocale_articles = fetch_chocale_news()
    if chocale_articles:
        all_news['chile_estrategico'] = chocale_articles + all_news.get('chile_estrategico', [])

    # RSS para categorías vacías (siempre se intenta Microsoft y demás)
    print('📡 Complementando con RSS feeds...')
    for category, urls in RSS_FEEDS.items():
        if all_news.get(category):
            continue
        for url in urls:
            articles = fetch_rss_feed(url)
            if articles:
                all_news[category].extend(articles[:4])
                break
        status = f'✅ {len(all_news[category])}' if all_news[category] else '❌ sin datos'
        print(f'   {category}: {status}')

    return all_news


if __name__ == '__main__':
    news = fetch_all_news()
    print('\n' + '=' * 60)
    print('RESUMEN DE NOTICIAS:')
    print('=' * 60)
    for cat, items in news.items():
        print(f'\n{cat}: {len(items)} noticias')
        for n in items[:2]:
            print(f'   • {n["title"][:70]}')
