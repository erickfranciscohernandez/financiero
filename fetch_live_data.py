#!/usr/bin/env python3
"""
Fetch indicadores macroeconómicos desde el Banco Central de Chile.

Prioridad:
  1. API oficial BCCh SI3  (requiere BCENTRAL_USER + BCENTRAL_PASS como secrets)
  2. mindicador.cl          (API pública que agrega datos del BCCh, sin auth)
  3. Datos mock             (fallback final)
"""
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# ── Credenciales BCCh (opcionales, configurar como GitHub Secrets) ──────────
BCENTRAL_USER = os.environ.get('BCENTRAL_USER', '')
BCENTRAL_PASS = os.environ.get('BCENTRAL_PASS', '')
BCENTRAL_URL  = 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx'

# Códigos de series BCCh SI3
BCENTRAL_SERIES = {
    'uf':  'F073.UF.PRE.Z.D',    # Unidad de Fomento
    'utm': 'F073.UTM.PRE.Z.M',   # Unidad Tributaria Mensual
}

# ── mindicador.cl (sin autenticación) ──────────────────────────────────────
MINDICADOR_URL = 'https://mindicador.cl/api'

MINDICADOR_SERIES = {
    'uf':     'uf',
    'utm':    'utm',
    'tpm':    'tpm',
    'imacec': 'imacec',
}


def _get(url, timeout=8):
    req = urllib.request.Request(url, headers={'User-Agent': 'FinancieroNewsletter/2.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


# ── Capa 1: BCCh SI3 API ───────────────────────────────────────────────────

def _bcentral_fetch(series_code):
    """Obtiene el último valor de una serie BCCh SI3."""
    if not BCENTRAL_USER or not BCENTRAL_PASS:
        return None
    today = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    params = urllib.parse.urlencode({
        'user':       BCENTRAL_USER,
        'pass':       BCENTRAL_PASS,
        'firstdate':  week_ago,
        'lastdate':   today,
        'timeseries': series_code,
        'function':   'GetSeries',
    })
    data = _get(f'{BCENTRAL_URL}?{params}')
    obs = data.get('Observaciones', {})
    # Tomar la última observación disponible
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
    """Intenta obtener todos los indicadores desde BCCh SI3."""
    resultado = {}
    for nombre, codigo in BCENTRAL_SERIES.items():
        try:
            d = _bcentral_fetch(codigo)
            if d:
                resultado[nombre] = d
        except Exception:
            pass
    return resultado


# ── Capa 2: mindicador.cl ─────────────────────────────────────────────────

def fetch_mindicador():
    """Obtiene indicadores desde mindicador.cl (agrega datos BCCh)."""
    resultado = {}
    for nombre, serie in MINDICADOR_SERIES.items():
        try:
            data = _get(f'{MINDICADOR_URL}/{serie}')
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


# ── Capa 3: Mock ──────────────────────────────────────────────────────────

MOCK_DATA = {
    'uf':     {'valor': 38120.0, 'fecha': datetime.now().strftime('%Y-%m-%d'), 'fuente': 'Simulado', 'mock': True},
    'utm':    {'valor': 66638.0, 'fecha': datetime.now().strftime('%Y-%m-%d'), 'fuente': 'Simulado', 'mock': True},
    'tpm':    {'valor': 4.75,    'fecha': datetime.now().strftime('%Y-%m-%d'), 'fuente': 'Simulado', 'mock': True},
    'imacec': {'valor': 4.1,     'fecha': datetime.now().strftime('%Y-%m-%d'), 'fuente': 'Simulado', 'mock': True},
}


# ── Orquestador principal ─────────────────────────────────────────────────

INDICADORES_META = {
    'uf':     {'label': 'UF',                        'unidad': '$', 'tipo': 'precio'},
    'utm':    {'label': 'UTM',                        'unidad': '$', 'tipo': 'precio'},
    'tpm':    {'label': 'TPM (Tasa Política Mon.)',   'unidad': '%', 'tipo': 'tasa'},
    'imacec': {'label': 'Imacec',                     'unidad': '%', 'tipo': 'porcentaje'},
}


def fetch_all_indicators():
    """Obtiene todos los indicadores con fallback en cascada."""
    print('\n📊 FETCH LIVE DATA — Banco Central de Chile\n')

    # Capa 1: BCCh SI3
    indicadores = {}
    if BCENTRAL_USER and BCENTRAL_PASS:
        print('🏦 Consultando API oficial BCCh SI3...')
        indicadores = fetch_bcentral()
        if indicadores:
            print(f'   ✅ BCCh SI3: {len(indicadores)} indicadores obtenidos')
        else:
            print('   ⚠️  BCCh SI3: sin resultados')
    else:
        print('   ℹ️  BCCh SI3: credenciales no configuradas (BCENTRAL_USER / BCENTRAL_PASS)')

    # Capa 2: mindicador.cl para los que faltan
    print('🌐 Consultando mindicador.cl (datos BCCh)...')
    mini = fetch_mindicador()
    for k, v in mini.items():
        if k not in indicadores:
            indicadores[k] = v

    if mini:
        nuevos = [k for k in mini if k not in indicadores or indicadores[k].get('fuente', '') == 'Simulado']
        print(f'   ✅ mindicador.cl: {len(mini)} indicadores disponibles')
    else:
        print('   ⚠️  mindicador.cl: sin respuesta')

    # Capa 3: mock para lo que aún falte
    for k, v in MOCK_DATA.items():
        if k not in indicadores:
            indicadores[k] = v

    # Enriquecer con metadata
    resultado = {
        'fecha':       datetime.now().isoformat(),
        'version':     'v5-bcentral',
        'indicadores': {},
    }
    for k, meta in INDICADORES_META.items():
        if k in indicadores:
            resultado['indicadores'][k] = {**meta, **indicadores[k]}

    # Guardar JSON
    with open('live_indicators.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    # Resumen en consola
    print('\n' + '='*60)
    print('📊 INDICADORES BANCO CENTRAL DE CHILE')
    print('='*60)
    for k, d in resultado['indicadores'].items():
        icono = '💰' if d['tipo'] == 'precio' else '📈'
        val = f"{d['unidad']}{d['valor']:,.2f}" if d['tipo'] == 'precio' else f"{d['valor']}%"
        mock_tag = ' ⚠️ (simulado)' if d.get('mock') else ''
        print(f'  {icono} {d["label"]:30} {val:>12}   {d["fecha"]}{mock_tag}')
    print('='*60)
    print(f'\n✅ Datos guardados en live_indicators.json')

    return resultado


if __name__ == '__main__':
    fetch_all_indicators()
