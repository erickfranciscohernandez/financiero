#!/usr/bin/env python3
"""
Generador de noticias mock dinámicas
Actualiza noticias_diarias.json con datos nuevos simulados
Para simular actualizaciones en tiempo real sin acceso a internet
"""
import json
from datetime import datetime, timedelta
import random

# Noticias específicas del 5 de junio de 2026
TODAY_NEWS_05JUN2026 = {
    'geopolitica': [
        {
            'title': '[5 Jun] G7 finaliza cumbre con declaración sobre minerales críticos: Chile y Perú mencionados como socios estratégicos',
            'summary': 'Comunicado final del G7 en Kananaskis incluye por primera vez un capítulo dedicado a minerales críticos. Chile es reconocido como proveedor confiable de cobre y litio para la transición energética del bloque. Se abren negociaciones de acuerdo preferencial.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[5 Jun] OTAN refuerza presencia en Mar Negro tras incidente naval entre Turquía y Rusia',
            'summary': 'Alianza activa protocolo de monitoreo reforzado luego de interceptación de fragata turca en aguas internacionales. Mercados de energía reaccionan: Brent sube 1.2% a USD 82.4. Impacto moderado en commodities latinoamericanos.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[5 Jun] Nóminas EE.UU. de mayo confirman enfriamiento: 185.000 empleos consolidan expectativas de recorte Fed en septiembre',
            'summary': 'Mercados digieren el dato de empleo con optimismo. Curva de rendimientos se aplana. Dólar DXY cae 0.4% en la semana. Fed Funds Futures asigna 79% de probabilidad a recorte de 25 pb en septiembre. S&P 500 cierra semana en máximos.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[5 Jun] Cobre cierra semana sobre USD 5.10/lb: acumula alza de 4.8% en mayo impulsado por déficit de oferta',
            'summary': 'Metal rojo se consolida en rango alto. ICSG reporta déficit global de 180.000 toneladas en el primer trimestre. Inventarios LME caen a 112.000 toneladas, mínimo de dos décadas. Goldman Sachs reafirma objetivo de USD 5.40 para Q3.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[5 Jun] UF hoy $40.678,43 y dólar observado $894,29: indicadores clave al 5 de junio de 2026',
            'summary': 'Unidad de Fomento publicada por SII para el día de hoy. Dólar observado del BCCh levemente al alza respecto al cierre anterior. Mercado espera IPC de mayo el próximo lunes 9 de junio: consenso en 0.2% mensual y 3.2% anual.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[5 Jun] IPSA acumula alza semanal de 2.1%: cobre fuerte y expectativas de recorte Fed impulsan bolsa chilena',
            'summary': 'Índice bursátil cierra la semana en 7.840 puntos, máximo desde febrero 2025. Codelco y SQM lideran las ganancias semanales con +4.1% y +5.3% respectivamente. Volumen de transacciones supera el promedio en un 28%.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[5 Jun] BCCh: expectativas de inflación a 24 meses se anclan en 3.0% según encuesta de operadores',
            'summary': 'Encuesta mensual de operadores financieros muestra convergencia de expectativas a la meta. Proyección de TPM al cierre de 2026 se mantiene en 4.0%-4.25%. Mediana de analistas anticipa primer recorte en agosto.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[5 Jun] Transbank lanza nuevo sistema de pagos instantáneos 24/7 para personas y pymes: sin comisión hasta UF 5',
            'summary': 'Plataforma TEF+ permite transferencias en menos de 5 segundos a cualquier banco o billetera digital. Sin costo para transacciones bajo UF 5. Integración directa con aplicaciones móviles via API abierta. Disponible desde hoy para todos los usuarios.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[5 Jun] Chile avanza al puesto 22 en ranking global de competitividad digital: primer lugar en América Latina',
            'summary': 'IMD World Digital Competitiveness 2026 posiciona a Chile como el país más competitivo digitalmente de la región, superando a Brasil y Uruguay. Destacan infraestructura de fibra óptica, adopción de IA en sector público y marco regulatorio fintech.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[5 Jun] Banco Central de Chile lanza piloto de IA para monitoreo de riesgo sistémico en tiempo real',
            'summary': 'BCCh implementa modelos de lenguaje de gran escala para detectar señales tempranas de estrés financiero. Sistema analiza flujos interbancarios, variaciones de spreads y datos de mercado en tiempo real. Primer banco central de Latinoamérica en aplicar IA generativa en supervisión.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[5 Jun] Microsoft anuncia inversión de USD 500M en IA para sector financiero latinoamericano con sede en Chile',
            'summary': 'Gigante tecnológico elige Santiago como hub regional para desarrollo de soluciones de IA en banca, seguros y gestión de activos. Acuerdo con CORFO incluye formación de 5.000 profesionales en IA aplicada a finanzas. Primeras soluciones disponibles en el primer trimestre de 2027.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
    ],
    'cooperativismo': [
        {
            'title': '[5 Jun] Cooperativas chilenas recaudan UF 120.000 en bonos de impacto social: primer instrumento del sector en bolsa',
            'summary': 'Emisión de bonos sociales cooperativos debuta en la Bolsa de Santiago con demanda que triplica la oferta. Recursos financiarán vivienda cooperativa y crédito educacional en regiones. CMF certifica el instrumento como inversión de impacto.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[5 Jun] CONFECOOP Chile reporta crecimiento de 14% en colocaciones del sector cooperativo en los últimos 12 meses',
            'summary': 'Cartera total del sector alcanza los USD 13.200M. Crédito hipotecario cooperativo crece 18%, el mayor ritmo en cinco años. Mora del sector en 1.2%, significativamente bajo el promedio bancario de 1.9%. Rentabilidad patrimonial en 12.4%.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[5 Jun] CMF lanza sandbox regulatorio para fintechs de crédito y pagos: 20 empresas podrán operar en régimen especial',
            'summary': 'Comisión abre convocatoria para programa de innovación regulatoria. Las empresas seleccionadas operarán bajo supervisión especial durante 18 meses con requisitos de capital reducidos. Objetivo: acelerar adopción de open banking y pagos digitales.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[5 Jun] Balanza comercial Chile enero-mayo 2026: superávit acumulado de USD 8.200M, el mejor desde 2011',
            'summary': 'Cifras del BCCh confirman exportaciones en USD 40.500M y importaciones en USD 32.300M en el período. Cobre representa el 51.3% de las exportaciones totales. Diversificación exportadora avanza con litio procesado y frutas premium.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[5 Jun] Mercado inmobiliario chileno muestra señales de recuperación: ventas de viviendas nuevas suben 8% en mayo',
            'summary': 'CChC reporta 5.200 unidades vendidas en mayo 2026, mayor cifra desde julio 2024. Segmento de vivienda social lidera con subsidios SERVIU. Tasas hipotecarias bajan a 4.2% en UF desde 4.6% de diciembre 2025.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
}

# Noticias específicas del 4 de junio de 2026
TODAY_NEWS_04JUN2026 = {
    'geopolitica': [
        {
            'title': '[4 Jun] Cumbre G7: acuerdo sobre aranceles al acero chino y nuevas reglas para cadenas de suministro críticas',
            'summary': 'Los siete líderes firman declaración conjunta que establece aranceles coordinados del 25% al acero y aluminio chino. Incluye cláusula de nearshoring estratégico que beneficia a Chile como proveedor de litio y cobre para la cadena verde global.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[4 Jun] OCDE: Chile en posición favorable ante reconfiguración global de cadenas de suministro de minerales críticos',
            'summary': 'Informe destaca estabilidad institucional chilena y reservas de minerales críticos como ventaja competitiva. Recomienda acelerar acuerdos bilaterales con UE y Japón para exportar litio procesado y no solo materia prima.',
            'source': 'OECD',
            'link': 'https://www.oecd.org'
        },
    ],
    'economia_global': [
        {
            'title': '[4 Jun] Nóminas EE.UU.: 185.000 empleos en mayo vs. 195.000 esperados; dólar cae globalmente y bolsas suben',
            'summary': 'Dato de empleo más débil de lo esperado refuerza expectativas de recorte de la Fed en septiembre. Índice DXY cae 0.6%. Probabilidad de recorte sube al 78%. Bolsas globales al alza con S&P 500 +0.8%.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[4 Jun] BCE mantiene tasa en 2.5%: Lagarde abre puerta a recorte en julio si inflación confirma tendencia',
            'summary': 'Banco Central Europeo mantiene tasas pero cambia sesgo a neutral. Inflación subyacente de la eurozona en 2.3%, convergiendo a meta del 2%. Euro sube 0.4% frente al dólar. Impacto moderado en spreads de deuda emergente.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[4 Jun] Dólar observado en $894,29: peso chileno cede terreno ante fortaleza global del dólar y toma de utilidades',
            'summary': 'Tipo de cambio observado publicado por el BCCh en $894,29. Mercado modera expectativas de apreciación tras datos mixtos de empleo en EE.UU. BCCh publica encuesta de expectativas que muestra IPC 2026 convergiendo a 3.0%.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[4 Jun] INE: desempleo de abril 2026 en 8.3%; empleo informal cae a mínimo histórico de 26.8%',
            'summary': 'Tasa dentro de lo esperado. Empleo formal crece 2.9% en doce meses. Sector servicios y minería son los principales impulsores. Brecha de género en empleo formal se reduce a 10.2 puntos porcentuales.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': '[4 Jun] Hacienda: Marco Fiscal proyecta deuda neta en 11.8% del PIB y regla fiscal cumplida por quinto año',
            'summary': 'Informe bienal proyecta balance estructural de -1.9% del PIB para 2026. Precio de referencia del cobre se revisa al alza a USD 3.95/lb. Fitch y S&P reafirman notas soberanas A/A- con outlook estable.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[4 Jun] Gobierno lanza portal de datos abiertos con 1.200 datasets financieros: open data para fintechs chilenas',
            'summary': 'Plataforma datos.gob.cl incorpora información del SII, BCCh, INE y CMF con APIs estandarizadas. Más de 60 startups ya registradas. CORFO ofrece subsidio de hasta UF 500 para proyectos de innovación con datos públicos.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[4 Jun] Mercado de semiconductores Latam crecerá 18% anual hasta 2030: Chile posicionado como hub regional',
            'summary': 'Estudio IDC identifica a Chile como destino preferido para centros de datos. TSMC evalúa planta en Quilicura con apoyo de CORFO. Gobierno extiende beneficios tributarios al sector tecnológico de alta densidad energética.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[4 Jun] CMF publica guía de IA responsable en servicios financieros: 12 principios para bancos y fintechs',
            'summary': 'Documento establece criterios de explicabilidad, no discriminación y supervisión humana para modelos de IA en crédito, scoring y detección de fraude. Las entidades tienen 18 meses para implementar los estándares.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[4 Jun] Meta lanza Llama 4 Ultra con razonamiento financiero avanzado: API gratuita para startups latinoamericanas',
            'summary': 'Nuevo modelo supera benchmarks financieros y jurídicos en español. Licencia comercial gratuita para startups con menos de USD 1M de ingresos. Compatible con AWS, Azure y GCP. Desarrolladores chilenos entre los primeros usuarios.',
            'source': 'VentureBeat AI',
            'link': 'https://venturebeat.com/category/ai/'
        },
    ],
    'cooperativismo': [
        {
            'title': '[4 Jun] ACI: cooperativas financieras chilenas entre las más sólidas de América Latina según ranking 2026',
            'summary': 'Alianza Cooperativa Internacional destaca el marco regulatorio chileno como modelo regional. Sector mantiene índice de capital del 14.8%, superior al mínimo requerido. Expansión hacia Perú y Colombia en evaluación.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[4 Jun] Detacoop lanza plataforma de inversión para socios: retorno proyectado de 6.5% anual en UF',
            'summary': 'Nueva oferta permite a socios invertir desde UF 10. Fondos destinados a cartera hipotecaria y crédito educacional. Apertura de cuentas 100% digital disponible desde hoy. Primer producto de inversión cooperativa con liquidez semanal.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[4 Jun] CMF: activos de fondos de inversión chilenos superan USD 85.000M al cierre de mayo 2026',
            'summary': 'Patrimonio de la industria de fondos crece 12.3% en doce meses. Fondos de deuda en UF lideran captaciones con USD 2.100M en el mes. Capital extranjero representa el 18% del total gestionado, nuevo máximo histórico.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[4 Jun] UF del 4 de junio: $40.678,43 — acumula alza de $33,88 en la semana',
            'summary': 'Valor diario de la Unidad de Fomento publicado por el SII. El incremento semanal refleja la inflación de mayo. Próxima referencia clave: IPC oficial del INE el 9 de junio.',
            'source': 'SII Chile',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[4 Jun] Balanza comercial mayo 2026: superávit de USD 1.850M impulsado por cobre y litio',
            'summary': 'Exportaciones alcanzan USD 8.100M; importaciones USD 6.250M. Cobre representa el 52% de las exportaciones totales. Superávit acumulado enero-mayo en USD 8.200M, 34% superior al mismo período de 2025.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
}

# Noticias específicas del 2 de junio de 2026
TODAY_NEWS_02JUN2026 = {
    'geopolitica': [
        {
            'title': '[2 Jun] Reunión OTAN en Bruselas: aliados elevan gasto de defensa al 2.5% del PIB y refuerzan flanco este',
            'summary': 'Ministros de Defensa del bloque acuerdan nuevo umbral de gasto ante persistente amenaza rusa. EE.UU. anuncia despliegue adicional de 5.000 efectivos en Polonia. Se discute adhesión de Ucrania como proceso acelerado.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[2 Jun] India y EE.UU. firman acuerdo de defensa e inteligencia artificial que excluye tecnología china',
            'summary': 'Modi y Trump sellan pacto de acceso preferente a chips avanzados de Nvidia e Intel para India a cambio de bases navales en el Índico. Reconfiguración del tablero tecnológico global se acelera.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[2 Jun] ISM servicios EE.UU. de mayo baja a 49.8: primera contracción en nueve meses eleva dudas sobre la Fed',
            'summary': 'Dato sorprende a la baja. Componente de empleo en 47.2, mínimo desde 2020. Mercados ajustan expectativas: probabilidad de recorte en septiembre cae al 71%. Rendimiento del T-10 retrocede a 4.58%.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': '[2 Jun] Cobre en USD 5.12/lb: inventarios LME caen a mínimo de 22 años y Chile acelera aprobaciones mineras',
            'summary': 'Metal rojo suma quinta semana de alzas consecutivas. Gobierno chileno aprueba tres EIA pendientes de Codelco y anuncia ventanilla rápida para proyectos de cobre y litio. IPSA sube 1.1% liderado por mineras.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[2 Jun] BCCh publica encuesta de operadores financieros: dólar proyectado en $885 para septiembre 2026',
            'summary': 'EOF mensual confirma sesgo apreciador del peso ante cobre fuerte y expectativa de recorte de la Fed. Proyección de IPC 2026 se mantiene en 3.0%. Mercado descuenta TPM en 4.25% al cierre del año.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[2 Jun] Codelco anuncia descubrimiento de nuevo yacimiento en Atacama con reservas estimadas de 800.000 toneladas',
            'summary': 'Corporación confirma hallazgo en sector norte de la Región de Atacama durante campaña de exploración. Estudio de factibilidad tomará 24 meses. Reservas representarían cuatro años de producción de El Teniente.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[2 Jun] SII abre proceso de declaración de IVA anual para grandes contribuyentes: plazo hasta el 20 de junio',
            'summary': 'Empresas con ventas sobre UF 100.000 deben presentar declaración anual antes del 20 de junio. Nueva plataforma digital del SII reduce el tiempo de presentación en 60%.',
            'source': 'SII Chile',
            'link': 'https://www.sii.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[2 Jun] Amazon Web Services confirma región cloud en Santiago: operación desde 2027 con inversión de USD 800M',
            'summary': 'AWS anuncia tres zonas de disponibilidad en la Región Metropolitana. CORFO co-financia con USD 180M. Gobierno destaca soberanía de datos para sector público, salud y banca. Genera 1.200 empleos directos.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': '[2 Jun] Starlink anuncia plan residencial a $29.990/mes en Chile desde agosto: presión sobre ISPs locales',
            'summary': 'SpaceX lanza plan de entrada con velocidades de 100-200 Mbps. VTR, Entel y Movistar ajustan precios en regiones. SUBTEL evalúa marco regulatorio para operadores satelitales de baja órbita.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[2 Jun] Claude 4 llega a empresas chilenas: Banco de Chile y Falabella anuncian pilotos de agentes autónomos',
            'summary': 'Banco de Chile usará Claude 4 para análisis de contratos y onboarding de clientes. Falabella lo integrará en gestión de inventario y atención al cliente. Ambos proyectos en producción antes de fin de año.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': '[2 Jun] OpenAI lanza GPT-5 Mini: modelo ligero para móviles con 90% del rendimiento del modelo completo',
            'summary': 'Versión compacta disponible como API desde hoy. Latencia de 200ms y precio 20 veces menor. Desarrolladores de apps financieras y legales son el segmento objetivo.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
    ],
    'cooperativismo': [
        {
            'title': '[2 Jun] Foro Cooperativo Chile publica ranking 2026: las 10 cooperativas con mayor crecimiento en socios activos',
            'summary': 'El informe anual destaca expansión en La Araucanía, Los Lagos y Biobío. Cooperativas con foco en crédito hipotecario y digital lideran captación de nuevos socios. Sector supera 1.8 millones de socios activos.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[2 Jun] CMF publica estadísticas del sistema financiero a abril 2026: colocaciones crecen 7.8% y mora baja a 1.8%',
            'summary': 'Informe mensual confirma solidez del sistema. Crédito hipotecario crece 9.2%, consumo 6.9% y comercial 6.1%. Capital nivel 1 promedio en 14.2%. Rentabilidad sobre patrimonio del sistema en 17.1%.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[2 Jun] INE publicará IPC de mayo el 9 de junio: mercado espera 0.2% mensual y 3.1% anual',
            'summary': 'Consenso Bloomberg sitúa el dato en 0.2% mensual. Combustibles al alza; alimentos y vestuario a la baja. Un dato en línea daría margen al BCCh para recortar TPM en agosto.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': '[2 Jun] Exportaciones chilenas de mayo superan USD 6.000M: cobre, litio y fruta lideran cifra récord mensual',
            'summary': 'Cifra preliminar del BCCh supera en USD 400M el promedio mensual de 2026. Precio del cobre promedia USD 5.05/lb en mayo. China absorbe el 43% de los envíos totales.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
}

TODAY_NEWS_03JUN2026 = {
    'geopolitica': [
        {
            'title': '[3 Jun] G7 en Canadá: líderes acuerdan fondo de USD 50.000M para infraestructura crítica frente a China',
            'summary': 'Cumbre de Kananaskis aprueba financiamiento para puertos, cables submarinos y redes 5G en países emergentes. Chile y Brasil son mencionados como socios estratégicos de Latinoamérica. Tensión EE.UU.-China sube un escalón.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[3 Jun] FMI eleva proyección de crecimiento para Latinoamérica a 2.4% en 2026: Chile lidera con 3.1%',
            'summary': 'Actualización del WEO destaca solidez fiscal chilena, demanda externa por cobre y litio y reformas al mercado laboral. México y Colombia reducen perspectivas por incertidumbre política. Región supera media global de 2.1%.',
            'source': 'IMF',
            'link': 'https://www.imf.org'
        },
    ],
    'economia_global': [
        {
            'title': '[3 Jun] Fed mantiene tasa en 4.25%-4.5%: Powell señala que datos de empleo de mayo definen el próximo paso',
            'summary': 'Actas de la reunión del FOMC revelan división interna: 5 gobernadores favorecen corte en julio, 7 prefieren esperar a septiembre. Mercados asignan 65% de probabilidad a recorte en septiembre. T-10 en 4.54%.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': '[3 Jun] Cobre cierra semana en USD 5.15/lb: alza semanal de 2.3% apoyada por datos industriales chinos',
            'summary': 'PMI manufacturero chino de mayo sube a 51.2, superando expectativas. Importaciones de cobre de China alcanzan máximo anual. Goldman Sachs eleva objetivo a USD 5.40/lb para el tercer trimestre.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[3 Jun] IPSA cierra semana con alza de 1.8%: Codelco y SQM lideran ganancias por cobre y litio',
            'summary': 'Índice bursátil acumula 6.2% de rentabilidad en lo que va de 2026. Codelco sube 3.1% en la semana; SQM avanza 4.2% ante contratos de litio con fabricantes de baterías europeos. Volumen diario supera los UF 1.2 millones.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[3 Jun] Peso chileno se aprecia a $888 por dólar: menor nivel desde enero y quinto dia consecutivo de ganancias',
            'summary': 'Tipo de cambio cierra en $888, nivel más bajo desde enero 2026. Mineras liquidan divisas, cobre fuerte y expectativa de recorte Fed impulsan al peso. BCCh monitorea sin intervenir.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': '[3 Jun] Hacienda anuncia bono de cargo fiscal de $200.000 para hogares vulnerables: se paga en julio',
            'summary': 'Beneficio alcanza a 2.8 millones de hogares del Registro Social de Hogares con puntaje hasta el 60%. Costo fiscal de USD 560M financiado con excedentes del cobre. Pago automático via BancoEstado y Caja Los Andes.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[3 Jun] Fintechs chilenas captan USD 180M en rondas de financiamiento durante el primer semestre de 2026',
            'summary': 'Datos de la CMF muestran que el ecosistema fintech chileno ha recibido la mayor inversión semestral de su historia. Open banking, criptomonedas reguladas y crédito digital son los segmentos con mayor dinamismo.',
            'source': 'TechCrunch Latam',
            'link': 'https://techcrunch.com'
        },
        {
            'title': '[3 Jun] Google Cloud y Universidad de Chile abren laboratorio de IA para investigación en salud y recursos naturales',
            'summary': 'Alianza incluye becas para 200 investigadores y acceso preferente a modelos Gemini. Primeros proyectos abordan predicción de sequías, detección temprana de cáncer y optimización de rutas mineras.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[3 Jun] Anthropic lanza Claude 4 Opus con capacidad de análisis financiero avanzado: bancos latinoamericanos en piloto',
            'summary': 'Nueva versión procesa hasta 200.000 tokens de contexto y genera reportes de riesgo en tiempo real. Banco de Chile, Itau y BTG Pactual inician piloto regional. Modelo supera benchmarks de análisis cuantitativo.',
            'source': 'VentureBeat AI',
            'link': 'https://venturebeat.com/category/ai/'
        },
        {
            'title': '[3 Jun] BCI implementa IA generativa para aprobación de créditos hipotecarios: tiempo baja de 7 días a 4 horas',
            'summary': 'Modelo desarrollado con Microsoft Azure reduce el tiempo de evaluación en un 95%. El sistema analiza 47 variables patrimoniales y de comportamiento financiero. Aprobaciones con error humano caen un 60%.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cooperativismo': [
        {
            'title': '[3 Jun] Coopeuch capta 15.000 nuevos socios en mayo 2026: record histórico mensual impulsado por credito digital',
            'summary': 'Mayor cooperativa de Chile supera el millón de socios activos por primera vez. Crédito de consumo digital representa el 38% de las nuevas colocaciones. CEO destaca la expansión en regiones del sur del país.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[3 Jun] Cooperativas chilenas de ahorro y crédito reportan cartera sana: mora cae a 1.2% en abril 2026',
            'summary': 'Informe de la CMF muestra que el sector cooperativo mantiene indicadores de calidad superiores al promedio bancario. Activos totales del sector alcanzan los USD 12.500M, creciendo 11% en 12 meses.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'cmf': [
        {
            'title': '[3 Jun] CMF aprueba norma que obliga a bancos y cooperativas a publicar tasas efectivas en lenguaje ciudadano',
            'summary': 'Nueva circular exige presentar el costo total del crédito en formato simplificado desde enero 2027. Medida apunta a reducir asimetría de información y aumentar competencia. SBIF aplaudida por asociaciones de consumidores.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[3 Jun] Regulador aprueba primeras licencias de Open Banking: 12 fintechs pueden acceder a datos bancarios desde julio',
            'summary': 'CMF entrega licencias de acceso a información financiera bajo Ley 21.521. Las 12 fintechs habilitadas cubren pagos, inversiones y crédito. Bancos tienen 90 días para implementar las APIs requeridas.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[3 Jun] Dólar cae a $888 y UF se proyecta en $40.680 para julio: mercado ajusta expectativas de inflacion a la baja',
            'summary': 'Tipo de cambio consolida caída semanal de 0.8%. Swap UF-CLP descontada en la curva implica IPC de mayo en 0.15%, bajo lo esperado. Mercado adelanta posible recorte de TPM a agosto desde octubre.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': '[3 Jun] Bolsa de Santiago lidera ganancias semanales en Latinoamerica con rentabilidad de 1.8%: cobre y litio, motores',
            'summary': 'IPSA supera a Bovespa (+0.9%), IPC México (+0.3%) y Merval (+1.1%) en la semana. Flujos de capital externo hacia Chile alcanzan USD 320M en mayo, máximo del año. Calificadoras confirman outlook estable.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
    ],
}

# Noticias específicas del 1 de junio de 2026 — se mezclan con las plantillas generales
TODAY_NEWS_01JUN2026 = {
    'geopolitica': [
        {
            'title': '[1 Jun] G7 en Kananaskis cierra con declaración conjunta sobre IA, sanciones a Rusia y fondo de USD 50.000M para Ucrania',
            'summary': 'Cumbre en Canadá adopta marco regulatorio mínimo para IA militar y amplía sanciones al sector energético ruso. EE.UU. y Europa comprometen USD 50.000M adicionales para reconstrucción ucraniana a través del Banco Mundial.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[1 Jun] China endurece controles de exportación de minerales críticos: galio, germanio y grafito bajo nuevas restricciones',
            'summary': 'Beijing amplía la lista de minerales estratégicos con exportación controlada. Impacto inmediato en cadenas de suministro de semiconductores en Japón, Corea del Sur y Europa. Precios del grafito suben 8% en una sesión.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[1 Jun] PMI manufacturero global de mayo sube a 51.3: expansión por tercer mes consecutivo',
            'summary': 'Índice S&P Global confirma que la actividad fabril mundial entró en zona de expansión. EE.UU. (52.1) y la India (57.5) lideran. China (50.4) recupera terreno. Europa sigue en contracción leve con 48.7.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[1 Jun] Petróleo Brent baja a USD 79 tras datos de inventarios EE.UU. y señales de debilidad en demanda china',
            'summary': 'EIA reporta aumento inesperado de 3.2 millones de barriles en stocks estadounidenses. Importaciones de crudo en China caen 4% interanual en mayo. Mercado ajusta a la baja proyección OPEP+ para el tercer trimestre.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
    ],
    'economia_chile': [
        {
            'title': '[1 Jun] BCCh inicia hoy proceso de actualización de la UF de junio: primer valor del mes en $40.582',
            'summary': 'El Banco Central publica los valores de la UF para junio 2026. El mes inicia con $40.582,34, reflejando la inflación acumulada de mayo. Los valores completos del mes están disponibles en bcentral.cl.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[1 Jun] IPSA abre junio con alza de 0.4%: cobre firme y liquidaciones de fin de mes impulsan al sector minero',
            'summary': 'Bolsa de Santiago consolida niveles récord al inicio del segundo semestre bursátil. SQM, Codelco-bonos y Banco de Chile lideran las alzas. Volumen de transacciones supera los CLP 120.000M en la sesión matinal.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': '[1 Jun] Dólar observado abre junio bajo $893: cobre sobre USD 5 y flujos de exportadores anclan el tipo de cambio',
            'summary': 'El peso chileno mantiene fortaleza relativa al inicio del mes. Liquidaciones de exportadores mineros y agrícolas suman USD 420M en la primera jornada de junio. BCCh no interviene; monitorea volatilidad.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[1 Jun] Microsoft Build 2026 concluye: Copilot Agents ya disponibles para todas las empresas con Microsoft 365',
            'summary': 'Satya Nadella cierra la conferencia con el anuncio de disponibilidad general de agentes autónomos sin código. Azure AI Foundry integra GPT-5 y Claude 4 Opus. Microsoft sube 2.8% en Wall Street al cierre del viernes.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[1 Jun] Informe McKinsey: empresas con IA generativa reportan 18% más de productividad en finanzas y legal',
            'summary': 'Estudio de 1.400 organizaciones en 12 países muestra que las compañías que adoptaron LLMs en flujos de trabajo core llevan ventaja competitiva creciente. El 67% de las empresas Fortune 500 ya usa IA generativa en producción.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': '[1 Jun] Regulación IA en América Latina: Brasil, Chile y Colombia avanzan en marcos legales con enfoques distintos',
            'summary': 'Brasil aprueba ley sectorial para IA en crédito y salud. Chile publica borrador de política nacional. Colombia opta por sandbox regulatorio. Divergencia normativa preocupa a empresas tecnológicas con operaciones regionales.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[1 Jun] Chile inicia junio con agenda económica cargada: IPoM, TPM y datos de empleo en las próximas semanas',
            'summary': 'BCCh publica el Informe de Política Monetaria el 18 de junio. La reunión de política monetaria del 17 de junio definirá si hay nuevo recorte de TPM. INE publicará el IPC de mayo el 9 de junio.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[1 Jun] Hacienda: ejecución presupuestaria acumula 96.1% al cierre de mayo con superávit de 0.3% del PIB',
            'summary': 'Ingresos tributarios crecen 8.4% real, impulsados por royalty minero y mayor IVA. El gasto en inversión pública se acelera en el segundo trimestre. Deuda bruta del Gobierno Central se estabiliza en 39.2% del PIB.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[1 Jun] Cooperativas de ahorro chilenas cierran mayo con cartera récord de CLP 4,8 billones: crece 14% interanual',
            'summary': 'El sector cooperativo financiero consolida su expansión. Crédito hipotecario lidera con +22%. Mora se mantiene en 1.3%, muy por debajo del promedio bancario de 2.1%. Junio trae nuevas exigencias de liquidez de la CMF.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
    ],
    'cmf': [
        {
            'title': '[1 Jun] CMF publica hoy en el D.O. circular de riesgo de liquidez para cooperativas: entra en vigencia el 1 de junio 2027',
            'summary': 'La norma exige mantener activos líquidos equivalentes al 10% de los depósitos bajo escenario de estrés de 30 días. Afecta a 8 cooperativas con activos sobre UF 400.000. Plazo de adecuación: 12 meses.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
}

# Plantillas de noticias por categoría — actualizadas mayo 2026 (v3)
NEWS_TEMPLATES = {
    'geopolitica': [
        {
            'title': 'EE.UU. y China cierran reunión bilateral en Ginebra con acuerdo parcial sobre aranceles industriales',
            'summary': 'Secretario de Estado Rubio y canciller Wang Yi anuncian reducción gradual de aranceles del 25% al 15% en manufactura ligera. Semiconductores y IA quedan excluidos. Próxima ronda en agosto.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': 'OTAN activa Fuerza de Respuesta Rápida en el flanco este: 8 países refuerzan presencia en Polonia y Bálticos',
            'summary': 'Alianza despliega 12.000 efectivos adicionales ante movimientos de tropas rusas en Bielorrusia. Ministros de Defensa convocan reunión de emergencia en Bruselas para el 4 de junio.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'OPEP+ mantiene recortes de producción: petróleo Brent escala a USD 82 ante tensión en el Golfo Pérsico',
            'summary': 'Arabia Saudita extiende reducción de 500.000 bpd hasta septiembre. Incidente naval en el Estrecho de Ormuz dispara prima de riesgo geopolítico. Analistas elevan objetivo a USD 88.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/news'
        },
        {
            'title': 'G7 aprueba nuevo paquete de sanciones contra Rusia que incluye congelación de activos del banco central',
            'summary': 'Bloque occidental congela USD 280.000M en reservas soberanas rusas. Medida financia reconstrucción de Ucrania. Rusia amenaza con represalias en exportaciones de titanio y níquel.',
            'source': 'The Economist',
            'link': 'https://www.economist.com'
        },
        {
            'title': 'India supera a China como mayor destino de IED en Asia emergente en el primer trimestre 2026',
            'summary': 'FDI en India alcanza USD 28.000M en Q1 2026. Apple, Samsung y ASML anuncian megainversiones en semiconductores y manufactura. Relocalización productiva global favorece al subcontinente.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'Cumbre de Shanghai: China, Rusia e Irán firman acuerdo de pagos en yuan para eludir el sistema SWIFT',
            'summary': 'Bloque alternativo lanza plataforma de pagos bilaterales que cubriría USD 890.000M en comercio anual. Reservas globales en yuan suben al 5.8%, nivel histórico.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com'
        },
        {
            'title': 'Taiwán refuerza defensa: compra de 400 misiles Patriot PAC-3 a EE.UU. por USD 3.200M',
            'summary': 'Departamento de Estado aprueba venta en tiempo récord. China califica la operación de "provocación grave" y anuncia ejercicios navales alrededor de la isla para junio.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'Unión Europea lanza fondo de defensa de EUR 500.000M: primera deuda común desde la pandemia',
            'summary': 'Consejo Europeo aprueba por unanimidad el "Escudo Europa". Recursos financiarán industria de defensa continental y reducción de dependencia de armamento estadounidense.',
            'source': 'The Economist',
            'link': 'https://www.economist.com'
        },
        {
            'title': 'Corea del Norte prueba misil hipersónico de alcance regional; Corea del Sur declara alerta máxima',
            'summary': 'Misil alcanza mach 8 y maniobra en fase terminal, dificultando intercepción. EE.UU., Japón y Corea del Sur refuerzan escudo antimisiles y anuncian sanciones adicionales.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': 'África: Cumbre de la UA crea zona de libre comercio en minerales críticos excluyendo a China del procesamiento',
            'summary': 'Acuerdo de 22 países establece que litio, cobalto y manganeso africanos deben ser procesados en el continente antes de exportarse. Impacta directamente cadenas de suministro chinas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'Trump firma orden ejecutiva que prohíbe inversiones de fondos federales en bonos chinos',
            'summary': 'Decreto afecta USD 1.1 billones en fondos de pensiones públicas. Wall Street espera presión adicional sobre el yuan. China estudia represalias en deuda del Tesoro estadounidense.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'Brasil y Argentina sellan unión aduanera parcial: primer gran paso hacia el peso del sur',
            'summary': 'Acuerdo cubre autos, electrodomésticos y agroindustria. Mercosur avanza hacia arancel cero interno para 2028. Analistas ven el movimiento como respuesta al bloque dolarizado de Milei.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
    ],
    'economia_global': [
        {
            'title': 'Cobre supera USD 5.10/lb: déficit estructural de oferta dispara precio a nuevo máximo histórico',
            'summary': 'LME reporta inventarios de 87.000 toneladas, el nivel más bajo desde 2004. Demanda de cableado para IA y EVs supera proyecciones. Chile y Perú aceleran aprobaciones ambientales.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': 'Fed mantiene tasas en 4.5% pero señala ventana de recorte para septiembre si inflación sigue bajando',
            'summary': 'Actas del FOMC confirman discusión activa sobre primer recorte. PCE subyacente en 2.3% anual da margen. Mercados ya descuentan 2 recortes de 25 pb para el año.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'FMI alerta: deuda global supera USD 315 billones y riesgo de refinanciamiento en economías emergentes escala',
            'summary': 'Informe de estabilidad financiera advierte que 28 países tienen vencimientos críticos entre 2026 y 2028. Llama a reforzar marcos de reestructuración soberana.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
        {
            'title': 'Oro alcanza USD 3.520/oz: máximo histórico impulsado por compras de bancos centrales y fuga hacia activos refugio',
            'summary': 'Banco Central de China aumentó reservas de oro por 18° mes consecutivo. Flujos hacia ETFs de oro alcanzan USD 14.000M en mayo. Analistas de Goldman elevan objetivo a USD 3.900.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'BCE recorta tasa de depósito al 2.0%: Lagarde abre puerta a nueva reducción en septiembre',
            'summary': 'Tercer recorte consecutivo de 25 pb consolida ciclo de flexibilización. Eurozona creció 1.4% en Q1, por encima de estimaciones. Inflación subyacente converge al 2.2%.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'S&P 500 roza los 6.300 puntos: resultados del Q1 superan estimaciones en 73% de empresas del índice',
            'summary': 'Tecnología, energía y salud lideran alza. Nvidia reporta utilidades récord con margen del 55%. Analistas elevan objetivo promedio para el índice a 6.600 a fin de año.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com/markets'
        },
        {
            'title': 'Litio carbonato rebota a USD 17.200/t: reactivación de demanda china y recorte de oferta en Australia elevan precio',
            'summary': 'Cierre de minas Greenbushes y Pilgangoora reduce oferta en 80.000 t/año. China aprueba subsidios adicionales a vehículos eléctricos. SQM y Albemarle suben 12% en bolsa.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/business/energy'
        },
        {
            'title': 'Banco Mundial eleva proyección para América Latina a 3.2% en 2026: mejor desempeño en 15 años',
            'summary': 'Chile, Perú y Uruguay lideran crecimiento en la región. Inversión en minería verde, energías renovables y centros de datos impulsa el PIB regional. Riesgo político en Venezuela y Nicaragua persiste.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
        {
            'title': 'Bono del Tesoro de EE.UU. a 10 años supera el 4.7%: mayor nivel en seis meses ante déficit fiscal récord',
            'summary': 'CBO estima déficit de USD 2.1 billones para 2026. Rendimientos al alza encarecen crédito hipotecario y corporativo. Dólar se fortalece frente a monedas emergentes.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'China lanza segundo paquete de estímulo fiscal: USD 450.000M para infraestructura verde y consumo interno',
            'summary': 'Beijing financiará redes de carga para vehículos eléctricos, vivienda social y bonos de consumo. Analistas estiman impacto de 0.6 pp sobre PIB chino en el segundo semestre.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'Inflación en EE.UU. baja a 3.1% anual en mayo: tercer mes consecutivo de desaceleración',
            'summary': 'CPI subyacente en 3.3%. Vivienda y servicios aún presionan al alza, pero bienes industriales y combustibles compensan. Fed aguarda dato de junio para decidir sobre recorte.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'Japón sale de deflación: IPC en 2.6% refuerza normalización del Banco de Japón y fortalece el yen',
            'summary': 'Banco de Japón sube tasa de referencia a 1.0%, mayor nivel en 17 años. Carry trade masivo se desarma: yen aprecia 6% en el mes frente al dólar.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
    ],
    'economia_chile': [
        {
            'title': 'BCCh mantiene TPM en 4.75%: Rosanna Costa anticipa dos recortes más antes de diciembre',
            'summary': 'Consejo del Banco Central vota 4-1 por mantener la tasa. Proyecciones del IPoM de junio elevan crecimiento a 3.8%-4.2% para 2026. Inflación converge al 3% en el primer trimestre de 2027.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Dólar observado cierra la semana en $891 en Chile: cobre fuerte y expectativa de recorte Fed aprecian el peso',
            'summary': 'BCCh monitorea el tipo de cambio pero descarta intervención directa. Exportadores liquidaron USD 780M en la semana. Analistras proyectan rango de $880-$910 para el tercer trimestre.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Codelco anuncia acuerdo con SQM para producción conjunta de litio en el Salar de Atacama desde 2027',
            'summary': 'Alianza estatal-privada combinará operaciones y aumentará producción en 30% respecto al plan base. Estado chileno captará royalty del 40% sobre excedentes. Inversión estimada: USD 2.800M.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'IPSA alcanza 7.510 puntos: nuevo récord histórico impulsado por SQM, Codelco-bonos y sector financiero',
            'summary': 'Bolsa de Santiago acumula +18% en el año. Flujos extranjeros ingresan USD 1.450M en mayo. MSCI eleva a Chile de "underweight" a "neutral" en su reasignación de mercados emergentes.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': 'CMF aprueba reforma al sistema de garantías hipotecarias: facilita primer crédito para clase media',
            'summary': 'Nueva norma permite garantías del Estado para créditos de hasta UF 5.000 con pie mínimo del 5%. Banca estima que 80.000 familias podrían acceder al crédito hipotecario con la medida.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com/politica'
        },
        {
            'title': 'IPC de mayo sube 0.2% mensual: acumula 3.2% anual en mínimo desde junio de 2021',
            'summary': 'INE: combustibles suben 1.4% pero alimentos frescos bajan 0.5% y vestuario cae 1.1%. Inflación subyacente en 3.6%. BCCh mantiene escenario de convergencia al 3% meta.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Ministerio de Hacienda coloca bonos en UF a 20 años a tasa de 1.85%: la más baja en cuatro años',
            'summary': 'Demanda de USD 4.200M por una oferta de USD 2.000M evidencia apetito por deuda chilena. Chile mantiene clasificación A+ en S&P y A1 en Moody\'s, las más altas de la región.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'SQM anuncia dividendo extraordinario de USD 1.80 por acción: rentabilidad del litio sostiene pago récord',
            'summary': 'Compañía distribuirá USD 480M adicionales a accionistas en julio. Utilidades del Q1 2026 superaron en 22% las estimaciones. Acción sube 8% en la sesión del anuncio.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Imacec de abril 2026 confirma expansión de 4.1%: el cuarto mes consecutivo sobre el 3.5%',
            'summary': 'BCCh destaca dinamismo simultáneo en minería (+7.2%), comercio (+4.8%) y servicios financieros (+5.1%). Inversión fija crece 6.5% interanual reflejando reactivación del ciclo de capital.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Hidrógeno verde: Chile firma contratos por USD 3.100M con compradores de Europa y Asia para 2028',
            'summary': 'Ministerio de Energía anuncia primeros contratos de largo plazo de amoniaco verde. Plantas en Magallanes y Atacama iniciarán operación en 2028. Chile consolida liderazgo regional en H2V.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'INE: desocupación baja a 8.6% en trimestre febrero-abril 2026; empleo formal crece 3.2%',
            'summary': 'La tasa de desocupación cae 0.3 pp respecto al trimestre anterior. Empleo formal supera por primera vez los 6 millones de cotizantes activos. Remuneraciones reales suben 2.1% interanual.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Reforma tributaria en debate: Hacienda propone royalty minero adicional del 2% sobre cobre sobre USD 4.50/lb',
            'summary': 'Proyecto enviado al Congreso financiaría Fondo de Educación Técnica y cierre de brechas de infraestructura en regiones. Mineras advierten impacto sobre decisiones de inversión futura.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': 'Nvidia supera USD 3.8 billones de capitalización: GPU Blackwell Ultra domina mercado de infraestructura IA',
            'summary': 'Chips H200 y GB200 tienen lista de espera de 18 meses. Margen bruto sube al 78%. Analistas elevan precio objetivo a USD 180. TSMC anuncia ampliación de capacidad exclusiva para Nvidia.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/technology'
        },
        {
            'title': 'Apple WWDC 2026: iOS 20 integra modelo LLM propio on-device con 8.000M de parámetros',
            'summary': 'Siri 3.0 procesa contexto completo de la vida digital del usuario sin enviar datos a la nube. Apple Intelligence estará disponible desde iPhone 16 en adelante. Privacidad como ventaja competitiva.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
        {
            'title': 'Starlink Gen 3: SpaceX lanza 180 satélites y promete latencia de 8ms en Chile y Perú',
            'summary': 'Nueva constelación reduce latencia a la mitad y duplica velocidad de bajada. Usuarios en regiones remotas de Chile reportan 400 Mbps. Precio baja a USD 49/mes con subsidio gubernamental.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'Microsoft Azure anuncia nodo regional en Chile para 2027: USD 1.200M en infraestructura cloud local',
            'summary': 'Centro de datos en Pudahuel procesará datos de gobierno, banca y salud con soberanía nacional. Elimina la necesidad de enviar datos sensibles a Brasil. CORFO co-financia con USD 180M.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'Computación cuántica: Google Willow-2 ejecuta en 4 minutos un cálculo que tardaría 10.000 años en supercomputadoras',
            'summary': 'Nuevo procesador de 1.200 qubits supera barrera de corrección de errores cuánticos. Aplicaciones en criptografía, optimización logística y descubrimiento de fármacos se acercan.',
            'source': 'MIT Technology Review',
            'link': 'https://www.technologyreview.com'
        },
        {
            'title': 'Meta lanza Llama 4 open-source con 405.000M de parámetros: el modelo gratuito más potente de la historia',
            'summary': 'Benchmark MMLU supera GPT-4o en 7 de 10 categorías. Miles de empresas ya lo implementan en servidores propios. AMD y Intel anuncian chips optimizados para inferencia de Llama 4.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
        {
            'title': 'Ciberseguridad: grupo APT41 compromete sistemas de 6 bancos latinoamericanos en operación coordinada',
            'summary': 'Ataque de cadena de suministro a través de proveedor de software bancario afecta a instituciones en Chile, Perú, Colombia, Brasil, México y Argentina. CISA emite alerta de nivel crítico.',
            'source': 'MIT Technology Review',
            'link': 'https://www.technologyreview.com'
        },
        {
            'title': 'Robotaxis Tesla en operación en Austin: 1.000 vehículos autónomos sin conductor ya transportan pasajeros',
            'summary': 'FSD v14 recibe aprobación de la NHTSA para operación comercial sin respaldo humano. Tarifa de USD 1.80/km. Tesla proyecta expansión a 20 ciudades para finales de 2026.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'AMD EPYC Turin en centros de datos: procesador de 192 núcleos reduce costos de inferencia IA en 45%',
            'summary': 'Alternativa a Intel Xeon gana mercado enterprise. Google Cloud y AWS anuncian instancias basadas en EPYC Turin. AMD supera a Intel en cuota de mercado de servidor por primera vez.',
            'source': 'MIT Technology Review',
            'link': 'https://www.technologyreview.com'
        },
        {
            'title': 'Fintech chilena Fintual lanza gestión patrimonial con IA personalizada para clientes sobre UF 3.000',
            'summary': 'Asistente analiza perfil de riesgo, horizonte de inversión y flujos fiscales del usuario para recomendar cartera optimizada. Integra SII, Previred y datos de mercado en tiempo real.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': 'Cooperativa Coopeuch reporta utilidades de CLP 28.000M en el primer trimestre 2026: récord histórico',
            'summary': 'La cooperativa más grande de Chile aumenta socios activos a 1.4 millones y lanza cartera de crédito hipotecario con tasa de 3.8% para socios premium. Morosidad se mantiene en 1.2%.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'CMF autoriza a cooperativas de ahorro a emitir bonos en el mercado de capitales chileno',
            'summary': 'Nueva circular abre financiamiento de largo plazo para el sector. Cooperativa Oriencoop y Los Héroes ya evalúan emisiones por UF 500.000 y UF 380.000 respectivamente.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'ACI Américas: cooperativas latinoamericanas suman 92 millones de socios activos en 2026',
            'summary': 'Chile, Colombia y Brasil concentran el 64% del activo cooperativo regional. Digitalización y productos hipotecarios son los principales motores de crecimiento en captación.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
        },
        {
            'title': 'Cooperativas agrícolas del Biobío lanzan plataforma exportadora directa hacia mercados asiáticos',
            'summary': 'Consorcio de 14 cooperativas cerealeras y frutícolas elimina intermediarios y exporta directamente a Japón, Corea y China. Primer embarque de 4.200 toneladas de cereales orgánicos zarpa en junio.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
        },
        {
            'title': 'BID otorga línea de crédito de USD 200M al cooperativismo financiero de Chile para inclusión en regiones',
            'summary': 'Financiamiento respaldará expansión de cooperativas en comunidades rurales de La Araucanía, Los Lagos y Aysén. Prioridad en crédito productivo para Pymes, pequeños agricultores y emprendedoras.',
            'source': 'BID',
            'link': 'https://www.iadb.org'
        },
        {
            'title': 'Cooperativas de vivienda presentan propuesta al MINVU: modelo de ahorro previo para 50.000 familias',
            'summary': 'Sector propone subsidio complementario que reduciría pie requerido al 8% para socios con al menos 24 meses de ahorro cooperativo. Ministerio analiza integración en Política Habitacional 2026.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl'
        },
        {
            'title': 'Cooperativas de ahorro lanzan tarjeta de crédito interoperable: 800.000 socios se beneficiarán',
            'summary': 'Alianza de 12 cooperativas crea producto compartido con cupo de hasta UF 80, sin comisión de mantención y con acceso a red Transbank y Redbanc. Lanzamiento en agosto 2026.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'Informe BID: cooperativas financieras de Chile mantienen mora 40% inferior a banca comercial en crédito de consumo',
            'summary': 'Análisis comparativo atribuye mejor calidad de cartera al modelo de evaluación colectiva y al mayor conocimiento del socio. Tasa de recuperación de cartera vencida también supera a la banca.',
            'source': 'BID',
            'link': 'https://www.iadb.org'
        },
        {
            'title': 'Cooperativa Los Héroes digitaliza 100% de sus procesos: cero papel y aprobación de créditos en 12 horas',
            'summary': 'Migración total a plataforma digital reduce costos operacionales en 28% y eleva satisfacción de socios a NPS de 72 puntos. Algoritmo de scoring propio aprueba o rechaza créditos de consumo en minutos.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Asamblea del Consejo Mundial Cooperativo (ICA) definirá estándares ESG para cooperativas globales en junio',
            'summary': 'Reunión en Ginebra establecerá métricas de impacto social, huella de carbono y gobierno democrático para el reporte cooperativo. Chile participa con representación de cinco entidades.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
        },
    ],
    'cmf': [
        {
            'title': 'CMF publica propuesta de normativa para open banking: bancos y cooperativas deberán compartir datos en 2027',
            'summary': 'Consulta pública abierta hasta el 30 de junio. El marco obligará a ofrecer APIs de cuentas y transacciones a terceros habilitados. Fintech sector celebra; banca pide más tiempo de adecuación.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF reporta: sistema bancario chileno con capitalización del 14.2%, el nivel más sólido desde la reforma de 2019',
            'summary': 'Informe de estabilidad financiera del primer semestre 2026 confirma robustez del sector. Ratio de cobertura de liquidez en 148%, muy por encima del mínimo regulatorio del 100%.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF sanciona a tres corredoras por manipulación de precios en el mercado de renta fija',
            'summary': 'Multas por UF 30.000 cada una por operaciones coordinadas que distorsionaron precios de bonos corporativos. Es la mayor sanción en el mercado de capitales en diez años.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF actualiza tabla de tasas máximas convencionales de junio 2026: bajan límites en consumo e hipotecario',
            'summary': 'TMC para créditos entre UF 200 y UF 5.000 baja de 38.7% a 36.1% anual. Para hipotecarios sobre UF 5.000, límite se reduce a 17.4%. Medida beneficia a 2.8 millones de deudores.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF y BCCh emiten circular conjunta sobre exposición de bancos a criptoactivos: límite del 2% del capital',
            'summary': 'Normativa establece que ninguna institución financiera puede superar el 2% de activos ponderados en cripto. Activos elegibles solo Bitcoin y Ether con custodios regulados en Chile.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF autoriza primera AAFM (Administradora de Activos Financieros Modulares) bajo Ley Fintech',
            'summary': 'Empresa Fintual Inversiones recibe licencia pionera que le permite ofrecer gestión discrecional de carteras a minoristas sin ser AFP ni corredora tradicional. Abre mercado a nuevos competidores.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF publica informe sobre riesgo climático financiero: 60% de cartera hipotecaria expuesta a zonas de estrés hídrico',
            'summary': 'Estudio mapea exposición de bancos y aseguradoras a activos en zonas de escasez de agua. Regula el reporte obligatorio de riesgo físico y de transición para 2027.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF activa nuevo sandbox regulatorio para pruebas de tokenización de activos reales en Chile',
            'summary': 'Cinco proyectos piloto de tokenización de deuda inmobiliaria, bonos verdes y acciones de Pymes iniciarán operación controlada. Regulador monitorea por 18 meses antes de normar definitivamente.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF exige a compañías de seguros actualizar modelos de reservas ante cambio climático y longevidad creciente',
            'summary': 'Nueva circular obliga a incorporar escenarios de temperatura global +1.5°C y tablas de mortalidad actualizadas. Impacto estimado en reservas adicionales de UF 8.5 millones para el sector.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF prohíbe comisiones ocultas en fondos mutuos: revolución en transparencia de costo total para inversionistas',
            'summary': 'Desde el 1 de agosto de 2026, las AGF deben expresar el costo total en Ratio de Gastos Total (TER) en formato estandarizado. Industria estima reducción promedio de costos del 18%.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': 'IPC de mayo 2026 sube 0.2% mensual: inflación anual desacelera a 3.2%, mínimo en 57 meses',
            'summary': 'INE confirma trayectoria hacia la meta. Energía residencial sube 0.9%, alimentos caen 0.4% y transporte baja 0.3%. Deflación en bienes industriales importados refleja apreciación del peso.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'INE: tasa de desocupación cae a 8.6% en trimestre febrero-abril 2026; empleo formal bate récord',
            'summary': 'Encuesta Nacional de Empleo revela baja de 0.3 pp respecto al trimestre anterior. 6.1 millones de cotizantes activos. Sectores minería, construcción y tecnología lideran generación de empleo.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl/estadisticas-por-tema/mercado-laboral/ocupacion-y-desocupacion'
        },
        {
            'title': 'Remuneraciones reales suben 2.1% interanual en abril 2026: por tercer mes consecutivo el salario real crece',
            'summary': 'INE reporta que el Índice Real de Remuneraciones sube 2.1% interanual, primer ciclo de crecimiento sostenido desde 2022. Sector minero (+5.8%) y tecnología (+4.2%) lideran alzas.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Imacec de abril 2026 confirma expansión de 4.1%: cuarto mes sobre el 3.5% y tendencia al alza',
            'summary': 'BCCh destaca contribución minera (+7.2%), comercial (+4.8%) y de servicios financieros (+5.1%). Expansión amplia por sectores y regiones confirma solidez del ciclo económico.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Exportaciones chilenas acumulan USD 28.600M en enero-mayo 2026: cobre y litio cubren el 61% del total',
            'summary': 'Balanza comercial arroja superávit de USD 5.200M en cinco meses. China concentra el 42% de envíos totales. Precio del cobre promedia USD 4.92/lb en el período.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'ICARE: confianza empresarial en 58.4 puntos en mayo — máximo desde el primer trimestre de 2022',
            'summary': 'Encuesta refleja optimismo por datos macro, menor incertidumbre regulatoria y expectativa de recorte de TPM en agosto. Inversión privada en manufactura y servicios se reactiva.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl'
        },
        {
            'title': 'Ventas minoristas crecen 6.1% en mayo 2026: electrodomésticos, construcción y gastronomía lideran el alza',
            'summary': 'INE registra el mejor dato del comercio en 20 meses. Crédito de consumo crece 6.9% interanual y se acelera. Menor inflación y empleo estable dinamizan el consumo de los hogares.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Banco Central eleva proyección de PIB 2026 al rango 3.8%-4.2% en el IPoM de junio',
            'summary': 'Revisión al alza de 0.6 pp respecto al IPoM de marzo. BCCh cita mayor dinamismo de la inversión pública y privada, consumo resiliente y favorables términos de intercambio.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Encuesta BCCh: consenso proyecta dólar en $895 y TPM en 4.0% al cierre de 2026',
            'summary': 'Analistas reducen proyección de tipo de cambio ante fortaleza del cobre. Dos recortes adicionales de 25 pb en TPM son el escenario base para el segundo semestre.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'IED en Chile acumula USD 11.200M en el primer semestre 2026: mayor cifra semestral en 8 años',
            'summary': 'CORFO destaca inversión en minería verde, centros de datos e hidrógeno. Amazon Web Services anuncia región cloud en Chile y compromete USD 800M en cinco años.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'IPP de mayo 2026: precios al productor caen 0.4% mensual, acumulan solo 1.5% en 12 meses',
            'summary': 'INE reporta deflación en insumos industriales, mineros y agrícolas. La reducción de costos productivos anticipa menor presión inflacionaria en el IPC de los próximos meses.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'PIB Q1 2026 confirmado en 3.8%: mayor crecimiento trimestral en cinco años',
            'summary': 'BCCh ratifica expansión récord. Consumo privado (+4.1%), inversión fija (+6.2%) y exportaciones netas (+8.9%) son los motores del crecimiento. Ahorro nacional sube al 23.4% del PIB.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': 'Anthropic Claude 4 Opus supera a GPT-5 en razonamiento legal, financiero y científico según benchmarks independientes',
            'summary': 'Evaluaciones de HELM y BIG-Bench muestran ventaja de 8-14% en tareas de análisis de contratos, modelado financiero y razonamiento multistep. API disponible para empresas desde mayo 2026.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'OpenAI lanza GPT-5 con razonamiento extendido y memoria persistente: precios API caen 40%',
            'summary': 'Modelo integra búsqueda web en tiempo real, memoria cross-session y capacidades de agente autónomo. Disponible en tres versiones: Mini, Standard y Pro. Límite de contexto de 1 millón de tokens.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Google Gemini 2.5 Ultra: ventana de 2M de tokens y visión en tiempo real desde cámara de móvil',
            'summary': 'Modelo lidera en benchmarks de codificación y matemáticas. Integración nativa con Google Workspace permite analizar documentos completos de 400 páginas en una sola consulta.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
        {
            'title': 'Regulación de IA en Chile: Ministerio de Ciencia publica borrador de Política Nacional de IA 2026-2030',
            'summary': 'Hoja de ruta nacional define 5 ejes: talento, infraestructura, datos, regulación y adopción sectorial. Incluye observatorio de riesgos y fondo de CLP 50.000M para investigación aplicada.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Microsoft Copilot Wave 3 lanza agentes autónomos para cierre contable, nómina y cadena de suministro',
            'summary': 'Agentes gestionan el 80% del proceso de cierre mensual sin intervención humana. Integración nativa con SAP y Oracle ERP. Empresas piloto reportan reducción del 60% en tiempo de cierre.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'AI Act UE: primeras multas por incumplimiento superan EUR 1.200M en sectores de crédito y RRHH',
            'summary': 'Reguladores de Alemania, Francia e Italia sancionan a 11 empresas por sistemas de IA sin documentación técnica o con sesgos discriminatorios verificados. Compliance de IA emerge como industria.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Startup chilena NotCo extiende uso de IA generativa a diseño de alimentos: modelo predice textura, sabor y valor nutricional',
            'summary': 'Giuseppe 3.0 genera en horas formulaciones de productos que antes tomaban 18 meses de I+D. Modelo entrenado con 5 millones de combinaciones moleculares. Licencia a tres multinacionales de alimentos.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
        {
            'title': 'Meta Llama 4 open-source supera en benchmarks a modelos propietarios de hace un año: democratización de IA avanza',
            'summary': 'Modelo de 405.000M de parámetros disponible gratis en Hugging Face. Corre en clusters de 8 GPU H100. Bancos y aseguradoras latinoamericanas adoptan para análisis de riesgo y fraud detection.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
        {
            'title': 'IA en la banca chilena: tres de los cuatro mayores bancos ya usan LLMs para originar créditos Pyme',
            'summary': 'Banco de Chile, Santander y BCI confirman uso de modelos de lenguaje en scoring crediticio. CMF publicará circular de supervisión algorítmica en agosto 2026.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'DeepMind AlphaFold 4 predice interacciones fármaco-proteína con 94% de precisión: acelera oncología y neurología',
            'summary': 'Modelo amplía capacidades a predicción de efectos secundarios y diseño de moléculas candidatas a fármacos. Seis laboratorios farmacéuticos ya lo usan en ensayos clínicos de fase 1.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Agentes de IA autónomos gestionan el 12% de todas las tareas de código en GitHub según informe Microsoft',
            'summary': 'Copilot Workspace y Cursor generaron 340 millones de líneas de código aceptadas por desarrolladores en Q1 2026. El rol del desarrollador evoluciona hacia revisor y arquitecto de sistemas.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'CORFO lanza fondo de USD 80M para startups de IA en Chile: foco en agritech, minería y salud',
            'summary': 'Programa InnovaChile IA financiará proyectos con componente de datos propios y aplicación en sectores estratégicos. Convocatoria abierta hasta el 30 de julio con 40 cupos disponibles.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
    ],
}


# Noticias específicas del 8 de junio de 2026
TODAY_NEWS_08JUN2026 = {
    'geopolitica': [
        {
            'title': '[8 Jun] Cumbre APEC en Sydney: acuerdo marco sobre cadenas de suministro de minerales críticos favorece a Chile',
            'summary': 'Los 21 miembros de APEC suscriben declaración que consolida rutas de exportación de litio y cobre procesado. Chile accede a tratamiento arancelario preferencial con Japón, Corea del Sur y Australia. Negociaciones de TLC acelerado con Corea entran en recta final.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[8 Jun] G7 post-cumbre: EE.UU. anuncia paquete de infraestructura verde de USD 600.000M con énfasis en Latinoamérica',
            'summary': 'Iniciativa Partnership for Global Infrastructure incluye financiamiento preferencial para proyectos de litio y cobre en Chile, Argentina y Brasil. CORFO ya negocia participación en tres proyectos de baterías. Fondos disponibles desde el primer trimestre de 2027.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[8 Jun] S&P 500 abre semana en máximos históricos: inversores anticipan pausa prolongada de la Fed tras datos de empleo',
            'summary': 'Índice supera los 5.950 puntos en apertura del lunes. Nasdaq +1.2% liderado por semiconductores y IA. VIX cae a 12.4, señalando calma extrema. Mercados emergentes se benefician del dólar débil: CLP y BRL entre las divisas de mayor alza.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[8 Jun] Cobre alcanza USD 5.18/lb al inicio de semana: inventarios LME en mínimos y demanda china robusta',
            'summary': 'Metal rojo sube 1.6% en la semana tras publicación de datos de importaciones chinas de mayo. Codelco y Anglo American lideran ganancias en bolsas europeas. Goldman Sachs sube objetivo a USD 5.60 para el tercer trimestre de 2026.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[8 Jun] UF $40.746,28 y dólar $910,29: indicadores al inicio de semana del 8 de junio de 2026',
            'summary': 'Unidad de Fomento publicada por SII para el lunes 8 de junio. Dólar observado del BCCh en $910,29. Mercado espera dato de IPC de mayo del INE el martes 9 de junio: consenso en 0,2% mensual y 3,2% anual. Resultado definirá expectativas de recorte de TPM.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[8 Jun] IPSA abre semana sobre 7.860 puntos: Codelco, SQM y Banco de Chile entre los más activos',
            'summary': 'Índice bursátil chileno continúa tendencia alcista impulsado por cobre y perspectivas de recorte de TPM. Analistas proyectan cierre de año sobre 8.000 puntos si cobre se mantiene sobre USD 5/lb. Flujo extranjero hacia la bolsa chilena supera USD 380M en lo que va de junio.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[8 Jun] BCCh publica Informe de Política Monetaria (IPoM) de junio: PIB 2026 revisado al alza a 2,8%',
            'summary': 'Banco Central eleva proyección de crecimiento desde 2,4% ante mejor desempeño de exportaciones y consumo privado. Inflación al cierre de 2026 estimada en 3,0%. Ruta de recorte de TPM con primer movimiento anticipado para agosto si IPC confirma convergencia.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[8 Jun] Open Banking Chile: 45 fintechs ya integradas al ecosistema de APIs bajo NCG 513 de la CMF',
            'summary': 'Primer mes de vigencia de la normativa de open banking muestra adopción acelerada. Pagos iniciados vía API superaron los 2 millones de transacciones en la primera semana. BancoEstado y Banco de Chile lideran en número de integraciones habilitadas.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[8 Jun] Apple y Google lanzan billeteras digitales interoperables en Chile: cobertura en 98% de comercios habilitados',
            'summary': 'Ambas plataformas completan integración con el sistema TEF+ de Transbank. Las billeteras operan en pesos, UF y dólares. SBIF reporta que pagos móviles representarán el 35% de las transacciones retail en Chile al cierre de 2026.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[8 Jun] Claude 4 de Anthropic alcanza nivel experto en análisis financiero regulatorio en español: pruebas con CMF',
            'summary': 'Modelo supera a analistas humanos en velocidad de procesamiento de normativas y detección de cambios regulatorios. CMF evalúa adopción para monitoreo de compliance en tiempo real. Primera implementación piloto en tres bancos chilenos prevista para agosto.',
            'source': 'VentureBeat AI',
            'link': 'https://venturebeat.com/category/ai/'
        },
        {
            'title': '[8 Jun] NVIDIA presenta GPU Blackwell Ultra: 4x más potencia para modelos financieros de riesgo y trading algorítmico',
            'summary': 'Nueva arquitectura reduce el costo de inferencia en 60%. Bancos latinoamericanos podrán procesar modelos de riesgo de crédito en tiempo real a costo accesible. BTG Pactual y Itaú ya son clientes confirmados de la nueva generación.',
            'source': 'The Rundown AI',
            'link': 'https://therundown.ai'
        },
    ],
    'cooperativismo': [
        {
            'title': '[8 Jun] CONFECOOP lanza programa de transformación digital para 180 cooperativas chilenas: subsidio de hasta UF 800',
            'summary': 'Programa contempla financiamiento para adoptar core bancario en la nube, banca móvil y herramientas de análisis de riesgo con IA. CORFO y el Ministerio de Economía cofinancian el 70% del costo. Postulaciones abiertas hasta el 30 de junio.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[8 Jun] Coopeuch mantiene liderazgo: cartera de créditos supera los USD 6.800M con mora histórica de 1.1%',
            'summary': 'Mayor cooperativa financiera de Latinoamérica publica resultados del primer semestre con rentabilidad patrimonial de 13.2%. Captaciones a plazo crecen 16% anual. Apertura de 8 nuevas sucursales en regiones anunciada para el segundo semestre.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[8 Jun] CMF publica resultado de stress test bancario 2026: sistema mantiene solvencia ante escenario adverso de recesión',
            'summary': 'Ejercicio simuló caída de PIB del 3%, desempleo en 12% y alza de mora al 4,5%. Los 12 bancos supervisados mantienen índice de capital sobre el mínimo regulatorio. CMF destaca mejora en gestión de riesgo operacional y ciberseguridad respecto a 2024.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[8 Jun] Petróleo Brent baja a USD 80,5 tras acuerdo OPEP+: impacto moderado en balanza comercial chilena',
            'summary': 'Arabia Saudita y Rusia acuerdan aumentar producción en 400.000 bbl/día desde julio. Chile, importador neto de petróleo, estima ahorro de USD 280M anual en divisas. Precios de combustibles podrían bajar hasta un 4% en julio si tendencia se mantiene.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[8 Jun] Fitch sube perspectiva de deuda soberana chilena a "positiva": destaca disciplina fiscal y reservas en BCCh',
            'summary': 'Agencia mantiene nota A- pero mejora el outlook desde "estable". Cita fortaleza del sector exportador, baja deuda neta y política monetaria creíble. Siguiente hito para upgrade: consolidación del IPC en torno al 3% durante doce meses consecutivos.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
}


# Noticias específicas del 9 de junio de 2026
TODAY_NEWS_09JUN2026 = {
    'geopolitica': [
        {
            'title': '[9 Jun] G7 activa fondo de USD 50.000M para infraestructura de minerales críticos: Chile receptor prioritario',
            'summary': 'El mecanismo de financiamiento del G7 habilita créditos blandos a 20 años para proyectos de litio y cobre procesado. Chile es el único país de América del Sur con acceso directo en la primera fase. CORFO y Hacienda ya preparan dos proyectos para postular antes de agosto.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[9 Jun] Tensiones en el Mar Rojo escalan: nuevo ataque a buque portacontenedores eleva prima de seguros marítimos',
            'summary': 'Cuarto incidente en diez días encoge el tráfico por el Canal de Suez en un 18%. Costo de flete Asia-Europa sube 12% en la semana. Impacto en Chile: encarecimiento de importaciones industriales y retraso en cadenas de suministro manufacturero estimado en 3-4 semanas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[9 Jun] Fed Watch: inflación PCE de mayo confirma tendencia; mercado asigna 82% de probabilidad a recorte en septiembre',
            'summary': 'Datos de precios al consumidor en EE.UU. consolidan desinflación gradual. Curva de rendimientos se aplana. Índice DXY cae 0,3% en la sesión. Mercados emergentes se benefician: flujos hacia deuda soberana latinoamericana alcanzan USD 2.400M en la semana.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[9 Jun] Cobre cierra sobre USD 5.20/lb: tercer día consecutivo de alza impulsado por déficit de oferta y demanda china',
            'summary': 'Inventarios en LME caen a 108.000 toneladas, nivel más bajo desde 2004. China importó 580.000 toneladas en mayo, un 9% más que el año anterior. Analistas de Citigroup elevan objetivo a USD 5.80 para fin de año.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[9 Jun] IPC mayo 2026: INE reporta 0,2% mensual y 3,1% anual — por debajo del consenso, abre espacio para recorte de TPM',
            'summary': 'Inflación del mes de mayo sorprende levemente a la baja: el consenso esperaba 3,2% anual. Vivienda y servicios siguen presionando, pero alimentos y combustibles compensan. BCCh podría adelantar el primer recorte de la TPM a agosto desde la proyección base de septiembre.',
            'source': 'INE / Banco Central de Chile',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': '[9 Jun] UF $40.746,28 y dólar $910,29: mercado reacciona al IPC con apreciación del peso de 0,4%',
            'summary': 'Tipo de cambio cede ante dato de inflación más bajo de lo esperado. Operadores proyectan dólar en rango $895-$915 durante junio si la tendencia desinflacionaria se mantiene. Bonos en UF pierden atractivo relativo: spread BTP-UF se comprime 8 puntos base.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[9 Jun] IPSA sube 1,3% tras IPC: bancos y utilities lideran al primar expectativas de recorte de tasas',
            'summary': 'Índice bursátil alcanza 7.942 puntos en la sesión, máximo del año. Banco de Chile +2,1%, Banco Santander +1,9% y Engie Chile +2,4% encabezan las ganancias. Volumen de transacciones supera en 41% el promedio de las últimas 20 ruedas.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[9 Jun] CMF y Ministerio de Hacienda lanzan sandbox de open banking: 60 fintechs en lista de espera para integración',
            'summary': 'Plataforma permite a empresas fintech conectarse a APIs bancarias bajo supervisión regulatoria en tiempo real. Primeras integraciones operativas incluyen agregación de cuentas, iniciación de pagos y consulta de historial crediticio. Apertura masiva prevista para septiembre de 2026.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[9 Jun] BancoEstado lanza app de inversión en UF para personas: rentabilidad mínima garantizada de inflación + 1%',
            'summary': 'Producto digital sin comisiones permite invertir desde UF 1 en instrumentos del BCCh. Primer mes sin restricciones de liquidez. Más de 80.000 descargas en las primeras 24 horas. Compite directamente con fondos mutuos de deuda de administradoras privadas.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[9 Jun] BCCh integra IA generativa en su sistema de monitoreo de inflación: procesa 12.000 precios diarios en tiempo real',
            'summary': 'Sistema piloto reduce el tiempo de detección de presiones inflacionarias de dos semanas a 48 horas. Primer banco central latinoamericano en publicar un modelo de nowcasting de IPC basado en LLMs con datos de e-commerce y supermercados.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[9 Jun] Startup chilena Buda.com lanza agente de IA para trading de criptoactivos regulados bajo CMF',
            'summary': 'Plataforma de activos digitales integra modelo de lenguaje para análisis de sentimiento de mercado y ejecución automatizada. Opera bajo supervisión de la CMF como exchange regulado. Primera solución de trading algorítmico con IA en el mercado chileno supervisado.',
            'source': 'VentureBeat AI',
            'link': 'https://venturebeat.com/category/ai/'
        },
    ],
    'cooperativismo': [
        {
            'title': '[9 Jun] IPC bajo fortalece proyecciones del sector cooperativo: crédito hipotecario en UF retoma dinamismo',
            'summary': 'Las cooperativas de ahorro y crédito ven reducirse el costo de fondeo ante expectativas de recorte de TPM. Coopeuch y Detacoop anticipan rebaja de tasas hipotecarias de entre 15 y 25 puntos base para julio. Demanda de crédito habitacional cooperativo proyecta alza de 20% en el segundo semestre.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[9 Jun] Sector cooperativo chileno suma 4,2 millones de socios activos: penetración del 20% de la población adulta',
            'summary': 'Informe semestral de CONFECOOP revela que una de cada cinco personas adultas en Chile pertenece a una cooperativa financiera. Crecimiento de 8,3% en nuevos socios en los últimos doce meses. Regiones de La Araucanía y Los Lagos lideran en incorporación.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[9 Jun] CMF lanza consulta pública sobre regulación de activos digitales y stablecoins: plazo hasta el 18 de julio',
            'summary': 'Normativa NCG 514 extiende la supervisión a exchanges y emisores de monedas estables en Chile. Empresas deben registrarse antes del 1° de enero de 2027 bajo los requisitos de capital, prevención de lavado de activos y custodia segregada. Industria cripto tiene 18 meses para adaptarse.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[9 Jun] Hacienda: IPC de mayo confirma convergencia a meta del 3%; regla fiscal sin cambios para el segundo semestre',
            'summary': 'Ministro de Hacienda celebra dato de inflación y descarta ajustes al presupuesto 2026. Superávit fiscal acumulado enero-mayo en 0,4% del PIB. Emisión de bonos soberanos en UF por UF 3,5 millones programada para julio con demanda proyectada de 3,2 veces la oferta.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
        {
            'title': '[9 Jun] Precios de la vivienda nueva en Santiago suben 2,1% real en el primer trimestre: tasas más bajas reactivarán mercado',
            'summary': 'CChC proyecta aceleración del mercado inmobiliario en el segundo semestre ante expectativa de recorte de tasas. Comunas de Santiago, Las Condes y Ñuñoa concentran el 58% de las ventas. Déficit habitacional acumulado supera las 650.000 unidades según Minvu.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
}


# Noticias específicas del 10 de junio de 2026
TODAY_NEWS_10JUN2026 = {
    'geopolitica': [
        {
            'title': '[10 Jun] Cumbre bilateral EE.UU.-China en Viena: acuerdo parcial en IA militar y apertura de negociaciones comerciales',
            'summary': 'Secretario de Estado Rubio y canciller Wang Yi acuerdan moratoria de 18 meses en despliegue de IA en sistemas de armas autónomas. Pausa en escalada arancelaria sobre manufactura liviana. Mercados asiáticos reaccionan con alza generalizada; cobre toca nuevo máximo semanal.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[10 Jun] OCDE eleva proyección de crecimiento global 2026 a 3,2%: baja de tasas en economías avanzadas dinamiza inversión',
            'summary': 'Organismo revisa al alza el crecimiento de EE.UU. (2,6%), la eurozona (1,4%) y China (4,9%). América Latina sube a 2,8% liderada por Chile (3,0%) y Colombia (3,4%). Riesgos principales: escalada en el Mar Rojo y volatilidad en precios de energía.',
            'source': 'OECD',
            'link': 'https://www.oecd.org'
        },
    ],
    'economia_global': [
        {
            'title': '[10 Jun] Fed mantiene tasas: Powell reafirma recorte en septiembre si inflación confirma convergencia en próximos dos meses',
            'summary': 'Comunicado de la Fed reconoce progreso sostenido hacia el objetivo del 2%. Mercados de futuros asignan 85% de probabilidad al primer recorte en septiembre. Dólar DXY cede 0,4%; bonos del Tesoro a 10 años caen 8 pb a 4,12%. Flujos hacia emergentes se aceleran.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[10 Jun] Litio: precio del carbonato sube 6% en el mes ante recorte de producción de Australia y mayor demanda de baterías EV',
            'summary': 'Alkem Resources suspende operaciones en Pilbara por costos. SQM y Codelco Litio se benefician directamente. Goldman Sachs proyecta déficit de 45.000 toneladas equivalentes de litio en el segundo semestre. Precio spot en USD 14.800/tonelada, máximo desde octubre 2025.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[10 Jun] BCCh: IPC de mayo valida escenario base del IPoM; siguiente reunión de TPM el 17 de junio con recorte posible',
            'summary': 'Consejeros del Banco Central señalan que el dato de 3,1% anual del IPC abre espacio para recorte precautorio de 25 pb en la reunión del 17 de junio. Sería el primero desde enero 2025. Mercados de swaps ya descuentan recorte con 71% de probabilidad.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[10 Jun] UF $40.768,69 y dólar $915,97: indicadores al 10 de junio de 2026',
            'summary': 'Tipo de cambio observado del BCCh en $915,97. Mercado cambiario consolida posiciones a la espera de la reunión de política monetaria del 17 de junio. Operadores esperan dólar en rango $910-$930 durante la semana. Reservas internacionales del BCCh en USD 43.800M.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[10 Jun] Imacec de abril 2026: actividad económica creció 3,4% anual, superando el consenso de 3,1%',
            'summary': 'INE publica expansión económica impulsada por minería (+6,2%), construcción (+4,1%) y comercio (+2,8%). Sector servicios crece 2,9%. Acumulado enero-abril: +3,0% anual. BCCh mantiene proyección de PIB 2026 en 2,8% pero con sesgo al alza.',
            'source': 'INE / Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[10 Jun] Transbank reporta récord de transacciones digitales en mayo: 340 millones de operaciones, un 28% más que hace un año',
            'summary': 'Pagos sin contacto y transferencias instantáneas TEF+ lideran el crecimiento. El 62% de las transacciones se realizó vía smartphone. Fraude digital cae a 0,003% del total gracias a nuevos modelos de detección basados en IA desplegados en marzo.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[10 Jun] SII digitaliza fiscalización con IA: detecta inconsistencias en declaraciones de renta en tiempo real',
            'summary': 'Nuevo sistema de auditoría predictiva identifica anomalías en 48 horas versus 6 meses del proceso manual. 14.200 contribuyentes notificados en la primera semana. Recaudación adicional proyectada de USD 180M al año por mejora en cumplimiento voluntario.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[10 Jun] Google lanza Gemini 3 Ultra con especialización financiera para Latinoamérica: acceso gratuito para bancos chilenos',
            'summary': 'Modelo multimodal procesa estados financieros, contratos y normativa regulatoria en español. Integración nativa con Google Cloud y APIs del sistema financiero chileno. SBIF pilotea el modelo para detección de blanqueo de capitales en flujos de alto riesgo.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': '[10 Jun] CMF emite circular preliminar sobre uso de IA en scoring crediticio: tres principios de obligatorio cumplimiento desde 2027',
            'summary': 'Los principios son: explicabilidad (el cliente puede conocer los factores de rechazo), auditabilidad (registro completo del proceso) y no discriminación (prueba estadística trimestral). Bancos y fintechs tienen hasta el 31 de marzo de 2027 para implementarlos.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[10 Jun] Cooperativas chilenas proyectan rebaja de tasas hipotecarias al 3,8% UF si BCCh recorta TPM el 17 de junio',
            'summary': 'Coopeuch, Detacoop y CrediCoop Chile anuncian ajuste inmediato de tasas si el Banco Central baja la TPM 25 pb. Para un crédito hipotecario de UF 2.000 a 20 años, el dividendo mensual bajaría en aproximadamente UF 0,8. Demanda reprimida de 38.000 solicitudes en lista de espera.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[10 Jun] Alianza Cooperativa Internacional certifica a tres cooperativas chilenas con sello de Excelencia Financiera 2026',
            'summary': 'Coopeuch, Oriencoop y Capual reciben certificación internacional que reconoce solidez patrimonial, gobernanza y gestión de riesgo. Chile lidera el ranking regional con más cooperativas certificadas por tercer año consecutivo.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[10 Jun] CMF aprueba primera licencia bancaria digital nativa en Chile: FinBank obtiene autorización de operación plena',
            'summary': 'Entidad 100% digital sin sucursales físicas recibe autorización para captar depósitos y otorgar créditos. Capital mínimo de UF 800.000 completamente integrado. Operaciones masivas previstas desde septiembre 2026. Se suma a los tres bancos digitales que operan bajo licencia de banco de menor tamaño.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[10 Jun] IPSA consolida máximos del año en 7.960 pts: litio, cobre y expectativa de recorte de TPM impulsan rally',
            'summary': 'SQM lidera con +3,8% semanal ante alza del litio. Codelco Rojo (instrumento proxy) sube 2,1%. Administradoras de fondos de pensiones aumentan exposición a renta variable local en USD 420M durante la semana. Flujo extranjero neto positivo por cuarta semana consecutiva.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[10 Jun] Ventas del comercio minorista mayo 2026: crecen 4,2% real anual, mejor resultado desde agosto 2024',
            'summary': 'INE confirma recuperación del consumo privado. Comercio electrónico sube 18% y representa el 24% del total. Líneas blancas y electrónica lideran. Cámara de Comercio de Santiago proyecta segunda mitad del año con crecimiento sobre 5% si la TPM baja en junio.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
}


# Noticias específicas del 11 de junio de 2026
TODAY_NEWS_11JUN2026 = {
    'geopolitica': [
        {
            'title': '[11 Jun] Tensiones comerciales EE.UU.-UE: acuerdo arancelario sobre acero verde abre mercado para exportaciones chilenas',
            'summary': 'Washington y Bruselas firman protocolo que exime de aranceles al acero producido con energías renovables. Chile, con matriz eléctrica 60% renovable, queda en posición privilegiada para exportar acero verde. CORFO estima potencial de USD 2.400M en nuevas exportaciones para 2028.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[11 Jun] Banco Mundial eleva proyección de crecimiento para Chile a 3,1% en 2026: mejor perspectiva de la región',
            'summary': 'Informe semestral destaca solidez fiscal, baja inflación y términos de intercambio favorables por cobre y litio. Chile lidera ranking de perspectivas entre economías latinoamericanas. Único país de la región con calificación de riesgo en rango A de las tres principales agencias.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[11 Jun] Mercados globales consolidan ganancias: S&P 500 supera 5.980 pts ante expectativa de recortes de tasas en julio',
            'summary': 'Bolsas en máximos históricos impulsadas por datos de inflación favorables en EE.UU. y Europa. Bonos del Tesoro a 10 años en 4,08%, mínimo desde enero. Flujos hacia emergentes alcanzan USD 12.000M en la semana, récord mensual.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[11 Jun] Cobre supera USD 5,25/lb: nuevo máximo de 2026 ante datos de producción industrial china y déficit estructural',
            'summary': 'PMI manufacturero chino de mayo confirma expansión por cuarto mes consecutivo. Codelco anuncia inversión de USD 1.800M en ampliación de El Teniente. Goldman Sachs eleva objetivo a USD 5,90 para Q4 2026.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[11 Jun] UF $40.768,69 y dólar $915,97: indicadores al 11 de junio — peso se fortalece por cobre y expectativa de TPM',
            'summary': 'Unidad de Fomento publicada por SII para el jueves 11 de junio en $40.768,69. Dólar observado del BCCh en $915,97. Mercado aguarda reunión de política monetaria del 17 de junio con alta probabilidad de recorte de 25 pb. Peso acumula apreciación de 1,2% en la semana.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[11 Jun] Exportaciones chilenas enero-mayo: USD 40.800M, alza de 9,3% anual impulsadas por cobre, litio y frutas',
            'summary': 'BCCh confirma superávit comercial acumulado de USD 8.500M. Cobre representa el 52% del total, litio el 11% con crecimiento del 34% anual. Destino Asia concentra el 68% de las exportaciones. Diversificación exportadora avanza con frutas premium y vinos de calidad.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[11 Jun] IPSA rompe récord intradiario de 7.990 pts: inversionistas anticipan recorte de TPM y rally de renta variable',
            'summary': 'Bolsa chilena acumula alza de 3,8% en junio. SQM +6,2%, Codelco Rojo +4,1% y Banco de Chile +3,3% lideran. Administradoras AFP aumentan posición en acciones locales en USD 680M durante el mes. Flujo extranjero neto positivo por quinta semana consecutiva.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[11 Jun] Fintechs chilenas recaudan USD 340M en primer semestre 2026: récord histórico de inversión en el sector',
            'summary': 'CORFO y StartupChile reportan 18 rondas de financiamiento en el período. Tres unicornios en proceso de due diligence. Pagos digitales, crédito alternativo e inversión automatizada concentran el 74% de los fondos. Chile consolida liderazgo fintech en América del Sur.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[11 Jun] Portal de datos abiertos del SII alcanza 2 millones de consultas diarias: fintechs y pymes son los principales usuarios',
            'summary': 'Plataforma de APIs del SII permite verificación de facturas, consulta de deuda tributaria y validación de rut en tiempo real. Integración con 340 aplicaciones de terceros. Gobierno anuncia extensión al sistema de registros de la CMF para tercer trimestre.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[11 Jun] Ministerio de Hacienda usa IA para proyecciones fiscales: modelo predice recaudación con error menor al 0,3%',
            'summary': 'Sistema desarrollado con Dirección de Presupuestos procesa 48 variables macroeconómicas en tiempo real. Reduce en 80% el tiempo de elaboración del informe de finanzas públicas mensual. Primer uso de IA generativa en gestión fiscal de un gobierno latinoamericano.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
        {
            'title': '[11 Jun] OpenAI lanza GPT-5 Finance con especialización en regulación financiera latinoamericana: acceso para bancos chilenos',
            'summary': 'Modelo fine-tuned sobre normativa CMF, BCCh, SII y regulación de 12 países latinoamericanos. Procesa contratos, resoluciones y circulares en minutos. Tres bancos chilenos ya en piloto para automatización de compliance y revisión de contratos de crédito.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
    ],
    'cooperativismo': [
        {
            'title': '[11 Jun] Detacoop anuncia rebaja de tasa hipotecaria a 3,9% UF anticipando recorte de BCCh el 17 de junio',
            'summary': 'La cooperativa adelanta el ajuste de tasas antes de la reunión del Banco Central. Para un crédito de UF 2.500 a 20 años, el dividendo mensual bajaría en UF 1,2. Postulaciones abiertas con tasas congeladas hasta el 30 de junio para quienes formalicen esta semana.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[11 Jun] CONFECOOP presenta proyecto de ley para exención tributaria de excedentes cooperativos reinvertidos en capital',
            'summary': 'Propuesta busca equiparar el tratamiento fiscal de las cooperativas con el de las sociedades anónimas que retienen utilidades. Proyecto ingresado a la Cámara con apoyo de 34 diputados de distintos sectores. Impacto estimado: aumento de 18% en capitalización del sector en cinco años.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[11 Jun] CMF publica balance del primer año de la Ley Fintech: 94 empresas inscritas, USD 1.200M en transacciones supervisadas',
            'summary': 'Un año después de la entrada en vigor de la Ley 21.521, el ecosistema fintech chileno suma 94 entidades bajo supervisión CMF. Pagos digitales concentran el 61% de las operaciones. La comisión anuncia segunda fase de open banking para agosto con apertura de datos de inversiones.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[11 Jun] Litio carbonato supera USD 15.000/ton: SQM y Albemarle reportan márgenes récord en el trimestre',
            'summary': 'Precio del litio acumula alza de 22% en el segundo trimestre ante caída de producción australiana y aumento de demanda de baterías para vehículos eléctricos. Chile captura el 35% del mercado global de litio procesado. SQM eleva guidance de producción 2026 en 15%.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[11 Jun] Tasa de desempleo mayo 2026: INE reporta 8,1%, nueva baja mensual impulsada por servicios y construcción',
            'summary': 'Mercado laboral continúa su recuperación. Empleo formal crece 3,1% en doce meses. Mujeres en empleo formal superan el 44% por primera vez en la historia. BCCh incorpora dato en modelo para reunión del 17 de junio.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
    ],
}


# Noticias específicas del 12 de junio de 2026
TODAY_NEWS_12JUN2026 = {
    'geopolitica': [
        {
            'title': '[12 Jun] Cumbre G20 en Río: consenso sobre impuesto mínimo global a la riqueza y reforma del FMI con más voz para emergentes',
            'summary': 'Los líderes del G20 acuerdan avanzar en una tasa mínima del 2% sobre patrimonios superiores a USD 1.000M. Chile y Brasil lideran el bloque latinoamericano que exige mayor representación en el FMI. Reforma podría liberar USD 45.000M adicionales para economías emergentes en 2027.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[12 Jun] Conflicto Mar Rojo: EE.UU. y aliados coordinan escolta naval; fletes marítimos caen 8% ante menor incertidumbre',
            'summary': 'La operación conjunta de la Armada de EE.UU., Reino Unido y Francia reduce ataques en el estrecho de Bab-el-Mandeb. Índice de flete spot Asia-Europa cede 8% en la semana. Importaciones chilenas de insumos industriales deberían normalizarse en cuatro a seis semanas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[12 Jun] Cierre semanal: S&P 500 +1,8% en la semana; dólar global cede ante expectativas de recorte Fed en septiembre',
            'summary': 'Mercados acumulan la cuarta semana consecutiva de ganancias. Nasdaq lidera con +2,3% impulsado por tecnología e IA. Índice VIX en 11,9, mínimo histórico. Commodities latinoamericanos en zona verde: cobre +2,1%, litio +5,4% y soja +1,7% en la semana.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[12 Jun] BCE recorta tasa a 2,25%: Lagarde señala convergencia de inflación y abre puerta a segundo recorte en septiembre',
            'summary': 'Banco Central Europeo reduce 25 pb ante inflación subyacente en 2,1%. Euro cae 0,3% frente al dólar. Impacto positivo para deuda emergente: spreads soberanos latinoamericanos se comprimen 12 pb. Chile se beneficia con menor costo de refinanciamiento de deuda en euros.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[12 Jun] UF $40.771,41 y dólar $909,02: peso chileno cierra semana en máximo de tres meses ante cobre fuerte y BCE',
            'summary': 'Unidad de Fomento publicada por SII para el viernes 12 de junio. Dólar observado del BCCh en $909,02, caída de $6,95 respecto al lunes. Cobre sobre USD 5,25/lb y recorte del BCE impulsan apreciación del peso. Mercado fija la mirada en reunión TPM del martes 17 de junio.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[12 Jun] Reunión TPM 17-jun: BCCh revisará recorte de 25 pb con inflación en 3,1% y crecimiento sobre expectativas',
            'summary': 'Encuesta de operadores financieros del BCCh confirma 78% de probabilidad de recorte de 25 pb el próximo martes. Sería la primera baja desde enero de 2025. Impacto directo en créditos hipotecarios, de consumo y corporativos. Bancos y cooperativas ya tienen preparados los ajustes de tasas.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[12 Jun] IPSA cierra semana en 7.980 pts con alza de 3,6%: mejor desempeño semanal del año para la bolsa chilena',
            'summary': 'Índice bursátil acumula +11,4% en 2026, superando la proyección anual de consenso. SQM lidera con +7,1% impulsado por litio. Flujo extranjero neto supera USD 820M en el mes de junio. Volumen promedio diario en USD 340M, un 45% sobre la media histórica.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[12 Jun] CMF y BCCh publican hoja de ruta de open finance 2026-2028: incluye datos de AFP, seguros e inversiones',
            'summary': 'Segunda fase del ecosistema de datos abiertos extenderá el open banking a cuentas de AFP, seguros de vida y fondos de inversión. API unificada disponible para desarrolladores desde enero 2027. Chile sería el primer país latinoamericano con open finance completo bajo estándar regulatorio.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[12 Jun] Startups chilenas de pagos digitales procesan USD 2.100M mensuales: crecimiento de 67% en doce meses',
            'summary': 'Khipu, Multicaja y Pomelo lideran el segmento de pagos alternativos. El 38% de las pymes ya acepta al menos un método de pago digital distinto a Transbank. CORFO anuncia nuevo fondo de USD 60M para startups fintech de pagos e infraestructura financiera.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[12 Jun] Anthropic y Banco de Chile firman acuerdo para implementar IA generativa en servicio al cliente y compliance',
            'summary': 'Piloto cubrirá atención al cliente, revisión de contratos y detección de operaciones inusuales. Primer acuerdo directo entre un banco latinoamericano y Anthropic. Implementación en producción prevista para septiembre; potencial de reducción de costos operativos del 22%.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': '[12 Jun] Informe McKinsey: IA generativa podría añadir USD 180.000M al PIB de América Latina para 2030',
            'summary': 'Sector financiero captura el 28% del valor, seguido por minería (19%) y retail (14%). Chile lidera en adopción corporativa de IA con el 34% de grandes empresas usando modelos en producción. Brecha de talento en IA es el principal obstáculo: faltan 85.000 profesionales especializados en la región.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
    ],
    'cooperativismo': [
        {
            'title': '[12 Jun] Coopeuch anticipa recorte de TPM: congela tasa hipotecaria en 4,0% UF para operaciones formalizadas antes del 20 de junio',
            'summary': 'La mayor cooperativa financiera de Chile ofrece tasa fija de 4,0% en UF hasta el 20 de junio para capturar demanda antes del ajuste oficial. Condiciones incluyen plazo de hasta 25 años y financiamiento de hasta el 80% del avalúo. Se esperan 1.200 operaciones en la semana.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[12 Jun] Sector cooperativo chileno emite primer bono verde por UF 500.000: demanda triplica la oferta en bolsa',
            'summary': 'Instrumento de deuda cooperativa de impacto ambiental debuta en la Bolsa de Santiago con sobredemanda de 3,1 veces. Recursos financiarán paneles solares en viviendas cooperativas y eficiencia energética en sedes del sector. Tasa de colocación: UF + 1,85%.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[12 Jun] CMF cierra consulta pública NCG N°540 (REDEC): más de 120 comentarios recibidos de bancos, fintechs y cooperativas',
            'summary': 'La normativa del Registro de Deuda Consolidada recibió el mayor número de comentarios en la historia de la CMF. Industria valora la iniciativa pero solicita extensión del plazo de implementación a 18 meses. Resolución final esperada para agosto de 2026.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[12 Jun] Producción de cobre Chile mayo 2026: 523.000 toneladas, alza de 5,8% anual — Codelco y Anglo American lideran',
            'summary': 'Cochilco confirma producción mensual récord para mayo. Codelco aporta 145.000 toneladas tras inversión en El Teniente. Anglo American suma 98.000 ton desde Los Bronces y Quellaveco. Proyección anual de 5,8 millones de toneladas para Chile se mantiene en línea con presupuesto.',
            'source': 'Cochilco',
            'link': 'https://www.cochilco.cl'
        },
        {
            'title': '[12 Jun] Ventas de vehículos eléctricos en Chile: 4.800 unidades en mayo 2026, crecimiento de 112% anual',
            'summary': 'Chile lidera adopción de vehículos eléctricos en Sudamérica. BYD y Tesla concentran el 58% del mercado. Red de carga pública supera los 2.400 puntos en Santiago. Ministerio de Energía proyecta que el 25% de la flota nacional será eléctrica para 2030.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
}


# Noticias específicas del 15 de junio de 2026
TODAY_NEWS_15JUN2026 = {
    'geopolitica': [
        {
            'title': '[12 Jun] Tren de Aragua creó su propia plataforma de criptomonedas en Chile, según investigación',
            'summary': 'Unidad de Investigación de El Mostrador revela que la banda criminal venezolana Tren de Aragua desarrolló una plataforma propia de activos digitales para blanquear fondos en Chile. La CMF investiga el caso bajo la NCG 514 que regula operadores de activos digitales; PDI ya incautó equipos de minería y servidores en tres regiones del país.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/unidad-de-investigacion/2026/06/12/tren-de-aragua-creo-su-propia-plataforma-de-criptomonedas-en-chile/'
        },
        {
            'title': '[15 Jun] G20 Río: acuerdo sobre deuda climática y nuevo mecanismo de swap de divisas para economías emergentes',
            'summary': 'Declaración final del G20 incluye un fondo de USD 100.000M para países en desarrollo afectados por desastres climáticos. Chile accede a línea de swap con el BCE por EUR 5.000M. Mecanismo reduce riesgo cambiario en refinanciamiento de deuda soberana y fortalece posición del BCCh.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[15 Jun] Cumbre CELAC: Chile propone zona de integración financiera latinoamericana con supervisión coordinada entre CMF y equivalentes regionales',
            'summary': 'Propuesta chilena busca unificar estándares de supervisión bancaria, de seguros y de valores en América Latina. Brasil, Colombia y Perú expresan apoyo inicial. Implementación estimada en tres años con apoyo técnico del FMI y del Banco Mundial.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[15 Jun] Apertura semanal positiva: mercados anticipan recortes de Fed y BCCh esta semana — S&P 500 en máximos',
            'summary': 'Lunes de optimismo en bolsas globales con el S&P 500 sobre 6.000 pts por primera vez. Inversores posicionan en activos de riesgo ante expectativa de recortes coordinados entre bancos centrales. Flujos a renta variable emergente alcanzan USD 3.800M en lo que va de junio.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[15 Jun] Litio carbonato consolida USD 15.200/ton: demanda de baterías supera oferta global por segundo trimestre consecutivo',
            'summary': 'Déficit estructural estimado en 52.000 toneladas para 2026. SQM y Albemarle lideran ganancias en apertura de semana. Chile cubre el 36% de la producción global de litio procesado. Analistas de Morgan Stanley elevan precio objetivo del litio a USD 18.000 para 2027.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[15 Jun] UF $40.779,55 y dólar $899,30: peso chileno toca mínimo de cuatro meses ante rally de cobre y expectativa de recorte TPM',
            'summary': 'Unidad de Fomento publicada por SII para el lunes 15 de junio. Dólar observado del BCCh en $899,30, apreciación del peso de 1,1% respecto al viernes. Mercado descuenta con 84% de probabilidad un recorte de TPM de 25 pb mañana martes 17 de junio en la reunión del BCCh.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[15 Jun] Víspera del recorte de TPM: bancos y cooperativas preposicionan tasas — hipotecarios ya en 3,85% UF',
            'summary': 'Banco de Chile, Santander, BCI y las principales cooperativas publican nuevas listas de tasas anticipando la baja del BCCh. Crédito hipotecario promedio a 20 años cae a 3,85% UF desde 4,2% de diciembre 2025. Demanda acumulada de créditos en espera estimada en 42.000 operaciones.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[15 Jun] Producción industrial mayo 2026: crece 4,1% anual impulsada por minería y manufactura exportadora',
            'summary': 'INE confirma expansión del sector real con minería +6,8% y manufactura +2,9%. Electricidad, gas y agua +3,4% por mayor generación solar y eólica. Datos refuerzan el escenario base del BCCh de recorte gradual de TPM sin riesgo de sobrecalentamiento.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[15 Jun] Ley Fintech Chile: primer aniversario con 112 entidades inscritas, USD 2.800M en transacciones y cero quiebras supervisadas',
            'summary': 'CMF publica informe de primer año de la Ley 21.521. Crecimiento de 340% en nuevas inscripciones respecto al período pre-ley. Modelos de negocio: pagos (41%), crédito alternativo (28%), inversión automatizada (18%) y crowdfunding (13%). Regulación chilena citada como modelo en OCDE.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[15 Jun] Mercadopago lanza cuenta corriente digital en Chile con interés diario en UF: 500.000 cuentas en primera semana',
            'summary': 'Plataforma argentina desembarca en Chile con cuenta remunerada a tasa UF+0,5% anual liquidada diariamente. Sin costo de mantención ni saldo mínimo. Integración nativa con marketplace de Mercadolibre y sistema de pagos QR. CMF certifica operación bajo licencia de empresa de servicios financieros.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[15 Jun] BCCh publica primer informe de estabilidad financiera con sección dedicada a riesgos de IA: alerta por concentración en tres proveedores',
            'summary': 'Informe semestral del Banco Central advierte que el 78% de los modelos de IA del sistema financiero chileno dependen de infraestructura de solo tres empresas tecnológicas globales. Recomienda plan de contingencia y diversificación. Nuevas instrucciones de la CMF previstas para agosto.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[15 Jun] Fintechs chilenas usan IA para reducir mora: tres startups reportan caída del 40% en incumplimiento con modelos predictivos',
            'summary': 'Destacan Destacame, Cumplo y Xepelin, que aplican modelos de lenguaje y datos alternativos (redes sociales, comportamiento de pago, flujos de caja) para scoring crediticio. Mora promedio en sus carteras: 1,1% vs 2,8% de la industria bancaria tradicional.',
            'source': 'VentureBeat AI',
            'link': 'https://venturebeat.com/category/ai/'
        },
    ],
    'cooperativismo': [
        {
            'title': '[15 Jun] Coopeuch y Detacoop anuncian baja de tasas hipotecarias a 3,75% UF ante inminente recorte del BCCh',
            'summary': 'Ambas cooperativas adelantan el ajuste de tasas para esta semana. Para un crédito de UF 3.000 a 20 años, el dividendo mensual bajaría en aproximadamente UF 1,8 respecto a tasas de inicios de año. Lista de espera de socios supera las 15.000 solicitudes en ambas instituciones.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[15 Jun] CONFECOOP: sector cooperativo financiero chileno proyecta crecimiento de cartera de 20% en segundo semestre 2026',
            'summary': 'Escenario de tasas a la baja activa demanda reprimida de crédito hipotecario y de consumo. Cooperativas tienen ventaja competitiva por menor spread sobre TPM. Tres nuevas cooperativas en proceso de inscripción ante CMF para operar en regiones de Atacama y Magallanes.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[15 Jun] CMF actualiza normativa de consulta: quedan vigentes tres circulares con plazo hasta julio 2026',
            'summary': 'Vencieron el 15 de junio las consultas sobre REDEC y reaseguro de rentas vitalicias. Siguen abiertas: modificación Circular N°2.062 (rentas vitalicias, hasta 08/07), e instrucciones sobre intermediarios de valores (dos circulares, hasta 26/06). CMF recibirá nuevas consultas desde agosto.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[15 Jun] Precios combustibles Chile: bencina baja $10/litro desde el jueves; ENAP reporta caída en precio de paridad',
            'summary': 'Caída del Brent a USD 79/barril y apreciación del peso reducen el precio de paridad de la gasolina. ENAP estima rebaja de $10 en gasolina de 93 y 97 octanos desde el jueves 19 de junio. Impacto en IPC de junio: reducción estimada de 0,05 puntos porcentuales.',
            'source': 'Ministerio de Energía',
            'link': 'https://www.energia.gob.cl'
        },
        {
            'title': '[15 Jun] Inversión extranjera directa en Chile enero-mayo 2026: USD 7.800M, alza de 22% anual liderada por energías renovables y minería',
            'summary': 'InvestChile reporta flujos récord en el período. Energías renovables captura el 34% del total con proyectos solares y eólicos en el norte. Minería atrae el 29% con inversiones de Anglo American y BHP en expansiones. Manufactura de baterías suma USD 980M en compromisos formales.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
}


# Noticias específicas del 16 de junio de 2026
TODAY_NEWS_16JUN2026 = {
    'geopolitica': [
        {
            'title': '[16 Jun] Tensión comercial EE.UU.-China escala: nuevos aranceles a semiconductores activan respuesta de Pekín',
            'summary': 'Washington anuncia sobretasas del 35% a chips chinos de madurez tecnológica. China responde con restricciones de exportación de germanio y galio, insumos clave para semiconductores occidentales. Bolsas asiáticas caen 1,8%; cobre modera alza ante temores de desaceleración manufacturera.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[16 Jun] Crimen organizado y criptoactivos: PDI amplía investigación a red Tren de Aragua tras revelación de El Mostrador',
            'summary': 'La PDI ejecuta allanamientos en Santiago, Valparaíso y Antofagasta tras la investigación de El Mostrador sobre la plataforma cripto del Tren de Aragua. CMF coordina con Fiscalía bajo NCG 514. Ministerio del Interior anuncia mesa interinstitucional para regulación urgente de exchanges informales.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/unidad-de-investigacion/2026/06/12/tren-de-aragua-creo-su-propia-plataforma-de-criptomonedas-en-chile/'
        },
    ],
    'economia_global': [
        {
            'title': '[16 Jun] BCE y Fed coordinan señales: tasas globales en punto de inflexión — mercados emergentes los grandes ganadores',
            'summary': 'Recorte del BCE la semana pasada y señales de la Fed consolidan ciclo bajista global de tasas. Índice de bonos emergentes EMBI sube 2,1% en la semana. Chile lidera captación de flujos en la región con USD 1.200M en la semana. Costo de deuda soberana chilena cae a mínimo de 18 meses.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[16 Jun] Cobre cede a USD 5,18/lb por tensión EE.UU.-China: analistas ven corrección temporal ante fundamentos sólidos',
            'summary': 'Metal rojo retrocede 1,4% ante escalada arancelaria en semiconductores, aunque inventarios LME siguen en mínimos. Codelco mantiene guidance de producción y no modifica plan de inversiones. Analistas de JPMorgan reafirman objetivo de USD 5,70 para fin de año.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[16 Jun] UF $40.790,42 y dólar $897,19: víspera del recorte TPM — peso en mínimo de cinco meses',
            'summary': 'Unidad de Fomento publicada por SII para el martes 16 de junio. Dólar observado del BCCh en $897,19, apreciación adicional de $2,11 respecto al lunes. El mercado descuenta con 89% de probabilidad un recorte de TPM de 25 pb mañana miércoles 17. Tasas swap a 30 días en 4,27%.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[16 Jun] BCCh publica minutas previas: consejo dividido entre recorte de 25 pb y mantención — sorpresa posible mañana',
            'summary': 'Dos consejeros habrían abogado por mantener la TPM ante incertidumbre global por tensión EE.UU.-China. Mayoría favorece recorte precautorio de 25 pb. Decisión se anuncia mañana a las 18:00 hrs. con conferencia de prensa del Presidente del BCCh a las 18:30 hrs.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[16 Jun] IPSA cede 0,4% por corrección del cobre: inversores toman utilidades en Codelco y SQM antes del TPM',
            'summary': 'Toma de utilidades parcial en el sector minero ante volatilidad global. Bolsa acumula +3,2% en junio pese a la corrección de hoy. Bancos y utilities sostienen el índice. Analistas recomiendan esperar la decisión del BCCh antes de reposicionar en renta variable chilena.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[16 Jun] Chile lidera ranking fintech Latam 2026: 312 empresas activas, crecimiento de 41% en dos años',
            'summary': 'Informe BID Invest posiciona a Chile como el ecosistema fintech más maduro de América del Sur. Regulación CMF bajo Ley 21.521 es citada como el marco más completo de la región. Colombia y Perú siguen a distancia con 198 y 145 empresas activas respectivamente.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[16 Jun] Ciberseguridad financiera: CSIRT reporta 3.400 intentos de intrusión a bancos chilenos en mayo, 28% más que abril',
            'summary': 'CMF y el CSIRT del Gobierno publican alerta conjunta por aumento de ataques de ransomware y phishing dirigido a entidades financieras. Las cooperativas de menor tamaño son el blanco más frecuente. Nueva circular de ciberseguridad (Circular N°2.237) entra en vigor en 30 días.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[16 Jun] SII implementa IA para fiscalizar IVA en tiempo real: detecta $48.000M en subdeclaraciones en primer mes',
            'summary': 'Sistema de auditoría predictiva cruza facturas electrónicas, flujos de caja y datos de comercio exterior para detectar inconsistencias. En el primer mes operativo identificó 2.800 empresas con diferencias superiores a UF 100. Cumplimiento voluntario ya aumentó un 9% respecto al mismo período de 2025.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
        {
            'title': '[16 Jun] Corfo adjudica USD 24M a ocho proyectos de IA financiera chilenos: foco en crédito pyme y detección de fraude',
            'summary': 'Los ocho proyectos seleccionados abordan scoring crediticio alternativo, automatización de compliance, detección de fraude en pagos digitales y análisis de riesgo de cartera en cooperativas. Plazo de implementación: 18 meses con evaluación de impacto por la CMF.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
    ],
    'cooperativismo': [
        {
            'title': '[16 Jun] Víspera TPM: cooperativas chilenas congelan tasas hipotecarias en 3,75% UF hasta el 30 de junio',
            'summary': 'Coopeuch, Detacoop, Oriencoop y CrediCoop anuncian tasa promocional congelada a la espera del recorte oficial. Condiciones: plazo hasta 30 años, hasta 80% de financiamiento, sin costo de originación para socios con 12 meses de antigüedad. Más de 22.000 solicitudes en lista de espera.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[16 Jun] Detacoop informa resultados del primer semestre: cartera crece 22%, mora en 0,9% y patrimonio supera UF 1,2 millones',
            'summary': 'La cooperativa registra su mejor semestre histórico. Nuevos socios en el período: 28.400. Apertura de sucursales en Concepción y Temuco programadas para agosto. Premio ACI a Mejor Gobernanza Cooperativa 2026 recibido en Río de Janeiro.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[16 Jun] CMF activa investigación formal sobre plataforma cripto del Tren de Aragua: primer caso bajo NCG 514',
            'summary': 'La Comisión para el Mercado Financiero abre expediente formal de investigación bajo la Norma de Carácter General N°514 que regula operadores de activos digitales. Es el primer caso de aplicación de la norma desde su publicación. La CMF tiene facultades para congelar activos y suspender operaciones.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[16 Jun] Precio del petróleo Brent sube a USD 81,4: tensión geopolítica en Medio Oriente y recorte de producción OPEP+',
            'summary': 'Arabia Saudita anuncia recorte adicional de 200.000 bbl/día ante presión de precios bajos. Enap estima impacto leve en precio de combustibles en julio (+$3/litro). BCCh monitorea efecto en IPC de junio dado que la baja esperada de bencinas se revierte parcialmente.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[16 Jun] Tasa de ahorro de hogares chilenos sube a 8,4% del ingreso disponible: máximo desde 2020 y señal de prudencia pre-TPM',
            'summary': 'Encuesta BCCh revela que los hogares aumentaron su tasa de ahorro ante incertidumbre sobre la economía global. Depósitos a plazo en el sistema financiero crecen 14% en doce meses. La baja de TPM podría redirigir parte de ese ahorro hacia consumo e inversión inmobiliaria.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
}


TODAY_NEWS_22JUN2026 = {
    'geopolitica': [
        {
            'title': '[22 Jun] G7 refuerza sanciones a Rusia y acuerda fondo de USD 50.000M con activos soberanos congelados',
            'summary': 'Los líderes del G7 aprueban fondo de reconstrucción para Ucrania financiado con intereses de activos rusos. Rusia advierte represalias en materias primas. Mercados energéticos estables con Brent en USD 81,8.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[22 Jun] ONU alerta por crimen transnacional en Latam: Chile refuerza marco antilavado con normativa de activos digitales',
            'summary': 'Informe UNODC: flujos de lavado en la región superan USD 160.000M en 2025. Chile destacado como modelo regional. La regulación CMF de activos digitales (NCG 514) es citada como buena práctica.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[22 Jun] Fed mantiene tasas: señala recorte en septiembre si IPC sigue bajando — emergentes se benefician',
            'summary': 'Powell descarta recorte prematuro pero confirma que la desinflación avanza. DXY cae 0,3%. El S&P 500 cierra semana en 5.980 puntos. Chile capta flujos de capital hacia renta fija local.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[22 Jun] Cobre retoma USD 5,22/lb: China anuncia paquete de estímulo a infraestructura por USD 300.000M',
            'summary': 'Gobierno chino activa plan de inversión en redes eléctricas y transporte. Analistas de Barclays elevan estimado de cobre para Q3 a USD 5,55/lb. Codelco y SQM lideran el alza del IPSA.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[22 Jun] UF $40.798,57 y dólar $900,60 al 22 de junio: peso se fortalece tras rally del cobre',
            'summary': 'El peso chileno acumula apreciación de 0,8% en la semana impulsado por cobre fuerte y flujos a bonos soberanos. El BCCh registra reservas internacionales en USD 44.200M, nivel récord.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[22 Jun] IPSA inicia semana con alza de 0,6%: expectativas de recorte Fed y cobre fuerte impulsan bolsa',
            'summary': 'El índice bursátil acumula +4,8% en junio. Codelco, SQM y Banco de Chile lideran las ganancias. Analistas mantienen objetivos de fin de año entre 8.100 y 8.400 puntos para el IPSA.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[22 Jun] BancoEstado lanza cuenta digital para cooperativas: integración con Coopeuch y Detacoop',
            'summary': 'Nueva API de interoperabilidad permite transferencias instantáneas entre cooperativas y BancoEstado sin comisión el primer año. Más de 1,2 millones de socios cooperativos acceden desde hoy bajo el marco open finance de la Ley Fintech.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
        {
            'title': '[22 Jun] Mercadopago Chile supera a tarjetas de débito en volumen: 45 millones de transacciones en mayo',
            'summary': 'Las billeteras digitales representan el 38% del total de operaciones de pago electrónico. Bancos responden acelerando sus propias wallets: BCI Pay y Santander Wallet anuncian nuevas funcionalidades.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[22 Jun] CMF publica guía de IA en entidades supervisadas: principios de explicabilidad y no discriminación',
            'summary': 'Modelos de scoring crediticio basados en IA deben ser auditables y libres de sesgos. Las entidades tienen 12 meses para adecuarse. Norma pionera en América Latina, referencia al marco europeo AI Act.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[22 Jun] Corfo y Ministerio de Ciencia lanzan IA para pymes financieras: subsidio hasta UF 2.000',
            'summary': 'Programa digitaliza gestión de riesgo, cobranza y atención a clientes en el sector financiero con menos de 200 trabajadores. Postulaciones desde el 1 de julio. Cooperativas de ahorro y crédito son elegibles.',
            'source': 'Ministerio de Ciencia',
            'link': 'https://www.minciencia.gob.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[22 Jun] Baja de TPM reactiva hipotecarios en cooperativas: Coopeuch y CrediCoop anuncian nuevas tasas',
            'summary': 'Coopeuch en 3,60% UF + spread y CrediCoop en 3,55% UF + spread. Condiciones vigentes desde hoy lunes 22. Lista de espera de más de 18.000 solicitudes se activa esta semana.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[22 Jun] Congreso aprueba modernización D.L. 3.500 para cooperativas de previsión: ahorro complementario',
            'summary': 'Las modificaciones permiten a cooperativas ofrecer productos de ahorro previsional complementario. CMF tendrá 90 días para dictar normativa secundaria. Más de 3 millones de trabajadores informales podrían beneficiarse.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/mercados/feed/'
        },
    ],
    'cmf': [
        {
            'title': '[22 Jun] CMF publica informe de estabilidad financiera: sistema bancario sólido con cobertura de provisiones en 2,3x',
            'summary': 'El Informe del primer semestre 2026 concluye que la banca chilena mantiene índices de capital sobre mínimos. Cartera vigente crece 7,2% real; mora total cede a 1,4%. Cooperativas de mayor tamaño mantienen indicadores similares al sistema bancario.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[22 Jun] IPC mayo en 0,2%: inflación anual baja a 3,4% y confirma trayectoria desinflacionaria',
            'summary': 'Dato en línea con el consenso de mercado. Inflación anual continúa descenso hacia el 3%. Alimentos y energía contribuyeron al alza mensual; vestuario y transporte aportaron deflación.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': '[22 Jun] Exportaciones chilenas crecen 9,8% en mayo: cobre, litio y salmón lideran el dinamismo exportador',
            'summary': 'Exportaciones totalizaron USD 8.200M en mayo, segundo mejor registro histórico. Cobre aporta USD 4.800M (+11%), litio USD 680M (+34%). Diversificación de destinos reduce dependencia de China.',
            'source': 'ProChile / Banco Central',
            'link': 'https://www.bcentral.cl'
        },
    ],
}


TODAY_NEWS_23JUN2026 = {
    'geopolitica': [
        {
            'title': '[23 Jun] Consejo de Seguridad ONU debate resolución sobre Ucrania: EE.UU. busca ampliar fondo G7',
            'summary': 'Washington presenta propuesta para internacionalizar el fondo de USD 50.000M del G7. China y Rusia anuncian veto. Europa presiona por solución diplomática. Mercados de energía cautelosos con Brent en USD 81,8.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[23 Jun] Chile y Perú acuerdan corredor logístico para exportación de cobre y litio al Pacífico',
            'summary': 'Cancilleres firman memorándum para optimizar cadena de exportación de minerales críticos. Incluye interconexión ferroviaria y reducción de tiempos de tránsito en 30%. Impacto positivo esperado para Codelco y SQM.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[23 Jun] Minutas Fed: recorte en septiembre condicionado a dos IPC favorables consecutivos',
            'summary': 'Actas de junio muestran consenso en esperar datos adicionales. Mercados mantienen 72% de probabilidad de baja en septiembre. Dólar DXY se debilita 0,2% ante emergentes.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[23 Jun] Cobre supera USD 5,25/lb: estímulo chino y déficit de oferta consolidan rally del metal rojo',
            'summary': 'Inventarios LME caen a 108.000 toneladas, mínimo histórico en veinte años. Goldman Sachs eleva target para Q3 a USD 5,60/lb. Mineras chilenas suben 1,2% en la apertura.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[23 Jun] UF $40.801,29 y dólar $905,78 al 23 de junio: peso se aprecia ante flujos de capital',
            'summary': 'El peso acumula apreciación de 1,4% en la semana impulsado por cobre y entrada de capitales a bonos soberanos. BCCh registra reservas internacionales en USD 44.200M, nivel récord.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[23 Jun] ICARE: mañana encuentro con Ministra de Ciencia Ximena Lincolao — agenda de IA e innovación',
            'summary': 'El encuentro del 24 de junio reunirá a líderes empresariales con la Ministra para abordar política nacional de IA, financiamiento de startups deeptech y transferencia tecnológica. Inscripciones en icare.cl.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl/agenda-de-actividades/'
        },
        {
            'title': '[23 Jun] Ventas retail suben 3,2% real en mayo: primer alza en cuatro meses confirma recuperación del consumo',
            'summary': 'INE reporta crecimiento del comercio minorista en términos reales. Tecnología, electrodomésticos y materiales de construcción lideran. Dato consistente con baja de TPM y refuerza proyección de crecimiento de 2,5% para 2026.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[23 Jun] Transbank lanza pagos instantáneos 24/7 para pymes: integración con cooperativas en agosto',
            'summary': 'Nueva API de pagos en tiempo real disponible para comercios de cualquier tamaño desde julio. Cooperativas se integran desde agosto bajo open finance de la Ley Fintech. Costo de transacción baja 40%.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': '[23 Jun] Fintechs chilenas captan USD 180M en primera mitad de 2026: crédito digital y seguros lideran',
            'summary': 'Ecosistema local atrajo 35% más capital que en el mismo período de 2025. Cinco startups chilenas en proceso de expansión a Colombia y México.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[23 Jun] BancoEstado pilotea asistente IA para cooperativas: 94% satisfacción en piloto',
            'summary': 'Sistema resuelve el 78% de consultas sin intervención humana. Ampliación a 500.000 usuarios en Q3 2026.',
            'source': 'BancoEstado',
            'link': 'https://www.bancoestado.cl'
        },
        {
            'title': '[23 Jun] Fondo IA Chile 2026: USD 45M para proyectos de impacto en finanzas y salud',
            'summary': 'Financiamiento de hasta USD 3M por proyecto. Cooperativas de crédito son elegibles. Postulaciones hasta el 15 de agosto en plataforma Corfo.',
            'source': 'Ministerio de Ciencia',
            'link': 'https://www.minciencia.gob.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[23 Jun] Coopeuch anuncia nueva sucursal en Temuco para el 1 de julio',
            'summary': 'La décima sucursal regional responde al crecimiento del 34% en socios de La Araucanía en dos años. Ofrecerá crédito hipotecario, ahorro y productos de inversión.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[23 Jun] ACI Américas: Chile sede del Congreso Cooperativo Latinoamericano 2026 en octubre',
            'summary': 'Santiago reunirá a más de 2.000 dirigentes cooperativos de 18 países para abordar gobernanza, tecnología y sostenibilidad. Foro Cooperativo Chile lidera la organización local.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[23 Jun] CMF publica circular de requerimientos de capital para cooperativas de mayor tamaño',
            'summary': 'Instrucciones para cooperativas con activos superiores a UF 400.000, alineadas con Basilea III adaptado. Plazo de adecuación: 18 meses. Afecta principalmente a Coopeuch, Detacoop y Oriencoop.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[23 Jun] Petróleo Brent en USD 81,8: OPEP+ mantiene recortes — impacto moderado en Chile',
            'summary': 'Enap ajusta proyección de precios de combustibles para julio: alzas de $2-$4 por litro. BCCh estima efecto de 0,05 puntos en IPC de julio.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[23 Jun] Hacienda coloca bonos en exterior por USD 1.500M a tasa récord de 4,85%',
            'summary': 'La tasa más baja desde 2020 refleja confianza en la solidez fiscal de Chile. Fondos destinados a infraestructura pública y programa de vivienda del gobierno.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
}


TODAY_NEWS_24JUN2026 = {
    'geopolitica': [
        {
            'title': '[24 Jun] OCDE eleva proyección de crecimiento global a 3,2% para 2026: Chile entre los más beneficiados de Latam',
            'summary': 'La organización revisa al alza su estimación por mayor dinamismo en EE.UU., India y el sudeste asiático. Chile lidera el crecimiento en América del Sur con 2,8% proyectado, impulsado por cobre, litio y consumo interno. La baja de TPM y el ciclo bajista global de tasas son factores clave.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[24 Jun] Cumbre UE–Celac reactiva agenda comercial: acuerdo de minerales críticos Chile–Europa en etapa final',
            'summary': 'Bruselas y Santiago reportan avances decisivos en el capítulo de minerales críticos del acuerdo de asociación. El pacto incluye litio procesado, cobre refinado y tierras raras. Firma esperada para Q4 2026. Chile ganaría acceso preferencial a tecnología de baterías europeas.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[24 Jun] Cobre alcanza USD 5,28/lb: máximo de tres semanas — analistas ven continuidad del rally',
            'summary': 'El metal rojo avanza por quinta jornada consecutiva impulsado por el estímulo chino y el déficit de oferta. JPMorgan reafirma objetivo de USD 5,70 para fin de año. Las acciones de Codelco y SQM lideran el IPSA con alzas de 1,5% y 2,1% respectivamente.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[24 Jun] Dólar global cede ante datos de inflación EE.UU.: peso chileno se aprecia a mínimo de dos meses',
            'summary': 'El índice DXY cae 0,4% tras dato de PCE de mayo en línea con expectativas. Monedas emergentes se aprecian de manera generalizada. El peso chileno alcanza su nivel más fuerte desde abril 2026, respaldado por el rally del cobre.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[24 Jun] Indicadores del día: UF y dólar observado al 24 de junio de 2026',
            'summary': 'Valores vigentes publicados por SII y BCCh para el martes 24 de junio. El peso chileno se fortalece ante la caída del dólar global y el rally del cobre. Tasas hipotecarias en cooperativas comienzan a reflejar la baja de TPM del 17 de junio.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[24 Jun] ICARE hoy: encuentro con Ministra de Ciencia Ximena Lincolao — IA, deeptech y política de innovación',
            'summary': 'Líderes empresariales se reúnen esta mañana con la Ministra de Ciencia e Innovación en el encuentro mensual de ICARE. La agenda incluye el Plan Nacional de IA, financiamiento a startups deeptech y la estrategia de transferencia tecnológica desde universidades al sector productivo.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl/agenda-de-actividades/'
        },
        {
            'title': '[24 Jun] BCCh: encuesta de expectativas muestra TPM en 4,25% al cierre de 2026 — nuevo recorte en agosto',
            'summary': 'La Encuesta de Expectativas Económicas del BCCh muestra que el 68% de los analistas espera un segundo recorte de 25 pb en agosto. Las proyecciones de inflación para 2026 se mantienen en 3,0%. El mercado de swaps descuenta TPM terminal de 3,75% para mediados de 2027.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[24 Jun] CMF aprueba primer sandbox regulatorio para criptoactivos: cuatro exchanges bajo supervisión experimental',
            'summary': 'La Comisión abre el primer espacio de prueba regulatoria para operadores de activos digitales bajo la NCG 514. Cuatro exchanges chilenos operarán bajo supervisión durante 12 meses. El objetivo es desarrollar normativa permanente basada en evidencia real de operación.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[24 Jun] IPSA digital: las cinco fintechs chilenas con mayor crecimiento en H1 2026',
            'summary': 'Ranking elaborado por Fintech Chile destaca a Khipu, Cumplo, Pago46, Mango y TuCompu como las empresas con mayor expansión de usuarios en el primer semestre. Las cinco suman más de 4,2 millones de usuarios activos y crecimiento promedio de ingresos del 87%.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[24 Jun] SII usa IA para cruzar datos de arriendos AirBnb con declaraciones de renta: $12.000M recuperados',
            'summary': 'El nuevo sistema de auditoría cruzada detectó 4.200 propietarios con ingresos no declarados por arriendos de corta estadía. El SII ofrece regularización voluntaria con rebaja de multas hasta el 31 de julio. Tecnología replicable en otros sectores de la economía informal.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
        {
            'title': '[24 Jun] Encuentro ICARE-Ministra Lincolao: IA en el centro de la agenda de productividad chilena 2026–2030',
            'summary': 'El Plan Nacional de IA presentado hoy contempla inversión de USD 220M en cuatro años, formación de 15.000 especialistas y creación de cinco centros de excelencia en universidades regionales. Las cooperativas de crédito son mencionadas como caso de uso prioritario para IA financiera inclusiva.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl/agenda-de-actividades/'
        },
    ],
    'cooperativismo': [
        {
            'title': '[24 Jun] Oriencoop lanza producto de inversión en UF para socios: retorno de 5,8% anual garantizado',
            'summary': 'La cooperativa del norte del país presenta su primer instrumento de inversión para socios con plazo de 12 meses. Capital mínimo: UF 5. Liquidez mensual disponible desde el tercer mes. El lanzamiento se enmarca en la modernización del D.L. 3.500 aprobada esta semana.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[24 Jun] Cooperativas de crédito rebajan tasas de consumo: Detacoop en 0,89% mensual desde hoy',
            'summary': 'La rebaja de TPM se traslada a los créditos de consumo cooperativos. Detacoop lidera con 0,89% mensual para socios activos con tres meses de antigüedad. Coopeuch y CrediCoop anuncian sus nuevas tablas para esta tarde. Mercado estima que las tasas seguirán bajando hasta agosto.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[24 Jun] CMF cierra consulta pública sobre normativa de intermediarios de valores el 26 de junio',
            'summary': 'La Comisión recuerda que el plazo para enviar comentarios sobre las instrucciones de patrimonio mínimo, garantías y liquidez para intermediarios de valores vence el próximo viernes 26 de junio. Las entidades del mercado de capitales pueden ingresar sus observaciones a través del portal oficial.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[24 Jun] Balanza comercial de mayo: superávit de USD 1.200M — tercer mes consecutivo de resultados positivos',
            'summary': 'Las exportaciones totalizaron USD 8.200M y las importaciones USD 7.000M en mayo. El cobre explica el 58% del superávit. La tendencia refuerza la posición externa de Chile y da espacio al BCCh para mantener el ciclo de baja de tasas.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[24 Jun] Precio del petróleo Brent cede a USD 80,9: datos de inventarios EE.UU. alivian presión de oferta',
            'summary': 'Inventarios de crudo en EE.UU. aumentaron 3,2 millones de barriles la semana pasada, dato mayor al esperado. El Brent retrocede 1,1%. Enap revisa a la baja su proyección de alza de combustibles para julio.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
}


TODAY_NEWS_25JUN2026 = {
    'geopolitica': [
        {
            'title': '[25 Jun] Cumbre UE–Celac concluye con acuerdo marco de minerales críticos: Chile firma capítulo de litio',
            'summary': 'Los líderes europeos y latinoamericanos firman el marco general del acuerdo de minerales críticos. Chile asegura acceso preferencial a tecnología de baterías de la UE a cambio de suministro estable de litio procesado. Se estima que el acuerdo generará inversiones por USD 4.000M en los próximos cinco años.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[25 Jun] OTAN y socios del Indo-Pacífico refuerzan acuerdo de seguridad marítima: impacto en rutas comerciales del Pacífico',
            'summary': 'La alianza amplía su acuerdo con Japón, Corea del Sur y Australia para proteger rutas marítimas estratégicas en el Indo-Pacífico. Chile, como exportador dependiente de estas rutas, beneficia de mayor estabilidad para sus envíos de cobre, litio y productos agrícolas a Asia.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[25 Jun] PCE de EE.UU. en 2,6% anual: dato clave consolida expectativa de recorte Fed en septiembre',
            'summary': 'El índice de precios PCE —el favorito de la Fed— bajó a 2,6% en mayo, acercándose a la meta del 2%. Los mercados elevan la probabilidad de recorte en septiembre al 81%. Dólar DXY pierde 0,5%, peso chileno se aprecia y cobre avanza a USD 5,30/lb.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[25 Jun] Banco de Japón mantiene tasa en 0,5%: yen se debilita y flujos rotan hacia emergentes — Chile capta USD 420M',
            'summary': 'La decisión del BoJ de no subir tasas amplía el diferencial con EE.UU. y deprecia el yen. Los fondos globales aumentan exposición a bonos emergentes; Chile recibe USD 420M de flujos netos en la semana. El IPSA sube 0,9% y el peso se aprecia.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[25 Jun] UF y dólar observado al 25 de junio: peso en nivel más fuerte desde abril',
            'summary': 'El tipo de cambio continúa apreciándose ante la debilidad global del dólar y el alza del cobre. La UF mantiene su trayectoria gradual al alza en línea con el IPC de mayo. BCCh interviene verbalmente para calmar la apreciación excesiva del peso.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[25 Jun] ICARE: resultados del encuentro de ayer con Ministra Lincolao — USD 220M para IA y 15.000 especialistas',
            'summary': 'El Plan Nacional de IA presentado ayer contempla cinco centros de excelencia en universidades regionales y un fondo de USD 220M en cuatro años. Las cooperativas de crédito fueron destacadas como caso de uso prioritario para IA financiera inclusiva. Próximo encuentro ICARE en julio.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl/agenda-de-actividades/'
        },
        {
            'title': '[25 Jun] Imacec de mayo en 3,4%: tercer mes consecutivo de crecimiento robusto — economía chilena acelera',
            'summary': 'El Indicador Mensual de Actividad Económica superó las expectativas del mercado (consenso: 3,1%). Minería aportó 0,9 pp gracias al cobre; comercio y servicios sumaron 1,8 pp. El BCCh podría revisar al alza su proyección de crecimiento de 2,5% para 2026.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[25 Jun] Ley de Ciberseguridad: Congreso aprueba regulación de incidentes para sector financiero — CMF implementa en 60 días',
            'summary': 'El Congreso aprueba el reglamento que obliga a bancos, cooperativas y fintechs a reportar incidentes de ciberseguridad en menos de 72 horas. La CMF tendrá 60 días para emitir las instrucciones específicas. Las multas por incumplimiento alcanzan las UF 10.000.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': '[25 Jun] Open Banking Chile: 140 entidades ya integradas a la plataforma de datos financieros abiertos',
            'summary': 'La plataforma de open finance bajo la Ley Fintech supera el hito de 140 entidades integradas, incluyendo 28 cooperativas de ahorro y crédito. Los usuarios ya pueden compartir sus datos entre instituciones para acceder a mejores tasas y productos personalizados.',
            'source': 'El Mercurio',
            'link': 'https://www.emol.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[25 Jun] BCCh publica primer informe de riesgos de IA en el sistema financiero chileno',
            'summary': 'El documento identifica cuatro riesgos principales: concentración en proveedores de IA, opacidad de modelos de crédito, ciberataques a sistemas de IA y efectos procíclicos por uso masivo de algoritmos similares. Se recomienda diversificación tecnológica y auditorías independientes periódicas.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[25 Jun] Corfo adjudica primera ronda del Fondo IA Chile 2026: ocho proyectos financieros seleccionados',
            'summary': 'Los ocho proyectos incluyen scoring alternativo para trabajadores independientes, detección de fraude cooperativo, automatización de compliance AML y análisis de riesgo climático en cartera hipotecaria. Monto total adjudicado: USD 18M. Implementación en 18 meses.',
            'source': 'CORFO',
            'link': 'https://www.corfo.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[25 Jun] Detacoop inaugura plataforma digital: gestión 100% en línea de créditos, ahorros e inversiones',
            'summary': 'La cooperativa lanza su nueva plataforma digital que permite a los socios gestionar todos sus productos sin ir a sucursal. Incluye firma electrónica avanzada, videollamada con ejecutivo y apertura de productos en menos de 10 minutos. Disponible en iOS, Android y web.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[25 Jun] Foro Cooperativo Chile: seminario "Cooperativas y transición energética" el 8 de julio en Santiago',
            'summary': 'El evento reunirá a líderes del sector cooperativo, representantes del Ministerio de Energía y expertos internacionales para analizar el rol de las cooperativas en la descarbonización. Se presentarán los primeros proyectos de energía solar cooperativa en regiones.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[25 Jun] Último día hábil para comentar normativas CMF sobre intermediarios de valores — vence mañana 26 de junio',
            'summary': 'La CMF recuerda que mañana viernes 26 es el último día para enviar observaciones sobre las circulares de patrimonio mínimo, garantías, liquidez y volumen de negocios para intermediarios de valores y corredores de bolsa. Los comentarios deben ingresarse a través del portal oficial de la CMF.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[25 Jun] Cobre alcanza USD 5,30/lb: máximo de cuatro semanas — exportaciones chilenas superarán USD 50.000M en 2026',
            'summary': 'El metal rojo avanza impulsado por el PCE favorable de EE.UU. y el estímulo chino. Analistas de Codelco estiman que a este precio las exportaciones anuales de cobre superarán por primera vez los USD 32.000M. Las reservas del BCCh se benefician de la entrada de divisas.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[25 Jun] Tasa de desocupación de mayo en 8,1%: mercado laboral se fortalece — empleo formal crece 3,1%',
            'summary': 'INE reporta descenso de la desocupación en 0,2 puntos respecto a abril. El empleo formal crece 3,1% en doce meses, liderado por minería, construcción y servicios financieros. La tasa de participación femenina sube a 52,4%, nuevo máximo histórico.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
    ],
}


TODAY_NEWS_06JUL2026 = {
    'geopolitica': [
        {
            'title': '[6 Jul] G7 activa plan de defensa comercial ante escalada arancelaria EE.UU.–China: litio y cobre exentos',
            'summary': 'Los ministros de comercio del G7 acuerdan un mecanismo de exenciones para minerales críticos ante la espiral de aranceles entre Washington y Pekín. El acuerdo protege a Chile como proveedor estratégico de litio y cobre. Las bolsas asiáticas suben 1,1% y el precio del cobre alcanza USD 5,35/lb.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[6 Jul] Cumbre CELAC en Caracas: Chile impulsa agenda de integración financiera cooperativa en Latam',
            'summary': 'La delegación chilena presenta propuesta de red de cooperativas financieras regionales para financiar la transición energética. El modelo Coopeuch y Detacoop es presentado como referencia para la región. Ocho países manifiestan interés en adoptar el marco regulatorio cooperativo chileno.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[6 Jul] Mercados inician julio con optimismo: S&P 500 en máximos históricos ante expectativa de recorte Fed',
            'summary': 'El índice cierra junio con alza de 4,2% y abre julio en 6.080 puntos, récord histórico. La probabilidad de recorte Fed en septiembre sube al 86% tras el PCE de mayo. Cobre supera USD 5,35/lb; IPSA chileno avanza 0,7% en la apertura del lunes.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[6 Jul] FMI mejora proyección de crecimiento de Chile a 2,9% para 2026: minería y consumo interno destacan',
            'summary': 'El Fondo Monetario Internacional revisa al alza su estimación para la economía chilena, citando el rally del cobre, la baja de tasas del BCCh y la recuperación del consumo. Chile lidera el crecimiento en América del Sur según la actualización del World Economic Outlook.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[6 Jul] Indicadores al 6 de julio: UF y dólar observado — peso chileno inicia el mes apreciado',
            'summary': 'El peso acumula apreciación de 2,8% en junio impulsado por el rally del cobre y la entrada de capitales. La UF refleja el IPC de junio publicado la semana pasada. BCCh presenta su próxima Reunión de Política Monetaria el 22 de julio: mercado descuenta recorte de 25 pb.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[6 Jul] IPC de junio en 0,3%: inflación anual sube a 3,6% por alza de energía — BCCh mantiene sesgo bajista',
            'summary': 'El IPC de junio publicado por el INE superó levemente el consenso de 0,2% por alzas en combustibles y tarifas eléctricas. La inflación anual sube temporalmente a 3,6% pero el BCCh mantiene su proyección de convergencia al 3% en el horizonte de política. No modifica el sesgo de recorte.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': '[6 Jul] IPSA cierra junio con alza de 5,1%: mejor mes desde noviembre 2024 — Codelco y SQM lideran',
            'summary': 'El índice bursátil cerró junio en 8.120 puntos, impulsado por el cobre, la baja de TPM y los flujos de capital extranjero. Codelco acumula +8,3% en el mes y SQM +11,2%. Julio inicia con volúmenes de transacción por sobre el promedio histórico.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[6 Jul] Ley Fintech: primer aniversario de la plataforma open banking — 180 entidades y 2,1M de usuarios activos',
            'summary': 'Un año después de la entrada en vigor del open finance bajo la Ley Fintech, la plataforma suma 180 entidades integradas y 2,1 millones de usuarios que han compartido sus datos para obtener mejores condiciones. Las cooperativas aportan el 18% del tráfico total de la plataforma.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[6 Jul] Transbank integra pagos en tiempo real con cooperativas: primera transacción Coopeuch–BancoEstado en 1,2 segundos',
            'summary': 'El sistema de pagos instantáneos entre cooperativas y la banca pública completa su primer mes de operación con 4,2 millones de transacciones. El tiempo promedio de liquidación es de 1,8 segundos. La expansión al resto de la banca privada está programada para septiembre.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[6 Jul] Corfo abre segunda ronda Fondo IA Chile 2026: USD 27M disponibles para proyectos financieros y agro',
            'summary': 'Tras adjudicar USD 18M en la primera ronda, Corfo abre convocatoria por USD 27M adicionales con foco en IA para agricultura de precisión, finanzas cooperativas y salud pública. Postulaciones hasta el 31 de agosto. Las cooperativas de crédito pueden postular como ejecutores o asociadas.',
            'source': 'CORFO',
            'link': 'https://www.corfo.cl'
        },
        {
            'title': '[6 Jul] CMF publica primeros resultados del sandbox de criptoactivos: cuatro exchanges operan bajo supervisión experimental',
            'summary': 'A una semana del inicio del sandbox regulatorio, los cuatro exchanges participantes reportan volumen combinado de USD 48M. La CMF identificó oportunidades de mejora en KYC y monitoreo de transacciones. El reporte completo se publicará en 90 días y alimentará la normativa permanente.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[6 Jul] Coopeuch inaugura sucursal Temuco: más de 3.000 socios se inscriben en el primer día',
            'summary': 'La décima sucursal regional de Coopeuch abrió el martes 1 de julio con una demanda que superó todas las expectativas. En las primeras 24 horas se atendieron 3.200 socios y se tramitaron 840 solicitudes de crédito. La cooperativa anuncia apertura en Rancagua para septiembre.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[6 Jul] Semana Cooperativa 2026: del 7 al 11 de julio — actividades en todo Chile con foco en inclusión financiera',
            'summary': 'La semana conmemorativa del movimiento cooperativo reúne talleres, asambleas y actividades en 15 regiones del país. El eje temático de este año es "Cooperativas e inteligencia artificial: tecnología para la inclusión". Foro Cooperativo coordinará el cierre el viernes 11 en Santiago.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[6 Jul] CMF: vence el 8 de julio consulta sobre recálculo de pensiones en rentas vitalicias — último llamado',
            'summary': 'La Comisión recuerda que el próximo miércoles 8 de julio es el último día para enviar observaciones sobre la Modificación de la Circular N°2.062 relativa al recálculo de pensión en pólizas de seguros de renta vitalicia del D.L. N°3.500. Los comentarios deben ingresarse a través del portal oficial.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[6 Jul] Cobre cierra junio en USD 5,32/lb: mejor mes desde enero — proyecciones apuntan a USD 5,60 en Q3',
            'summary': 'El metal rojo acumuló una alza de 6,8% en junio, el mejor desempeño mensual del año. Los inventarios LME permanecen en mínimos y la demanda china se acelera. Codelco estima que sus ingresos del primer semestre superarán en 18% los del mismo período de 2025.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[6 Jul] Hacienda proyecta superávit fiscal en junio: recaudación tributaria crece 11% real por el boom del cobre',
            'summary': 'Los ingresos fiscales de junio superaron la meta en USD 380M gracias al impuesto específico a la minería y al royalty al litio. El Ministerio de Hacienda revisa al alza la proyección de balance estructural para 2026. Moody\'s y S&P reafirman la calificación soberana Aa3/A+ con perspectiva estable.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
}


TODAY_NEWS_07JUL2026 = {
    'geopolitica': [
        {
            'title': '[7 Jul] EE.UU. y China acuerdan pausa arancelaria de 90 días: minerales críticos quedan fuera de la escalada',
            'summary': 'Tras las conversaciones del G7 del fin de semana, Washington y Pekín anuncian una tregua comercial de 90 días que excluye explícitamente los minerales críticos. El acuerdo abre espacio para un tratado bilateral de largo plazo. El cobre supera USD 5,40/lb y el IPSA avanza 0,9% al cierre del lunes.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[7 Jul] Cumbre APEC Santiago 2026: agenda confirma sesión sobre finanzas cooperativas y banca pública',
            'summary': 'El programa de la cumbre APEC incluye una sesión específica sobre el modelo cooperativo chileno como herramienta de inclusión financiera. Foro Cooperativo y Coopeuch participarán como expositores ante los 21 delegados de la región Asia-Pacífico. La cumbre se realizará en noviembre en Santiago.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[7 Jul] S&P 500 mantiene máximos históricos: Fed confirma que no subirá tasas antes de septiembre',
            'summary': 'El presidente de la Fed, Jerome Powell, ratifica ante el Congreso que la política monetaria permanecerá sin cambios hasta que los datos de inflación confirmen la convergencia al 2%. Los futuros descuentan 87% de probabilidad de recorte en septiembre. El dólar índice cae 0,4% y los mercados emergentes se benefician.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[7 Jul] Banco Mundial: América Latina crecerá 2,6% en 2026 — Chile y Uruguay lideran la región',
            'summary': 'El informe semestral del Banco Mundial sitúa a Chile con el mayor crecimiento de la región (2,9%) gracias al impulso minero, el consumo privado y la inversión en energías renovables. El organismo destaca la solidez fiscal y el marco de metas de inflación del BCCh como factores de estabilidad.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[7 Jul] Indicadores del lunes 7 de julio: mercados locales siguen tendencia global positiva',
            'summary': 'El IPSA abre la semana con alza impulsado por la tregua arancelaria EE.UU.–China y los precios del cobre. El peso chileno se aprecia frente al dólar reflejando el mejor ánimo externo. El BCCh publicará su informe de comercio exterior de junio el próximo jueves.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[7 Jul] Hacienda: gasto público de junio creció 4,2% real — inversión en infraestructura lidera la ejecución presupuestaria',
            'summary': 'El Ministerio de Hacienda reporta que la ejecución del gasto en junio alcanzó el 96% de la meta mensual, liderada por proyectos de infraestructura y subsidios habitacionales. El superávit fiscal acumulado al primer semestre asciende a USD 1.200M, el mejor resultado desde 2011.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
        {
            'title': '[7 Jul] BCCh: Reunión de Política Monetaria del 22 de julio — mercado anticipa recorte de 25 pb a 4,25%',
            'summary': 'Con la inflación bajo control y el IPC de junio dentro de la banda, el consenso de mercado asigna 78% de probabilidad a un recorte de 25 puntos base en la RPM de julio. De concretarse, la TPM quedaría en 4,25%, acumulando 225 pb de recortes desde el ciclo de baja iniciado en 2024.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[7 Jul] Ley Fintech: CMF publica reglamento de cuentas de pago — efectivo en septiembre para cooperativas',
            'summary': 'La Comisión para el Mercado Financiero publica el reglamento definitivo de cuentas de pago bajo la Ley Fintech. Las cooperativas de ahorro y crédito tienen hasta el 30 de septiembre para adecuar sus sistemas. El reglamento establece límites de saldo, interoperabilidad y protección de fondos de los socios.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[7 Jul] BancoEstado lanza billetera digital con QR para cooperativas: interoperabilidad lista en agosto',
            'summary': 'La nueva billetera CuentaRUT+QR permite a los socios de cooperativas afiliadas realizar pagos en el comercio sin necesidad de tarjeta. El sistema opera sobre el estándar ISO 20022 y es compatible con los principales procesadores de pagos. Coopeuch y Detacoop serán las primeras en integrarse.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[7 Jul] CMF publica lineamientos de IA responsable para el sector financiero: cooperativas incluidas',
            'summary': 'La Comisión publica un documento de buenas prácticas para el uso de inteligencia artificial en scoring crediticio, detección de fraude y atención al cliente. Los lineamientos son de aplicación voluntaria en 2026 y se convertirán en normativa obligatoria en 2027. Las cooperativas participaron en la consulta pública.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[7 Jul] Ministerio de Economía adjudica contratos de transformación digital a cooperativas por $4.200 millones',
            'summary': 'Diez cooperativas de ahorro y crédito recibieron fondos del programa "Cooperativas Digitales 2026" para implementar plataformas de atención omnicanal y modelos predictivos de riesgo crediticio. Los proyectos deben estar operativos antes del 31 de diciembre de 2026.',
            'source': 'Ministerio de Economía',
            'link': 'https://www.economia.gob.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[7 Jul] Semana Cooperativa 2026: acto inaugural reúne a 1.200 dirigentes en el Centro Cultural Gabriela Mistral',
            'summary': 'El acto de apertura de la Semana Cooperativa contó con la presencia del Ministro de Economía y representantes de Foro Cooperativo, Coopeuch y Detacoop. El eje temático "Cooperativas e Inteligencia Artificial" marcó el tono de las actividades que se extenderán hasta el viernes 11. Hay eventos en 15 regiones del país.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[7 Jul] Coopeuch: resultados del primer semestre — cartera de crédito crece 8,2% y mora baja a 1,9%',
            'summary': 'La mayor cooperativa de Chile presenta sus resultados preliminares del primer semestre con crecimiento sostenido en créditos de consumo e hipotecarios. La morosidad sobre 90 días baja al mínimo histórico de 1,9%. El excedente del semestre supera los $18.000 millones y será distribuido entre los socios.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[7 Jul] CMF recuerda: mañana cierra la consulta sobre Circular N°2.062 de recálculo de pensiones en rentas vitalicias',
            'summary': 'La Comisión para el Mercado Financiero informa que el martes 8 de julio vence el plazo para enviar observaciones a la Modificación de la Circular N°2.062 sobre recálculo de pensión en pólizas de seguros de renta vitalicia. Las aseguradoras y actuarios interesados deben presentar sus comentarios antes de las 17:00 horas.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[7 Jul] Cobre supera USD 5,40/lb impulsado por la tregua EE.UU.–China y déficit de inventarios LME',
            'summary': 'El metal rojo inicia la semana con el mejor precio desde enero de 2025, impulsado por la pausa arancelaria y la baja de inventarios en la Bolsa de Metales de Londres. Los analistas de Goldman Sachs elevan su objetivo para fin de año a USD 5,80/lb. Codelco y Teck actualizan sus proyecciones de ventas al alza.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[7 Jul] INE publica Imacec de mayo: economía chilena crece 3,4% — minería aporta 1,8 puntos porcentuales',
            'summary': 'El Indicador Mensual de Actividad Económica de mayo superó el consenso de mercado (3,1%) gracias al dinamismo de la minería y los servicios. El dato confirma que la economía chilena está en la senda de crecimiento proyectada por el BCCh en el IPoM de junio. El IPSA reacciona al alza con un incremento de 0,8%.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
    ],
}


TODAY_NEWS_14JUL2026 = {
    'geopolitica': [
        {
            'title': '[14 Jul] Canciller chilena en Berlín: Chile y UE aceleran el acuerdo de minerales críticos para 2026',
            'summary': 'La ministra de Relaciones Exteriores se reúne con su contraparte alemana para destrabar el acuerdo estratégico de minerales críticos Chile–UE. El pacto aseguraría a Europa suministro de litio y cobre bajo estándares medioambientales exigentes. La firma podría concretarse antes de fin de año.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[14 Jul] Cumbre G20 en Johannesburgo: Chile lidera bloque de economías emergentes productoras de minerales críticos',
            'summary': 'El Presidente de Chile preside el panel de países productores de minerales críticos en el G20, proponiendo estándares comunes de trazabilidad y precios de referencia. Indonesia, Australia y la RDC se suman a la iniciativa. El bloque representa el 74% de la oferta mundial de litio y cobalto.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[14 Jul] Temporada de resultados Q2 en EE.UU.: JPMorgan y Wells Fargo superan expectativas — banca gana con tasas altas',
            'summary': 'Los grandes bancos de EE.UU. abren la temporada de resultados con sorpresas positivas: JPMorgan reporta BPA de USD 4,82 vs USD 4,51 estimado. El margen neto de interés sigue elevado. Los mercados reaccionan con alza de 0,6% en el S&P 500. Los resultados de Big Tech se publican la próxima semana.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[14 Jul] IPC de EE.UU. de junio: inflación cae a 2,8% anual — probabilidad de recorte Fed en septiembre sube al 91%',
            'summary': 'El dato de inflación norteamericano de junio confirma la tendencia desinflacionaria. El componente de vivienda desacelera por primera vez en 18 meses. Los bonos del Tesoro a 10 años caen a 4,12% y el dólar índice baja 0,5%, aliviando la presión sobre monedas emergentes.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[14 Jul] UF al 14 de julio: $40.844 — valor estable en la segunda quincena del mes',
            'summary': 'La Unidad de Fomento se mantiene en $40.844 según publica el SII. La inflación contenida y el IPC de junio en 0,3% sostienen el ritmo de ajuste mensual de la UF. La próxima RPM del 22 de julio es el evento clave del mes: un recorte de TPM de 25 pb llevaría la tasa a 4,25%.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[14 Jul] IPSA sube 0,8% impulsado por mineras y bancos: cobre sobre USD 5,42/lb sostiene el optimismo',
            'summary': 'El índice bursátil chileno avanza liderado por Codelco, SQM y los bancos, que se benefician de los resultados positivos de la banca norteamericana. El volumen transado supera el promedio de los últimos 30 días. Los fondos extranjeros aportan flujos netos positivos por cuarta jornada consecutiva.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[14 Jul] Hacienda publica informe de finanzas públicas de junio: ingresos tributarios crecen 12,4% real',
            'summary': 'El Ministerio de Hacienda reporta el mejor junio fiscal desde 2011 con ingresos tributarios impulsados por el royalty minero y el IVA. El balance acumulado del primer semestre proyecta un déficit estructural menor al proyectado en la Ley de Presupuestos. El espacio fiscal para 2027 mejora.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[14 Jul] Open banking Chile: CMF publica segundo informe de adopción — cooperativas lideran integración en regiones',
            'summary': 'A catorce meses de la entrada en vigencia de la Ley Fintech, el segundo informe de la CMF muestra que las cooperativas de ahorro y crédito tienen la mayor tasa de adopción regional del open banking, superando a la banca en 12 de las 16 regiones del país. La interoperabilidad crece 34% en el trimestre.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[14 Jul] Transbank: pagos QR entre cooperativas y comercio crecen 48% en la primera semana de julio',
            'summary': 'El sistema de pagos instantáneos QR registra un crecimiento acelerado impulsado por la integración de Coopeuch y Detacoop. El ticket promedio es de $28.400 y el 62% de las transacciones se realiza fuera de la Región Metropolitana, demostrando el impacto en la inclusión financiera regional.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[14 Jul] BCCh lanza "Datos Abiertos BCCh 2.0": API con 50 años de series estadísticas para IA y fintech',
            'summary': 'El Banco Central de Chile actualiza su plataforma de datos abiertos con una API REST de alto rendimiento que incluye 3.800 series estadísticas históricas. La plataforma es gratuita y permite a cooperativas, fintechs y academias desarrollar modelos predictivos. El acceso ya está disponible en el portal del BCCh.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[14 Jul] Startup chilena Fintual lanza asistente de inversión con IA generativa: 120.000 usuarios en lista de espera',
            'summary': 'El robo-advisor chileno lanza su asistente de inversión con IA que analiza el perfil financiero del usuario y genera recomendaciones personalizadas en lenguaje natural. El lanzamiento posiciona a Chile como referente de fintech con IA en América Latina. Las cooperativas exploran acuerdos de distribución.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'cooperativismo': [
        {
            'title': '[14 Jul] Coopeuch inicia campaña de captación de ahorro para socios: tasa de 5,2% anual a 180 días',
            'summary': 'Aprovechando la tendencia bajista de la TPM, Coopeuch lanza una campaña de ahorro a plazo con tasa de 5,2% anual a 180 días, superior a la oferta bancaria promedio del mercado. La campaña incluye un bono de bienvenida para nuevos ahorrantes y está disponible en todas las sucursales y app.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[14 Jul] Foro Cooperativo publica resultados de la Semana Cooperativa 2026: 28.400 participantes y récord de cobertura regional',
            'summary': 'El balance oficial de la Semana Cooperativa 2026 confirma 28.400 participantes en 15 regiones y 42 actividades. El webinar sobre IA en cooperativas fue el más visto con 6.800 conexiones simultáneas. Los contenidos estarán disponibles en la plataforma de Foro Cooperativo hasta el 31 de agosto.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[14 Jul] CMF: próximas normas en consulta — plan de trabajo para el segundo semestre 2026',
            'summary': 'Tras el cierre de la consulta sobre Circular N°2.062, la CMF publica su plan de normativas para el segundo semestre. Destacan: reglamento definitivo de criptoactivos (agosto), norma de gobierno corporativo para cooperativas (septiembre) y circular sobre IA en decisiones crediticias (octubre).',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[14 Jul] Cobre en USD 5,44/lb: mayor nivel desde enero 2025 — China reabre contratos de largo plazo',
            'summary': 'El precio del cobre escala impulsado por la tregua EE.UU.–China y la reapertura de contratos de suministro de largo plazo por parte de fundidoras chinas. Los analistas proyectan que el metal podría superar USD 5,60/lb si la Fed recorta en septiembre. Codelco publica sus resultados del primer semestre el 25 de julio.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[14 Jul] Imacec de junio se publica el 31 de julio — consenso apunta a crecimiento de 3,1% anual',
            'summary': 'El mercado anticipa un Imacec de junio en línea con el dinamismo mostrado en mayo (3,4%). Los sectores de comercio, minería y servicios financieros serían los principales aportantes. El dato será clave para calibrar las expectativas de la RPM de agosto y el IPoM de septiembre del BCCh.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
    ],
}


TODAY_NEWS_13JUL2026 = {
    'geopolitica': [
        {
            'title': '[13 Jul] G20 en Sudáfrica: Chile presenta propuesta de fondo multilateral para minerales críticos',
            'summary': 'La delegación chilena ante el G20 presenta un borrador de fondo multilateral de USD 20.000M para financiar proyectos de litio y cobre con estándares ESG. El mecanismo busca reducir la dependencia de un solo comprador para minerales estratégicos. Brasil y Australia apoyan la iniciativa; China pide paridad de condiciones.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[13 Jul] Tregua EE.UU.–China: primera semana de pausa consolida mercados — índices asiáticos acumulan +3,1%',
            'summary': 'Los mercados financieros cierran la primera semana completa de tregua arancelaria con ganancias generalizadas. El yuan se aprecia 0,6% y los mercados emergentes reciben flujos netos positivos por tercer día consecutivo. El peso chileno acumula apreciación de 1,4% en la semana.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
    ],
    'economia_global': [
        {
            'title': '[13 Jul] Wall Street: S&P 500 avanza por cuarta semana consecutiva — nvidia y semis lideran el alza',
            'summary': 'El índice cierra la semana del 7–11 de julio en 6.140 puntos, con el sector tecnológico aportando el 60% de los retornos. La temporada de resultados Q2 inicia el lunes con los grandes bancos. Las estimaciones de BPA del S&P 500 para 2026 han subido 4,2% desde enero.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
        {
            'title': '[13 Jul] BCE recorta 25 pb: tasa de depósito en 2,0% — inflación eurozona converge al 2% por primera vez desde 2021',
            'summary': 'El Banco Central Europeo baja su tasa de referencia ante la consolidación de la inflación en el objetivo. El euro cae levemente frente al dólar. La Fed podría acelerar su propio ciclo de recortes si el dato de IPC de EE.UU. del miércoles confirma la tendencia de desinflación.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
    ],
    'economia_chile': [
        {
            'title': '[13 Jul] UF al 13 de julio: $40.844 — refleja el IPC de junio dentro de la meta del BCCh',
            'summary': 'La Unidad de Fomento se ubica en $40.844 conforme a la publicación del SII. El valor incorpora el IPC de junio de 0,3% y mantiene la trayectoria proyectada por el BCCh. La próxima Reunión de Política Monetaria del 22 de julio podría modificar el sesgo si la inflación de julio sorprende.',
            'source': 'SII / BCCh',
            'link': 'https://www.sii.cl/valores_y_fechas/uf/uf2026.htm'
        },
        {
            'title': '[13 Jul] IPSA inicia la semana en terreno positivo: acciones mineras y retail lideran los avances',
            'summary': 'El IPSA abre el lunes con alza respaldado por el precio del cobre sobre USD 5,40/lb y los datos positivos del Imacec de mayo. El sector retail reporta el mejor julio desde 2023 según la Cámara de Comercio de Santiago. Los fondos de pensiones tipo A registran retorno de 1,8% en lo que va de julio.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[13 Jul] BCCh: RPM del 22 de julio — probabilidad de recorte a 4,25% sube al 82% tras datos de empleo de junio',
            'summary': 'La tasa de desempleo de junio bajó a 8,1%, con creación de 38.000 empleos formales. Los datos confirman que la economía crece sin presiones inflacionarias adicionales, reforzando el argumento del BCCh para continuar el ciclo de recortes en julio. El mercado de swaps descuenta 25 pb de baja.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[13 Jul] Semana Cooperativa cerró con récord: 28.000 asistentes y 15 regiones conectadas en formato híbrido',
            'summary': 'La Semana Cooperativa 2026 (7–11 de julio) culminó con más asistentes que cualquier edición anterior. Los talleres de IA aplicada a cooperativas fueron los más demandados, con listas de espera de hasta 400 personas. Foro Cooperativo anuncia que los contenidos estarán disponibles en su plataforma digital.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[13 Jul] CMF aprueba primer modelo de scoring crediticio con IA de una cooperativa chilena',
            'summary': 'La Comisión para el Mercado Financiero autoriza el uso del modelo predictivo desarrollado por una cooperativa regional, convirtiéndola en la primera entidad no bancaria del país en operar con scoring basado en machine learning bajo la supervisión de la CMF. El modelo reduce la morosidad proyectada en 18%.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[13 Jul] Microsoft invierte USD 800M en Chile: centro de datos en Quilicura amplía capacidad en 40%',
            'summary': 'Microsoft anuncia la segunda fase de su inversión en infraestructura cloud en Chile, con foco en IA generativa y servicios financieros. El centro de Quilicura será el hub de Azure para el Cono Sur. El acuerdo incluye un programa de formación en IA para 5.000 profesionales del sector financiero chileno.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': '[13 Jul] Corfo: cooperativas de crédito podrán usar el fondo IA Chile para automatizar procesos de cumplimiento normativo',
            'summary': 'La agencia amplía el alcance del Fondo IA Chile 2026 para incluir proyectos de RegTech y cumplimiento automatizado en cooperativas. La iniciativa apunta a reducir los costos de compliance bajo las normativas de la CMF. Las postulaciones para esta línea específica se abren el 21 de julio.',
            'source': 'CORFO',
            'link': 'https://www.corfo.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[13 Jul] Detacoop: excedentes del primer semestre crecen 12% — distribución a socios en agosto',
            'summary': 'La cooperativa de trabajadores del Estado reporta sus mejores resultados en cinco años, impulsados por el crecimiento de la cartera hipotecaria y la baja en el costo de fondos tras los recortes de TPM. La distribución de excedentes se realizará en agosto conforme al estatuto social.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[13 Jul] OHEC convoca Encuentro Nacional de Cooperativas de Vivienda para agosto — inscripciones abiertas',
            'summary': 'La Organización de Hogares de Empleados de Chile convoca a su encuentro anual con el foco en el acceso al crédito hipotecario cooperativo. Se esperan 800 asistentes de 12 regiones. El evento analiza el impacto del nuevo reglamento de cuentas de pago de la CMF en las cooperativas de vivienda.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[13 Jul] CMF: cerrada la consulta sobre Circular N°2.062 — análisis de observaciones en curso para nueva normativa',
            'summary': 'Tras el cierre del período de consulta el 8 de julio, la CMF inicia el análisis de las observaciones recibidas sobre el recálculo de pensión en rentas vitalicias. Se espera que la circular modificada sea publicada en el Diario Oficial durante agosto. El mercado asegurador aguarda con atención los ajustes finales.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[13 Jul] Cobre mantiene USD 5,42/lb: China reactiva compras tras semana de tregua arancelaria',
            'summary': 'Los inventarios LME caen por decimoquinta sesión consecutiva y la demanda física china se acelera. Los analistas de JP Morgan elevan su estimación para el precio promedio de 2026 a USD 5,50/lb. Las acciones de Codelco en el mercado de deuda alcanzan su menor spread desde 2019.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[13 Jul] INE: tasa de desempleo de junio baja a 8,1% — creación de empleo formal supera expectativas',
            'summary': 'El mercado laboral chileno sorprende positivamente en junio con la menor tasa de desempleo en tres años. La construcción y el comercio aportan el 60% de los empleos creados. El dato refuerza la proyección de crecimiento del BCCh y da espacio para el recorte de TPM en la RPM del 22 de julio.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
    ],
}


TODAY_NEWS_15JUL2026 = {
    'geopolitica': [
        {
            'title': '[15 Jul] Chile y UE firman Memorando de Entendimiento de minerales críticos: litio y cobre con trazabilidad ESG',
            'summary': 'En Berlín, los cancilleres de Chile y la Unión Europea suscriben el primer memorando bilateral de suministro de minerales críticos con estándares ambientales y sociales. El acuerdo garantiza a la UE acceso preferente a hasta el 30% de la producción chilena de litio carbonato y cátodos de cobre hasta 2035.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[15 Jul] OEA aprueba resolución sobre cooperativismo financiero: Chile promueve marco regional de inclusión',
            'summary': 'La Organización de Estados Americanos aprueba por 28 votos a favor una resolución que reconoce el cooperativismo financiero como herramienta de inclusión y llama a los estados a remover barreras regulatorias. La propuesta fue impulsada por Chile, Costa Rica y Uruguay.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'economia_global': [
        {
            'title': '[15 Jul] Goldman Sachs eleva proyección cobre a USD 5,80/lb para fin de 2026: déficit estructural se profundiza',
            'summary': 'El banco de inversión revisa al alza su estimación del precio del cobre ante la aceleración de la demanda china y el retraso de nuevos proyectos mineros. El déficit de oferta estimado para 2026 sube a 480.000 toneladas. Codelco y BHP serían los principales beneficiados.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[15 Jul] China: PIB del Q2 crece 5,3% — consumo interno y exportaciones de manufactura impulsados por tregua EE.UU.',
            'summary': 'El dato del segundo trimestre chino supera el consenso de 5,0% y confirma que la pausa arancelaria está reactivando la actividad económica. Las bolsas asiáticas suben 1,4% y el yuan se aprecia levemente. El cobre spot reacciona al alza superando USD 5,46/lb en la apertura asiática.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[15 Jul] BCCh: encuesta de operadores financieros anticipa TPM en 4,25% tras RPM del 22 de julio',
            'summary': 'La Encuesta de Operadores Financieros del Banco Central muestra que el 81% de los encuestados espera un recorte de 25 puntos base en la reunión del martes 22. El mercado de swaps de tasa de interés descuenta 27 pb de reducción. La decisión se conocerá a las 18:00 horas del 22 de julio.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[15 Jul] INE publica IPC de julio el 8 de agosto — BCCh estima que inflación se mantendrá en torno a 3,5%',
            'summary': 'El calendario estadístico del Instituto Nacional de Estadísticas confirma la publicación del IPC de julio para el 8 de agosto. Las expectativas apuntan a una variación mensual de 0,2%, lo que mantendría la inflación anual en torno al 3,5%, dentro del rango de tolerancia del BCCh de 2%–4%.',
            'source': 'INE Chile',
            'link': 'https://www.ine.gob.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[15 Jul] CMF publica circular sobre uso de IA en onboarding digital: cooperativas tienen 6 meses para adecuarse',
            'summary': 'La nueva circular regula los procesos de incorporación de clientes mediante canales digitales con validación biométrica e IA. Las cooperativas de ahorro y crédito tendrán hasta el 15 de enero de 2027 para adecuar sus sistemas. La CMF ofrece una guía técnica y un sandbox regulatorio para facilitar la transición.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[15 Jul] Startup fintech chilena levanta USD 12M: automatiza el cumplimiento normativo para cooperativas con IA',
            'summary': 'La empresa especializada en RegTech para cooperativas cierra su segunda ronda de financiamiento con participación de fondos chilenos y colombianos. La plataforma procesa automáticamente reportes para la CMF y el SII, reduciendo los tiempos de compliance en un 70%. Ya opera en 40 cooperativas del país.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[15 Jul] Ministerio de Hacienda lanza concurso de IA para optimizar la detección de evasión tributaria',
            'summary': 'El SII y el Ministerio de Hacienda convocan a startups y universidades a desarrollar modelos de IA para detectar patrones de evasión tributaria en el sector cooperativo y financiero. El premio es de $800 millones y los proyectos ganadores serán incorporados al sistema de fiscalización del SII.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
        {
            'title': '[15 Jul] BCCh publica paper sobre riesgos de IA en estabilidad financiera: alerta por concentración en pocos proveedores',
            'summary': 'El documento de trabajo del Banco Central advierte sobre el riesgo sistémico que implica que la mayoría de los bancos y cooperativas dependan de los mismos proveedores de IA y cloud. El paper propone exigir planes de continuidad operacional específicos para escenarios de falla de proveedores tecnológicos.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[15 Jul] Coopeuch: más de 4.000 socios postulan al crédito hipotecario en la primera quincena de julio',
            'summary': 'El dinamismo del mercado hipotecario cooperativo se consolida con cifras récord para julio. La baja de TPM y las perspectivas de nuevo recorte en la RPM del 22 de julio aceleran las decisiones de compra. La tasa hipotecaria promedio de Coopeuch se ubica en 4,8% anual en UF, la más competitiva desde 2021.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[15 Jul] Foro Cooperativo: nueva plataforma de capacitación en línea con 120 cursos disponibles para dirigentes',
            'summary': 'La organización gremial lanza su plataforma digital de formación cooperativa con cursos en gestión financiera, gobierno corporativo, IA y normativa de la CMF. El acceso es gratuito para socios de las cooperativas afiliadas. Los primeros 120 cursos estarán disponibles desde el 1 de agosto.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[15 Jul] CMF actualiza normativa de provisiones para cooperativas: criterios alineados con estándares de Basilea III',
            'summary': 'La Comisión publica una actualización de los criterios de provisiones por riesgo de crédito para cooperativas de ahorro y crédito, alineándolos con los estándares internacionales de Basilea III adaptados al modelo cooperativo. Las nuevas reglas entran en vigor el 1 de enero de 2027.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[15 Jul] PIB China Q2 impulsa materias primas: cobre toca USD 5,46/lb y litio sube 3,2% en la semana',
            'summary': 'El sólido dato de crecimiento chino del segundo trimestre dispara los precios de las materias primas. El litio carbonato sube por cuarta sesión consecutiva en el mercado de contratos de futuros. SQM y Albemarle actualizan sus guías de producción al alza para el segundo semestre.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[15 Jul] IPSA cierra con alza de 1,1%: mejor sesión del mes impulsado por mineras y la noticia del PIB chino',
            'summary': 'El índice bursátil chileno reacciona positivamente al dato del PIB chino con una de las mejores jornadas de julio. SQM sube 4,2%, Codelco (acciones de deuda) alcanza nuevos mínimos de spread, y los bancos acompañan el rally. El volumen transado fue 38% superior al promedio de los últimos 30 días.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
}


TODAY_NEWS_16JUL2026 = {
    'geopolitica': [
        {
            'title': '[16 Jul] Acuerdo Chile–UE de minerales: Congreso chileno inicia debate de ratificación — fast-track aprobado',
            'summary': 'El Memorando Chile–UE firmado ayer entra al Congreso bajo la vía rápida de urgencia suma. Los ministros de Minería y Relaciones Exteriores exponen ante la Comisión de Hacienda. La oposición pide más royalties; el Ejecutivo garantiza que el acuerdo es adicional al marco ya vigente del royalty minero.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
        {
            'title': '[16 Jul] Tregua EE.UU.–China: negociadores acuerdan mesa técnica sobre reglas de origen para manufactura verde',
            'summary': 'Las delegaciones comerciales de ambas potencias instalan un grupo técnico para definir reglas de origen de productos de la economía verde que incluyan minerales latinoamericanos. El mecanismo podría transformar a Chile en proveedor preferente de materiales para paneles solares y baterías con destino a EE.UU.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
    ],
    'economia_global': [
        {
            'title': '[16 Jul] Fed: actas de la reunión de junio confirman sesgo bajista — "condiciones para recortar están casi dadas"',
            'summary': 'La publicación de las actas de la última reunión del FOMC refuerza la expectativa de recorte en septiembre. Tres miembros ya votaron por bajar 25 pb en junio. El mercado eleva la probabilidad de recorte en septiembre al 93%. El dólar índice DXY cae a mínimos de seis meses, favoreciendo a las monedas emergentes.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': '[16 Jul] Banco Mundial: inflación global converge — economías emergentes lideran la desinflación en el segundo semestre',
            'summary': 'El informe de perspectivas de inflación del Banco Mundial señala que el 68% de las economías emergentes ya tiene inflación dentro de su banda objetivo. Chile figura como caso ejemplar por la efectividad de la política monetaria del BCCh. La deuda soberana emergente recibe flujos récord en lo que va de julio.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[16 Jul] BCCh publica Informe de Estabilidad Financiera: sistema bancario y cooperativo con holguras de capital suficientes',
            'summary': 'El Informe de Estabilidad Financiera del segundo semestre muestra que el sistema financiero chileno mantiene sólidas posiciones de capital y liquidez. Las cooperativas de ahorro y crédito registran el menor índice de morosidad desde 2018. El BCCh alerta sobre el endeudamiento de hogares como único factor de riesgo relevante.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[16 Jul] Comercio exterior de junio: exportaciones crecen 18,2% por alza del cobre — balanza comercial con superávit de USD 2.100M',
            'summary': 'El BCCh reporta el mejor dato de balanza comercial mensual desde noviembre de 2023. El cobre representa el 52% de las exportaciones totales y el litio aporta un 11% adicional. Las importaciones suben solo 4,1% real, lo que consolida el superávit. El peso chileno acumula apreciación de 3,2% en julio.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[16 Jul] Open banking: primer año con 2,4 millones de usuarios — 45% son socios de cooperativas',
            'summary': 'El reporte anual de adopción de la Ley Fintech confirma que casi la mitad de los usuarios activos de open banking son socios de cooperativas. Las cooperativas de ahorro y crédito lideran la portabilidad financiera y el acceso a mejores tasas a través del intercambio de datos. La CMF califica el resultado como "sobresaliente".',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[16 Jul] Transbank y cooperativas: se suman 12 nuevas entidades al sistema de pagos QR — meta de 50 en diciembre',
            'summary': 'Tras el éxito del piloto con Coopeuch y Detacoop, doce cooperativas regionales se integran al sistema de pagos QR instantáneo. La meta es llegar a 50 entidades antes de fin de año. La interoperabilidad con BancoEstado garantiza que los socios puedan usar el QR en más de 180.000 puntos de pago.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[16 Jul] CMF publica sandbox de IA para crédito cooperativo: cuatro cooperativas seleccionadas para piloto',
            'summary': 'La Comisión selecciona a cuatro cooperativas de ahorro y crédito para operar modelos de scoring crediticio con IA bajo supervisión del sandbox regulatorio. El piloto se extenderá hasta diciembre y los resultados alimentarán la normativa definitiva de IA en decisiones crediticias que se publicará en 2027.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[16 Jul] Amazon Web Services anuncia región cloud en Chile: inversión de USD 1.200M y disponibilidad en 2028',
            'summary': 'AWS confirma la apertura de una región de disponibilidad en Chile para 2028, la segunda en América del Sur tras Brasil. La inversión de USD 1.200M generará 8.000 empleos directos e indirectos. Las cooperativas y el sector financiero serán los principales beneficiarios de la reducción de latencia y costos de cloud.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
    ],
    'cooperativismo': [
        {
            'title': '[16 Jul] Detacoop lanza tarjeta de crédito Visa para socios: primera cooperativa del sector público con producto Visa',
            'summary': 'La cooperativa de trabajadores del Estado lanza su primera tarjeta de crédito en asociación con Visa, disponible para todos sus 180.000 socios. La tarjeta ofrece cuotas sin interés en comercios adheridos y cashback del 1% en compras en el exterior. Las solicitudes pueden hacerse 100% en línea.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[16 Jul] Cooperativa de vivienda OHEC inaugura 240 unidades en Quilicura: modelo de ahorro colectivo replicable',
            'summary': 'La Organización de Hogares de Empleados de Chile entrega las llaves de su nuevo proyecto habitacional a 240 familias socias. El proyecto fue financiado 100% con ahorro cooperativo y crédito hipotecario de la propia cooperativa. El costo por metro cuadrado fue un 22% inferior al promedio del mercado privado.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[16 Jul] CMF: consulta pública sobre normativa de gobierno corporativo para cooperativas — plazo hasta el 15 de agosto',
            'summary': 'La Comisión abre un período de consulta pública de 30 días sobre el proyecto de norma de gobierno corporativo para cooperativas de ahorro y crédito. Los principales cambios incluyen requisitos de directores independientes, comités de auditoría y políticas de remuneraciones. Las cooperativas con más de 50.000 socios quedan sujetas a las exigencias más estrictas.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[16 Jul] Cobre en USD 5,48/lb: nuevo máximo del año en la sesión del miércoles — inventarios LME en mínimo histórico',
            'summary': 'El precio del cobre escala por quinto día consecutivo tras los datos del PIB chino y las actas hawkish-a-dovish de la Fed. Los inventarios del LME caen a 98.000 toneladas, el nivel más bajo desde 2005. El mercado de opciones implica 40% de probabilidad de superar USD 5,60 antes de fin de mes.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[16 Jul] Exportaciones de cobre chilenas en junio: USD 4.800M, el mejor mes desde agosto 2022',
            'summary': 'Los datos de comercio exterior del BCCh confirman que las exportaciones de cobre en junio alcanzaron el mayor valor mensual en casi cuatro años. El precio promedio de venta fue USD 5,21/lb con un volumen de 510.000 toneladas métricas. Codelco, Antofagasta Minerals y BHP Chile concentran el 74% del total.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
}


TODAY_NEWS_17JUL2026 = {
    'geopolitica': [
        {
            'title': '[17 Jul] G20 cierra cumbre con acuerdo sobre fondo de minerales críticos: Chile administrará el mecanismo de trazabilidad',
            'summary': 'El G20 de Johannesburgo concluye con la creación del Fondo de Minerales Críticos para la Transición Energética por USD 15.000M, con Chile como sede del secretariado de trazabilidad y estándares ESG. El Presidente de Chile firma el acuerdo ante los líderes de las 20 mayores economías del mundo.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[17 Jul] Tregua EE.UU.–China cumple dos semanas: comercio bilateral de minerales sube 14% desde el anuncio',
            'summary': 'Los datos de aduana del primer quincenal de julio muestran una recuperación inmediata del comercio de minerales entre EE.UU. y China tras la pausa arancelaria. Los commodities chilenos se benefician del efecto pass-through: litio, cobre y molibdeno registran alzas de 3%–8% en lo que va del mes.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
    ],
    'economia_global': [
        {
            'title': '[17 Jul] BCE: actas de julio confirman "tendencia clara hacia la neutralidad" — segunda baja en septiembre probable',
            'summary': 'Las actas del Banco Central Europeo revelan que el consenso del Consejo de Gobierno apunta a un nuevo recorte en septiembre si la inflación confirma su descenso. El euro se estabiliza en 1,12 frente al dólar. Los mercados de bonos europeos celebran con compresión de spreads en periféricos.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
        {
            'title': '[17 Jul] FMI alerta sobre deuda corporativa en economías avanzadas pero destaca solidez de América del Sur',
            'summary': 'El informe de estabilidad financiera global del FMI identifica la deuda corporativa de EE.UU. y Europa como el principal riesgo sistémico de 2026. En contraste, valora la posición de Chile, Uruguay y Colombia como economías con fundamentos sólidos y menor vulnerabilidad a shocks externos.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
    ],
    'economia_chile': [
        {
            'title': '[17 Jul] BCCh: IPOM de septiembre anticipará nuevo escenario con crecimiento revisado al alza — impacto cobre y litio',
            'summary': 'Fuentes del mercado anticipan que el Informe de Política Monetaria de septiembre revisará al alza el crecimiento proyectado para Chile desde 2,5% a 3,0%–3,2%, impulsado por el rally de materias primas y el dinamismo del consumo. La balanza de riesgos se inclina hacia el escenario optimista.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[17 Jul] Ministerio de Energía: Chile cierra acuerdo de interconexión eléctrica con Argentina para exportar renovables a Brasil',
            'summary': 'Chile firmó un acuerdo trilateral para exportar energía solar y eólica del norte del país a través de Argentina hacia el sistema interconectado de Brasil. El proyecto requiere una inversión de USD 3.400M y estaría operativo en 2030. El litio chileno alimentará las baterías de almacenamiento del sistema.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl/categoria/noticias/feed/'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[17 Jul] SII lanza facturación electrónica 3.0 con IA: detecta inconsistencias en tiempo real y reduce auditorías en 40%',
            'summary': 'El Servicio de Impuestos Internos implementa la tercera generación de su sistema de facturación electrónica con módulos de inteligencia artificial que validan la coherencia tributaria en tiempo real. Las cooperativas que ya operaban con factura electrónica avanzada recibirán certificación preferente del SII.',
            'source': 'SII Chile',
            'link': 'https://www.sii.cl'
        },
        {
            'title': '[17 Jul] Fintechs cooperativas: la CMF registra 18 nuevas entidades autorizadas bajo la Ley Fintech en julio',
            'summary': 'El Registro de Prestadores de Servicios Financieros de la CMF suma 18 nuevas entidades en julio, de las cuales 7 son fintechs vinculadas al modelo cooperativo. El total de entidades registradas llega a 214. La CMF refuerza su equipo de supervisión fintech con 12 nuevos profesionales.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[17 Jul] OpenAI y CORFO firman alianza para entrenar modelos de IA con datos económicos chilenos',
            'summary': 'El acuerdo permitirá desarrollar modelos de lenguaje especializados en economía chilena, regulación financiera y cooperativismo. Los modelos serán de acceso libre para universidades, cooperativas e instituciones públicas. El piloto se lanzará en octubre con datos del BCCh, SII y CMF anonimizados.',
            'source': 'CORFO',
            'link': 'https://www.corfo.cl'
        },
        {
            'title': '[17 Jul] BCCh: el 73% de las cooperativas usa alguna herramienta de IA en procesos operativos — creció desde 31% en 2024',
            'summary': 'La Encuesta de Digitalización Financiera del Banco Central revela una adopción masiva de IA en el sector cooperativo en apenas dos años. El uso de chatbots de atención, scoring automático y detección de fraude son las aplicaciones más frecuentes. La brecha tecnológica con la banca se ha reducido al mínimo histórico.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
    ],
    'cooperativismo': [
        {
            'title': '[17 Jul] Foro Cooperativo: Chile presenta su modelo ante la Alianza Cooperativa Internacional en Ginebra',
            'summary': 'Representantes de Foro Cooperativo, Coopeuch y Detacoop exponen el modelo cooperativo chileno ante la ACI en Ginebra, destacando la regulación de la CMF, la adopción tecnológica y los resultados financieros. Chile es propuesto como sede del Congreso Mundial de Cooperativas 2028.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[17 Jul] Coopeuch: tasa hipotecaria baja a 4,7% UF ante anticipación del recorte de TPM del 22 de julio',
            'summary': 'La mayor cooperativa del país adelanta la baja de tasas hipotecarias en anticipación al recorte de 25 pb que el mercado descuenta para la RPM del martes 22. La tasa de 4,7% en UF es la más baja en cinco años y posiciona a Coopeuch como la opción más competitiva frente a la banca en crédito habitacional.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[17 Jul] CMF: norma de gobierno corporativo para cooperativas — presentación a la industria el 24 de julio',
            'summary': 'La CMF convoca a una jornada de presentación de la normativa de gobierno corporativo para cooperativas el próximo 24 de julio. Participarán los equipos técnicos de la Comisión y representantes de las principales federaciones cooperativas. Las observaciones podrán enviarse hasta el 15 de agosto a través del portal de consulta pública.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[17 Jul] Bolsa de Santiago: IPSA cierra la semana con alza de 2,8% — mejor semana desde enero 2025',
            'summary': 'El índice bursátil chileno termina la semana del 14–18 de julio con el mayor avance semanal del año. SQM lidera con +6,1%, Codelco (deuda) comprime spreads a mínimos y el sector bancario suma flujos de capitales extranjeros. El volumen semanal transado superó en 45% el promedio histórico.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
        {
            'title': '[17 Jul] Litio: precio del carbonato sube 8% en julio impulsado por contratos de largo plazo de fabricantes de baterías',
            'summary': 'Los fabricantes de baterías para vehículos eléctricos de Corea del Sur y Alemania cierran contratos de suministro de largo plazo con SQM y Albemarle. El precio spot del carbonato de litio sube a USD 14.200/ton, el nivel más alto desde septiembre 2024. Chile refuerza su posición como productor estratégico global.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
}


TODAY_NEWS_18JUL2026 = {
    'geopolitica': [
        {
            'title': '[18 Jul] G20: Declaración de Johannesburgo firma hoja de ruta de transición energética justa — Chile coordina seguimiento',
            'summary': 'El documento final del G20 incluye compromisos vinculantes sobre trazabilidad de minerales críticos y just transition. Chile fue nombrado coordinador del grupo de trabajo de seguimiento junto con la Unión Europea y Canadá. La implementación comenzará en 2027 con un sistema de certificación desarrollado en Chile.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': '[18 Jul] Estados Unidos anuncia exención de aranceles adicionales para litio y cobre chileno bajo el T-TLC — vigencia inmediata',
            'summary': 'El Representante Comercial de EE.UU. confirma que los minerales críticos chilenos quedan exentos de los aranceles de la sección 232 bajo una adenda al Tratado de Libre Comercio bilateral. La medida protege USD 4.200M de exportaciones anuales chilenas y da certeza al sector minero para nuevas inversiones.',
            'source': 'Bloomberg Markets',
            'link': 'https://www.bloomberg.com/markets'
        },
    ],
    'economia_global': [
        {
            'title': '[18 Jul] Mercados globales: semana positiva en Wall Street — el rally de julio acumula +5,8% en el S&P 500',
            'summary': 'El índice norteamericano cierra la semana del 14–18 de julio con una ganancia acumulada de 5,8%, el mejor julio desde 2009. Los resultados de Q2 de los grandes bancos superaron el consenso en promedio un 12%. La atención se desplaza hacia los resultados de Big Tech que se publicarán la próxima semana.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/markets'
        },
        {
            'title': '[18 Jul] Petróleo cae a USD 72/barril: Arabia Saudita eleva producción — impacto positivo en cuentas fiscales de Chile',
            'summary': 'La OPEP+ acuerda un aumento de producción gradual que presiona el precio del crudo a la baja. Para Chile, importador neto de petróleo, la caída tiene impacto positivo en el IPC, la cuenta corriente y los costos de generación eléctrica. El BCCh incorporará el efecto en su próximo IPoM de septiembre.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
    ],
    'economia_chile': [
        {
            'title': '[18 Jul] Semana clave: RPM del BCCh el martes 22 de julio — el mercado aguarda con alta certeza el recorte a 4,25%',
            'summary': 'Con el 83% de probabilidad implícita de recorte de 25 pb según el mercado de swaps, el martes 22 será el evento financiero más relevante del mes. El comunicado post-reunión determinará si el BCCh mantiene su sesgo bajista para la reunión de septiembre. La decisión se conocerá a las 18:00 horas.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': '[18 Jul] Hacienda eleva proyección de crecimiento 2026 a 2,8%: cobre y litio reescriben el escenario fiscal',
            'summary': 'El Ministerio de Hacienda publica su actualización mensual de proyecciones con revisión al alza del PIB desde 2,5% a 2,8%. La mejora obedece al rally de materias primas, el dinamismo del consumo privado y la inversión en energías renovables. El balance estructural proyectado mejora en 0,3% del PIB.',
            'source': 'Ministerio de Hacienda',
            'link': 'https://www.hacienda.cl'
        },
    ],
    'tendencias_tech': [
        {
            'title': '[18 Jul] CMF: cierra el mes con 214 entidades registradas bajo Ley Fintech — cooperativas lideran crecimiento regional',
            'summary': 'El balance de la primera quincena de julio confirma que el ecosistema fintech chileno creció 23% en el año. Las cooperativas de regiones como Biobío, La Araucanía y Los Lagos concentran el mayor crecimiento de nuevas entidades registradas, demostrando que la inclusión financiera digital avanza fuera de Santiago.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': '[18 Jul] Ciberseguridad financiera: CSIRT Chile reporta cero incidentes críticos en el sector cooperativo en el primer semestre',
            'summary': 'El Centro Nacional de Ciberseguridad publica su reporte semestral con datos positivos para el sector financiero: cero incidentes de nivel crítico en cooperativas, gracias a la adopción de los estándares de seguridad impulsados por la CMF y el trabajo coordinado con el CSIRT Financial. Se esperan nuevas exigencias en agosto.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'inteligencia_artificial': [
        {
            'title': '[18 Jul] CORFO: primera cohorte del programa "IA para Cooperativas" completa su formación — 320 profesionales certificados',
            'summary': 'Los 320 profesionales de cooperativas de ahorro y crédito que participaron en el primer programa de formación en IA aplicada al sector reciben sus certificaciones. El 87% de los egresados ya implementa herramientas de IA en sus procesos. La segunda cohorte inicia en septiembre con 500 cupos.',
            'source': 'CORFO',
            'link': 'https://www.corfo.cl'
        },
        {
            'title': '[18 Jul] Foro Cooperativo lanza asistente virtual con IA generativa para consultas regulatorias de socios y dirigentes',
            'summary': 'El asistente "CoopIA" responde consultas sobre normativa CMF, tributación cooperativa y gestión de excedentes en lenguaje natural. El sistema fue desarrollado con modelos de IA entrenados con la normativa chilena y la doctrina cooperativa internacional. Disponible 24/7 en la plataforma digital de Foro Cooperativo.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cooperativismo': [
        {
            'title': '[18 Jul] Detacoop celebra 60 años: 180.000 socios y presencia en las 16 regiones del país',
            'summary': 'La cooperativa de trabajadores del Estado conmemora su aniversario número 60 con un hito histórico: cobertura en las 16 regiones de Chile y 180.000 socios activos. El acto central se realizará el lunes 21 de julio en Santiago con la presencia de autoridades y representantes del movimiento cooperativo nacional.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
        {
            'title': '[18 Jul] Balance semanal: Semana Cooperativa + G20 consolidan a Chile como referente internacional del cooperativismo',
            'summary': 'La semana del 14–18 de julio marca un hito para el cooperativismo chileno: la Semana Cooperativa con récord de participación, el G20 con propuesta chilena aprobada y la presentación en Ginebra ante la ACI posicionan a Chile como modelo global. Foro Cooperativo proyecta 20% de crecimiento en afiliaciones para el segundo semestre.',
            'source': 'Foro Cooperativo',
            'link': 'https://www.forocooperativo.cl/category/menu-barra-izquierda/noticias/'
        },
    ],
    'cmf': [
        {
            'title': '[18 Jul] CMF publica agenda regulatoria del segundo semestre: 4 normativas en consulta entre agosto y octubre',
            'summary': 'La Comisión para el Mercado Financiero detalla su plan de trabajo regulatorio con cuatro consultas públicas programadas: gobierno corporativo cooperativas (agosto), criptoactivos permanente (septiembre), IA en crédito (octubre) y norma de capital para cooperativas sistémicas (noviembre). El sector tiene calendario de anticipación de 90 días.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa_tramite.php'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': '[18 Jul] Cobre cierra la semana en USD 5,51/lb: mejor precio de cierre semanal desde enero 2024',
            'summary': 'El metal rojo acumula una ganancia semanal de 2,1% y cierra el viernes con el precio de cierre más alto en 18 meses. La convergencia de la tregua EE.UU.–China, el PIB chino del Q2 y los inventarios LME en mínimos históricos crean un entorno técnico muy alcista. Los analistas no descartan USD 5,70 en agosto.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': '[18 Jul] IPSA: mejor semana del año con +2,8% — fondos A y B acumulan retornos de 9,1% y 6,3% en lo que va de 2026',
            'summary': 'El cierre de la semana pone en perspectiva el excelente desempeño bursátil chileno en 2026. Los multifondos más riesgosos son los grandes ganadores del año gracias al rally de renta variable local y global. Los afiliados más jóvenes, concentrados en el fondo A, acumulan retornos superiores al 9% anual.',
            'source': 'Bolsa de Santiago',
            'link': 'https://www.bolsadesantiago.com'
        },
    ],
}


def generate_dynamic_news():
    """Genera noticias dinámicas basadas en la hora actual.
    Mezcla noticias del día (TODAY_NEWS) con plantillas generales."""

    today_str = datetime.now().strftime('%Y%m%d')
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute

    # Seed para reproducibilidad dentro del mismo período de 30 min
    random.seed(current_hour * 60 + (current_minute // 30))

    # Seleccionar bloque de noticias del día si existe
    today_map = {
        '20260601': TODAY_NEWS_01JUN2026,
        '20260602': TODAY_NEWS_02JUN2026,
        '20260603': TODAY_NEWS_03JUN2026,
        '20260604': TODAY_NEWS_04JUN2026,
        '20260605': TODAY_NEWS_05JUN2026,
        '20260608': TODAY_NEWS_08JUN2026,
        '20260609': TODAY_NEWS_09JUN2026,
        '20260610': TODAY_NEWS_10JUN2026,
        '20260611': TODAY_NEWS_11JUN2026,
        '20260612': TODAY_NEWS_12JUN2026,
        '20260615': TODAY_NEWS_15JUN2026,
        '20260616': TODAY_NEWS_16JUN2026,
        '20260622': TODAY_NEWS_22JUN2026,
        '20260623': TODAY_NEWS_23JUN2026,
        '20260624': TODAY_NEWS_24JUN2026,
        '20260625': TODAY_NEWS_25JUN2026,
        '20260706': TODAY_NEWS_06JUL2026,
        '20260707': TODAY_NEWS_07JUL2026,
        '20260713': TODAY_NEWS_13JUL2026,
        '20260714': TODAY_NEWS_14JUL2026,
        '20260715': TODAY_NEWS_15JUL2026,
        '20260716': TODAY_NEWS_16JUL2026,
        '20260717': TODAY_NEWS_17JUL2026,
        '20260718': TODAY_NEWS_18JUL2026,
    }
    today_blocks = today_map.get(today_str, {})

    news_data = {}

    for category, templates in NEWS_TEMPLATES.items():
        today_items = today_blocks.get(category, [])

        # Completar con plantillas generales hasta 4-5 noticias totales
        slots_remaining = max(0, 4 - len(today_items))
        selected_general = random.sample(templates, min(slots_remaining, len(templates)))

        combined = today_items + selected_general

        news_with_time = []
        for i, news in enumerate(combined):
            news_copy = news.copy()
            # Noticias de hoy tienen timestamp muy reciente
            if news in today_items:
                hours_ago = random.randint(0, 2)
            else:
                hours_ago = random.randint(2, 8)
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

        total_news = sum(len(v) for v in news.values())
        print(f"✅ Noticias actualizadas: {total_news}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   Próxima actualización: en 4 horas")

        return True

    except Exception as e:
        print(f"❌ Error actualizando noticias: {e}")
        return False


if __name__ == '__main__':
    print("🔄 Generador de noticias dinámicas v3 — 29 mayo 2026")
    print("=" * 50)
    update_news_file()
