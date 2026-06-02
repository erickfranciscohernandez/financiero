#!/usr/bin/env python3
"""
Análisis editorial con Claude AI (Anthropic)
Genera análisis profesional por sección a partir de noticias del día.
"""
import os
from datetime import datetime

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

SYSTEM_PROMPT = """Eres el editor principal de un newsletter premium diario orientado a ejecutivos, \
empresarios, inversionistas, analistas financieros, family offices y tomadores de decisión en Latinoamérica.

Tu objetivo es transformar noticias crudas en análisis ejecutivo claro, estratégico y accionable.

Para cada sección debes responder:
• Qué ocurrió (síntesis breve)
• Por qué importa para la región
• Cómo afecta a Chile y Latinoamérica
• Qué riesgos u oportunidades genera
• Qué tendencia debe monitorearse

ESTILO:
- Tono: profesional, sofisticado, analítico, neutral
- Modelo: Bloomberg, The Economist, Diario Financiero
- Evitar: sensacionalismo, titulares exagerados, lenguaje informal
- Máximo 3 párrafos por sección
- Cada párrafo: 2-4 oraciones concretas
- No repetir los titulares literalmente; sintetiza y conecta

Responde SOLO el análisis editorial, sin encabezados, sin numeración, sin markdown."""


SECTION_CONTEXTS = {
    'geopolitica': 'geopolítica global, tensiones internacionales, diplomacia y seguridad',
    'economia_mercados': 'economía global, mercados financieros, bancos centrales y tasas de interés',
    'chile_estrategico': 'economía chilena, política local, minería, energía y empresas de Chile',
    'cooperativismo': 'sector cooperativo, economía solidaria y finanzas cooperativas en Chile y Latinoamérica',
    'cmf': 'regulación financiera chilena, CMF, sistema bancario, fintech y normativa',
    'noticias_economicas': 'mercados bursátiles, commodities, divisas y tendencias macroeconómicas',
    'tendencias': 'tecnología, innovación, transformación digital y startups en Latinoamérica',
    'ia': 'inteligencia artificial, modelos de lenguaje, automatización e impacto económico de la IA',
}


def _build_news_text(news_list):
    """Convierte lista de noticias a texto para el prompt."""
    lines = []
    for i, item in enumerate(news_list[:5], 1):
        title   = item.get('title', '').strip()
        summary = item.get('summary', '').strip()[:250]
        source  = item.get('source', '')
        if title:
            lines.append(f"{i}. [{source}] {title}")
            if summary:
                lines.append(f"   {summary}")
    return '\n'.join(lines)


def analyze_section(section_key, news_list, client):
    """Genera análisis editorial de una sección usando Claude."""
    if not news_list:
        return None

    context = SECTION_CONTEXTS.get(section_key, section_key)
    news_text = _build_news_text(news_list)
    date_str = datetime.now().strftime('%d de %B de %Y').replace('May', 'Mayo')

    prompt = f"""Fecha: {date_str}
Sección: {context}

Noticias del día:
{news_text}

Escribe el análisis editorial ejecutivo de esta sección (máximo 3 párrafos)."""

    try:
        response = client.messages.create(
            model='claude-opus-4-7',
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f'   ⚠️  Error en sección {section_key}: {e}')
        return None


def generate_executive_summary(all_news, client):
    """Genera el resumen ejecutivo general del día."""
    top_items = []
    for section_key in ['geopolitica', 'economia_mercados', 'chile_estrategico', 'ia']:
        for item in all_news.get(section_key, [])[:2]:
            title = item.get('title', '').strip()
            if title:
                top_items.append(f"- {title}")

    if not top_items:
        return None

    date_str = datetime.now().strftime('%d de %B de %Y').replace('May', 'Mayo')
    news_text = '\n'.join(top_items[:8])

    prompt = f"""Fecha: {date_str}

Principales noticias del día:
{news_text}

Escribe un resumen ejecutivo del día de máximo 2 párrafos. \
Conecta los eventos globales con su impacto en Chile y Latinoamérica. \
Identifica el tema dominante del día y la tendencia más relevante a monitorear."""

    try:
        response = client.messages.create(
            model='claude-opus-4-7',
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f'   ⚠️  Error en resumen ejecutivo: {e}')
        return None


def run_ai_analysis(all_news):
    """
    Punto de entrada principal.
    Retorna dict con análisis por sección + resumen ejecutivo.
    Si no hay API key o falla, retorna dict vacío (el newsletter sigue funcionando).
    """
    if not ANTHROPIC_AVAILABLE:
        print('⚠️  Librería anthropic no instalada — sin análisis AI')
        return {}

    if not ANTHROPIC_API_KEY:
        print('⚠️  ANTHROPIC_API_KEY no configurada — sin análisis AI')
        return {}

    print('🤖 Generando análisis editorial con Claude AI...')
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    analyses = {}

    # Resumen ejecutivo
    print('   -> Resumen ejecutivo del dia...')
    summary = generate_executive_summary(all_news, client)
    if summary:
        analyses['resumen_ejecutivo'] = summary
        print('   ✅ Resumen ejecutivo')

    # Análisis por sección
    sections_to_analyze = [
        'geopolitica', 'economia_mercados', 'chile_estrategico',
        'cooperativismo', 'cmf', 'noticias_economicas', 'tendencias', 'ia',
    ]

    for section_key in sections_to_analyze:
        news_list = all_news.get(section_key, [])
        if not news_list:
            continue
        print(f'   -> {section_key}...')
        analysis = analyze_section(section_key, news_list, client)
        if analysis:
            analyses[section_key] = analysis
            print(f'   ✅ {section_key}')

    total = len([k for k in analyses if k != 'resumen_ejecutivo'])
    print(f'✅ Claude AI: {total} secciones analizadas\n')
    return analyses
