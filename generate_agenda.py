#!/usr/bin/env python3
"""
Generador de agenda de actividades — banner horizontal
"""
from datetime import datetime

AGENDA_EVENTS = {
    "icare": [
        {
            "fecha": "2026-06-03",
            "titulo": "Conoce a tu ministro: Martín Arrau, Ministro de Obras Públicas",
            "descripcion": "Encuentro directo con el Ministro de Obras Públicas.",
            "hora": "08:30",
            "tipo": "encuentro",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
        {
            "fecha": "2026-06-10",
            "titulo": "Conoce a tu ministro: Ximena Rincón, Ministra de Energía",
            "descripcion": "Encuentro con la Ministra de Energía sobre renovables y sostenibilidad.",
            "hora": "08:30",
            "tipo": "encuentro",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
        {
            "fecha": "2026-06-18",
            "titulo": "El Pulso de la Economía Nacional: Claves del IPoM – Junio",
            "descripcion": "Análisis del Informe de Política Monetaria de junio.",
            "hora": "08:00",
            "tipo": "seminario",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
        {
            "fecha": "2026-06-24",
            "titulo": "Conoce a tu ministra: Ximena Lincolao, Ministra de Ciencia e Innovación",
            "descripcion": "Encuentro con la Ministra de Ciencia y Tecnología.",
            "hora": "08:30",
            "tipo": "encuentro",
            "enlace": "https://www.icare.cl/agenda-de-actividades/"
        },
    ],
    "cooperativas": [
        {
            "fecha": "2026-06-12",
            "titulo": "Asamblea General de Cooperativa Nacional",
            "descripcion": "Reunión anual de miembros para aprobación de estados financieros.",
            "hora": "18:00",
            "tipo": "asamblea",
            "enlace": "https://www.cooperativas.cl"
        },
        {
            "fecha": "2026-06-20",
            "titulo": "Foro de Cooperativismo Sostenible",
            "descripcion": "Encuentro de líderes cooperativos sobre sostenibilidad.",
            "hora": "14:00",
            "tipo": "foro",
            "enlace": "https://www.cooperativas.cl/eventos"
        },
    ]
}

TYPE_COLORS = {
    "encuentro": "#2563eb",
    "seminario": "#7c3aed",
    "asamblea":  "#b45309",
    "foro":      "#059669",
}

TYPE_ICONS = {
    "encuentro": "🤝",
    "seminario": "🎓",
    "asamblea":  "🏛️",
    "foro":      "💬",
}


def _format_date(fecha_str):
    """Convierte '2026-06-03' a '3 Jun'"""
    try:
        d = datetime.strptime(fecha_str, "%Y-%m-%d")
        meses = ['Ene','Feb','Mar','Abr','May','Jun',
                 'Jul','Ago','Sep','Oct','Nov','Dic']
        return f"{d.day} {meses[d.month - 1]}"
    except Exception:
        return fecha_str


def generate_agenda_html():
    """Banner horizontal con próximos eventos, ordenados por fecha."""

    today = datetime.now().strftime("%Y-%m-%d")

    # Reunir todos los eventos futuros (o del día)
    all_events = []
    for source, events in AGENDA_EVENTS.items():
        for ev in events:
            if ev["fecha"] >= today:
                ev_copy = ev.copy()
                ev_copy["source"] = source
                all_events.append(ev_copy)

    all_events.sort(key=lambda x: x["fecha"])
    upcoming = all_events[:6]   # máximo 6 en el banner

    if not upcoming:
        return ""

    # Construir pills de eventos
    pills_html = ""
    for ev in upcoming:
        color  = TYPE_COLORS.get(ev["tipo"], "#374151")
        icon   = TYPE_ICONS.get(ev["tipo"], "📌")
        label  = _format_date(ev["fecha"])
        titulo = ev["titulo"][:52] + "…" if len(ev["titulo"]) > 52 else ev["titulo"]

        pills_html += f"""
        <a href="{ev['enlace']}" target="_blank" class="agenda-pill" style="--pill-color:{color};">
          <span class="pill-date">{label} · {ev['hora']}</span>
          <span class="pill-icon">{icon}</span>
          <span class="pill-title">{titulo}</span>
          <span class="pill-type">{ev['tipo'].upper()}</span>
        </a>"""

    html = f"""
    <!-- BANNER AGENDA DE ACTIVIDADES -->
    <div class="agenda-banner">
      <div class="agenda-banner-header">
        <span class="agenda-banner-label">📅 AGENDA</span>
        <span class="agenda-banner-sub">Próximos eventos · iCare · Cooperativas</span>
      </div>
      <div class="agenda-pills">
        {pills_html}
      </div>
    </div>
"""
    return html


def get_agenda_css():
    """CSS del banner de agenda."""

    css = """
    /* ── BANNER AGENDA ───────────────────────────────────────── */
    .agenda-banner {
      background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 100%);
      border-radius: 10px;
      padding: 22px 28px;
      margin: 40px 0;
      box-shadow: 0 4px 16px rgba(30,64,175,0.25);
    }

    .agenda-banner-header {
      display: flex;
      align-items: baseline;
      gap: 14px;
      margin-bottom: 16px;
    }

    .agenda-banner-label {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      white-space: nowrap;
    }

    .agenda-banner-sub {
      font-size: 12px;
      color: rgba(255,255,255,0.6);
      letter-spacing: 0.04em;
    }

    .agenda-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .agenda-pill {
      display: flex;
      flex-direction: column;
      gap: 4px;
      background: rgba(255,255,255,0.10);
      border: 1px solid rgba(255,255,255,0.18);
      border-left: 4px solid var(--pill-color, #60a5fa);
      border-radius: 6px;
      padding: 10px 14px;
      text-decoration: none;
      cursor: pointer;
      transition: background 0.2s, transform 0.15s;
      min-width: 200px;
      max-width: 260px;
      flex: 1 1 200px;
    }

    .agenda-pill:hover {
      background: rgba(255,255,255,0.18);
      transform: translateY(-2px);
    }

    .pill-date {
      font-size: 11px;
      font-weight: 700;
      color: rgba(255,255,255,0.70);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .pill-icon {
      font-size: 16px;
      line-height: 1;
    }

    .pill-title {
      font-size: 13px;
      font-weight: 600;
      color: #fff;
      line-height: 1.4;
    }

    .pill-type {
      font-size: 10px;
      font-weight: 700;
      color: var(--pill-color, #93c5fd);
      letter-spacing: 0.08em;
      margin-top: 2px;
    }

    @media (max-width: 600px) {
      .agenda-pill {
        min-width: 100%;
        max-width: 100%;
      }
      .agenda-banner {
        padding: 16px 16px;
      }
    }

    @media print {
      .agenda-banner {
        background: #1e3a5f !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
    }
    """

    return css


if __name__ == '__main__':
    print("📅 Banner Agenda\n")
    print(generate_agenda_html())
