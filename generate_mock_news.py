#!/usr/bin/env python3
"""
Generador de noticias mock dinámicas
Actualiza noticias_diarias.json con datos nuevos simulados
Para simular actualizaciones en tiempo real sin acceso a internet
"""
import json
from datetime import datetime, timedelta
import random

# Plantillas de noticias por categoría — actualizadas junio 2026 (v2)
NEWS_TEMPLATES = {
    'geopolitica': [
        {
            'title': 'EE.UU. y China acuerdan cumbre presidencial para formalizar acuerdo comercial fase 2',
            'summary': 'Trump y Xi acuerdan reunirse en Ginebra en julio para sellar segunda fase del acuerdo comercial. Aranceles industriales bajarían del 25% al 12% en sectores clave.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': 'Ucrania y Rusia acuerdan corredor humanitario permanente bajo supervisión de Cruz Roja',
            'summary': 'Negociación mediada por Turquía logra primer acuerdo operacional desde inicio del conflicto. Permite evacuación civil y envío de ayuda a zonas en disputa.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'OPEP+ extiende recortes de producción hasta diciembre de 2026 para defender precio del crudo',
            'summary': 'Arabia Saudita liderará reducción adicional de 500.000 bpd. Mercado petrolero proyecta Brent entre USD 72-80 para el segundo semestre.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/news'
        },
        {
            'title': 'Unión Europea anuncia sanciones a 47 entidades chinas por vulneración de propiedad intelectual',
            'summary': 'Medida es la más amplia adoptada por Bruselas contra Pekín. China amenaza con represalias arancelarias sobre automóviles y vinos europeos.',
            'source': 'The Economist',
            'link': 'https://www.economist.com'
        },
        {
            'title': 'Trump firma orden ejecutiva que restringe inversión china en semiconductores y energía nuclear de EE.UU.',
            'summary': 'Decreto refuerza revisión del CFIUS y suspende acuerdos pendientes por USD 12.000M. Sector tecnológico global ajusta cadenas de suministro.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'ONU adopta resolución histórica sobre gobernanza global de inteligencia artificial',
            'summary': 'Consejo de Seguridad aprueba por primera vez marco vinculante para uso de IA en sistemas de armas. 142 países firman compromiso de auditoría internacional.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com'
        },
        {
            'title': 'Irán firma acuerdo nuclear con potencias occidentales que limita enriquecimiento de uranio a 20%',
            'summary': 'Diplomacia de tres años culmina en Viena con reducción gradual de sanciones a cambio de inspecciones permanentes del OIEA. Israel mantiene reservas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'Cumbre ASEAN en Bangkok aprueba zona de libre comercio digital con reglas de datos transfronterizos',
            'summary': 'Bloque de 10 países del sudeste asiático establece primer marco regional para flujos de datos comerciales. Cubre USD 340.000M en comercio digital.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'Corea del Norte lanza misil de alcance intercontinental que sobrevuela Japón',
            'summary': 'Misil recorre 4.800 km antes de caer en el Océano Pacífico. EE.UU., Japón y Corea del Sur convocan consultas de emergencia y refuerzan ejercicios conjuntos.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/world'
        },
        {
            'title': 'Rusia congela activos de empresas europeas en represalia por nuevas sanciones del G7',
            'summary': 'Moscú retiene propiedades y participaciones de 180 compañías de Francia, Alemania y Polonia. Medida afecta USD 6.400M en inversiones previas al conflicto.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/politics'
        },
        {
            'title': 'Africa lanza moneda de reserva panafricana AFRO respaldada por oro y commodities',
            'summary': 'Unión Africana aprueba instrumento monetario regional en cumbre de Addis Abeba. Fase piloto cubre 12 países y USD 80.000M en intercambios comerciales intrarregionales.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/world'
        },
        {
            'title': 'G7 lanza iniciativa de cadenas de suministro críticas para reducir dependencia de China en minerales',
            'summary': 'Plan moviliza USD 70.000M en diez años para financiar minas de litio, cobalto y tierras raras en países aliados. Chile, Australia y Canadá son socios clave.',
            'source': 'The Economist',
            'link': 'https://www.economist.com'
        },
    ],
    'economia_global': [
        {
            'title': 'Cobre alcanza récord de USD 4.92/lb impulsado por déficit de oferta y demanda de transición energética',
            'summary': 'LME registra inventarios más bajos desde 2005. Analistas proyectan precio promedio de USD 5.10/lb para 2027 ante persistente brecha entre oferta y demanda estructural.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/commodities'
        },
        {
            'title': 'Fed anticipa primer recorte de tasas para septiembre con inflación PCE convergiendo al 2.1%',
            'summary': 'Actas del FOMC revelan consenso creciente para iniciar ciclo de relajación. Mercados asignan 78% de probabilidad a recorte de 25 pb en septiembre.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'FMI eleva proyección global a 3.4% para 2026: mayor optimismo en 4 años',
            'summary': 'India crece 7.1%, Vietnam 6.8% y EE.UU. 2.6%. FMI advierte que tensiones comerciales y deuda soberana siguen siendo riesgos principales.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
        {
            'title': 'Petróleo Brent repunta a USD 79 tras extensión de recortes OPEP+ hasta diciembre 2026',
            'summary': 'Arabia Saudita lidera restricción adicional de 500.000 bpd. Posición de inventarios globales cae a mínimos de tres años, reforzando perspectivas alcistas.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/business/energy'
        },
        {
            'title': 'BCE recorta tasas por tercera vez en 2026, la tasa de depósito queda en 2.25%',
            'summary': 'Christine Lagarde confirma normalización monetaria gradual. Euro cede frente al dólar pero Lagarde descarta recortes adicionales antes de septiembre.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'S&P 500 supera los 6.200 puntos: sector tecnológico y energético lideran rally',
            'summary': 'Bolsas de EE.UU. alcanzan nuevos máximos históricos impulsadas por resultados corporativos mejor a lo esperado y expectativas de recorte de la Fed en septiembre.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com/markets'
        },
        {
            'title': 'Oro supera USD 3.450/oz: bancos centrales emergentes aceleran compras para diversificar reservas',
            'summary': 'China, India y Turquía aumentan reservas de oro al ritmo más alto en 55 años. Analistas proyectan precio hacia USD 3.700/oz si Fed recorta en septiembre.',
            'source': 'Bloomberg',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'Banco Mundial: América Latina crecerá 3.1% en 2026, la mejor performance desde 2011',
            'summary': 'Impulso de commodities, inversión extranjera y consumo privado elevan perspectivas regionales. Chile, Brasil y Perú lideran entre exportadores de materias primas.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
        {
            'title': 'Litio carbonato supera USD 16.500/t: boom de vehículos eléctricos relanza ciclo alcista',
            'summary': 'China reporta ventas récord de 1.8M de vehículos eléctricos en mayo. SQM eleva guía de producción y proyecta ingresos de USD 3.200M para 2026.',
            'source': 'Reuters',
            'link': 'https://www.reuters.com/business/energy'
        },
        {
            'title': 'Déficit fiscal de EE.UU. alcanza USD 1.8 billones en 2026: deuda supera el 130% del PIB',
            'summary': 'CBO advierte que la trayectoria fiscal es insostenible sin ajuste. Rendimiento del bono T-10 trepa a 4.6%, presionando al alza el costo del crédito global.',
            'source': 'CNBC',
            'link': 'https://www.cnbc.com'
        },
        {
            'title': 'China lanza plan fiscal de USD 600.000M para estimular consumo interno y reactivar sector inmobiliario',
            'summary': 'Beijing inyecta recursos en subsidios al consumo, infraestructura urbana y rescate de desarrolladores. Analistas estiman impulso de 0.8 pp al PIB en 2026.',
            'source': 'Bloomberg Commodities',
            'link': 'https://www.bloomberg.com/markets'
        },
        {
            'title': 'Banco de Japón sube tasa de interés a 0.75%, mayor nivel desde 2008, ante presiones inflacionarias',
            'summary': 'BoJ confirma normalización monetaria gradual. Yen se aprecia frente al dólar por primera vez en tres años. Exportadores japoneses ajustan coberturas cambiarias.',
            'source': 'Financial Times',
            'link': 'https://www.ft.com/economics'
        },
    ],
    'economia_chile': [
        {
            'title': 'BCCh recorta TPM a 4.75% en señal de inicio de nuevo ciclo de relajación monetaria',
            'summary': 'Banco Central reduce tasa por primera vez desde 2024 ante convergencia de inflación al 3% y crecimiento sostenido. Próximo recorte proyectado para agosto.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Dólar cae a $928: máximo histórico de cobre y pausa Fed aprecian el peso chileno',
            'summary': 'Tipo de cambio alcanza mínimo en 18 meses. BCCh monitorea posible intervención si tendencia persiste. Exportadores incrementan liquidaciones de divisas.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Codelco supera producción trimestral: 430.000 toneladas en Q1 2026, récord en seis años',
            'summary': 'Corporación estatal eleva guía anual a 1.65 millones de toneladas. División El Teniente y Chuquicamata lideran incremento. Resultado fortalece posición fiscal.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'IPSA alcanza récord histórico de 7.480 puntos: minería, retail y banca lideran alza',
            'summary': 'Bolsa de Santiago registra mejor semestre desde 2010. Flujos extranjeros ingresan USD 1.200M. Analistas elevan proyección al rango 7.500-7.800 para el año.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': 'Ley de pensiones promulgada: sistema mixto con 3% a fondo solidario entrará en vigencia en enero 2027',
            'summary': 'Presidente Boric promulga reforma histórica tras tres años de tramitación. Nuevas pensiones promediarán CLP 320.000 adicionales según proyecciones del Ministerio.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com/politica'
        },
        {
            'title': 'IPC de mayo sube apenas 0.1% mensual y acumula 3.4% anual, mínimo en dos años',
            'summary': 'INE confirma desaceleración inflacionaria. Caída en precios de combustibles y alimentos frescos modera el indicador. BCCh tiene margen para nuevos recortes.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Gobierno lanza Ley de Datos Personales y activa regulación de IA en el sector financiero',
            'summary': 'Legislación moderniza marco de privacidad y establece primera normativa nacional para sistemas algorítmicos de crédito y seguros. Entidades tienen 18 meses para adecuarse.',
            'source': 'La Tercera',
            'link': 'https://www.latercera.com'
        },
        {
            'title': 'SQM eleva producción de litio a 220.000 toneladas anuales con nueva planta en el Salar de Atacama',
            'summary': 'Compañía inaugura instalación que eleva capacidad en 40%. Acuerdo con el Estado asegura royalty creciente vinculado al precio del carbonato de litio.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'PIB chileno crece 3.8% en primer trimestre 2026, el mejor dato desde 2021',
            'summary': 'Banco Central confirma expansión impulsada por minería, construcción y servicios. Consumo privado sube 4.1% interanual apoyado por menor inflación y empleo estable.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Ministerio de Hacienda proyecta superávit fiscal de 0.4% del PIB para 2026 gracias a cobre y litio',
            'summary': 'Mejora en balance estructural permite financiar Plan de Inversión en Infraestructura y mantener holgura para eventualidades macroeconómicas.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Aeropuerto de Santiago inaugura terminal ampliada con capacidad para 30 millones de pasajeros anuales',
            'summary': 'Concesionaria Nuevo Pudahuel entrega obra que duplica la superficie actual. Inversión de USD 920M mejora conectividad y posiciona al país como hub regional.',
            'source': 'EMOL',
            'link': 'https://www.emol.com'
        },
        {
            'title': 'Tasa de desempleo baja a 7.2% en trimestre febrero-abril 2026: mejor dato en cuatro años',
            'summary': 'INE registra 180.000 nuevos empleos formales. Sector servicios, construcción y comercio lideran creación de puestos. Brecha de género en empleo cae al 10.3%.',
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
            'title': 'Sector cooperativo de ahorro en Chile mantiene tendencia de crecimiento sostenido en 2026',
            'summary': 'El cooperativismo financiero chileno continúa ganando participación de mercado frente a la banca tradicional, impulsado por menores tasas y mayor cercanía con socios en regiones.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'Cooperativas chilenas aceleran transformación digital para competir con la banca en productos hipotecarios',
            'summary': 'El sector avanza en digitalización de procesos de crédito inmobiliario. La reducción de tiempos de aprobación y la mejora en experiencia de usuario son las principales apuestas.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Análisis: cooperativas de ahorro en Chile ante el desafío de escalar sin perder el modelo solidario',
            'summary': 'Expertos debaten cómo el cooperativismo financiero puede crecer en activos y cobertura geográfica manteniendo su identidad democrática y los beneficios para sus socios.',
            'source': 'El Mostrador',
            'link': 'https://www.elmostrador.cl'
        },
        {
            'title': 'Cooperativas agrícolas del sur de Chile apuestan por la exportación directa para mejorar márgenes',
            'summary': 'El modelo cooperativo permite a pequeños agricultores acceder a mercados de exportación en Asia y Europa que individualmente serían inalcanzables.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
        },
        {
            'title': 'BID destaca al cooperativismo latinoamericano como motor de inclusión financiera rural en 2026',
            'summary': 'Organismo multilateral resalta el rol de las cooperativas en llevar servicios financieros formales a comunidades alejadas de la banca comercial tradicional.',
            'source': 'BID',
            'link': 'https://www.iadb.org'
        },
        {
            'title': 'Cooperativas de vivienda ganan terreno en segmento de clase media ante altas tasas hipotecarias bancarias',
            'summary': 'El modelo de ahorro previo cooperativo se posiciona como alternativa viable al crédito hipotecario convencional en un contexto de tasas aún elevadas.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
        {
            'title': 'Jóvenes chilenos entre 18 y 30 años lideran apertura de cuentas en cooperativas de ahorro',
            'summary': 'La generación Z valora la propiedad colectiva y las tasas competitivas del sector cooperativo. Las apps móviles han sido clave para acercar el modelo a nuevos socios.',
            'source': 'Cooperativas.cl',
            'link': 'https://www.cooperativas.cl'
        },
        {
            'title': 'Informe BID: cooperativismo latinoamericano muestra mayor resiliencia que banca tradicional ante ciclos de estrés',
            'summary': 'Análisis comparativo concluye que las cooperativas financieras mantienen menores índices de morosidad y mayor retención de socios durante períodos de contracción económica.',
            'source': 'BID',
            'link': 'https://www.iadb.org'
        },
        {
            'title': 'ACI Américas: cooperativas de ahorro latinoamericanas crecen sostenidamente en socios activos',
            'summary': 'Chile, Colombia y México lideran la incorporación de nuevos socios al sistema cooperativo financiero, con foco en digitalización y productos de bajo costo.',
            'source': 'ACI Américas',
            'link': 'https://www.aciamericas.coop'
        },
        {
            'title': 'Tecnología e inteligencia artificial: nuevos aliados del sector cooperativo para mejorar evaluación crediticia',
            'summary': 'Las cooperativas de ahorro comienzan a adoptar modelos de scoring con IA que permiten evaluar perfiles de riesgo con mayor precisión y en menor tiempo que los métodos tradicionales.',
            'source': 'Diario Financiero',
            'link': 'https://www.df.cl'
        },
    ],
    'cmf': [
        {
            'title': 'CMF avanza en nuevos estándares de resiliencia operacional para el sistema financiero chileno',
            'summary': 'El regulador trabaja en normativas que exigirán mayor robustez ante ciberataques y fallas sistémicas. El sector financiero evalúa inversiones en continuidad operacional.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF fortalece fiscalización del mercado de valores con foco en conflictos de interés y transparencia',
            'summary': 'El regulador intensifica la supervisión de administradoras de fondos y corredoras de bolsa, priorizando la protección de inversionistas minoristas y la integridad del mercado.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF avanza en reglamentación del equity crowdfunding bajo la Ley Fintech para Pymes chilenas',
            'summary': 'El marco regulatorio para plataformas de financiamiento colectivo busca ampliar el acceso de pequeñas empresas a capital sin pasar por la banca tradicional.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF lanza portal de datos abiertos con información consolidada del sistema financiero chileno',
            'summary': 'Plataforma Open Data publica en tiempo real indicadores de bancos, cooperativas, compañías de seguros y fondos de inversión. Integra API pública para desarrolladores.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF reporta caída de morosidad bancaria a 1.8%: sistema financiero en mejor posición desde 2019',
            'summary': 'Índice de cartera vencida sobre colocaciones totales alcanza mínimo histórico. Capital de nivel 1 promedio supera 13.5% en todos los bancos supervisados.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF emite circular que obliga a publicar tasas efectivas en créditos de consumo en formato estándar',
            'summary': 'Medida de transparencia exige a bancos, cooperativas y Fintechs mostrar CAE y costo total en todas las cotizaciones. Entrará en vigor el 1 de septiembre de 2026.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF regula uso de IA en modelos de scoring crediticio: obliga a explicabilidad y auditoría externa',
            'summary': 'Nueva circular exige que algoritmos de crédito cumplan principios de transparencia, imparcialidad y derecho a explicación. Plazo de adecuación: 12 meses.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF y BCCh publican informe conjunto sobre riesgos sistémicos del mercado de criptoactivos en Chile',
            'summary': 'Documento identifica tres exchanges con concentración sistémica y propone regulación de reservas mínimas para emisores de stablecoins vinculados al peso chileno.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF actualiza tabla de tasas máximas convencionales: rebaja tope para créditos de consumo en junio 2026',
            'summary': 'Tasa máxima convencional para créditos entre UF 200 y UF 5.000 baja de 41.2% a 38.7% anual. Medida beneficia a 2.3 millones de deudores de consumo.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
        {
            'title': 'CMF autoriza inicio de operaciones de cuatro nuevas cooperativas de ahorro y crédito en regiones',
            'summary': 'Resoluciones habilitantes cubren cooperativas en Atacama, Aysén, Los Lagos y Maule, ampliando acceso a crédito formal en zonas con baja cobertura bancaria.',
            'source': 'CMF Chile',
            'link': 'https://www.cmfchile.cl'
        },
    ],
    'noticias_economicas_actuales': [
        {
            'title': 'IPC de mayo 2026 registra 0.1% mensual: inflación cae a 3.4% anual, mínimo desde diciembre 2021',
            'summary': 'INE confirma desaceleración sostenida. Combustibles caen 1.2% y alimentos frescos bajan 0.3%. Resultado fortalece expectativas de recorte de TPM en agosto.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Desempleo baja a 7.2% en trimestre febrero-abril 2026: mejor dato desde el segundo trimestre de 2022',
            'summary': 'INE registra 180.000 nuevos empleos formales. Construcción, servicios financieros y tecnología lideran contratación. Empleo femenino sube al 46.8% de la fuerza laboral.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'Imacec de abril 2026 anota 4.1% de crecimiento interanual, superando todas las estimaciones',
            'summary': 'Banco Central destaca dinamismo simultáneo en minería, comercio y manufactura. Es el cuarto mes consecutivo sobre el 3.5%, consolidando tendencia de expansión.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Exportaciones chilenas acumulan superávit de USD 4.800M en enero-mayo 2026',
            'summary': 'Cobre, litio y fruta fresca lideran ingresos por USD 26.300M. China mantiene 41% de participación. Balanza energética mejora por menor precio del petróleo importado.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'ICARE: confianza empresarial sube a 57.8 puntos en junio, el nivel más alto desde el primer trimestre de 2022',
            'summary': 'Encuesta mensual refleja menor incertidumbre regulatoria, optimismo por datos macro y expectativa de recorte de TPM. Inversión privada se reactiva en manufacturas y retail.',
            'source': 'ICARE',
            'link': 'https://www.icare.cl'
        },
        {
            'title': 'Ventas minoristas crecen 5.8% en mayo: electrodomésticos, vestuario y restaurantes lideran alza',
            'summary': 'INE registra el mejor dato de ventas del comercio en 18 meses. Mayor empleo y menor inflación dinamizan consumo de hogares. Crédito de consumo creció 6.3% interanual.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'IED en Chile supera USD 9.600M en primer semestre 2026: minería limpia y centros de datos lideran inversión',
            'summary': 'CORFO reporta cifra histórica. Proyectos de hidrógeno verde, plantas solares y data centers concentran el 56% del total. Regiones de Antofagasta y Atacama atraen mayor inversión.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Banco Central eleva rango de crecimiento del PIB 2026 a 3.5%-4.0% en IPoM de junio',
            'summary': 'Revisión al alza respaldada por mayor dinamismo de inversión, consumo y exportaciones. BCCh advierte que deterioro del entorno externo sigue siendo riesgo principal.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'Encuesta BCCh: mercado anticipa dólar en $910 y TPM en 4.25% al cierre de 2026',
            'summary': 'Consenso de analistas ajusta proyecciones ante recorte ya realizado y mejores datos macro. Tres recortes adicionales de 25 pb son el escenario base para el segundo semestre.',
            'source': 'Banco Central de Chile',
            'link': 'https://www.bcentral.cl'
        },
        {
            'title': 'INE publica IPP de mayo: precios al productor caen 0.3% mensual, acumulan solo 1.8% en 12 meses',
            'summary': 'Reducción en precios de insumos industriales anticipa menor presión inflacionaria aguas abajo. Sectores agrícola, minero e industrial registran contracción de costos.',
            'source': 'INE',
            'link': 'https://www.ine.gob.cl'
        },
        {
            'title': 'PIB primer trimestre 2026 confirmado en 3.8%: el mayor crecimiento trimestral en cinco años',
            'summary': 'Revisión final del BCCh confirma expansión récord. Consumo privado (+4.1%), inversión fija (+6.2%) y exportaciones (+8.9%) fueron los motores del crecimiento.',
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
