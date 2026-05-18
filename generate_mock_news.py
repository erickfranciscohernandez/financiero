#!/usr/bin/env python3
"""
Generador de noticias mock dinámicas
Actualiza noticias_diarias.json con datos nuevos simulados
Para simular actualizaciones en tiempo real sin acceso a internet
"""
import json
from datetime import datetime, timedelta
import random

# Plantillas de noticias por categoría
NEWS_TEMPLATES = {
    'geopolitica': [
        {
            'title': 'China intensifica presión comercial contra semiconductores estadounidenses',
            'summary': 'Nuevas restricciones comerciales impactan la industria tecnológica global. Analistas advierten sobre escalada de tensiones.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/news/articles'
        },
        {
            'title': 'Rusia y OPEP+ coordinan estrategia energética en contexto geopolítico',
            'summary': 'Reunión estratégica entre líderes energéticos genera preocupación en mercados occidentales.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/business'
        },
        {
            'title': 'EE.UU. anuncia nuevas medidas de defensa en Pacífico',
            'summary': 'Inversiones militares sin precedentes en la región generan reacciones de potencias asiáticas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': 'Cobre toca mínimos de 4 semanas en USD 4.12/lb por debilidad de demanda',
            'summary': 'Commodity clave para Chile cae por preocupaciones de recesión global y menor actividad manufacturera.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com/commodities'
        },
        {
            'title': 'Fed mantiene tasas en máximos; mercados anticipan cambio de política',
            'summary': 'Expectativas de recortes de tasas en próximos meses generan volatilidad en mercados de renta fija.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/news'
        },
        {
            'title': 'Oro recupera terreno ante incertidumbre económica global',
            'summary': 'Metal precioso sube impulsado por demanda defensiva de inversores institucionales.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com'
        },
        {
            'title': 'Mercados accionarios globales en volatilidad por datos económicos mixtos',
            'summary': 'S&P 500 cierra mixto mientras se esperan reportes de empleo en EE.UU.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'Banco Central Europeo considera nuevas medidas de estímulo',
            'summary': 'Preocupaciones por desaceleración económica empujan a BCE a evaluación de política monetaria.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com'
        },
        {
            'title': 'Petróleo recupera 2% en sesión de volatilidad',
            'summary': 'Conflictos geopolíticos y datos de demanda impulsan precios del crudo.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/energy'
        },
    ],
    'economia_chile': [
        {
            'title': 'BCCh mantiene tasas de interés en 5.25% en nueva reunión de política monetaria',
            'summary': 'Banco Central Chile mantiene postura restrictiva ante persistencia de presiones inflacionarias.',
            'source': 'Diario Financiero',
            'link': 'https://www.diariofinanciero.com'
        },
        {
            'title': 'Minería de cobre reporta caída de 8% en producción por menor demanda global',
            'summary': 'Principales empresas mineras ajustan operaciones ante perspectivas económicas débiles.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'Gobierno anuncia nuevo programa de estímulo económico para Pymes',
            'summary': 'Medidas incluyen reducción de impuestos y líneas de crédito preferente para micro y pequeñas empresas.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': 'Bolsa de Santiago cierra con alza de 1.2% impulsada por sector tecnológico',
            'summary': 'Índice IPSA sube en sesión positiva reflejando recuperación de valores de software y telecomunicaciones.',
            'source': 'Diario Financiero',
            'link': 'https://www.diariofinanciero.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': 'OpenAI lanza nuevos modelos de IA con capacidades mejoradas de razonamiento',
            'summary': 'Competencia se intensifica en carrera de inteligencia artificial con nuevas capacidades de análisis complejo.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'Meta invierte $10B en infraestructura de datos para AI generativa',
            'summary': 'Gasto récord refleja compromiso de Meta con desarrollo de tecnologías de próxima generación.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
        {
            'title': 'Startups de semiconductores logran $2.3B en rondas de financiamiento',
            'summary': 'Inversores ven oportunidad en empresas especializadas en chips para IA y computación de borde.',
            'source': 'Crunchbase',
            'link': 'https://crunchbase.com'
        },
    ],
    'cooperativismo': [
        {
            'title': 'Cooperativa de Ahorro chilena alcanza 500K miembros activos',
            'summary': 'Crecimiento de 12% anual refleja aumento de confianza en modelo cooperativo de servicios financieros.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'Red de cooperativas agrícolas invierte en tecnología de riego sostenible',
            'summary': 'Iniciativa incluye monitoreo IoT y análisis de datos para optimizar uso de agua en cultivos.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl'
        },
        {
            'title': 'Congreso Internacional de Cooperativismo se realizará en Santiago en agosto',
            'summary': 'Evento reunirá a líderes de movimiento cooperativo de 50 países para debatir sostenibilidad.',
            'source': 'ACI Americas',
            'link': 'https://www.aciamericas.coop'
        },
    ],
    'cmf': [
        {
            'title': 'CMF publica normas sobre transparencia en comisiones de fondos mutuos',
            'summary': 'Medida regulatoria busca proteger derechos de inversionistas mediante mayor claridad de costos.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'Comisión del Mercado Financiero sanciona a tres corredoras por incumplimientos',
            'summary': 'Multas por falta de diligencia debida en procesos de Know Your Customer alcanza $150 millones.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF aprueba nueva plataforma de crowdfunding con regulación flexible',
            'summary': 'Resolución permite inversión en startups con límites de monto y perfil de inversionista.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': 'IPC de mayo muestra moderación en presiones inflacionarias',
            'summary': 'Índice de Precios al Consumidor sube 0.3% mensual, por debajo de expectativas de analistas.',
            'source': 'INE',
            'link': 'https://www.ine.cl'
        },
        {
            'title': 'Desempleo se sitúa en 8.2% según cifras de ocupación de trimestre',
            'summary': 'Tasa de desocupación se mantiene estable pese a moderación del crecimiento económico.',
            'source': 'Banco Central',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Remesas de trabajadores chilenos en el exterior caen 5% interanual',
            'summary': 'Menores ingresos por transferencias internacionales reflejan desaceleración en economías receptoras.',
            'source': 'INE',
            'link': 'https://www.ine.cl'
        },
        {
            'title': 'Índice de Confianza del Consumidor mejora por primera vez en 6 meses',
            'summary': 'Expectativas sobre situación económica se fortalecen impulsadas por menor volatilidad política.',
            'source': 'Universidad de Chile',
            'link': 'https://www.uchile.cl'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': 'Investigadores desarrollan modelo de IA que explica sus propias decisiones',
            'summary': 'Avance en "AI explicable" abre puertas a adopción en sectores regulados como finanzas y salud.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Google llama a regulación responsable de IA generativa en próxima década',
            'summary': 'Directiva destaca importancia de marcos regulatorios que balanceen innovación con seguridad.',
            'source': 'Ben\'s Bites',
            'link': 'https://bensbites.com'
        },
        {
            'title': 'Detectan sesgos importantes en sistemas de IA de grandes empresas tecnológicas',
            'summary': 'Estudio académico revela problemas de equidad en modelos de lenguaje usados por plataformas.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
        {
            'title': 'Startups de AI logran valuaciones record en rondas de Series B y C',
            'summary': 'Inversión en empresas de IA crece 300% respecto a año anterior impulsada por demanda corporativa.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Universidades crean programa de certificación en IA responsable',
            'summary': 'Iniciativa educativa busca formar profesionales preparados en aspectos éticos de IA.',
            'source': 'Ben\'s Bites',
            'link': 'https://bensbites.com'
        },
        {
            'title': 'Sector financiero integra IA en detección de fraude con precisión del 99.2%',
            'summary': 'Bancos de región implementan sistemas de machine learning que reducen casos de fraude.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
    ],
}


def generate_dynamic_news():
    """Genera noticias dinámicas basadas en la hora actual"""

    # Usar la hora actual para seleccionar noticias diferentes
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute

    # Seed para reproducibilidad dentro del mismo período de 30 min
    random.seed(current_hour * 60 + (current_minute // 30))

    news_data = {}

    for category, templates in NEWS_TEMPLATES.items():
        # Seleccionar 3-4 noticias aleatorias por categoría
        num_news = random.randint(3, 4)
        selected = random.sample(templates, min(num_news, len(templates)))

        # Agregar variación temporal
        news_with_time = []
        for i, news in enumerate(selected):
            news_copy = news.copy()
            # Agregar "updated" timestamp
            hours_ago = random.randint(0, 6)
            news_copy['date'] = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            news_with_time.append(news_copy)

        news_data[category] = news_with_time

    return news_data


def update_news_file():
    """Actualiza el archivo noticias_diarias.json con noticias dinámicas"""

    try:
        news = generate_dynamic_news()

        with open('noticias_diarias.json', 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)

        # Mostrar resumen
        total_news = sum(len(v) for v in news.values())
        print(f"✅ Noticias actualizadas: {total_news}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   Próxima actualización: en 30 minutos")

        return True

    except Exception as e:
        print(f"❌ Error actualizando noticias: {e}")
        return False


if __name__ == '__main__':
    print("🔄 Generador de noticias dinámicas")
    print("=" * 50)
    update_news_file()
