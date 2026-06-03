#!/usr/bin/env python3
"""
Fetch indicadores macroeconómicos.

Prioridad para UF:
  1. SII (sii.cl)          — tabla mensual oficial
  2. BCCh SI3              — requiere BCENTRAL_USER + BCENTRAL_PASS
  3. mindicador.cl         — API pública sin auth
  4. Datos mock            — fallback final

Resto de indicadores (UTM, TPM, Imacec):
  1. BCCh SI3  →  2. mindicador.cl  →  3. mock
"""
import os
import re
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# ── Credenciales BCCh (opcionales) ───────────────────────────────────────────
BCENTRAL_USER = os.environ.get('BCENTRAL_USER', '')
BCENTRAL_PASS = os.environ.get('BCENTRAL_PASS', '')
BCENTRAL_URL  = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx'

BCENTRAL_SERIES = {
    'utm':     'F073.UTM.PRE.Z.M',
    'usd_clp': 'F073.TCO.PRE.Z.D',   # Dólar observado
}

MINDICADOR_URL = 'https://mindicador.cl/api'

MINDICADOR_SERIES = {
    'uf':      'uf',
    'utm':     'utm',
    'tpm':     'tpm',
    'usd_clp': 'dolar',
}


def _get_html(url, timeout=10):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-CL,es;q=0.9',
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')


def _get_json(url, timeout=8):
    req = urllib.request.Request(url, headers={'User-Agent': 'FinancieroNewsletter/2.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


# ── Capa 1 (UF): SII ─────────────────────────────────────────────────────────

def _sii_scrape(url, rango_min, rango_max, es_mensual=False):
    """Extrae el valor vigente de una página de tabla SII.

    es_mensual=True: toma el valor del mes actual (UTM).
    es_mensual=False: toma el valor del día actual (UF).
    """
    month = datetime.now().month
    day   = datetime.now().day

    html = _get_html(url)

    month_names = ['enero','febrero','marzo','abril','mayo','junio',
                   'julio','agosto','septiembre','octubre','noviembre','diciembre']
    mes_nombre = month_names[month - 1]

    idx = html.lower().find(mes_nombre)
    if idx == -1:
        return None

    bloque = html[idx:idx + 3000]
    valores = re.findall(r'(\d{2}[.\s]\d{3}[,.]\d{2})', bloque)
    if not valores:
        return None

    if es_mensual:
        # UTM: un valor por mes — tomar el primero del bloque
        idx_val = 0
    else:
        # UF: un valor por día
        idx_val = min(day - 1, len(valores) - 1)

    valor_str = valores[idx_val].replace('.', '').replace(',', '.').replace(' ', '')
    try:
        valor = float(valor_str)
        if rango_min < valor < rango_max:
            return {
                'valor':  valor,
                'fecha':  datetime.now().strftime('%Y-%m-%d'),
                'fuente': 'SII (sii.cl)',
            }
    except ValueError:
        pass
    return None


def fetch_uf_sii():
    """Obtiene el valor diario de la UF desde sii.cl."""
    year = datetime.now().year
    return _sii_scrape(
        url       = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm',
        rango_min = 30000,
        rango_max = 50000,
        es_mensual= False,
    )


def fetch_utm_sii():
    """Obtiene el valor mensual de la UTM desde sii.cl."""
    year = datetime.now().year
    return _sii_scrape(
        url       = f'https://www.sii.cl/valores_y_fechas/utm/utm{year}.htm',
        rango_min = 60000,
        rango_max = 120000,
        es_mensual= True,
    )


def fetch_usd_sii():
    """Obtiene el valor diario del dólar observado desde sii.cl."""
    year = datetime.now().year
    return _sii_scrape(
        url       = f'https://www.sii.cl/valores_y_fechas/dolar/dolar{year}.htm',
        rango_min = 700,
        rango_max = 1200,
        es_mensual= False,
    )


# ── Capa 2: BCCh SI3 ─────────────────────────────────────────────────────────

def _bcentral_fetch(series_code):
    if not BCENTRAL_USER or not BCENTRAL_PASS:
        return None
    today    = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    params = urllib.parse.urlencode({
        'user': BCENTRAL_USER, 'pass': BCENTRAL_PASS,
        'firstdate': week_ago, 'lastdate': today,
        'timeseries': series_code, 'function': 'GetSeries',
    })
    data = _get_json(f'{BCENTRAL_URL}?{params}')
    obs  = data.get('Observaciones', {})
    for key in sorted(obs.keys(), reverse=True):
        val = obs[key].get('value', '')
        if val and val not in ('.', 'N/E', ''):
            return {
                'valor':  float(val.replace(',', '.')),
                'fecha':  obs[key].get('indexDateString', today),
                'fuente': 'Banco Central de Chile',
            }
    return None


def fetch_bcentral():
    resultado = {}
    for nombre, codigo in BCENTRAL_SERIES.items():
        try:
            d = _bcentral_fetch(codigo)
            if d:
                resultado[nombre] = d
        except Exception:
            pass
    return resultado


# ── Capa 3: mindicador.cl ────────────────────────────────────────────────────

def fetch_mindicador():
    resultado = {}
    for nombre, serie in MINDICADOR_SERIES.items():
        try:
            data = _get_json(f'{MINDICADOR_URL}/{serie}')
            series_list = data.get('serie', [])
            if series_list:
                ultimo = series_list[0]
                resultado[nombre] = {
                    'valor':  float(ultimo['valor']),
                    'fecha':  ultimo['fecha'][:10],
                    'fuente': 'Banco Central de Chile vía mindicador.cl',
                }
        except Exception:
            pass
    return resultado


# ── Capa 4: Mock ─────────────────────────────────────────────────────────────

MOCK_DATA = {
    'uf':      {'valor': 40644.55, 'fecha': '2026-06-03', 'fuente': 'SII (03-jun-2026)', 'mock': True},
    'utm':     {'valor': 71506.0,  'fecha': '2026-06-03', 'fuente': 'BCCh (03-jun-2026)', 'mock': True},
    'tpm':     {'valor': 4.50,     'fecha': '2026-06-03', 'fuente': 'BCCh (03-jun-2026)', 'mock': True},
    'usd_clp': {'valor': 888.00,   'fecha': '2026-06-03', 'fuente': 'BCCh SI3 (03-jun-2026)', 'mock': True},
}

INDICADORES_META = {
    'uf':      {'label': 'UF',                      'unidad': '$',   'tipo': 'precio'},
    'utm':     {'label': 'UTM',                      'unidad': '$',   'tipo': 'precio'},
    'tpm':     {'label': 'TPM (Tasa Política Mon.)', 'unidad': '%',   'tipo': 'tasa'},
    'usd_clp': {'label': 'Dólar observado',          'unidad': '$',   'tipo': 'precio'},
}


# ── Orquestador ──────────────────────────────────────────────────────────────

def fetch_all_indicators():
    print('\n📊 FETCH LIVE DATA\n')
    indicadores = {}

    # UF: SII primero
    print('🏛️  Consultando UF en sii.cl...')
    try:
        uf = fetch_uf_sii()
        if uf:
            indicadores['uf'] = uf
            print(f'   ✅ UF desde SII: ${uf["valor"]:,.2f}')
        else:
            print('   ⚠️  SII: sin resultado, usando fallback')
    except Exception as e:
        print(f'   ⚠️  SII: {e}')

    # Dólar: SII primero
    print('🏛️  Consultando dólar en sii.cl...')
    try:
        usd = fetch_usd_sii()
        if usd:
            indicadores['usd_clp'] = usd
            print(f'   ✅ Dólar desde SII: ${usd["valor"]:,.2f}')
        else:
            print('   ⚠️  SII: sin resultado, usando fallback')
    except Exception as e:
        print(f'   ⚠️  SII dólar: {e}')

    # UTM: SII primero
    print('🏛️  Consultando UTM en sii.cl...')
    try:
        utm = fetch_utm_sii()
        if utm:
            indicadores['utm'] = utm
            print(f'   ✅ UTM desde SII: ${utm["valor"]:,.0f}')
        else:
            print('   ⚠️  SII: sin resultado, usando fallback')
    except Exception as e:
        print(f'   ⚠️  SII UTM: {e}')

    # BCCh SI3 para lo que falte
    if BCENTRAL_USER and BCENTRAL_PASS:
        print('🏦 Consultando BCCh SI3...')
        bcentral = fetch_bcentral()
        for k, v in bcentral.items():
            if k not in indicadores:
                indicadores[k] = v
        if bcentral:
            print(f'   ✅ BCCh SI3: {len(bcentral)} indicadores')
    else:
        print('   ℹ️  BCCh SI3: sin credenciales (BCENTRAL_USER / BCENTRAL_PASS)')

    # mindicador.cl para lo que falta
    print('🌐 Consultando mindicador.cl...')
    mini = fetch_mindicador()
    for k, v in mini.items():
        if k not in indicadores:
            indicadores[k] = v
    if mini:
        print(f'   ✅ mindicador.cl: {len(mini)} indicadores disponibles')
    else:
        print('   ⚠️  mindicador.cl: sin respuesta')

    # Mock para lo que aún falte
    for k, v in MOCK_DATA.items():
        if k not in indicadores:
            indicadores[k] = v

    resultado = {
        'fecha':       datetime.now().isoformat(),
        'version':     'v6-sii',
        'indicadores': {},
    }
    for k, meta in INDICADORES_META.items():
        if k in indicadores:
            resultado['indicadores'][k] = {**meta, **indicadores[k]}

    with open('live_indicators.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print('\n' + '='*60)
    print('📊 INDICADORES')
    print('='*60)
    for k, d in resultado['indicadores'].items():
        icono  = '💰' if d['tipo'] == 'precio' else '📈'
        val    = f"{d['unidad']}{d['valor']:,.2f}" if d['tipo'] == 'precio' else f"{d['valor']}%"
        origen = ' ⚠️ (simulado)' if d.get('mock') else f"  ← {d['fuente']}"
        print(f'  {icono} {d["label"]:30} {val:>12}{origen}')
    print('='*60)
    print('\n✅ Datos guardados en live_indicators.json')
    return resultado


# ── Compatibilidad con generate_newsletter_v4.py ─────────────────────────────

class LiveDataFetcher:
    def get_all_indicators(self):
        return fetch_all_indicators()


def generate_chart_data(indicators):
    return {k: v for k, v in indicators.get('indicadores', {}).items()}


if __name__ == '__main__':
    fetch_all_indicators()
