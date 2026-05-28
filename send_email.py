#!/usr/bin/env python3
"""
Envía notificación de actualización del newsletter con indicadores y alertas del día
"""
import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

email_from     = os.environ.get('EMAIL_FROM', '')
email_password = os.environ.get('EMAIL_PASSWORD', '')
email_to_raw   = os.environ.get('EMAIL_TO', '')

if not all([email_from, email_password, email_to_raw]):
    print('⚠️  Secrets de email no configurados, omitiendo envío.')
    exit(0)

recipients = [e.strip() for e in email_to_raw.split(',') if e.strip()]
newsletter_url = 'https://erickfranciscohernandez.github.io/financiero/'
fecha = datetime.now().strftime('%d/%m/%Y')
hora  = datetime.now().strftime('%H:%M')


def _load_indicators():
    """Tabla HTML con los indicadores del día."""
    try:
        with open('live_indicators.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        ind = data.get('indicadores', {})
        icons = {'uf': '📐', 'utm': '🧾', 'tpm': '🏦', 'usd_clp': '💵'}
        rows = ''
        for key, meta in ind.items():
            icono     = icons.get(key, '•')
            label     = meta.get('label', key.upper())
            val       = meta.get('valor', 0)
            unidad    = meta.get('unidad', '')
            tipo      = meta.get('tipo', 'precio')
            fuente    = meta.get('fuente', '')
            mock      = meta.get('mock', False)
            valor_fmt = f"{val:.2f}%" if tipo == 'tasa' else f"{unidad}{val:,.2f}"
            fuente_txt = '⚠️ Simulado' if mock else fuente
            rows += f"""
            <tr style="border-bottom:1px solid #e5e7eb;">
              <td style="padding:10px 14px;font-size:20px;">{icono}</td>
              <td style="padding:10px 8px;font-size:14px;font-weight:600;color:#1a1a1a;">{label}</td>
              <td style="padding:10px 14px;font-size:16px;font-weight:700;color:#1e40af;text-align:right;">{valor_fmt}</td>
              <td style="padding:10px 14px;font-size:11px;color:#9ca3af;">{fuente_txt}</td>
            </tr>"""
        return rows
    except Exception:
        return '<tr><td colspan="4" style="padding:10px;color:#9ca3af;">No disponible</td></tr>'


def _load_alerts():
    """Filas HTML con alertas críticas del día."""
    try:
        today = datetime.now().strftime('%Y%m%d')
        with open(f'alerts_{today}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        alertas = data.get('alertas', [])[:5]
        if not alertas:
            return ''
        rows = ''
        for a in alertas:
            nivel  = a.get('nivel', '🔴 CRÍTICO')
            score  = a.get('score', 0)
            titulo = a.get('titulo', '')
            enlace = a.get('enlace', '#')
            color  = '#dc2626' if '🔴' in nivel else '#ea580c'
            rows += f"""
            <tr style="border-bottom:1px solid #fecaca;">
              <td style="padding:10px 14px;">
                <span style="font-size:11px;font-weight:700;color:{color};">{nivel} · {score}/10</span><br>
                <a href="{enlace}" target="_blank"
                   style="font-size:13px;font-weight:600;color:#1a1a1a;text-decoration:none;">
                  {titulo}
                </a>
              </td>
            </tr>"""
        return rows
    except Exception:
        return ''


indicator_rows = _load_indicators()
alert_rows     = _load_alerts()

alerts_section = f"""
    <!-- Alertas críticas -->
    <div style="margin-top:24px;">
      <div style="background:#fef2f2;border-radius:6px;overflow:hidden;">
        <div style="background:#dc2626;padding:10px 14px;">
          <span style="font-size:12px;font-weight:800;color:#fff;letter-spacing:0.08em;
                       text-transform:uppercase;">🚨 Alertas Críticas del Día</span>
        </div>
        <table style="width:100%;border-collapse:collapse;">
          {alert_rows}
        </table>
      </div>
    </div>
""" if alert_rows else ''

subject = f'🔔 El Despacho actualizado · {fecha} {hora} UTC'

html_body = f"""
<html>
<body style="font-family:Arial,sans-serif;max-width:620px;margin:0 auto;padding:20px;background:#f4f4f4;">

  <!-- Cabecera -->
  <div style="background:#1e3a5f;border-radius:8px 8px 0 0;padding:24px 32px;">
    <h1 style="color:#fff;font-family:Georgia,serif;font-size:26px;margin:0 0 4px;">El Despacho</h1>
    <p style="color:rgba(255,255,255,0.65);font-size:12px;margin:0;letter-spacing:0.1em;text-transform:uppercase;">
      Newsletter Estratégico · Actualización {fecha} · {hora} UTC
    </p>
  </div>

  <!-- Cuerpo -->
  <div style="background:#fff;padding:28px 32px;border-left:1px solid #e5e7eb;border-right:1px solid #e5e7eb;">

    <p style="color:#374151;font-size:15px;line-height:1.7;margin-top:0;">
      Tu newsletter ha sido <strong>actualizado automáticamente</strong>. A continuación los
      indicadores macroeconómicos vigentes y las alertas del día:
    </p>

    <!-- Tabla indicadores -->
    <table style="width:100%;border-collapse:collapse;margin:20px 0;background:#f8faff;border-radius:8px;overflow:hidden;">
      <thead>
        <tr style="background:#1e40af;">
          <th colspan="4" style="padding:10px 14px;text-align:left;color:#fff;font-size:12px;
                                  letter-spacing:0.08em;text-transform:uppercase;">
            📊 Indicadores del día
          </th>
        </tr>
      </thead>
      <tbody>
        {indicator_rows}
      </tbody>
    </table>

    {alerts_section}

    <!-- Botón CTA -->
    <div style="text-align:center;margin:32px 0 20px;">
      <a href="{newsletter_url}"
         style="background:#8b1a1a;color:#fff;padding:15px 44px;text-decoration:none;
                font-size:15px;font-weight:bold;border-radius:4px;display:inline-block;">
        Ver Newsletter completo →
      </a>
    </div>

  </div>

  <!-- Pie -->
  <div style="background:#f9fafb;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;
              padding:14px 32px;text-align:center;">
    <p style="color:#9ca3af;font-size:11px;margin:0;">
      El Despacho · Newsletter Estratégico · Actualización automática cada 4 horas<br>
      Este boletín es de carácter informativo y no constituye asesoría de inversión.
    </p>
  </div>

</body>
</html>
"""

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From']    = email_from
msg['To']      = ', '.join(recipients)
msg.attach(MIMEText(html_body, 'html'))

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_from, email_password)
        server.sendmail(email_from, recipients, msg.as_string())
    print(f'✅ Notificación enviada a: {", ".join(recipients)}')
except Exception as e:
    print(f'❌ Error enviando email: {e}')
    exit(1)
