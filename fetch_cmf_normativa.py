#!/usr/bin/env python3
"""
Fetcher de Normativa en Consulta — CMF Chile
https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php

Columnas: Tipo de Norma | Número | Materia | Inicio Consulta | Término Consulta
"""
import urllib.request
import urllib.error
import ssl
import re
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

CMF_NORMATIVA_URL = (
    'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
)

# Datos de respaldo — normativa representativa 03-jun-2026
MOCK_NORMATIVA = [
    {
        'tipo':   'Norma de Carácter General',
        'numero': 'NCG 513',
        'materia': 'Open Banking: estándar de APIs y requisitos de seguridad para proveedores de servicios financieros bajo Ley 21.521',
        'inicio': '02/06/2026',
        'termino': '02/07/2026',
    },
    {
        'tipo':   'Circular',
        'numero': 'N° 2.236',
        'materia': 'Publicación obligatoria de Costo Total del Crédito (CTC) en lenguaje ciudadano para bancos, cooperativas y emisores de tarjetas',
        'inicio': '03/06/2026',
        'termino': '03/07/2026',
    },
    {
        'tipo':   'Norma de Carácter General',
        'numero': 'NCG 512',
        'materia': 'Modifica requisitos de capital y liquidez para cooperativas de ahorro y crédito con activos superiores a UF 400.000',
        'inicio': '12/05/2026',
        'termino': '12/06/2026',
    },
    {
        'tipo':   'Circular',
        'numero': 'N° 2.235',
        'materia': 'Uso de inteligencia artificial en modelos de scoring crediticio: requisitos de explicabilidad, auditoría externa y no discriminación',
        'inicio': '28/05/2026',
        'termino': '28/06/2026',
    },
    {
        'tipo':   'Circular',
        'numero': 'N° 2.234',
        'materia': 'Transparencia en comisiones de fondos mutuos y de inversión: obligación de publicar Ratio de Gastos Total (TER) estandarizado',
        'inicio': '20/05/2026',
        'termino': '20/06/2026',
    },
    {
        'tipo':   'Resolución Exenta',
        'numero': 'N° 8.901',
        'materia': 'Gestión de riesgo climático y de transición: requerimientos de divulgación para compañías de seguros generales',
        'inicio': '02/06/2026',
        'termino': '17/06/2026',
    },
    {
        'tipo':   'Norma de Carácter General',
        'numero': 'NCG 514',
        'materia': 'Prevención de lavado de activos y financiamiento del terrorismo para operadores de activos digitales y exchanges bajo supervisión CMF',
        'inicio': '03/06/2026',
        'termino': '18/07/2026',
    },
]


def _strip_tags(text):
    return re.sub(r'<[^>]+>', '', text or '').strip()


def _fetch_normativa_html():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        CMF_NORMATIVA_URL,
        headers={
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-CL,es;q=0.9',
            'Referer': 'https://www.cmfchile.cl/',
        },
    )
    with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
        return r.read().decode('utf-8', errors='replace')


def _parse_normativa_bs4(html):
    """Extrae filas usando BeautifulSoup (más robusto que regex)."""
    soup = BeautifulSoup(html, 'lxml')
    rows = []
    # Buscar cualquier tabla con al menos 5 columnas
    for table in soup.find_all('table'):
        trs = table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) >= 5:
                row = {
                    'tipo':    tds[0].get_text(strip=True),
                    'numero':  tds[1].get_text(strip=True),
                    'materia': tds[2].get_text(strip=True),
                    'inicio':  tds[3].get_text(strip=True),
                    'termino': tds[4].get_text(strip=True),
                }
                # Ignorar filas vacías o encabezados que hayan quedado en <td>
                if row['tipo'] and row['numero'] and row['materia']:
                    rows.append(row)
        if rows:
            break
    return rows


def _parse_normativa_regex(html):
    """Extrae filas con regex — funciona aun sin <tbody> explícito."""
    rows = []
    # Intentar primero dentro de <tbody>
    tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL | re.IGNORECASE)
    search_zone = tbody_match.group(1) if tbody_match else html

    tr_list = re.findall(r'<tr[^>]*>(.*?)</tr>', search_zone, re.DOTALL | re.IGNORECASE)
    for tr in tr_list:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL | re.IGNORECASE)
        if len(tds) >= 5:
            row = {
                'tipo':    _strip_tags(tds[0]),
                'numero':  _strip_tags(tds[1]),
                'materia': _strip_tags(tds[2]),
                'inicio':  _strip_tags(tds[3]),
                'termino': _strip_tags(tds[4]),
            }
            if row['tipo'] and row['numero'] and row['materia']:
                rows.append(row)
    return rows


def _parse_normativa(html):
    """Extrae filas de la tabla de normativa en tramite."""
    if BS4_AVAILABLE:
        rows = _parse_normativa_bs4(html)
        if rows:
            return rows
    return _parse_normativa_regex(html)


def fetch_normativa():
    """Devuelve lista de normativas en consulta. Fallback a mock si CMF no responde."""
    try:
        html = _fetch_normativa_html()
        rows = _parse_normativa(html)
        if rows:
            print(f'   ✅ CMF normativa: {len(rows)} normas en consulta')
            return rows, False   # (datos, es_mock)
        print('   ⚠️  CMF normativa: tabla vacía, usando datos de referencia')
    except Exception as e:
        print(f'   ⚠️  CMF normativa: {e} — usando datos de referencia')
    return MOCK_NORMATIVA, True  # (datos, es_mock)


def generate_normativa_html():
    """Genera el bloque HTML completo del recuadro de normativa en consulta."""
    normas, es_mock = fetch_normativa()
    if not normas:
        return ''

    mock_badge = (
        '<span style="font-size:10px;color:#f59e0b;font-weight:600;margin-left:8px;">'
        '⚠ referencia</span>'
        if es_mock else ''
    )

    filas_html = ''
    for n in normas:
        filas_html += f"""
        <tr>
          <td class="cmf-tipo">{n['tipo']}</td>
          <td class="cmf-num">{n['numero']}</td>
          <td class="cmf-materia">{n['materia']}</td>
          <td class="cmf-fecha">{n['inicio']}</td>
          <td class="cmf-fecha">{n['termino']}</td>
        </tr>"""

    html = f"""
    <!-- NORMATIVA CMF EN CONSULTA -->
    <div class="cmf-normativa-box">
      <div class="cmf-norm-header">
        <span class="cmf-norm-icon">🏛️</span>
        <span class="cmf-norm-title">Normativa CMF en Consulta</span>
        {mock_badge}
        <a href="{CMF_NORMATIVA_URL}" target="_blank" class="cmf-norm-link">
          Ver en cmfchile.cl →
        </a>
      </div>
      <div class="cmf-table-wrap">
        <table class="cmf-table">
          <thead>
            <tr>
              <th>Tipo de Norma</th>
              <th>Número</th>
              <th>Materia</th>
              <th>Inicio Consulta</th>
              <th>Término Consulta</th>
            </tr>
          </thead>
          <tbody>
            {filas_html}
          </tbody>
        </table>
      </div>
    </div>
"""
    return html


def get_normativa_css():
    return """
    /* ── NORMATIVA CMF ───────────────────────────────────────── */
    .cmf-normativa-box {
      background: #fff;
      border-radius: 10px;
      border-left: 4px solid #1e40af;
      box-shadow: 0 2px 10px rgba(0,0,0,0.07);
      margin: 32px 0;
      overflow: hidden;
    }

    .cmf-norm-header {
      background: linear-gradient(90deg, #1e3a5f 0%, #1e40af 100%);
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .cmf-norm-icon { font-size: 18px; }

    .cmf-norm-title {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      flex: 1;
    }

    .cmf-norm-link {
      font-size: 11px;
      color: rgba(255,255,255,0.75);
      text-decoration: none;
      white-space: nowrap;
    }
    .cmf-norm-link:hover { color: #fff; text-decoration: underline; }

    .cmf-table-wrap { overflow-x: auto; }

    .cmf-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    .cmf-table thead tr {
      background: #f0f4ff;
    }

    .cmf-table th {
      padding: 10px 14px;
      text-align: left;
      font-size: 11px;
      font-weight: 700;
      color: #1e3a5f;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      white-space: nowrap;
      border-bottom: 2px solid #dbeafe;
    }

    .cmf-table tbody tr {
      border-bottom: 1px solid #f1f5f9;
      transition: background 0.15s;
    }
    .cmf-table tbody tr:last-child { border-bottom: none; }
    .cmf-table tbody tr:hover { background: #f8faff; }

    .cmf-table td {
      padding: 10px 14px;
      vertical-align: top;
      color: #374151;
      line-height: 1.5;
    }

    .cmf-tipo {
      font-size: 11px;
      font-weight: 600;
      color: #6b7280 !important;
      white-space: nowrap;
    }

    .cmf-num {
      font-weight: 700;
      color: #1e40af !important;
      white-space: nowrap;
    }

    .cmf-materia { min-width: 260px; }

    .cmf-fecha {
      white-space: nowrap;
      font-size: 12px;
      color: #6b7280 !important;
    }

    @media (max-width: 600px) {
      .cmf-table { font-size: 12px; }
      .cmf-table th, .cmf-table td { padding: 8px 10px; }
    }

    @media print {
      .cmf-normativa-box {
        border: 1px solid #1e40af;
        break-inside: avoid;
      }
    }
    """


if __name__ == '__main__':
    print('🏛️  Normativa CMF en Consulta\n')
    normas, mock = fetch_normativa()
    print(f'Fuente: {"Mock" if mock else "CMF live"} — {len(normas)} normas')
    for n in normas:
        print(f"  • [{n['numero']}] {n['materia'][:70]} ({n['inicio']} → {n['termino']})")
