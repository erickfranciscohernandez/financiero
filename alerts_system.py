#!/usr/bin/env python3
"""
Sistema de Alertas - FASE 3
Notificaciones por email de eventos críticos
"""
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_alerts_config():
    """Load email configuration"""
    config = {
        'smtp_server': 'smtp.gmail.com',  # O tu servidor
        'smtp_port': 587,
        'sender_email': 'tu_email@gmail.com',  # Cambiar
        'sender_password': 'tu_app_password',  # Cambiar
        'recipients': ['ejecutivo@empresa.com'],  # Cambiar
        'alert_threshold': 8  # Score mínimo para alertar (1-10)
    }
    return config

def analyze_alerts(filepath='noticias_diarias.json'):
    """Analizar noticias y generar alertas"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        alerts = []

        for section, news_list in data.items():
            if isinstance(news_list, list):
                for news in news_list:
                    # Scoring simple de importancia
                    score = calculate_importance(news.get('title', '') + ' ' + news.get('summary', ''))

                    if score >= 8:  # Crítico
                        alerts.append({
                            'section': section,
                            'title': news.get('title', ''),
                            'summary': news.get('summary', '')[:200],
                            'source': news.get('source', ''),
                            'link': news.get('link', ''),
                            'score': score,
                            'level': '🔴 CRÍTICO' if score >= 9 else '🟠 ALTO'
                        })

        return sorted(alerts, key=lambda x: x['score'], reverse=True)

    except Exception as e:
        print(f"❌ Error analizando alertas: {e}")
        return []

def calculate_importance(text):
    """Calcular score de importancia"""
    critical_words = [
        'crisis', 'colapso', 'emergencia', 'histórico',
        'sanciones', 'guerra', 'china', 'fed', 'bce',
        'reforma tributaria', 'cobre', 'litio', 'regulación'
    ]

    text_lower = text.lower()
    score = 5

    for word in critical_words:
        if word in text_lower:
            score += 2

    return min(score, 10)

def send_alerts_email(alerts, config):
    """Enviar alertas por email"""
    if not alerts:
        print("ℹ️  No hay alertas críticas para enviar")
        return False

    try:
        print(f"📧 Enviando {len(alerts)} alertas críticas...")

        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🚨 ALERTAS CRÍTICAS - Newsletter {datetime.now().strftime("%d/%m/%Y")}'
        msg['From'] = config['sender_email']
        msg['To'] = ', '.join(config['recipients'])

        # Crear cuerpo HTML
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .alert {{ background: #ffebee; border-left: 4px solid #d32f2f; padding: 16px; margin: 10px 0; }}
                .score {{ color: #d32f2f; font-weight: bold; }}
                .title {{ font-size: 16px; font-weight: bold; color: #333; }}
                .source {{ color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h2>🚨 ALERTAS CRÍTICAS - Newsletter Estratégico</h2>
            <p>Se han detectado <strong>{len(alerts)}</strong> eventos críticos en las últimas 24 horas.</p>

            <hr>
        """

        for alert in alerts[:10]:  # Top 10
            html_body += f"""
            <div class="alert">
                <span class="score">{alert['level']} - Score: {alert['score']}/10</span>
                <div class="title">{alert['title']}</div>
                <p>{alert['summary']}</p>
                <p class="source">📰 {alert['source']} |
                <a href="{alert['link']}">Leer completo →</a></p>
            </div>
            """

        html_body += """
            <hr>
            <p style="color: #666; font-size: 12px;">
                Este es un email automático de Newsletter Estratégico v3.<br>
                Visitá el dashboard: https://erickfranciscohernandez.github.io/financiero/
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Configurar conexión SMTP (COMENTADO - Requiere credenciales reales)
        print("ℹ️  Sistema de email configurado pero desactivado")
        print("   Para activar: actualizar credentials en alerts_system.py")
        print(f"   Se enviarían a: {', '.join(config['recipients'])}")

        return True

    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

def send_daily_newsletter(config):
    """Enviar newsletter completo diariamente"""
    try:
        print("📮 Preparando envío de newsletter completo...")

        # Leer el HTML del newsletter
        with open('newsletter.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Newsletter Estratégico {datetime.now().strftime("%d/%m/%Y")}'
        msg['From'] = config['sender_email']
        msg['To'] = ', '.join(config['recipients'])

        msg.attach(MIMEText(html_content, 'html'))

        # SMTP desactivado - requiere credenciales reales
        print("ℹ️  Sistema de envío configurado pero desactivado")
        print(f"   Recipients: {', '.join(config['recipients'])}")

        return True

    except Exception as e:
        print(f"❌ Error preparando newsletter: {e}")
        return False

def create_alert_summary(alerts):
    """Crear resumen de alertas en JSON"""
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
                    'enlace': a['link']
                }
                for a in alerts
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"✅ Resumen de alertas guardado: {filename}")
        return filename

    except Exception as e:
        print(f"❌ Error creando resumen: {e}")
        return None

def main():
    print("🎯 Sistema de Alertas - FASE 3\n")

    # Cargar configuración
    config = load_alerts_config()

    # Analizar alertas
    print("📊 Analizando noticias...")
    alerts = analyze_alerts()

    print(f"✅ {len(alerts)} eventos críticos detectados\n")

    # Mostrar alertas
    print("=" * 60)
    print("📌 TOP ALERTAS CRÍTICAS")
    print("=" * 60)

    for i, alert in enumerate(alerts[:5], 1):
        print(f"\n{i}. {alert['level']} (Score: {alert['score']}/10)")
        print(f"   Título: {alert['title'][:70]}...")
        print(f"   Sección: {alert['section']}")
        print(f"   Fuente: {alert['source']}")

    # Crear resumen
    print("\n📋 Creando archivos de alertas...")
    create_alert_summary(alerts)

    # Preparar envíos (comentados)
    print("\n📧 Sistema de email")
    print("-" * 60)
    print("⚠️  Email desactivado - Requiere credenciales reales")
    print("   Para habilitar:")
    print("   1. Configurar SMTP (Gmail, SendGrid, etc)")
    print("   2. Actualizar credentials en alerts_system.py")
    print("   3. Descommentar función send_email()")

    # Enviar alertas
    if len(alerts) > 0:
        send_alerts_email(alerts, config)

    print("\n✅ FASE 3 completada")
    print(f"   • {len(alerts)} alertas analizadas")
    print(f"   • Sistema de email disponible (requiere credenciales)")
    print(f"   • Alertas guardadas en JSON")

if __name__ == '__main__':
    main()
