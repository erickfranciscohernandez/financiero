#!/usr/bin/env python3
"""
Generador de noticias mock dinámicas
Actualiza noticias_diarias.json con datos nuevos simulados
Para simular actualizaciones en tiempo real sin acceso a internet
"""
import json
from datetime import datetime, timedelta
import random

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
