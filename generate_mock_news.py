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
        {
            'title': 'India y Pakistán firman acuerdo de cese al fuego bajo mediación de ONU y EE.UU.',
            'summary': 'Tensión en la frontera de Cachemira cede tras semanas de enfrentamientos. Comunidad internacional celebra el acuerdo como alivio para estabilidad regional.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'G7 acuerda fondo de USD 50.000M para infraestructura en países en desarrollo como alternativa a BRICS',
            'summary': 'Naciones industrializadas lanzan iniciativa conjunta para financiar proyectos de energía limpia, puertos y carreteras en África y Asia.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'Taiwán refuerza defensa con nuevo escudo de misiles tras ejercicios militares chinos',
            'summary': 'Gobierno de Taipéi anuncia compra de sistemas antimisiles Patriot PAC-3 a EE.UU. por USD 3.500M en respuesta a maniobras del Ejército Popular de Liberación.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': 'EE.UU.-China: tregua arancelaria de 90 días entra en fase de implementación técnica',
            'summary': 'Equipos negociadores de Washington y Pekín acuerdan calendario de revisión de aranceles industriales. Reducción gradual afectará semiconductores, acero y productos agrícolas.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'Cumbre G20 en Johannesburgo aborda deuda soberana de países emergentes y financiamiento verde',
            'summary': 'Líderes del G20 discuten reestructuración coordinada de deudas para economías vulnerables y nuevas reglas de reporte climático para multilaterales.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'BRICS lanza moneda de reserva digital como alternativa al dólar para comercio entre miembros',
            'summary': 'Nuevo instrumento financiero respaldado por canasta de divisas y commodities busca reducir dependencia del dólar en transacciones intrabloques.',
            'source': 'The Economist',
            'link': 'https://www.economist.com'
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
        {
            'title': 'Dólar índice DXY cae a mínimos de dos años ante expectativas de recortes Fed en julio',
            'summary': 'Debilidad del billete verde favorece commodities y emergentes. Oro supera USD 3.300/oz mientras cobre y litio refuerzan alzas.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'Banco Mundial eleva proyección de crecimiento para América Latina a 2.8% en 2026',
            'summary': 'Mejora impulsada por mayores precios de materias primas y moderación de tasas en economías avanzadas. Chile y Perú lideran entre minero-exportadores.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
        {
            'title': 'Litio mantiene recuperación: carbonato supera USD 14.000/t ante nueva ola de demanda para baterías',
            'summary': 'Aceleración de ventas de vehículos eléctricos en China y Europa reactiva demanda. SQM y Albemarle ajustan planes de producción al alza.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/business/energy'
        },
        {
            'title': 'Fed pausa ciclo de tasas: mercados despejan 2 recortes posibles para segundo semestre 2026',
            'summary': 'Actas del FOMC confirman postura de espera. Inflación PCE en 2.3% despeja camino para recortes en septiembre y diciembre.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'Cobre alcanza USD 4.56/lb: déficit de oferta y demanda eléctrica global impulsan cotización',
            'summary': 'Inventarios en LME caen a mínimos históricos mientras proyectos de redes eléctricas en India y EE.UU. elevan consumo estructural.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': 'Dólar índice DXY en mínimos de 18 meses: emergentes y commodities se benefician de debilidad del billete verde',
            'summary': 'Expectativas de recorte Fed y déficit fiscal de EE.UU. presionan al dólar. Peso chileno, sol peruano y real brasileño registran apreciaciones significativas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
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
        {
            'title': 'Gobierno anuncia plan de inversión pública de USD 5.400M para 2026-2027 en infraestructura y energía',
            'summary': 'Cartera de proyectos contempla líneas de transmisión eléctrica, autopistas regionales y modernización de puertos. Concesiones privadas movilizarán recursos adicionales.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': 'Peso chileno se aprecia 3.2% en mayo apoyado por cobre y menor demanda de dólares',
            'summary': 'Fortaleza del metal rojo y pausa Fed reducen presión sobre tipo de cambio. Empresas exportadoras y BCCh monitorean nivel de $930.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Senado aprueba en general reforma tributaria que crea impuesto a ganancias de capital del 10%',
            'summary': 'Legislación avanza a segundo trámite. Medida impactará ganancias en bolsa, bienes raíces y fondos de inversión. Mercado reacciona con cautela.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Reforma de pensiones Chile: Senado aprueba artículo sobre fondo colectivo con 21 votos a favor',
            'summary': 'Votación histórica en Cámara Alta consolida el sistema mixto de pensiones. AFP deberán ceder 3% de cotización a fondo solidario intergeneracional.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com/politica'
        },
        {
            'title': 'Codelco inicia obras de modernización El Teniente: mayor proyecto de cobre subterráneo del mundo',
            'summary': 'Inversión de USD 2.800M permitirá extender vida útil hasta 2060 con producción de 400.000 t/año. Primer blast marcó inicio de construcción.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'IPSA supera los 7.250 puntos: sector minero y energético lideran alza en bolsa local',
            'summary': 'Índice bursátil chileno acumula retorno de 8.3% en 2026. Analistas proyectan rango 7.100-7.400 para el año ante precios del cobre y datos macro positivos.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
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
        {
            'title': 'Meta lanza Ray-Ban 3 con pantalla holográfica y asistente de IA integrado',
            'summary': 'Tercera generación de gafas inteligentes incluye proyección AR de baja latencia y reconocimiento facial en tiempo real. Precio: USD 499.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
        {
            'title': 'AMD lanza GPU Instinct MI400 para centros de datos desafiando dominio de Nvidia en IA',
            'summary': 'Nuevo acelerador ofrece 40% más TFLOPS por dólar versus H200. Microsoft Azure y Google Cloud anuncian integración inmediata.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'Ciberseguridad: brecha en proveedor cloud expone datos de 200 millones de usuarios en Europa',
            'summary': 'Incidente activa protocolos GDPR con notificaciones obligatorias. Reguladores europeos abren investigación y multas podrían superar EUR 800M.',
            'source': 'MIT Technology Review',
            'link': 'https://www.technologyreview.com'
        },
        {
            'title': 'Apple Intelligence llega a iOS 19: Siri reescrito con LLM propio y procesamiento 100% on-device',
            'summary': 'Nueva generación de IA de Apple integra razonamiento contextual sin enviar datos a la nube. Compatible con iPhone 16 y superiores desde junio 2026.',
            'source': 'The Verge',
            'link': 'https://www.theverge.com'
        },
        {
            'title': 'SpaceX Starship completa primer vuelo comercial: lleva satélites de NASA y ESA a órbita polar',
            'summary': 'Cohete más poderoso del mundo logra misión operacional tras cuatro años de pruebas. Abre nueva era de lanzamientos pesados a bajo costo.',
            'source': 'TechCrunch',
            'link': 'https://techcrunch.com'
        },
        {
            'title': 'Chips neuromórficos de Intel Loihi 3 reducen consumo energético de IA en 95%',
            'summary': 'Nueva arquitectura inspirada en el cerebro humano permite inferencia de modelos LLM en dispositivos edge sin GPU. Aplicaciones en robótica, IoT y salud.',
            'source': 'MIT Technology Review',
            'link': 'https://www.technologyreview.com'
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
        {
            'title': 'Coopeuch integra IA generativa en atención al socio con reducción del 60% en tiempos de consulta',
            'summary': 'Asistente virtual procesa solicitudes de crédito, ahorro y seguros en lenguaje natural. Proyecto piloto cubre 150.000 socios en fase 1.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'CONFECOOP lanza programa de educación financiera cooperativa para jóvenes de 18-30 años',
            'summary': 'Iniciativa busca incorporar 200.000 nuevos socios jóvenes al sistema cooperativo en dos años con talleres presenciales y plataforma digital.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'Informe BID: cooperativas latinoamericanas gestionan activos por USD 380.000M con crecimiento de 11% anual',
            'summary': 'Sector muestra resiliencia superior a banca tradicional en ciclos de estrés financiero. Chile destaca por solidez de Coopeuch y cobertura regional de cooperativas agrícolas.',
            'source': 'BID',
            'link': 'https://www.iadb.org'
        },
        {
            'title': 'Coopeuch lanza app renovada con pagos QR, inversiones y crédito digital integrados',
            'summary': 'Nueva plataforma móvil concentra todos los productos financieros cooperativos en una sola app. Más de 500.000 socios ya activos en versión beta.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'ACI Américas: cooperativas de ahorro latinoamericanas crecen 14% en socios activos durante 2025',
            'summary': 'Incorporación de jóvenes de 18-35 años lidera expansión. Chile, Colombia y México reportan mayor dinamismo en apertura de cuentas cooperativas digitales.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
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
        {
            'title': 'CMF lanza sandbox regulatorio para startups fintech con hasta 18 meses de operación supervisada',
            'summary': 'Marco experimental permite probar productos de crédito digital, pagos y gestión de inversiones con requisitos de capital reducidos y monitoreo mensual.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF exige a bancos y cooperativas divulgación de riesgos climáticos en reportes anuales desde 2027',
            'summary': 'Nueva norma alinea Chile con estándares TCFD y ISSB. Instituciones deben revelar exposición a riesgos físicos y de transición energética.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF autoriza primer fondo de inversión de activos tokenizados en blockchain pública en Chile',
            'summary': 'Administradora AGF emite participaciones tokenizadas bajo normativa aprobada en marzo. Instrumento permite fraccionar inversión en activos reales desde UF 10.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF publica consulta pública sobre regulación de stablecoins y criptoactivos en Chile',
            'summary': 'Regulador abre período de 60 días para recibir observaciones sobre marco legal para emisores de monedas estables y exchanges de criptoactivos.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF amplía requerimientos de capital para cooperativas con activos superiores a UF 1.000.000',
            'summary': 'Norma de Basilea adaptada exige índice de adecuación de capital mínimo de 10%. Cooperativas tienen plazo hasta diciembre 2026 para adecuarse.',
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
        {
            'title': 'Ventas del comercio minorista suben 4.2% en abril impulsadas por consumo de servicios y electrónica',
            'summary': 'INE destaca recuperación del gasto de hogares tras período de contracción. Tasas de interés más bajas dinamizan crédito de consumo.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Inversión extranjera directa en Chile supera USD 7.200M en primer cuatrimestre 2026',
            'summary': 'Cifra representa alza de 18% respecto a igual período 2025. Sectores minería, energías renovables y tecnología concentran el 74% de los flujos.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Banco Central proyecta crecimiento del PIB chileno entre 2.5% y 3.5% para 2026',
            'summary': 'IPoM de mayo eleva rango por mayor dinamismo de inversión privada y consumo. Riesgo principal sigue siendo deterioro de condiciones externas.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Encuesta de Expectativas Económicas BCCh: mercado anticipa dólar en $935 y TPM en 4.75% a fin de año',
            'summary': 'Consenso de analistas espera apreciación adicional del peso y dos recortes de 25 pb en TPM en el segundo semestre ante convergencia de inflación.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'INE publica IPP de abril: precios al productor suben 0.1% mensual, acumulan 2.9% en 12 meses',
            'summary': 'Moderación en precios mayoristas anticipa presiones inflacionarias contenidas en cadena de precios. Sectores agrícola e industrial registran menores alzas.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'ICARE: índice de confianza empresarial alcanza zona de expansión por primera vez desde 2024',
            'summary': 'Encuesta de mayo muestra 55.3 puntos, sobre umbral de 50. Ejecutivos destacan menor incertidumbre regulatoria y mejora de condiciones de crédito.',
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
        {
            'title': 'Google lanza Gemini Ultra 2 con ventana de contexto de 2 millones de tokens y razonamiento multimodal',
            'summary': 'Nuevo modelo lidera benchmarks de codificación y matemáticas. Integración nativa con Google Workspace permite analizar documentos empresariales completos.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Microsoft lanza Copilot Wave 3 con agentes autónomos para finanzas, RRHH y cadena de suministro',
            'summary': 'Tercera ola del asistente IA empresarial incorpora orquestación multi-agente. Demos muestran cierre automático de libros contables y gestión de órdenes de compra.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'AI Act UE: primeras auditorías a sistemas de IA de alto riesgo revelan brechas de compliance en banca',
            'summary': 'Reguladores europeos identifican 34 sistemas de scoring crediticio sin documentación técnica suficiente. Instituciones tienen 6 meses para remediar o suspender uso.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Anthropic Claude 4: nuevo modelo supera GPT-5 en benchmarks de razonamiento legal y financiero',
            'summary': 'Evaluaciones independientes muestran ventaja en análisis de contratos, modelado financiero y generación de código seguro. API disponible para empresas desde junio.',
            'source': "Ben's Bites",
            'link': 'https://bensbites.com'
        },
        {
            'title': 'OpenAI GPT-5 integra búsqueda web en tiempo real y memoria persistente cross-session',
            'summary': 'Nuevo modelo accede a información actualizada sin fechas de corte y recuerda contexto entre conversaciones. Precios API caen 40% respecto a GPT-4.',
            'source': 'TLDR AI',
            'link': 'https://tldr.ai'
        },
        {
            'title': 'Google Gemini Ultra 2 lidera benchmarks multimodales con ventana de 2M tokens y análisis de video',
            'summary': 'Modelo puede analizar contratos completos, estados financieros y presentaciones en minutos. Integración nativa en Google Workspace potencia productividad empresarial.',
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
