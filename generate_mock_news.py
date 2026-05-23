#!/usr/bin/env python3
"""
Generador de noticias mock dinámicas
Actualiza noticias_diarias.json con datos nuevos simulados
Para simular actualizaciones en tiempo real sin acceso a internet
"""
import json
from datetime import datetime, timedelta
import random

# Plantillas de noticias por categoría — actualizadas mayo 2026
NEWS_TEMPLATES = {
    'geopolitica': [
        {
            'title': 'EE.UU. y China retoman negociaciones comerciales tras tregua arancelaria de 90 días',
            'summary': 'Washington y Pekín acuerdan mesa de trabajo técnica para revisar aranceles industriales. Mercados reaccionan positivamente ante señales de distensión.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': 'OTAN refuerza presencia en Europa del Este con nuevas brigadas multinacionales',
            'summary': 'Alianza despliega 20.000 efectivos adicionales en Polonia y los países bálticos en respuesta a tensiones persistentes con Rusia.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'Arabia Saudita y Emiratos Árabes negocian acuerdo de normalización con Israel bajo mediación de EE.UU.',
            'summary': 'Diplomacia activa en Medio Oriente podría reconfigurar alianzas regionales y estabilizar precios del petróleo.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/news'
        },
        {
            'title': 'BRICS amplía membresía con incorporación de Indonesia y Turquía',
            'summary': 'Bloque suma peso económico y demográfico significativo, consolidando alternativa al orden financiero occidental.',
            'source': 'The Economist',
            'link': 'https://www.economist.com'
        },
        {
            'title': 'Trump impone nuevos aranceles del 25% a acero y aluminio europeos',
            'summary': 'Medida proteccionista reactiva tensiones transatlánticas y genera alertas en industria manufacturera global.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'ONU alerta sobre crisis humanitaria en Sudán con 10 millones de desplazados',
            'summary': 'Conflicto interno en el país africano genera presión migratoria y riesgo de inestabilidad regional.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com'
        },
    ],
    'economia_global': [
        {
            'title': 'Cobre cotiza en USD 4.58/lb impulsado por demanda china y transición energética',
            'summary': 'Metal rojo alcanza máximos del año respaldado por compras de China y aceleración de proyectos de energías renovables globales.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': 'Fed mantiene tasa en 4.25% y señala dos recortes posibles para segundo semestre',
            'summary': 'Jerome Powell indica que inflación converge al 2% pero el mercado laboral sigue robusto. Próxima reunión en julio será clave.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'FMI revisa al alza crecimiento global a 3.2% para 2026 liderado por Asia',
            'summary': 'India y Vietnam lideran expansión en economías emergentes mientras Europa enfrenta estancamiento productivo.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
        {
            'title': 'Petróleo Brent cae a USD 71 por exceso de oferta de OPEP+ y menor demanda europea',
            'summary': 'Cártel petrolero enfrenta tensiones internas tras decisión de Arabia Saudita de mantener cuotas de producción elevadas.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/business/energy'
        },
        {
            'title': 'BCE reduce tasas 25 puntos base ante señales de desinflación en zona euro',
            'summary': 'Christine Lagarde anticipa ciclo gradual de relajación monetaria. Euro se deprecia frente al dólar.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'Bolsas asiáticas cierran en alza tras dato de exportaciones chinas mejor a lo esperado',
            'summary': 'Exportaciones de China suben 6.1% interanual en abril, superando estimaciones y reduciendo temores de desaceleración.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com/asia-pacific'
        },
    ],
    'economia_chile': [
        {
            'title': 'BCCh mantiene TPM en 5.0% y proyecta recorte en reunión de julio',
            'summary': 'Banco Central evalúa que inflación se aproxima a meta del 3%. Mercado anticipa dos recortes adicionales en 2026.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Dólar observado cierra en $945 ante fortalecimiento global del peso',
            'summary': 'Tipo de cambio retrocede impulsado por alza del cobre y señales de Fed. Exportadores ajustan coberturas cambiarias.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Codelco anuncia inversión de USD 2.800M para modernizar división El Teniente',
            'summary': 'Proyecto aumentará producción en 100.000 toneladas anuales y reducirá emisiones de carbono un 30% al 2030.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'IPSA sube 1.8% y supera los 7.200 puntos en mejor sesión del año',
            'summary': 'Bolsa local lidera ganancias en Latinoamérica impulsada por sector minero y retail ante datos macro favorables.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': 'Reforma de pensiones avanza en comisión del Senado con acuerdo sobre reparto',
            'summary': 'Legisladores aprueban artículo clave sobre fondo colectivo solidario. Sistema mixto podría quedar aprobado antes de agosto.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com/politica'
        },
        {
            'title': 'IPC de abril anota 0.2% mensual y acumula 3.8% en doce meses',
            'summary': 'Inflación continúa tendencia bajista según INE. Alimentos y transporte explican la mayor parte del alza mensual.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': 'Apple lanza iPhone 17 con chip A19 y funciones avanzadas de IA en cámara',
            'summary': 'Nuevo dispositivo integra procesamiento de imágenes con IA local y mejora autonomía de batería en 40%.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
        {
            'title': 'Starlink expande cobertura en Latinoamérica con nueva constelación de satélites',
            'summary': 'SpaceX despliega 120 satélites adicionales para reducir latencia y ampliar conectividad rural en Chile, Perú y Colombia.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'Quantum computing alcanza hito: procesador de 1.000 qubits supera barrera de corrección de errores',
            'summary': 'IBM y Google reportan avances simultáneos que acercan la computación cuántica a aplicaciones comerciales en criptografía y logística.',
            'source': 'MIT Technology Review',
            'link': 'https://www.technologyreview.com'
        },
        {
            'title': 'Nvidia supera USD 3 billones de capitalización bursátil impulsada por demanda de chips IA',
            'summary': 'GPU H100 y Blackwell Architecture consolidan dominio en infraestructura de entrenamiento de modelos de lenguaje.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/technology'
        },
    ],
    'cooperativismo': [
        {
            'title': 'Cooperativas de ahorro chilenas registran crecimiento de 14% en colocaciones durante primer trimestre 2026',
            'summary': 'Sector cooperativo gana participación de mercado frente a banca tradicional. CONFECOOP proyecta cierre de año con activos por USD 8.500M.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'Coopeuch lanza plataforma digital para créditos hipotecarios con aprobación en 24 horas',
            'summary': 'Mayor cooperativa de ahorro de Chile digitaliza proceso de crédito inmobiliario reduciendo tiempos de 30 días a 24 horas.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Congreso aprueba ley que amplía cobertura del Fogacoope a cooperativas medianas',
            'summary': 'Nueva norma permite que cooperativas con activos entre UF 500.000 y UF 1.000.000 accedan al Fondo de Garantía Cooperativa.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl'
        },
        {
            'title': 'ACI Américas presenta informe: cooperativismo chileno entre los cinco más sólidos de la región',
            'summary': 'Chile destaca por índices de solvencia, penetración rural y adopción tecnológica del sector cooperativo financiero.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
        },
        {
            'title': 'Red de cooperativas agrícolas del Biobío accede a financiamiento verde del BID por USD 45M',
            'summary': 'Recursos financiarán proyectos de riego eficiente, almacenamiento solar y reducción de huella de carbono.',
            'source': 'BID',
            'link': 'https://www.iadb.org'
        },
    ],
    'cmf': [
        {
            'title': 'CMF publica nueva norma sobre gestión de riesgos de ciberseguridad para bancos y cooperativas',
            'summary': 'Regulador exige planes de continuidad operacional ante ataques cibernéticos y pruebas anuales de penetración a sistemas críticos.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF sanciona a cinco administradoras de fondos por fallas en información a inversionistas',
            'summary': 'Multas totalizan UF 18.000. Irregularidades incluyen omisión de información material y conflictos de interés no declarados.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF actualiza normativa de open banking con nuevos estándares de API para Fintechs',
            'summary': 'Circular 2026 obliga a instituciones financieras a exponer datos bajo protocolo OAuth 2.0 y formato JSON estándar para diciembre.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF aprueba reglamento de tokenización de activos financieros en Chile',
            'summary': 'Primera regulación latinoamericana integral sobre activos digitales nativos permite emisión de bonos y acciones tokenizadas.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF reporta morosidad bancaria en 2.1%, nivel más bajo en tres años',
            'summary': 'Sistema financiero chileno muestra solvencia con índices de Basilea III sobre el 14%. Crédito hipotecario lidera recuperación.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': 'IPC de abril 2026 registra 0.2% mensual: inflación acumula 3.8% anual',
            'summary': 'INE confirma tendencia desaceleradora. División alimentos sube 0.4% y transporte 0.3%, mientras vestuario cae 0.2%.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Desempleo en Chile baja a 7.8% en trimestre enero-marzo 2026',
            'summary': 'INE registra creación neta de 45.000 empleos. Sector servicios y construcción lideran contratación.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Imacec de marzo 2026 crece 3.4% interanual, superando estimaciones del mercado',
            'summary': 'Banco Central destaca dinamismo en comercio y servicios. Sector minero aportó 0.8 puntos porcentuales al crecimiento.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Exportaciones chilenas suben 12% en primer cuatrimestre impulsadas por cobre y litio',
            'summary': 'Balanza comercial acumula superávit de USD 3.200M. China sigue siendo el principal destino con el 38% del total exportado.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Confianza empresarial ICARE sube 4 puntos y alcanza nivel neutral en mayo',
            'summary': 'Encuesta mensual refleja menor incertidumbre regulatoria y mejores perspectivas de demanda interna para el segundo semestre.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': 'OpenAI lanza GPT-5 con capacidad de razonamiento extendido y memoria persistente',
            'summary': 'Nuevo modelo supera benchmarks de matemáticas y codificación. Integra memoria a largo plazo entre conversaciones y herramientas autónomas.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Google DeepMind presenta AlphaFold 3 para diseño de proteínas y fármacos',
            'summary': 'Modelo amplía capacidades de predicción de estructuras moleculares a ADN y ARN, acelerando desarrollo de tratamientos médicos.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
        {
            'title': 'Anthropic lanza Claude 4 con mejoras en seguridad y capacidad de agentes autónomos',
            'summary': 'Nuevo modelo integra capacidades de uso de computadora, navegación web y ejecución de código con supervisión humana mejorada.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'UE aprueba reglamento de IA de alto riesgo con multas de hasta el 7% de facturación global',
            'summary': 'AI Act entra en vigencia plena. Sistemas de reconocimiento biométrico, crédito y contratación quedan sujetos a auditorías obligatorias.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Microsoft integra Copilot en toda la suite Office 365 con nuevas capacidades de análisis financiero',
            'summary': 'Asistente IA analiza balances, genera proyecciones y redacta informes ejecutivos directamente desde Excel y PowerPoint.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'Startup chilena Xepelin lanza motor de IA para evaluación de crédito Pyme en tiempo real',
            'summary': 'Fintech usa modelos de lenguaje para analizar flujo de caja, historial tributario y comportamiento de pagos en menos de 2 minutos.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
    ],
}


def generate_dynamic_news():
    """Genera noticias dinámicas basadas en la hora actual"""

    # Usar la hora actual para seleccionar noticias diferentes
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute

    # Seed para reproducibilidad dentro del mismo período de 30 min
    random.seed(current_hour * 60 + (current_minute // 30))

    news_data = {}

    for category, templates in NEWS_TEMPLATES.items():
        # Seleccionar 3-4 noticias aleatorias por categoría
        num_news = random.randint(3, 4)
        selected = random.sample(templates, min(num_news, len(templates)))

        # Agregar variación temporal
        news_with_time = []
        for i, news in enumerate(selected):
            news_copy = news.copy()
            # Agregar "updated" timestamp
            hours_ago = random.randint(0, 6)
            news_copy['date'] = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            news_with_time.append(news_copy)

        news_data[category] = news_with_time

    return news_data


def update_news_file():
    """Actualiza el archivo noticias_diarias.json con noticias dinámicas"""

    try:
        news = generate_dynamic_news()

        with open('noticias_diarias.json', 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)

        # Mostrar resumen
        total_news = sum(len(v) for v in news.values())
        print(f"✅ Noticias actualizadas: {total_news}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   Próxima actualización: en 30 minutos")

        return True

    except Exception as e:
        print(f"❌ Error actualizando noticias: {e}")
        return False


if __name__ == '__main__':
    print("🔄 Generador de noticias dinámicas")
    print("=" * 50)
    update_news_file()
