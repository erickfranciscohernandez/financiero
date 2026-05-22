#!/usr/bin/env python3
"""
Sistema de Alertas y Envío de Newsletter por Email
Lee credenciales desde variables de entorno (secrets de GitHub Actions)
"""
import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_email_config():
    """Load email config from environment variables."""
    return {
        'smtp_server': os.environ.get('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.environ.get('EMAIL_SMTP_PORT', '587')),
        'sender_email': os.environ.get('EMAIL_FROM', ''),
        'sender_password': os.environ.get('EMAIL_PASSWORD', ''),
        'recipients': [r.strip() for r in os.environ.get('EMAIL_TO', '').split(',') if r.strip()],
        'alert_threshold': 8,
    }


def calculate_importance(text):
    """Score de importancia 1-10."""
    critical_words = [
        'crisis', 'colapso', 'emergencia', 'histórico',
        'sanciones', 'guerra', 'china', 'fed', 'bce',
        'reforma tributaria', 'cobre', 'litio', 'regulación',
    ]
    score = 5
    text_lower = text.lower()
    for word in critical_words:
        if word in text_lower:
            score += 2
    return min(score, 10)


def analyze_alerts(filepath='noticias_diarias.json'):
    """Analizar noticias y generar lista de alertas críticas."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        alerts = []
        for section, news_list in data.items():
            if isinstance(news_list, list):
                for news in news_list:
                    score = calculate_importance(
                        news.get('title', '') + ' ' + news.get('summary', '')
                    )
                    if score >= 8:
                        alerts.append({
                            'section': section,
                            'title': news.get('title', ''),
                            'summary': news.get('summary', '')[:200],
                            'source': news.get('source', ''),
                            'link': news.get('link', '#'),
                            'score': score,
                            'level': '🔴 CRÍTICO' if score >= 9 else '🟠 ALTO',
                        })
        return sorted(alerts, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        print(f'❌ Error analizando alertas: {e}')
        return []


def build_email_html(newsletter_html, alerts):
    """Usar el newsletter HTML completo como cuerpo del email."""
    try:
        with open(newsletter_html, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        pass

    # Fallback: solo alertas
    date_str = datetime.now().strftime('%d/%m/%Y')
    rows = ''
    for alert in alerts[:10]:
        rows += f"""
        <div style="background:#fff3e0;border-left:4px solid #e65100;padding:14px;margin:10px 0;border-radius:4px;">
          <span style="color:#e65100;font-weight:bold;">{alert['level']} · {alert['score']}/10</span>
          <div style="font-size:15px;font-weight:bold;color:#212121;margin:6px 0;">{alert['title']}</div>
          <p style="color:#555;margin:4px 0;">{alert['summary']}</p>
          <small style="color:#888;">📰 {alert['source']} &nbsp;
            <a href="{alert['link']}" style="color:#1565c0;">Leer →</a>
          </small>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:20px;">
  <div style="max-width:700px;margin:0 auto;background:#fff;border-radius:8px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#1a237e,#283593);color:#fff;padding:30px;text-align:center;">
      <h1 style="margin:0;font-size:24px;">Newsletter Estratégico</h1>
      <p style="margin:8px 0 0;opacity:.8;">{date_str} · Alertas Críticas</p>
    </div>
    <div style="padding:24px;">
      <p>Se detectaron <strong>{len(alerts)}</strong> alertas críticas:</p>
      {rows}
    </div>
    <div style="background:#f5f5f5;padding:16px;text-align:center;font-size:12px;color:#999;">
      Newsletter Estratégico &nbsp;·&nbsp;
      <a href="https://erickfranciscohernandez.github.io/financiero/newsletter.html"
         style="color:#1565c0;">Ver en línea</a>
    </div>
  </div>
</body>
</html>"""


def send_email(subject, html_body, config):
    """Enviar email usando SMTP. Retorna True si tuvo éxito."""
    if not config['sender_email'] or not config['sender_password']:
        print('⚠️  EMAIL_FROM / EMAIL_PASSWORD no configurados — email omitido')
        return False
    if not config['recipients']:
        print('⚠️  EMAIL_TO no configurado — email omitido')
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config['sender_email']
        msg['To'] = ', '.join(config['recipients'])
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.ehlo()
            server.starttls()
            server.login(config['sender_email'], config['sender_password'])
            server.sendmail(config['sender_email'], config['recipients'], msg.as_string())

        print(f'✅ Email enviado a: {", ".join(config["recipients"])}')
        return True

    except smtplib.SMTPAuthenticationError:
        print('❌ Error de autenticación SMTP. Verifica EMAIL_FROM y EMAIL_PASSWORD.')
        return False
    except Exception as e:
        print(f'❌ Error enviando email: {e}')
        return False


def create_alert_summary(alerts):
    """Guardar resumen de alertas en JSON."""
    try:
        current_date = datetime.now().strftime('%Y%m%d')
        filename = f'alerts_{current_date}.json'
        summary = {
            'fecha': datetime.now().isoformat(),
            'total_alertas': len(alerts),
            'alertas_criticas': len([a for a in alerts if a['score'] >= 9]),
            'alertas_altas': len([a for a in alerts if 7 <= a['score'] < 9]),
            'alertas': [
                {
                    'titulo': a['title'],
                    'seccion': a['section'],
                    'score': a['score'],
                    'nivel': a['level'],
                    'enlace': a['link'],
                }
                for a in alerts
            ],
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f'✅ Alertas guardadas: {filename}')
        return filename
    except Exception as e:
        print(f'❌ Error creando resumen: {e}')
        return None


def main():
    print('🎯 Sistema de Alertas y Envío de Newsletter\n')

    config = load_email_config()
    alerts = analyze_alerts()
    print(f'📊 {len(alerts)} alertas críticas detectadas\n')

    for i, alert in enumerate(alerts[:5], 1):
        print(f'{i}. {alert["level"]} ({alert["score"]}/10) — {alert["title"][:65]}')

    create_alert_summary(alerts)

    # Enviar newsletter completo por email
    date_str = datetime.now().strftime('%d/%m/%Y')
    subject = f'📊 Newsletter Estratégico — {date_str}'
    html_body = build_email_html('newsletter.html', alerts)

    print(f'\n📧 Enviando newsletter...')
    send_email(subject, html_body, config)

    print('\n✅ Sistema de alertas completado')


if __name__ == '__main__':
    main()
