#!/usr/bin/env python3
"""
API REST para el Diccionario de Problemas de Soporte Técnico
Permite consultar problemas por categoría, severidad, búsqueda de texto, etc.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

DATA_FILE = Path(__file__).parent / 'issues_dictionary.json'

def load_problems():
    """Carga los problemas desde el archivo JSON"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"problems": []}

@app.route('/api/problems', methods=['GET'])
def get_problems():
    """
    Obtiene lista de todos los problemas con filtros opcionales

    Query parameters:
    - category: Software, Hardware, Accesos, DLP
    - severity: critical, high, medium
    - search: texto para buscar en título, descripción, síntomas, soluciones
    """
    data = load_problems()
    problems = data.get('problems', [])

    # Filtrar por categoría
    category = request.args.get('category', '').strip()
    if category:
        problems = [p for p in problems if p['category'] == category]

    # Filtrar por severidad
    severity = request.args.get('severity', '').strip()
    if severity:
        problems = [p for p in problems if p['severity'] == severity]

    # Buscar en texto
    search = request.args.get('search', '').lower().strip()
    if search:
        filtered = []
        for p in problems:
            if (search in p['title'].lower() or
                search in p['description'].lower() or
                any(search in s.lower() for s in p.get('symptoms', [])) or
                any(search in s.lower() for s in p.get('solutions', []))):
                filtered.append(p)
        problems = filtered

    return jsonify({
        'count': len(problems),
        'problems': problems
    })

@app.route('/api/problems/<problem_id>', methods=['GET'])
def get_problem(problem_id):
    """Obtiene un problema específico por su ID"""
    data = load_problems()
    problems = data.get('problems', [])

    problem = next((p for p in problems if p['id'] == problem_id), None)

    if problem:
        return jsonify(problem)
    return jsonify({'error': 'Problema no encontrado'}), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Obtiene lista de categorías disponibles"""
    data = load_problems()
    problems = data.get('problems', [])

    categories = {}
    for problem in problems:
        category = problem['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1

    return jsonify({
        'categories': sorted(categories.items())
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Obtiene estadísticas sobre los problemas"""
    data = load_problems()
    problems = data.get('problems', [])

    stats = {
        'total_problems': len(problems),
        'by_category': {},
        'by_severity': {},
        'critical_count': 0,
        'high_count': 0,
        'medium_count': 0
    }

    for problem in problems:
        # Contar por categoría
        category = problem['category']
        if category not in stats['by_category']:
            stats['by_category'][category] = 0
        stats['by_category'][category] += 1

        # Contar por severidad
        severity = problem['severity']
        if severity not in stats['by_severity']:
            stats['by_severity'][severity] = 0
        stats['by_severity'][severity] += 1

        # Contar severidades específicas
        if severity == 'critical':
            stats['critical_count'] += 1
        elif severity == 'high':
            stats['high_count'] += 1
        elif severity == 'medium':
            stats['medium_count'] += 1

    return jsonify(stats)

@app.route('/api/search', methods=['POST'])
def search_problems():
    """
    Búsqueda avanzada de problemas

    POST body:
    {
        "query": "texto a buscar",
        "category": "Software",
        "severity": "critical",
        "limit": 10
    }
    """
    req_data = request.get_json() or {}
    data = load_problems()
    problems = data.get('problems', [])

    # Parámetros
    query = req_data.get('query', '').lower().strip()
    category = req_data.get('category', '').strip()
    severity = req_data.get('severity', '').strip()
    limit = req_data.get('limit', 50)

    # Aplicar filtros
    results = []
    for problem in problems:
        match = True

        # Filtro de categoría
        if category and problem['category'] != category:
            match = False

        # Filtro de severidad
        if severity and problem['severity'] != severity:
            match = False

        # Búsqueda de texto
        if query:
            text_match = (
                query in problem['title'].lower() or
                query in problem['description'].lower() or
                any(query in s.lower() for s in problem.get('symptoms', [])) or
                any(query in s.lower() for s in problem.get('solutions', []))
            )
            if not text_match:
                match = False

        if match:
            results.append(problem)

    # Limitar resultados
    results = results[:limit]

    return jsonify({
        'count': len(results),
        'total_available': len([p for p in problems if p]),
        'problems': results
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Verifica el estado de la API"""
    data = load_problems()
    problems_count = len(data.get('problems', []))

    return jsonify({
        'status': 'ok',
        'problems_loaded': problems_count
    })

@app.route('/api/export', methods=['GET'])
def export_problems():
    """Exporta todos los problemas en formato JSON"""
    data = load_problems()
    return jsonify(data)

if __name__ == '__main__':
    print("🚀 API de Diccionario de Problemas iniciada")
    print("📍 http://localhost:5000")
    print("\nEndpoints disponibles:")
    print("  GET  /api/problems                 - Lista todos los problemas")
    print("  GET  /api/problems/<id>            - Obtiene un problema específico")
    print("  GET  /api/categories               - Lista categorías")
    print("  GET  /api/statistics               - Estadísticas")
    print("  POST /api/search                   - Búsqueda avanzada")
    print("  GET  /api/health                   - Estado de la API")
    print("  GET  /api/export                   - Exporta todos los datos")

    app.run(debug=True, host='0.0.0.0', port=5000)
