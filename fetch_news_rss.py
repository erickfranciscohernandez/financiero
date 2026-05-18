#!/usr/bin/env python3
"""
Fetcher de Noticias desde RSS Feeds
Obtiene noticias de El Mostrador, EMOL, La Tercera, Bloomberg, etc.
"""
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from html.parser import HTMLParser

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
    """Remove HTML tags from text"""
    if not html:
        return ""
    s = MLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except:
        return html[:200]

# RSS Feeds de noticias chilenas y globales
RSS_FEEDS = {
    "geopolitica": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.reuters.com/world",
        "https://feeds.bloomberg.com/politics/news.rss"
    ],
    "economia_chile": [
        "https://www.diariofinanciero.com/feed",
        "https://www.emol.com/rss/economia.xml",
        "https://www.latercera.com/feed/",
    ],
    "economia_global": [
        "https://feeds.bloomberg.com/markets/commodities.rss",
        "https://feeds.bloomberg.com/markets/currencies.rss",
        "https://feeds.cnbc.com/id/100003114/rss.xml"
    ],
    "tendencias_tech": [
        "https://feeds.bloomberg.com/technology/news.rss",
    ]
}

def fetch_feed(url, timeout=5):
    """Fetch and parse RSS feed"""
    try:
        print(f"  📡 Obteniendo: {url[:50]}...", end=" ")
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            root = ET.fromstring(data)

            # Detectar namespace
            ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}

            articles = []

            # Buscar items en el feed
            for item in root.findall('.//item'):
                try:
                    title = item.findtext('title', '').strip()
                    link = item.findtext('link', '').strip()
                    description = item.findtext('description', '')
                    content = item.findtext('content:encoded', '', ns)
                    pub_date = item.findtext('pubDate', '')

                    # Tomar el contenido más largo disponible
                    text = content if content else description
                    text = strip_html(text)[:300]

                    if title and link:
                        articles.append({
                            'title': title,
                            'link': link,
                            'summary': text,
                            'source': url.split('/')[2],
                            'date': pub_date
                        })
                except:
                    continue

            print(f"✅ {len(articles)} noticias")
            return articles

    except urllib.error.URLError as e:
        print(f"❌ Error de conexión")
        return []
    except Exception as e:
        print(f"❌ Error al parsear")
        return []

def categorize_news(news_item):
    """Categorize news based on keywords"""
    title_lower = news_item['title'].lower()
    summary_lower = news_item['summary'].lower()
    full_text = title_lower + " " + summary_lower

    if any(word in full_text for word in ['guerra', 'conflicto', 'sanciones', 'china', 'rusia', 'geopolítica', 'trump']):
        return 'geopolitica'
    elif any(word in full_text for word in ['cobre', 'litio', 'minería', 'codelco', 'chile', 'reforma tributaria']):
        return 'chile_estrategico'
    elif any(word in full_text for word in ['ia', 'inteligencia artificial', 'ai', 'tecnología', 'datos']):
        return 'tendencias'
    elif any(word in full_text for word in ['banco central', 'tasa', 'inflación', 'dólar', 'bolsa', 'mercado']):
        return 'economia_mercados'
    else:
        return 'economia_mercados'

def fetch_all_news():
    """Fetch news from all feeds"""
    print("🔄 Obteniendo noticias de RSS feeds...\n")

    all_news = {
        'geopolitica': [],
        'economia_mercados': [],
        'chile_estrategico': [],
        'tendencias': []
    }

    for category, urls in RSS_FEEDS.items():
        print(f"\n📰 Categoría: {category}")
        for url in urls:
            articles = fetch_feed(url)
            for article in articles:
                cat = categorize_news(article)
                if len(all_news[cat]) < 5:  # Máximo 5 por categoría
                    all_news[cat].append(article)

    return all_news

def news_to_json(all_news):
    """Convert news to JSON format for newsletter"""
    import json

    # Crear resúmenes por categoría
    summary = {
        'timestamp': datetime.now().isoformat(),
        'geopolitica': [f"• {n['title']}" for n in all_news['geopolitica'][:3]],
        'economia': [f"• {n['title']}" for n in all_news['economia_mercados'][:3]],
        'chile': [f"• {n['title']}" for n in all_news['chile_estrategico'][:3]],
        'tendencias': [f"• {n['title']}" for n in all_news['tendencias'][:3]],
        'all_news': all_news
    }

    return summary

if __name__ == '__main__':
    news = fetch_all_news()
    summary = news_to_json(news)

    print("\n" + "="*60)
    print("✅ NOTICIAS OBTENIDAS:")
    print("="*60)
    print(f"\n🌍 Geopolítica: {len(news['geopolitica'])} noticias")
    for n in news['geopolitica'][:3]:
        print(f"   • {n['title'][:70]}")

    print(f"\n💹 Economía: {len(news['economia_mercados'])} noticias")
    for n in news['economia_mercados'][:3]:
        print(f"   • {n['title'][:70]}")

    print(f"\n🇨🇱 Chile: {len(news['chile_estrategico'])} noticias")
    for n in news['chile_estrategico'][:3]:
        print(f"   • {n['title'][:70]}")

    print(f"\n🚀 Tendencias: {len(news['tendencias'])} noticias")
    for n in news['tendencias'][:3]:
        print(f"   • {n['title'][:70]}")
