import nltk
import spacy

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

def responder(mensaje, estado):
    """
    Lógica conversacional del chatbot.
    """
    tokens = obtener_tokens(mensaje)
    respuesta = ""

    # Saludo inicial obligatorio
    if not estado['saludo']:
        if any(palabra in tokens for palabra in ["hola", "buenas", "saludos", "hey", "holi"]):
            estado['saludo'] = True
            respuesta = "¡Hola! ¿Cómo estás? Puedes preguntarme sobre anime, pedir recomendaciones o simplemente conversar."
        else:
            respuesta = "Salúdame primero para darte recomendaciones."
        return respuesta

    # Despedida
    if any(palabra in tokens for palabra in ["adios", "chao", "hasta luego", "nos vemos", "bye"]):
        respuesta = "Adiós, ¡hasta luego! Fue un gusto conversar contigo."
        estado['saludo'] = False
        return respuesta

    # Estado de ánimo
    if any(palabra in tokens for palabra in ["bien", "feliz", "excelente", "contento", "alegre"]):
        respuesta = "¡Me alegra que estés bien! ¿Te gustaría una recomendación de anime o hablar de algún tema?"
        return respuesta
    if any(palabra in tokens for palabra in ["mal", "triste", "regular", "cansado", "aburrido"]):
        respuesta = "Lo siento mucho. Si quieres distraerte, puedo recomendarte un anime o conversar contigo."
        return respuesta

    # Opciones de anime y conversación ampliadas
    if any(palabra in tokens for palabra in [
        "anime", "naruto", "one piece", "dragon ball", "recomienda", "recomendar", "personaje", "opening", "ending", "temporada",
        "autor", "género", "manga", "película", "shonen", "isekai", "waifu", "husbando", "villano", "protagonista",
        "capítulo", "episodio", "studio", "crunchyroll", "netflix", "cosplay", "japon", "evento", "convención", "curiosidad",
        "seiyuu", "voz", "soundtrack", "ost", "live action", "figura", "colección", "merchandising", "fanart", "fanfic",
        "kawaii", "otaku", "senpai", "sensei", "samurai", "ninja", "idol", "jpop", "jrock", "drama", "dorama", "light novel",
        "webtoon", "manhwa", "manhua", "ranking", "popular", "estreno", "temporada nueva", "remake", "spin-off", "parodia"
    ]):
        if "recomienda" in tokens or "recomendar" in tokens:
            respuesta = (
                "¡Claro! Te recomiendo ver: 'Fullmetal Alchemist', 'Attack on Titan', 'Jujutsu Kaisen', 'Demon Slayer', "
                "'Spy x Family', 'Mob Psycho 100', 'Chainsaw Man', 'Death Note', 'My Hero Academia', 'Haikyuu!!', "
                "'One Piece', 'Naruto', 'Dragon Ball', 'Bleach', 'Kimetsu no Yaiba', 'Tokyo Ghoul', 'Berserk', 'Monster', 'Vagabond', 'Vinland Saga', 'Blue Lock', 'Frieren', 'Oshi no Ko', 'Solo Leveling' y muchos más."
            )
        elif "personaje" in tokens or "protagonista" in tokens or "villano" in tokens or "waifu" in tokens or "husbando" in tokens:
            respuesta = "¿De qué anime quieres saber sobre un personaje? Ejemplo: 'personaje Naruto', 'villano One Piece', 'waifu Demon Slayer'. ¿Buscas héroes, villanos, waifus o husbando favoritos?"
        elif "opening" in tokens or "soundtrack" in tokens or "ost" in tokens:
            respuesta = "Algunos openings y OST famosos: 'Guren no Yumiya' (Attack on Titan), 'Unravel' (Tokyo Ghoul), 'Blue Bird' (Naruto), 'Again' (Fullmetal Alchemist Brotherhood), 'Departure!' (Hunter x Hunter), 'Tank!' (Cowboy Bebop). ¿Quieres saber más sobre música de anime?"
        elif "ending" in tokens:
            respuesta = "Algunos endings populares: 'Secret Base' (Anohana), 'Wind' (Naruto), 'Lost in Paradise' (Jujutsu Kaisen), 'Kimi no Shiranai Monogatari' (Bakemonagatari)."
        elif "temporada" in tokens or "estreno" in tokens or "temporada nueva" in tokens:
            respuesta = "¿Te gustaría saber cuántas temporadas tiene un anime o cuándo se estrena la próxima? Ejemplo: 'temporada My Hero Academia', 'estreno Solo Leveling'."
        elif "autor" in tokens or "seiyuu" in tokens or "voz" in tokens:
            respuesta = "¿Quieres saber el autor o los actores de voz de algún anime? Ejemplo: 'autor One Piece' (Eiichiro Oda), 'voz Goku' (Masako Nozawa)."
        elif "género" in tokens or "shonen" in tokens or "isekai" in tokens or "drama" in tokens or "dorama" in tokens:
            respuesta = "¿Buscas recomendaciones por género? Ejemplo: 'recomienda isekai', 'recomienda shonen', 'recomienda drama', 'recomienda dorama'."
        elif "manga" in tokens or "light novel" in tokens or "webtoon" in tokens or "manhwa" in tokens or "manhua" in tokens:
            respuesta = "¿Te interesa leer manga, light novels, webtoons, manhwa o manhua? Recomendaciones: 'Berserk', 'Monster', 'Solo Leveling', 'Tower of God', 'Lookism', 'Vagabond', 'One Piece', 'Chainsaw Man'."
        elif "película" in tokens or "live action" in tokens:
            respuesta = "Algunas películas recomendadas: 'Your Name', 'A Silent Voice', 'El viaje de Chihiro', 'Weathering With You', 'La tumba de las luciérnagas', 'Paprika', 'Perfect Blue', 'Belle', 'Suzume', 'live action Rurouni Kenshin'."
        elif "capítulo" in tokens or "episodio" in tokens or "ranking" in tokens or "popular" in tokens:
            respuesta = "¿Quieres saber cuántos episodios tiene un anime o cuáles son los más populares? Ejemplo: 'episodios One Piece', 'ranking anime 2024'."
        elif "studio" in tokens or "remake" in tokens or "spin-off" in tokens or "parodia" in tokens:
            respuesta = "Algunos estudios famosos: MAPPA, Ufotable, Madhouse, Bones, Toei Animation, Studio Ghibli, Wit Studio, CloverWorks, Sunrise, Pierrot. ¿Te interesan remakes, spin-offs o parodias?"
        elif "crunchyroll" in tokens or "netflix" in tokens or "amazon" in tokens or "plataforma" in tokens:
            respuesta = "Puedes ver anime en plataformas como Crunchyroll, Netflix, Amazon Prime Video, HIDIVE, AnimeFLV, AnimeID. ¿Buscas recomendaciones en alguna plataforma?"
        elif "cosplay" in tokens or "evento" in tokens or "convención" in tokens:
            respuesta = "¿Te interesa el cosplay o los eventos de anime? Hay convenciones como Anime Expo, Japan Weekend, Comic-Con, y muchos más. ¿Quieres consejos de cosplay?"
        elif "curiosidad" in tokens or "fanart" in tokens or "fanfic" in tokens or "colección" in tokens or "figura" in tokens or "merchandising" in tokens:
            respuesta = "¿Buscas curiosidades, fanarts, fanfics o coleccionables? El mundo otaku tiene figuras, merchandising, fanarts y fanfics de casi todos los animes populares."
        elif "kawaii" in tokens or "otaku" in tokens or "senpai" in tokens or "sensei" in tokens or "samurai" in tokens or "ninja" in tokens or "idol" in tokens or "jpop" in tokens or "jrock" in tokens:
            respuesta = "¿Te interesa la cultura japonesa, idols, música J-Pop/J-Rock, samuráis, ninjas o el mundo kawaii? ¡Pregúntame lo que quieras!"
        elif "anime" in tokens:
            respuesta = "¡Me encanta el anime! Puedes preguntarme por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, cultura japonesa, eventos, curiosidades, y mucho más."
        elif "naruto" in tokens:
            respuesta = "Naruto es un anime muy popular sobre ninjas. ¿Quieres saber más sobre sus personajes, historia, villanos o openings?"
        elif "one piece" in tokens:
            respuesta = "One Piece trata sobre piratas y aventuras. ¿Te gustaría saber más sobre Luffy, los Mugiwara, los villanos o los arcos de la historia?"
        elif "dragon ball" in tokens:
            respuesta = "Dragon Ball es famoso por sus batallas épicas. ¿Quieres saber más sobre Goku, Vegeta, los villanos, las transformaciones o las películas?"
        elif "japon" in tokens:
            respuesta = "Japón es la cuna del anime y manga. ¿Te interesa la cultura, la comida, los festivales, el idioma o los lugares turísticos?"
        else:
            respuesta = "¿Quieres hablar de algún anime, cultura japonesa, evento, curiosidad, música, cosplay, manga, película o personaje en particular? ¡Pregúntame lo que quieras!"
        return respuesta

    # Conversación genérica
    if len(tokens) <= 10:
        respuesta = "¡Interesante! ¿Quieres que te recomiende un anime, hablar de algún personaje, cultura japonesa, eventos o necesitas ayuda con algo más?"
    else:
        respuesta = "¡Gracias por tu mensaje! Si quieres recomendaciones, escribe palabras como 'anime', 'recomienda', 'personaje', 'evento', 'curiosidad', etc."

    return respuesta