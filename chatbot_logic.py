import nltk
import spacy

# Importar módulos personalizados
try:
    from sentiment_analyzer import get_sentiment_analyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False
    print("⚠️ Módulo de sentimientos no disponible")

try:
    from llm_module import get_gemma_llm
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("⚠️ Módulo LLM no disponible")

try:
    from config import SENTIMENT_CONFIG, LLM_CONFIG, CHATBOT_CONFIG
except ImportError:
    # Configuración por defecto si no existe config.py
    SENTIMENT_CONFIG = {'enabled': True, 'min_confidence': 0.6, 'adapt_tone': True}
    LLM_CONFIG = {'enabled': False, 'use_for_enhancement': False}
    CHATBOT_CONFIG = {'nombre': 'SciTech Bot', 'version': '3.0'}

# Descargar recursos de NLTK si es necesario
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

nlp = spacy.load("es_core_news_sm")

# Inicializar analizador de sentimientos si está disponible
sentiment_analyzer = None
if SENTIMENT_AVAILABLE and SENTIMENT_CONFIG.get('enabled', False):
    sentiment_analyzer = get_sentiment_analyzer()
    print("✅ Análisis de sentimientos activado")

# Inicializar LLM si está disponible (sin cargar el modelo aún)
llm_model = None
if LLM_AVAILABLE and LLM_CONFIG.get('enabled', False):
    llm_model = get_gemma_llm(auto_load=LLM_CONFIG.get('auto_load', False))
    print("✅ Módulo LLM disponible")

def obtener_tokens(texto):
    """Tokeniza el texto usando NLTK."""
    return nltk.word_tokenize(texto.lower())

def analizar_texto(texto):
    """
    Devuelve una lista de diccionarios con análisis lingüístico:
    palabra, lema, POS, etiqueta y dependencia.
    """
    doc = nlp(texto)
    resultado = []
    for token in doc:
        info_token = {
            'texto': token.text,
            'lema': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dependencia': token.dep_
        }
        resultado.append(info_token)
    return resultado

def validar_mensaje(mensaje):
    """
    Valida que el mensaje sea apropiado y no vacío.
    Retorna (es_valido, mensaje_error)
    """
    if not mensaje or mensaje.strip() == "":
        return False, "Por favor, escribe un mensaje para poder ayudarte."
    
    if len(mensaje.strip()) < 2:
        return False, "Tu mensaje es muy corto. ¿Podrías ser más específico?"
    
    # Detectar spam (mismo caracter repetido muchas veces)
    if len(set(mensaje.replace(" ", ""))) <= 2 and len(mensaje) > 5:
        return False, "Mensaje no válido. ¿Qué tema de ciencia o tecnología te interesa?"
    
    # Detectar solo números
    if mensaje.strip().isdigit():
        return False, "Parece que escribiste solo números. Pregúntame sobre algún tema científico o tecnológico."
    
    return True, ""

def obtener_categoria_tema(tokens):
    """
    Identifica la categoría del tema basado en los tokens.
    Retorna: categoria (str) o None
    """
    categorias = {
        "ia": ["inteligencia", "artificial", "ia", "ai", "machine", "learning", "chatgpt", "gpt", "robot", "automatización", "algoritmo"],
        "espacio": ["espacio", "nasa", "astronomía", "planeta", "marte", "luna", "telescopio", "james webb", "webb", "estrella", "galaxia", "spacex"],
        "computacion": ["cuántica", "quantum", "computación", "ordenador", "procesador", "chip", "semiconductor", "hardware"],
        "medicina": ["medicina", "salud", "cáncer", "enfermedad", "vacuna", "crispr", "genética", "adn", "gen", "terapia"],
        "energia": ["energía", "renovable", "solar", "eólica", "fusión", "nuclear", "batería", "clima", "carbono"],
        "blockchain": ["blockchain", "bitcoin", "criptomoneda", "crypto", "ethereum", "nft", "web3", "metaverso", "realidad", "virtual", "vr", "ar"]
    }
    
    for categoria, palabras_clave in categorias.items():
        if any(palabra in tokens for palabra in palabras_clave):
            return categoria
    
    return None

def procesar_respuesta(respuesta_base, sentimiento_data=None, usar_llm=False):
    """
    Procesa y mejora una respuesta base agregando empatía y usando LLM si está disponible.
    
    Args:
        respuesta_base (str): Respuesta original
        sentimiento_data (dict): Datos del análisis de sentimiento
        usar_llm (bool): Si usar LLM para mejorar la respuesta
        
    Returns:
        str: Respuesta procesada
    """
    respuesta_final = respuesta_base
    
    # Agregar mensaje empático si corresponde
    if sentimiento_data and sentiment_analyzer and SENTIMENT_CONFIG.get('adapt_tone', True):
        mensaje_emp = sentiment_analyzer.generar_mensaje_empatico(sentimiento_data)
        if mensaje_emp:
            respuesta_final = mensaje_emp + respuesta_final
    
    # Mejorar con LLM si está disponible y habilitado
    if usar_llm and llm_model and llm_model.enabled and LLM_CONFIG.get('use_for_enhancement', False):
        try:
            sentimiento_usuario = sentimiento_data['sentimiento'] if sentimiento_data else 'NEU'
            respuesta_mejorada = llm_model.mejorar_respuesta(respuesta_final, sentimiento_usuario)
            if respuesta_mejorada:
                respuesta_final = respuesta_mejorada
        except Exception as e:
            print(f"Error al mejorar con LLM: {e}")
    
    return respuesta_final

def responder(mensaje, estado):
    """
    Lógica conversacional del chatbot sobre ciencia y tecnología.
    Incluye validación, contexto, análisis de sentimientos y guía inteligente.
    """
    # Validar mensaje
    es_valido, mensaje_error = validar_mensaje(mensaje)
    if not es_valido:
        return mensaje_error
    
    tokens = obtener_tokens(mensaje)
    respuesta = ""
    
    # Inicializar contexto si no existe
    if 'ultimo_tema' not in estado:
        estado['ultimo_tema'] = None
    if 'temas_discutidos' not in estado:
        estado['temas_discutidos'] = []
    if 'analisis_sentimiento' not in estado:
        estado['analisis_sentimiento'] = None
    
    # === ANÁLISIS DE SENTIMIENTOS ===
    sentimiento_data = None
    mensaje_empatico = ""
    
    if sentiment_analyzer and SENTIMENT_CONFIG.get('enabled', False):
        try:
            sentimiento_data = sentiment_analyzer.analyze(mensaje)
            estado['analisis_sentimiento'] = sentimiento_data
            
            # Generar mensaje empático si es necesario
            if SENTIMENT_CONFIG.get('adapt_tone', True):
                mensaje_emp = sentiment_analyzer.generar_mensaje_empatico(sentimiento_data)
                if mensaje_emp:
                    mensaje_empatico = mensaje_emp
        except Exception as e:
            print(f"Error en análisis de sentimientos: {e}")

    # Saludo inicial obligatorio
    if not estado['saludo']:
        if any(palabra in tokens for palabra in ["hola", "buenas", "saludos", "hey", "holi", "buenos", "dias", "tardes", "noches"]):
            estado['saludo'] = True
            
            # Adaptar saludo según sentimiento
            saludo_base = "¡Hola! 👋 Bienvenido al chatbot de ciencia y tecnología.\n\n"
            
            if mensaje_empatico and sentimiento_data:
                saludo_base = mensaje_empatico + saludo_base
            
            respuesta = (
                saludo_base +
                "Puedo ayudarte con información sobre:\n"
                "🤖 Inteligencia Artificial\n"
                "🚀 Exploración Espacial\n"
                "💻 Computación Cuántica\n"
                "🧬 Medicina y Genética\n"
                "⚡ Energías Renovables\n"
                "🔗 Blockchain y Web3\n\n"
                "¿Sobre qué tema te gustaría saber más?"
            )
        else:
            respuesta = "¡Hola! 👋 Para comenzar, salúdame y te mostraré cómo puedo ayudarte a explorar el mundo de la ciencia y tecnología."
        return respuesta

    # Despedida
    if any(palabra in tokens for palabra in ["adios", "chao", "hasta luego", "nos vemos", "bye", "adió"]):
        if estado['temas_discutidos']:
            temas = ", ".join(set(estado['temas_discutidos']))
            respuesta = f"¡Adiós! 👋 Me alegró conversar contigo sobre {temas}. Espero que hayas aprendido algo nuevo. ¡Hasta pronto!"
        else:
            respuesta = "¡Adiós! 👋 Espero verte pronto para conversar sobre ciencia y tecnología. ¡Hasta luego!"
        estado['saludo'] = False
        estado['ultimo_tema'] = None
        estado['temas_discutidos'] = []
        return respuesta

    # Estado de ánimo con sugerencias contextuales
    if any(palabra in tokens for palabra in ["bien", "feliz", "excelente", "contento", "alegre", "genial", "perfecto"]):
        respuesta = "¡Me alegra que estés bien! 😊 ¿Te gustaría conocer alguna noticia científica fascinante o explorar algún avance tecnológico reciente?"
        return respuesta
    
    if any(palabra in tokens for palabra in ["mal", "triste", "regular", "cansado", "aburrido"]):
        respuesta = (
            "Lamento que no estés en tu mejor momento. 💙 Quizás un descubrimiento fascinante te anime.\n"
            "¿Te interesaría saber sobre:\n"
            "• Los últimos descubrimientos del James Webb 🔭\n"
            "• Avances en inteligencia artificial 🤖\n"
            "• Nuevas terapias médicas revolucionarias 💊"
        )
        return respuesta
    
    # Agradecimiento
    if any(palabra in tokens for palabra in ["gracias", "gracia", "thank", "agradezco"]):
        if estado['ultimo_tema']:
            respuesta = f"¡De nada! 😊 Me alegra ayudarte con {estado['ultimo_tema']}. ¿Hay otro tema que te gustaría explorar?"
        else:
            respuesta = "¡De nada! 😊 Estoy aquí para ayudarte. ¿Qué tema de ciencia o tecnología te interesa?"
        return respuesta
    
    # Preguntas sobre el bot
    if any(palabra in tokens for palabra in ["quién", "quien", "eres", "qué eres", "que eres", "tu nombre"]):
        respuesta = (
            "Soy un chatbot especializado en ciencia y tecnología 🤖. Mi propósito es compartir información "
            "sobre los últimos avances científicos, innovaciones tecnológicas y descubrimientos fascinantes. "
            "¿Sobre qué tema te gustaría aprender hoy?"
        )
        return respuesta
    
    # Ayuda
    if any(palabra in tokens for palabra in ["ayuda", "help", "como funciona", "qué puedes", "que puedes"]):
        respuesta = (
            "¡Claro! Puedo ayudarte con estos temas:\n\n"
            "🤖 **IA**: Pregunta sobre ChatGPT, robots, machine learning\n"
            "🚀 **Espacio**: NASA, James Webb, Marte, SpaceX\n"
            "💻 **Computación**: Computación cuántica, hardware\n"
            "🧬 **Medicina**: CRISPR, terapias génicas, tratamientos\n"
            "⚡ **Energía**: Fusión nuclear, renovables, baterías\n"
            "🔗 **Blockchain**: Criptomonedas, NFT, Web3\n\n"
            "Simplemente pregúntame sobre cualquiera de estos temas o pide 'recomendaciones' de noticias."
        )
        return respuesta

    # Identificar categoría del tema
    categoria_actual = obtener_categoria_tema(tokens)
    if categoria_actual:
        estado['ultimo_tema'] = categoria_actual
        if categoria_actual not in estado['temas_discutidos']:
            estado['temas_discutidos'].append(categoria_actual)

    # Temas de ciencia y tecnología
    if any(palabra in tokens for palabra in [
        "inteligencia", "artificial", "ia", "ai", "machine", "learning", "aprendizaje", "automático", "chatgpt", "gpt", 
        "neural", "robot", "automatización", "deep", "modelo", "algoritmo", "datos", "big data"
    ]):
        estado['ultimo_tema'] = "Inteligencia Artificial"
        if "chatgpt" in tokens or "gpt" in tokens:
            respuesta = (
                "**ChatGPT y GPT** 🤖\n\n"
                "Son modelos de lenguaje desarrollados por OpenAI que revolucionaron la IA conversacional. "
                "Estos sistemas utilizan redes neuronales transformers con miles de millones de parámetros. En 2024-2025, "
                "GPT-4 y sus sucesores han mostrado capacidades impresionantes en razonamiento, creatividad y programación.\n\n"
                "¿Te gustaría saber sobre otros modelos de IA, aplicaciones prácticas o el futuro de la IA?"
            )
        elif "robot" in tokens or "automatización" in tokens:
            respuesta = (
                "**Robótica y Automatización** 🦾\n\n"
                "La robótica avanza rápidamente: robots humanoides como Optimus de Tesla, robots quirúrgicos de precisión, "
                "drones autónomos y robots industriales colaborativos (cobots). La automatización está transformando "
                "manufactura, logística, medicina y exploración espacial.\n\n"
                "¿Quieres profundizar en robots humanoides, médicos o industriales?"
            )
        else:
            respuesta = (
                "**Inteligencia Artificial** 🧠\n\n"
                "La IA está revolucionando el mundo. Destacan: modelos de lenguaje como GPT-4 y Claude, "
                "sistemas de generación de imágenes (DALL-E, Midjourney, Stable Diffusion), IA en medicina para diagnóstico, "
                "vehículos autónomos, y asistentes virtuales avanzados.\n\n"
                "¿Qué aspecto específico te interesa? (modelos de lenguaje, robótica, IA en medicina, etc.)"
            )
        return respuesta

    if any(palabra in tokens for palabra in [
        "espacio", "nasa", "astronomía", "planeta", "marte", "luna", "telescopio", "james webb", "webb", 
        "estrella", "galaxia", "universo", "spacex", "cohete", "satélite", "agujero negro", "exoplaneta"
    ]):
        estado['ultimo_tema'] = "Exploración Espacial"
        if "james webb" in tokens or "webb" in tokens:
            respuesta = (
                "**Telescopio Espacial James Webb** 🔭\n\n"
                "El James Webb ha revolucionado la astronomía con imágenes sin precedentes del universo. "
                "Ha capturado galaxias primitivas, exoplanetas con atmósferas, nebulosas espectaculares y ha ayudado a "
                "entender la formación estelar y planetaria con un detalle nunca antes visto.\n\n"
                "¿Te gustaría saber sobre sus últimos descubrimientos o compararlo con el Hubble?"
            )
        elif "marte" in tokens:
            respuesta = (
                "**Exploración de Marte** 🔴\n\n"
                "La exploración de Marte avanza: los rovers Perseverance y Curiosity continúan investigando el planeta rojo, "
                "buscando signos de vida antigua. SpaceX planea misiones tripuladas para establecer una colonia marciana. "
                "Se han encontrado evidencias de agua líquida antigua y compuestos orgánicos complejos.\n\n"
                "¿Quieres saber más sobre los rovers, las misiones tripuladas o la búsqueda de vida?"
            )
        elif "spacex" in tokens or "cohete" in tokens:
            respuesta = (
                "**SpaceX y Cohetes Reutilizables** 🚀\n\n"
                "SpaceX lidera la innovación espacial con sus cohetes reutilizables Falcon 9 y el revolucionario Starship. "
                "Han lanzado miles de satélites Starlink, llevado astronautas a la ISS y planean misiones a la Luna y Marte. "
                "La reutilización de cohetes ha reducido dramáticamente los costos de acceso al espacio.\n\n"
                "¿Te interesa el Starship, Starlink o las misiones lunares Artemis?"
            )
        else:
            respuesta = (
                "**Astronomía y Exploración Espacial** 🌌\n\n"
                "La astronomía y exploración espacial viven una era dorada: el James Webb revela el universo primitivo, "
                "se descubren exoplanetas potencialmente habitables, agujeros negros supermasivos, y misiones a asteroides "
                "y lunas heladas buscan vida.\n\n"
                "¿Qué tema espacial te fascina más? (telescopios, planetas, misiones, exoplanetas)"
            )
        return respuesta

    if any(palabra in tokens for palabra in [
        "cuántica", "quantum", "computación", "ordenador", "supercomputadora", "procesador", "chip", 
        "semiconductor", "transistor", "informática", "hardware"
    ]):
        estado['ultimo_tema'] = "Computación"
        if "cuántica" in tokens or "quantum" in tokens:
            respuesta = (
                "**Computación Cuántica** ⚛️\n\n"
                "La computación cuántica promete revolucionar el procesamiento: empresas como IBM, Google, Microsoft y startups "
                "desarrollan qubits cada vez más estables. Google alcanzó la 'supremacía cuántica' con su procesador Sycamore. "
                "Aplicaciones futuras incluyen criptografía, diseño de fármacos, optimización y simulación molecular avanzada.\n\n"
                "¿Te gustaría entender cómo funcionan los qubits o conocer aplicaciones prácticas?"
            )
        else:
            respuesta = (
                "**Avances en Hardware** 💻\n\n"
                "Los avances en hardware son impresionantes: chips con arquitectura de 3nm, procesadores con IA integrada, "
                "memoria cuántica, fotónica para comunicaciones ultra-rápidas, y neuromorphic chips que imitan el cerebro humano. "
                "La Ley de Moore continúa desafiándose con nuevas tecnologías.\n\n"
                "¿Quieres profundizar en procesadores de IA, chips cuánticos o tecnologías emergentes?"
            )
        return respuesta

    if any(palabra in tokens for palabra in [
        "medicina", "salud", "cáncer", "enfermedad", "vacuna", "crispr", "genética", "adn", "gen", 
        "terapia", "farmaco", "tratamiento", "diagnóstico", "biomedicina", "célula"
    ]):
        estado['ultimo_tema'] = "Medicina y Biotecnología"
        if "crispr" in tokens or "genética" in tokens or "adn" in tokens or "gen" in tokens:
            respuesta = (
                "**CRISPR y Edición Genética** 🧬\n\n"
                "CRISPR-Cas9 revoluciona la edición genética: permite corregir mutaciones causantes de enfermedades, "
                "desarrollar cultivos resistentes y crear terapias personalizadas. En 2024-2025, terapias génicas aprobadas "
                "tratan anemia falciforme, distrofia muscular y ceguera hereditaria. La medicina de precisión es una realidad.\n\n"
                "¿Te interesa conocer tratamientos específicos, la ética de CRISPR o aplicaciones en agricultura?"
            )
        elif "cáncer" in tokens:
            respuesta = (
                "**Avances contra el Cáncer** 💊\n\n"
                "La lucha contra el cáncer avanza: inmunoterapias como CAR-T cells, vacunas personalizadas contra tumores, "
                "terapias dirigidas con inteligencia artificial, y detección temprana mediante biopsias líquidas. Los tratamientos "
                "son cada vez más precisos, efectivos y con menos efectos secundarios.\n\n"
                "¿Quieres saber más sobre inmunoterapias, vacunas personalizadas o métodos de detección temprana?"
            )
        else:
            respuesta = (
                "**Biomedicina y Avances Médicos** 🏥\n\n"
                "La biomedicina progresa aceleradamente: terapias génicas, medicina regenerativa con células madre, "
                "órganos bioartificiales, diagnóstico con IA, nanomedicina para entrega dirigida de fármacos, "
                "y vacunas de ARNm adaptables.\n\n"
                "¿Qué avance médico te interesa explorar? (terapias génicas, células madre, IA médica)"
            )
        return respuesta

    if any(palabra in tokens for palabra in [
        "energía", "renovable", "solar", "eólica", "fusión", "nuclear", "batería", "electricidad", 
        "sostenible", "clima", "carbono", "emisiones", "calentamiento", "ambiental"
    ]):
        estado['ultimo_tema'] = "Energía y Clima"
        if "fusión" in tokens or "nuclear" in tokens:
            respuesta = (
                "**Fusión Nuclear** ⚡\n\n"
                "La fusión nuclear es el santo grial energético: en 2022, el NIF logró ganancia neta de energía por primera vez. "
                "Proyectos como ITER en Francia y startups como Commonwealth Fusion Systems buscan comercializar fusión para 2030s. "
                "Promete energía limpia, segura e ilimitada sin residuos radiactivos de larga duración.\n\n"
                "¿Quieres entender cómo funciona la fusión o conocer proyectos actuales como ITER?"
            )
        elif "batería" in tokens:
            respuesta = (
                "**Tecnología de Baterías** 🔋\n\n"
                "Las baterías evolucionan: baterías de estado sólido con mayor densidad energética, baterías de sodio más baratas, "
                "supercondensadores de grafeno, y sistemas de almacenamiento a escala de red. Tesla, CATL y otras empresas "
                "impulsan la revolución del almacenamiento energético para vehículos eléctricos y redes eléctricas.\n\n"
                "¿Te interesa las baterías de estado sólido, almacenamiento en red o vehículos eléctricos?"
            )
        else:
            respuesta = (
                "**Energías Renovables y Clima** 🌱\n\n"
                "Las energías renovables crecen exponencialmente: paneles solares perovskita más eficientes, turbinas eólicas "
                "flotantes offshore, hidrógeno verde como vector energético, y redes inteligentes. La transición energética "
                "es imparable para combatir el cambio climático.\n\n"
                "¿Qué tecnología verde te interesa? (solar, eólica, hidrógeno verde, cambio climático)"
            )
        return respuesta

    if any(palabra in tokens for palabra in [
        "blockchain", "bitcoin", "criptomoneda", "crypto", "ethereum", "nft", "web3", "metaverso", 
        "realidad", "virtual", "aumentada", "vr", "ar", "gafas"
    ]):
        estado['ultimo_tema'] = "Blockchain y Web3"
        if "blockchain" in tokens or "bitcoin" in tokens or "criptomoneda" in tokens or "crypto" in tokens:
            respuesta = (
                "**Blockchain y Criptomonedas** 🔗\n\n"
                "Blockchain y criptomonedas transforman las finanzas: Bitcoin como oro digital, Ethereum con contratos inteligentes, "
                "DeFi (finanzas descentralizadas), stablecoins, y aplicaciones en cadena de suministro y verificación de identidad. "
                "La regulación evoluciona mientras la adopción institucional crece.\n\n"
                "¿Te interesa Bitcoin, DeFi, contratos inteligentes o aplicaciones empresariales?"
            )
        elif "realidad" in tokens or "virtual" in tokens or "aumentada" in tokens or "vr" in tokens or "ar" in tokens:
            respuesta = (
                "**Realidad Extendida (XR)** 🥽\n\n"
                "XR (Realidad Extendida) avanza: Apple Vision Pro y Meta Quest ofrecen experiencias inmersivas, AR para navegación "
                "y trabajo remoto, entrenamiento médico en VR, y aplicaciones industriales. La línea entre físico y digital se difumina.\n\n"
                "¿Quieres saber sobre VR gaming, aplicaciones industriales o el futuro del metaverso?"
            )
        else:
            respuesta = (
                "**Web3 y Tecnologías Emergentes** 🌐\n\n"
                "Web3 y tecnologías emergentes remodelan internet: blockchain descentralizado, metaversos inmersivos, "
                "NFTs para propiedad digital, identidad descentralizada y nuevos modelos económicos digitales.\n\n"
                "¿Qué aspecto de Web3 te interesa? (blockchain, NFTs, metaverso, identidad digital)"
            )
        return respuesta

    if any(palabra in tokens for palabra in [
        "recomienda", "noticia", "novedad", "descubrimiento", "avance", "innovación", "investigación", 
        "estudio", "científico", "tecnológico", "reciente", "actual", "último", "últimas"
    ]):
        respuesta = (
            "**📰 Noticias destacadas de ciencia y tecnología (2024-2025)**\n\n"
            "🧬 Terapias génicas aprobadas para enfermedades raras\n"
            "🤖 Modelos de IA multimodales superan pruebas profesionales\n"
            "🚀 Starship de SpaceX avanza hacia misiones lunares\n"
            "⚛️ Avances en fusión nuclear hacia energía comercial\n"
            "🔬 James Webb descubre galaxias primitivas inesperadas\n"
            "💊 Vacunas personalizadas contra el cáncer muestran éxito\n"
            "🔋 Baterías de estado sólido alcanzan producción piloto\n"
            "🧠 Interfaces cerebro-computadora para comunicación\n\n"
            "¿Sobre cuál te gustaría profundizar? Escribe el nombre del tema."
        )
        return respuesta
    
    # Manejo de preguntas fuera de tema con redirección inteligente
    palabras_fuera_tema = ["futbol", "fútbol", "deporte", "comida", "musica", "música", "película", "juego", "videojuego"]
    if any(palabra in tokens for palabra in palabras_fuera_tema):
        respuesta = (
            "Entiendo tu interés, pero me especializo en ciencia y tecnología. 🔬\n\n"
            "Sin embargo, puedo relacionarlo:\n"
            "• Si te interesa el deporte, puedo hablarte sobre **tecnología deportiva y biomecánica**\n"
            "• Si te gusta la música, puedo explicarte sobre **IA generativa de música**\n"
            "• Si te interesan los videojuegos, puedo contarte sobre **motores gráficos y IA en gaming**\n\n"
            "¿Alguno de estos temas te interesa?"
        )
        return respuesta

    # Conversación genérica con contexto
    if len(tokens) <= 3:
        if estado['ultimo_tema']:
            respuesta = (
                f"Hmm, ¿podrías ser más específico? 🤔\n\n"
                f"Estábamos hablando de **{estado['ultimo_tema']}**. ¿Quieres continuar con este tema "
                f"o explorar algo diferente como IA, espacio, medicina o energía?"
            )
        else:
            respuesta = (
                "Tu mensaje es muy corto. ¿Podrías ser más específico? 😊\n\n"
                "Puedo ayudarte con: IA, espacio, medicina, energía, computación o blockchain."
            )
    elif len(tokens) <= 10:
        if estado['ultimo_tema']:
            respuesta = (
                f"¡Interesante! Veo que te interesa **{estado['ultimo_tema']}**.\n\n"
                f"¿Quieres profundizar más en este tema o explorar otro como IA, espacio, medicina, energía o computación?"
            )
        else:
            respuesta = (
                "¡Interesante! 💡 Puedo hablarte sobre:\n"
                "🤖 Inteligencia Artificial\n"
                "🚀 Exploración Espacial\n"
                "💻 Computación Cuántica\n"
                "🧬 Medicina y Genética\n"
                "⚡ Energías Renovables\n"
                "🔗 Blockchain y Web3\n\n"
                "¿Qué tema te gustaría explorar?"
            )
    else:
        if estado['ultimo_tema']:
            respuesta = (
                f"Entiendo tu interés. Basándome en nuestra conversación sobre **{estado['ultimo_tema']}**, "
                f"puedo darte información más específica.\n\n"
                f"¿Podrías reformular tu pregunta usando palabras clave como: IA, robot, espacio, James Webb, "
                f"CRISPR, energía, fusión, blockchain, etc.?"
            )
        else:
            respuesta = (
                "Puedo ayudarte mejor si usas palabras clave relacionadas con ciencia y tecnología. 🔍\n\n"
                "Ejemplos: 'ChatGPT', 'James Webb', 'CRISPR', 'fusión nuclear', 'blockchain', 'robótica'\n\n"
                "O simplemente pide 'recomendaciones' para ver noticias destacadas."
            )

    # === PROCESAMIENTO FINAL DE LA RESPUESTA ===
    # Aplicar análisis de sentimientos y mejora con LLM si están disponibles
    respuesta = procesar_respuesta(
        respuesta,
        sentimiento_data=sentimiento_data,
        usar_llm=LLM_CONFIG.get('use_for_enhancement', False)
    )

    return respuesta