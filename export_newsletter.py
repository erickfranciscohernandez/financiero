#!/usr/bin/env python3
"""
Exportador de Newsletter - PDF, JSON, CSV
Genera múltiples formatos del newsletter
"""
import json
from datetime import datetime

def export_to_pdf():
    """Generar PDF del newsletter HTML"""
    try:
        from weasyprint import HTML, CSS

        print("📄 Generando PDF del newsletter...")

        # Leer el HTML
        with open('newsletter.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Generar PDF
        current_date = datetime.now().strftime('%Y%m%d')
        pdf_filename = f'newsletter_{current_date}.pdf'

        HTML(string=html_content).write_pdf(pdf_filename)

        print(f"✅ PDF generado: {pdf_filename}")
        return pdf_filename

    except Exception as e:
        print(f"⚠️  Error al generar PDF: {e}")
        return None

def export_to_json():
    """Exportar datos estructurados a JSON"""
    try:
        print("📋 Exportando a JSON...")

        with open('noticias_diarias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        current_date = datetime.now().strftime('%Y%m%d')
        json_filename = f'newsletter_data_{current_date}.json'

        # Agregar metadata
        output_data = {
            'metadata': {
                'fecha_generacion': datetime.now().isoformat(),
                'version': 'v3',
                'total_noticias': sum(len(v) for v in data.values() if isinstance(v, list))
            },
            'datos': data
        }

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON exportado: {json_filename}")
        return json_filename

    except Exception as e:
        print(f"⚠️  Error al exportar JSON: {e}")
        return None

def export_to_csv():
    """Exportar noticias a CSV"""
    try:
        import csv

        print("📊 Exportando a CSV...")

        with open('noticias_diarias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        current_date = datetime.now().strftime('%Y%m%d')
        csv_filename = f'noticias_{current_date}.csv'

        # Flatear los datos
        all_news = []
        for section, news_list in data.items():
            if isinstance(news_list, list):
                for news in news_list:
                    all_news.append({
                        'seccion': section,
                        'titulo': news.get('title', ''),
                        'resumen': news.get('summary', ''),
                        'fuente': news.get('source', ''),
                        'enlace': news.get('link', ''),
                        'fecha': datetime.now().strftime('%Y-%m-%d')
                    })

        # Escribir CSV
        if all_news:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['seccion', 'titulo', 'resumen', 'fuente', 'enlace', 'fecha'])
                writer.writeheader()
                writer.writerows(all_news)

            print(f"✅ CSV exportado: {csv_filename} ({len(all_news)} noticias)")
            return csv_filename

    except Exception as e:
        print(f"⚠️  Error al exportar CSV: {e}")
        return None

def create_summary_report():
    """Crear reporte resumen del newsletter"""
    try:
        print("📈 Generando reporte resumen...")

        with open('noticias_diarias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        current_date = datetime.now().strftime('%Y%m%d')
        report_filename = f'resumen_{current_date}.txt'

        total_noticias = 0
        sections_info = {}

        for section, news_list in data.items():
            if isinstance(news_list, list):
                count = len(news_list)
                total_noticias += count
                sections_info[section] = {
                    'cantidad': count,
                    'titulos': [n.get('title', '')[:60] for n in news_list[:3]]
                }

        # Escribir reporte
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(f"{'='*70}\n")
            f.write(f"REPORTE RESUMEN - NEWSLETTER ESTRATÉGICO\n")
            f.write(f"{'='*70}\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%d de %B, %Y').replace('May', 'Mayo')}\n")
            f.write(f"Versión: v3 (Análisis Inteligente)\n\n")

            f.write(f"ESTADÍSTICAS GENERALES\n")
            f.write(f"{'-'*70}\n")
            f.write(f"Total de noticias analizadas: {total_noticias}\n")
            f.write(f"Secciones cubiertas: {len(sections_info)}\n\n")

            f.write(f"DETALLES POR SECCIÓN\n")
            f.write(f"{'-'*70}\n")
            for section, info in sections_info.items():
                f.write(f"\n📰 {section.upper()}: {info['cantidad']} noticias\n")
                f.write(f"   Titulares principales:\n")
                for i, titulo in enumerate(info['titulos'], 1):
                    f.write(f"   {i}. {titulo}...\n")

            f.write(f"\n\n{'='*70}\n")
            f.write(f"Generado por: Newsletter Estratégico v3\n")
            f.write(f"{'='*70}\n")

        print(f"✅ Reporte generado: {report_filename}")
        return report_filename

    except Exception as e:
        print(f"⚠️  Error al generar reporte: {e}")
        return None

def main():
    print("🎯 Exportador de Newsletter - Generando múltiples formatos\n")

    outputs = {
        'PDF': export_to_pdf(),
        'JSON': export_to_json(),
        'CSV': export_to_csv(),
        'Reporte': create_summary_report()
    }

    print(f"\n{'='*50}")
    print("✅ EXPORTACIÓN COMPLETADA")
    print(f"{'='*50}\n")

    for format_name, filename in outputs.items():
        status = "✅" if filename else "❌"
        print(f"{status} {format_name}: {filename or 'No generado'}")

    print(f"\n📁 Archivos disponibles en el repositorio")
    print(f"📧 Listos para compartir por email")
    print(f"🖨️  Listos para imprimir\n")

if __name__ == '__main__':
    main()
