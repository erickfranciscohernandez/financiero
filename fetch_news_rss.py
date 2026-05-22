#!/usr/bin/env python3
"""
Fetcher de Noticias - NewsAPI + RSS Feeds
Prioriza NewsAPI (noticias reales) con fallback a RSS y mock
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

NEWSAPI_QUERIES = {
    'geopolitica': 'geopolitica OR guerra OR sanciones OR OTAN OR diplomacia',
    'economia_mercados': 'economia global OR fed reserva federal OR banco central OR inflacion mercados',
    'chile_estrategico': 'Chile economia OR codelco OR peso chileno OR litio chile OR gobierno chile',
    'tendencias': 'tecnologia innovacion OR startup latinoamerica OR transformacion digital',
    'cooperativismo': 'cooperativa OR cooperativismo OR economia solidaria',
    'cmf': 'CMF Chile OR regulacion financiera Chile OR superintendencia valores',
    'noticias_economicas': 'bolsa latinoamerica OR dolar peso OR commodities OR cobre precio',
    'ia': 'inteligencia artificial OR ChatGPT OR OpenAI OR IA generativa',
}

RSS_FEEDS = {
    'geopolitica': [
        'https://feeds.reuters.com/Reuters/worldNews',
        'https://feeds.bloomberg.com/politics/news.rss',
    ],
    'chile_estrategico': [
        'https://www.diariofinanciero.com/feed',
        'https://www.emol.com/rss/economia.xml',
    ],
    'economia_mercados': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.cnbc.com/id/100003114/rss.xml',
    ],
    'tendencias': [
        'https://feeds.bloomberg.com/technology/news.rss',
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
                    if title and link:
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


def fetch_all_news():
    """Fetch news: NewsAPI first, RSS fallback, then return what we have."""
    all_news = {
        'geopolitica': [],
        'economia_mercados': [],
        'chile_estrategico': [],
        'tendencias': [],
        'cooperativismo': [],
        'cmf': [],
        'noticias_economicas': [],
        'ia': [],
    }

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
            return all_news
        print('⚠️  NewsAPI sin resultados, intentando RSS...\n')

    # RSS fallback
    print('📡 Intentando RSS feeds...')
    for category, urls in RSS_FEEDS.items():
        for url in urls:
            articles = fetch_rss_feed(url)
            if articles:
                all_news[category].extend(articles[:4])
        if all_news[category]:
            print(f'   {category}: ✅ {len(all_news[category])} noticias')
        else:
            print(f'   {category}: ❌ sin conexión')

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
