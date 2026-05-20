#!/usr/bin/env python3
"""
Generador de agenda de actividades
Agrega eventos e información de agendas cooperativas
"""
import json
from datetime import datetime, timedelta

AGENDA_EVENTS = {
    "icare": [
        {
            "fecha": "2026-06-03",
            "titulo": "Conoce a tu ministro: Martín Arrau, Ministro de Obras Públicas",
            "descripcion": "Encuentro directo con el Ministro de Obras Públicas para conocer sus iniciativas y políticas públicas.",
            "hora": "08:30",
            "tipo": "encuentro",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
        {
            "fecha": "2026-06-10",
            "titulo": "Conoce a tu ministro: Ximena Rincón, Ministra de Energía",
            "descripcion": "Encuentro con la Ministra de Energía para discutir políticas de energía renovable y sostenibilidad.",
            "hora": "08:30",
            "tipo": "encuentro",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
        {
            "fecha": "2026-06-24",
            "titulo": "Conoce a tu ministra: Ximena Lincolao, Ministra de Ciencia, Tecnología, Conocimiento e Innovación",
            "descripcion": "Encuentro con la Ministra de Ciencia y Tecnología para explorar iniciativas de innovación en Chile.",
            "hora": "08:30",
            "tipo": "encuentro",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
        {
            "fecha": "2026-06-18",
            "titulo": "El Pulso de la Economía Nacional: Claves del IPoM – Junio",
            "descripcion": "Análisis de la situación económica nacional con enfoque en el Informe de Política Monetaria de junio.",
            "hora": "08:00",
            "tipo": "seminario",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        }
    ],
    "cooperativas": [
        {
            "fecha": "2026-05-21",
            "titulo": "Asamblea General de Cooperativa Nacional",
            "descripcion": "Reunión anual de miembros para aprobación de estados financieros y dirección.",
            "hora": "18:00",
            "tipo": "asamblea",
            "enlace": "https://www.cooperativas.cl"
        },
        {
            "fecha": "2026-05-24",
            "titulo": "Foro de Cooperativismo Sostenible",
            "descripcion": "Encuentro de líderes cooperativos para discutir iniciativas de sostenibilidad.",
            "hora": "14:00",
            "tipo": "foro",
            "enlace": "https://www.cooperativas.cl/eventos"
        }
    ]
}


def generate_agenda_html():
    """Genera sección HTML con agenda de actividades ordenada por fecha"""

    html = """
    <div class="section">
        <h2 class="section-header">
            <span class="section-emoji">📅</span>
            Agenda de Actividades
        </h2>
        <span class="section-subtitle">Eventos próximos · Seminarios · Asambleas</span>

        <div class="agenda-container">
"""

    # Combinar todos los eventos y ordenar por fecha
    all_events = []

    # Agregar eventos de iCare con fuente
    for event in AGENDA_EVENTS.get('icare', []):
        event_copy = event.copy()
        event_copy['source'] = 'icare'
        all_events.append(event_copy)

    # Agregar eventos de cooperativas con fuente
    for event in AGENDA_EVENTS.get('cooperativas', []):
        event_copy = event.copy()
        event_copy['source'] = 'cooperativas'
        all_events.append(event_copy)

    # Ordenar por fecha (YYYY-MM-DD se ordena alfabéticamente correctamente)
    all_events.sort(key=lambda x: x['fecha'])

    # Agrupar por fuente para mostrar con encabezados
    html += '<div class="agenda-section"><h3>📅 iCare</h3>'
    icare_events = [e for e in all_events if e['source'] == 'icare']
    for event in icare_events:
        html += f'''
        <div class="agenda-item">
            <div class="agenda-date">
                <span class="agenda-day">{event['fecha']}</span>
                <span class="agenda-time">{event['hora']}</span>
            </div>
            <div class="agenda-content">
                <h4>{event['titulo']}</h4>
                <p>{event['descripcion']}</p>
                <div class="agenda-meta">
                    <span class="agenda-type">{event['tipo'].upper()}</span>
                    <a href="{event['enlace']}" target="_blank" class="agenda-link">Más info →</a>
                </div>
            </div>
        </div>
'''
    html += '</div>'

    # Agregar eventos cooperativas
    html += '<div class="agenda-section"><h3>🤝 Movimiento Cooperativo</h3>'
    coop_events = [e for e in all_events if e['source'] == 'cooperativas']
    for event in coop_events:
        html += f'''
        <div class="agenda-item">
            <div class="agenda-date">
                <span class="agenda-day">{event['fecha']}</span>
                <span class="agenda-time">{event['hora']}</span>
            </div>
            <div class="agenda-content">
                <h4>{event['titulo']}</h4>
                <p>{event['descripcion']}</p>
                <div class="agenda-meta">
                    <span class="agenda-type">{event['tipo'].upper()}</span>
                    <a href="{event['enlace']}" target="_blank" class="agenda-link">Más info →</a>
                </div>
            </div>
        </div>
'''
    html += '</div>'

    html += """
        </div>
    </div>
"""

    return html


def get_agenda_css():
    """Retorna estilos CSS para la agenda"""

    css = """
    /* AGENDA DE ACTIVIDADES */
    .agenda-container {
      display: flex;
      flex-direction: column;
      gap: 30px;
    }

    .agenda-section h3 {
      font-size: 16px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 16px;
      padding-bottom: 10px;
      border-bottom: 2px solid var(--rule);
    }

    .agenda-item {
      display: flex;
      gap: 20px;
      padding: 16px;
      background: var(--cream);
      border-radius: 4px;
      border-left: 4px solid var(--accent);
      margin-bottom: 12px;
      transition: all 0.2s;
    }

    .agenda-item:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      transform: translateX(4px);
    }

    .agenda-date {
      display: flex;
      flex-direction: column;
      gap: 4px;
      min-width: 80px;
      font-weight: 600;
    }

    .agenda-day {
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
    }

    .agenda-time {
      font-size: 14px;
      color: var(--accent);
      font-weight: 700;
    }

    .agenda-content h4 {
      font-size: 15px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 8px;
    }

    .agenda-content p {
      font-size: 14px;
      color: var(--ink);
      margin-bottom: 10px;
      line-height: 1.6;
    }

    .agenda-meta {
      display: flex;
      gap: 12px;
      align-items: center;
      font-size: 12px;
    }

    .agenda-type {
      background: var(--light-accent);
      color: var(--accent);
      padding: 4px 10px;
      border-radius: 12px;
      font-weight: 600;
    }

    .agenda-link {
      color: var(--accent);
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
    }

    .agenda-link:hover {
      text-decoration: underline;
    }

    @media (max-width: 768px) {
      .agenda-item {
        flex-direction: column;
        gap: 10px;
      }

      .agenda-date {
        flex-direction: row;
        gap: 10px;
        justify-content: space-between;
      }
    }
    """

    return css


if __name__ == '__main__':
    print("📅 Generador de Agenda\n")
    print(generate_agenda_html())
