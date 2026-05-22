#!/usr/bin/env python3
"""
Newsletter Estratégico - Generador Automático
Genera contenido diario usando la API de Anthropic Claude
"""

import os
import sys
from datetime import datetime
from anthropic import Anthropic

# Configuración
API_KEY = os.environ.get('ANTHROPIC_API_KEY')
OUTPUT_DIR = 'output'
TEMPLATE_PATH = 'templates/newsletter-template.html'

# Prompt del sistema (tu documento de instrucciones)
SYSTEM_PROMPT = """Eres un comunicador experto en análisis de noticias, geopolítica, economía global, mercados financieros y tendencias estratégicas.
Tu función es actuar como editor principal de un newsletter premium diario orientado a:
• Ejecutivos 
• Empresarios 
• Inversionistas 
• Analistas financieros 
• Family offices 
• Consultores 
• Tomadores de decisión en Latinoamérica 

Tu objetivo es entregar información ejecutiva, clara y estratégica sobre los acontecimientos más relevantes del día.

OBJETIVO DEL AGENTE
Generar automáticamente un boletín informativo (Newsletter) con un resumen ejecutivo de las noticias más relevantes y recientes del día, enfocadas en:
• Geopolítica 
• Economía global 
• Mercados financieros 
• Tecnología e IA 
• Tendencias estratégicas 
• Chile y Latinoamérica 
• Información financiera y regulatoria 

El newsletter debe ayudar a comprender:
• Qué ocurrió 
• Por qué importa 
• Cómo afecta a Chile y Latinoamérica 
• Qué riesgos u oportunidades genera 
• Qué tendencias deben monitorearse 

FUENTES DE INFORMACIÓN
Priorizar noticias de:

Medios Nacionales: El Mostrador, BioBioChile, La Tercera, Diario Financiero, EMOL
Medios Internacionales: Bloomberg, Reuters, Financial Times, The Economist, CNBC
Tecnología e IA: Microsoft News, TLDR AI, Ben's Bites, The Rundown AI
Organismos: CMF, Banco Central de Chile, FMI, OCDE

TEMAS PRIORITARIOS

Geopolítica: China vs EE.UU., BRICS, Europa, Medio Oriente, América Latina, tensiones comerciales, elecciones, conflictos
Economía y Mercados: Tasas de interés, inflación, dólar, cobre, petróleo, commodities, bolsas globales, criptomonedas, bancos centrales
Chile Estratégico: Gobierno, reformas, minería, energía, AFP, bancos, empresas, inversión, mercado inmobiliario, startups
CMF: Sistema bancario, liquidez, crédito, morosidad, solvencia, regulación financiera, fintech
Cooperativismo: Datos recientes del sector cooperativo chileno cuando haya información relevante

ESTILO DE COMUNICACIÓN
Tono: Profesional, ejecutivo, sofisticado, claro, analítico, estratégico, neutral
Escribir como: Bloomberg, The Economist, Financial Times, Diario Financiero
Evitar: Sensacionalismo, opiniones emocionales, titulares exagerados, lenguaje informal

REGLAS DEL NEWSLETTER
• El boletín debe contener EXACTAMENTE 6 párrafos
• Cada párrafo debe abordar un tema distinto
• No copiar titulares textualmente
• Sintetizar información compleja en lenguaje ejecutivo
• Conectar eventos globales con impacto local
• Detectar tendencias emergentes
• Priorizar noticias de alto impacto económico y estratégico"""


def generar_contenido():
    """Genera el contenido del newsletter usando Claude API con web search"""
    
    if not API_KEY:
        print("❌ Error: ANTHROPIC_API_KEY no está configurada")
        sys.exit(1)
    
    client = Anthropic(api_key=API_KEY)
    
    # Fecha de hoy
    hoy = datetime.now()
    fecha_es = hoy.strftime("%A, %d de %B de %Y")
    fecha_corta = hoy.strftime("%d-%m-%Y")
    
    # Mapeo de días y meses al español
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
             'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    dia_semana = dias[hoy.weekday()]
    mes_nombre = meses[hoy.month - 1]
    fecha_formateada = f"{dia_semana.capitalize()}, {hoy.day} de {mes_nombre} de {hoy.year}"
    
    prompt_usuario = f"""Genera el newsletter estratégico de HOY: {fecha_formateada}.

INSTRUCCIONES CRÍTICAS:
1. Usa la herramienta de búsqueda web para obtener noticias de las ÚLTIMAS 24 HORAS
2. Busca información actualizada en las siguientes áreas (haz múltiples búsquedas):
   - Geopolítica global (China-EE.UU., Medio Oriente, Europa, Latinoamérica)
   - Economía y mercados financieros (Fed, inflación, bolsas, commodities)
   - Chile (economía, mercados, política, minería, cobre, dólar)
   - Tecnología e IA (Google, Microsoft, OpenAI, startups)
   - Cooperativismo en Chile (si hay noticias recientes)
   - CMF y regulación financiera

3. Genera contenido ORIGINAL basado en las noticias que encuentres hoy

4. ESTRUCTURA REQUERIDA - Entrégame el contenido en este formato JSON:

{{
  "fecha": "{fecha_formateada}",
  "fecha_corta": "{fecha_corta}",
  "numero_edicion": "{hoy.strftime('%j')}",
  "ticker": [
    {{"label": "USD/CLP", "value": "$XXX", "trend": "neutral"}},
    {{"label": "COBRE", "value": "US$X.XX/lb", "trend": "up"}},
    {{"label": "BRENT", "value": "US$XXX", "trend": "down"}},
    {{"label": "TPM CHILE", "value": "X.XX%", "trend": "neutral"}},
    {{"label": "IPC", "value": "X.X% a/a", "trend": "neutral"}}
  ],
  "titular": "Titular ejecutivo principal que captura los eventos clave del día",
  "resumen_ejecutivo": "2-3 oraciones con visión estratégica del panorama global del día",
  "indicadores": [
    {{"label": "Dólar Obs.", "value": "$XXX", "delta": "CLP/USD · BCCh", "trend": "neutral"}},
    {{"label": "Cobre Comex", "value": "US$X.XX", "delta": "Descripción del movimiento", "trend": "up"}},
    {{"label": "TPM Chile", "value": "X.XX%", "delta": "Banco Central", "trend": "neutral"}},
    {{"label": "IPC anual", "value": "X.X%", "delta": "Descripción", "trend": "down"}},
    {{"label": "Brent", "value": "US$XXX", "delta": "Descripción", "trend": "up"}}
  ],
  "articulos": [
    {{
      "numero": "I",
      "categoria": "Geopolítica",
      "titulo": "Título del artículo",
      "cuerpo": ["Primer párrafo del artículo.", "Segundo párrafo del artículo."]
    }},
    {{
      "numero": "II",
      "categoria": "Economía global",
      "titulo": "Título del artículo",
      "cuerpo": ["Párrafo 1", "Párrafo 2"]
    }},
    {{
      "numero": "III",
      "categoria": "Mercados & Commodities",
      "titulo": "Título del artículo",
      "cuerpo": ["Párrafo 1", "Párrafo 2"]
    }},
    {{
      "numero": "IV",
      "categoria": "Chile estratégico",
      "titulo": "Título del artículo",
      "cuerpo": ["Párrafo 1", "Párrafo 2"]
    }},
    {{
      "numero": "V",
      "categoria": "Tecnología & IA",
      "titulo": "Título del artículo",
      "cuerpo": ["Párrafo 1", "Párrafo 2"]
    }},
    {{
      "numero": "VI",
      "categoria": "Tema emergente del día",
      "titulo": "Título del artículo",
      "cuerpo": ["Párrafo 1", "Párrafo 2"]
    }}
  ],
  "insight": "Reflexión estratégica final tipo think tank o fondo de inversión (2-3 oraciones potentes)",
  "fuentes": "Lista de fuentes consultadas separadas por · "
}}

IMPORTANTE: Responde SOLO con el JSON, sin texto adicional antes ni después."""

    print(f"🔍 Generando newsletter para {fecha_formateada}...")
    print("📡 Llamando a la API de Claude con búsqueda web...")
    
    try:
        # Llamada a la API con web search habilitado
        mensaje = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0.7,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_usuario}
            ],
            # Habilitar web search
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }]
        )
        
        # Extraer el contenido de texto de la respuesta
        contenido = ""
        for bloque in mensaje.content:
            if bloque.type == "text":
                contenido += bloque.text
        
        print("✅ Contenido generado exitosamente")
        return contenido
        
    except Exception as e:
        print(f"❌ Error al generar contenido: {e}")
        sys.exit(1)


def limpiar_json(texto):
    """Limpia el JSON de posibles artefactos de markdown"""
    import re
    # Remover bloques de código markdown
    texto = re.sub(r'```json\s*', '', texto)
    texto = re.sub(r'```\s*', '', texto)
    return texto.strip()


def generar_html(contenido_json):
    """Genera el HTML del newsletter desde el JSON"""
    import json
    
    try:
        # Limpiar y parsear JSON
        contenido_limpio = limpiar_json(contenido_json)
        datos = json.loads(contenido_limpio)
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        print(f"Contenido recibido: {contenido_json[:500]}...")
        sys.exit(1)
    
    # Leer template
    with open('templates/newsletter-template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generar ticker HTML
    ticker_items = ""
    for item in datos['ticker'] * 2:  # Duplicar para loop
        trend_class = f"ticker-{item['trend']}" if item['trend'] != 'neutral' else ''
        ticker_items += f'<div class="ticker-item"><span class="ticker-label">{item["label"]}</span> <span class="ticker-value {trend_class}">{item["value"]}</span></div>\n    '
    
    # Generar indicadores HTML
    indicadores_html = ""
    for ind in datos['indicadores']:
        trend_map = {'up': 'delta-up', 'down': 'delta-down', 'neutral': ''}
        trend_class = trend_map.get(ind['trend'], '')
        indicadores_html += f'''    <div class="indicator">
      <div class="indicator-label">{ind["label"]}</div>
      <div class="indicator-value">{ind["value"]}</div>
      <div class="indicator-delta {trend_class}">{ind["delta"]}</div>
    </div>\n'''
    
    # Generar artículos HTML
    articulos_html = ""
    toc_html = ""
    
    for i, art in enumerate(datos['articulos'], 1):
        cuerpo_html = "".join([f"<p>{parrafo}</p>\n        " for parrafo in art['cuerpo']])
        
        articulos_html += f'''
    <article class="article" id="art-{i}">
      <div class="article-meta">
        <span class="article-number">{art["numero"]}.</span>
        <span class="article-category">{art["categoria"]}</span>
      </div>
      <h2 class="article-title">{art["titulo"]}</h2>
      <div class="article-body">
        {cuerpo_html}
      </div>
    </article>
'''
        
        toc_html += f'''        <li class="toc-item">
          <a href="#art-{i}" class="toc-link">
            <span class="toc-num">{art["numero"]}.</span>
            <span class="toc-text">
              <strong>{art["titulo"]}</strong>
              <small>{art["categoria"]}</small>
            </span>
          </a>
        </li>\n'''
    
    # Reemplazos en el template
    html = template.replace('{{FECHA}}', datos['fecha'])
    html = html.replace('{{FECHA_CORTA}}', datos['fecha_corta'])
    html = html.replace('{{NUMERO_EDICION}}', datos['numero_edicion'])
    html = html.replace('{{TICKER_ITEMS}}', ticker_items)
    html = html.replace('{{TITULAR}}', datos['titular'])
    html = html.replace('{{RESUMEN_EJECUTIVO}}', datos['resumen_ejecutivo'])
    html = html.replace('{{INDICADORES}}', indicadores_html)
    html = html.replace('{{ARTICULOS}}', articulos_html)
    html = html.replace('{{TOC}}', toc_html)
    html = html.replace('{{INSIGHT}}', datos['insight'])
    html = html.replace('{{FUENTES}}', datos['fuentes'])
    
    return html


def main():
    """Función principal"""
    print("=" * 60)
    print("  NEWSLETTER ESTRATÉGICO - GENERADOR AUTOMÁTICO")
    print("=" * 60)
    print()
    
    # Generar contenido
    contenido = generar_contenido()
    
    # Generar HTML
    print("🎨 Generando HTML...")
    html = generar_html(contenido)
    
    # Guardar archivo
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    hoy = datetime.now()
    archivo_salida = f"{OUTPUT_DIR}/index.html"
    archivo_historico = f"{OUTPUT_DIR}/newsletter-{hoy.strftime('%Y-%m-%d')}.html"
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    with open(archivo_historico, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Newsletter generado: {archivo_salida}")
    print(f"📁 Copia histórica: {archivo_historico}")
    print()
    print("=" * 60)
    print("  ✨ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()
