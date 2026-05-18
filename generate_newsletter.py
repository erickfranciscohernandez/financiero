#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timedelta
from urllib.parse import quote

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
REPO_OWNER = 'erickfranciscohernandez'
REPO_NAME = 'financiero'
API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits'

def get_commits_from_last_day():
    """Fetch commits from the last 24 hours"""
    since_date = (datetime.utcnow() - timedelta(days=1)).isoformat() + 'Z'

    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'

    params = {
        'since': since_date,
        'per_page': 30
    }

    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def format_commit(commit):
    """Format a single commit for display"""
    author = commit['commit']['author']['name']
    message = commit['commit']['message'].split('\n')[0]
    date = datetime.fromisoformat(commit['commit']['author']['date'].replace('Z', '+00:00'))
    url = commit['html_url']
    sha_short = commit['sha'][:7]

    return {
        'author': author,
        'message': message,
        'date': date.strftime('%Y-%m-%d %H:%M'),
        'url': url,
        'sha': sha_short
    }

def generate_html(commits):
    """Generate newsletter HTML with commits"""
    current_date = datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo')

    commits_html = ''
    if commits:
        for commit in commits:
            commits_html += f'''
    <div class="news-item">
      <div class="news-date">{commit['date']}</div>
      <h3 class="news-title">{commit['message']}</h3>
      <p class="news-meta">Por <strong>{commit['author']}</strong> • <a href="{commit['url']}" style="color: var(--accent); text-decoration: none;">{commit['sha']}</a></p>
    </div>'''
    else:
        commits_html = '''
    <div class="news-item">
      <p style="color: var(--muted); font-style: italic;">No hay commits en las últimas 24 horas.</p>
    </div>'''

    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Newsletter Estratégico — {current_date}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #0d0d0d;
    --paper: #f5f0e8;
    --cream: #ede7d5;
    --accent: #c0392b;
    --gold: #b8860b;
    --steel: #2c3e50;
    --muted: #6b6457;
    --rule: #c9b99a;
    --tag-bg: #0d0d0d;
    --tag-text: #f5f0e8;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: var(--paper);
    color: var(--ink);
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 15px;
    line-height: 1.7;
    max-width: 780px;
    margin: 0 auto;
    padding: 40px 24px 80px;
  }}

  .masthead {{
    border-top: 3px solid var(--ink);
    border-bottom: 1px solid var(--rule);
    padding: 20px 0 14px;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}

  .masthead-title {{
    font-family: 'Playfair Display', serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--steel);
  }}

  .masthead-meta {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    text-align: right;
    line-height: 1.5;
  }}

  .edition-bar {{
    background: var(--ink);
    color: var(--paper);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 5px 10px;
    display: inline-block;
    margin-bottom: 28px;
  }}

  .headline-block {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 28px;
  }}

  .headline-block h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 900;
    line-height: 1.2;
    color: var(--ink);
    margin-bottom: 10px;
  }}

  .headline-block .deck {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 14px;
    font-weight: 300;
    color: var(--muted);
    font-style: italic;
    line-height: 1.5;
  }}

  .exec-summary {{
    background: var(--cream);
    border: 1px solid var(--rule);
    padding: 20px 24px;
    margin-bottom: 32px;
    border-radius: 2px;
  }}

  .exec-summary h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ink);
    margin-bottom: 12px;
  }}

  .exec-summary p {{
    font-size: 14px;
    line-height: 1.7;
    color: var(--ink);
  }}

  .exec-summary p + p {{
    margin-top: 10px;
  }}

  .news-section {{
    margin-bottom: 40px;
  }}

  .news-section h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--rule);
  }}

  .news-item {{
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--rule);
  }}

  .news-item:last-child {{
    border-bottom: none;
  }}

  .news-date {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
  }}

  .news-title {{
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
    line-height: 1.3;
  }}

  .news-meta {{
    font-size: 13px;
    color: var(--muted);
    font-style: italic;
  }}

  .footer {{
    border-top: 1px solid var(--rule);
    padding-top: 20px;
    margin-top: 40px;
    font-size: 12px;
    color: var(--muted);
    text-align: center;
  }}

  a {{
    color: var(--accent);
    text-decoration: none;
  }}

  a:hover {{
    text-decoration: underline;
  }}
</style>
</head>
<body>
  <div class="masthead">
    <div class="masthead-title">Financiero Newsletter</div>
    <div class="masthead-meta">
      {current_date}<br>
      EDICIÓN DIARIA
    </div>
  </div>

  <div class="edition-bar">Actualización de Commits</div>

  <div class="headline-block">
    <h1>Resumen de Actividad</h1>
    <p class="deck">Commits y cambios en el repositorio {REPO_OWNER}/{REPO_NAME}</p>
  </div>

  <div class="exec-summary">
    <h2>Resumen Ejecutivo</h2>
    <p>Se han detectado <strong>{len(commits)}</strong> cambios en el repositorio en las últimas 24 horas. Este newsletter se genera automáticamente basado en la actividad del repositorio en GitHub.</p>
  </div>

  <div class="news-section">
    <h2>Commits Recientes</h2>
    {commits_html}
  </div>

  <div class="footer">
    <p>Este newsletter se genera automáticamente diariamente.</p>
    <p><a href="https://github.com/{REPO_OWNER}/{REPO_NAME}">Ver en GitHub</a></p>
  </div>
</body>
</html>'''

    return html_content

def main():
    try:
        print(f'Obteniendo commits del repositorio {REPO_OWNER}/{REPO_NAME}...')
        commits = get_commits_from_last_day()
        commits_formatted = [format_commit(c) for c in commits]

        print(f'Se encontraron {len(commits_formatted)} commits')

        html = generate_html(commits_formatted)

        output_file = 'newsletter.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'Newsletter generado exitosamente en {output_file}')

    except Exception as e:
        print(f'Error: {e}')
        raise

if __name__ == '__main__':
    main()
