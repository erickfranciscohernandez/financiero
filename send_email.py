#!/usr/bin/env python3
"""
Envía email diario con link al newsletter
"""
import smtplib
import os
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

subject = f'📰 El Despacho · Newsletter Estratégico — {fecha}'

html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #faf8f3;">
  <div style="border-top: 4px solid #8b1a1a; padding-top: 20px; background: white; padding: 30px;">
    <h2 style="color: #1a1a1a; font-size: 28px; margin-bottom: 4px; font-family: Georgia, serif;">El Despacho</h2>
    <p style="color: #8a8a8a; font-size: 12px; margin: 0; text-transform: uppercase; letter-spacing: 0.1em;">Newsletter Estratégico · {fecha}</p>
    <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
    <p style="color: #1a1a1a; font-size: 16px; line-height: 1.6;">
      Tu newsletter del día está listo. Análisis ejecutivo de geopolítica,
      mercados financieros, Chile estratégico, tecnología e inteligencia artificial.
    </p>
    <div style="text-align: center; margin: 35px 0;">
      <a href="{newsletter_url}"
         style="background: #8b1a1a; color: white; padding: 16px 40px;
                text-decoration: none; font-size: 16px; font-weight: bold;
                border-radius: 3px; display: inline-block;">
        Ver Newsletter →
      </a>
    </div>
    <p style="color: #8a8a8a; font-size: 13px; text-align: center;">
      Generado a las {hora} UTC · Actualizado automáticamente
    </p>
    <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
    <p style="color: #aaa; font-size: 11px; text-align: center;">
      El Despacho · Newsletter Estratégico<br>
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
    print(f'✅ Email enviado a: {", ".join(recipients)}')
except Exception as e:
    print(f'❌ Error enviando email: {e}')
    exit(1)
