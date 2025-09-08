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

    # Saludo inicial
    if not estado['saludo']:
        if any(palabra in tokens for palabra in ["hola", "buenas", "saludos", "hey", "holi"]):
            estado['saludo'] = True
            respuesta = "¡Hola! ¿Cómo estás? Puedes preguntarme sobre anime, pedir recomendaciones o simplemente conversar."
        else:
            respuesta = "¡Hola! Para comenzar, salúdame con 'hola', 'buenas', 'saludos' o algo similar."
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

    # Opciones de anime y conversación
    if any(palabra in tokens for palabra in [
        "anime", "naruto", "one piece", "dragon ball", "recomienda", "recomendar", "personaje", "opening", "ending", "temporada",
        "autor", "género", "manga", "película", "shonen", "isekai", "waifu", "husbando", "villano", "protagonista",
        "capítulo", "episodio", "studio", "crunchyroll", "netflix"
    ]):
        if "recomienda" in tokens or "recomendar" in tokens:
            respuesta = (
                "¡Claro! Te recomiendo ver: 'Fullmetal Alchemist', 'Attack on Titan', 'Jujutsu Kaisen', 'Demon Slayer', "
                "'Spy x Family', 'Mob Psycho 100', 'Chainsaw Man', 'Death Note', 'My Hero Academia', 'Haikyuu!!', "
                "'One Piece', 'Naruto', 'Dragon Ball', 'Bleach', 'Kimetsu no Yaiba', 'Tokyo Ghoul' y muchos más."
            )
        elif "personaje" in tokens or "protagonista" in tokens or "villano" in tokens or "waifu" in tokens or "husbando" in tokens:
            respuesta = "¿De qué anime quieres saber sobre un personaje? Ejemplo: 'personaje Naruto', 'villano One Piece', 'waifu Demon Slayer'."
        elif "opening" in tokens:
            respuesta = "Algunos openings famosos: 'Guren no Yumiya' (Attack on Titan), 'Unravel' (Tokyo Ghoul), 'Blue Bird' (Naruto), 'Cha-La Head-Cha-La' (Dragon Ball Z), 'Again' (Fullmetal Alchemist Brotherhood)."
        elif "ending" in tokens:
            respuesta = "Algunos endings populares: 'Secret Base' (Anohana), 'Wind' (Naruto), 'Lost in Paradise' (Jujutsu Kaisen), 'Kimi no Shiranai Monogatari' (Bakemonogatari)."
        elif "temporada" in tokens:
            respuesta = "¿Te gustaría saber cuántas temporadas tiene un anime? Ejemplo: 'temporada My Hero Academia'."
        elif "autor" in tokens:
            respuesta = "¿Quieres saber el autor de algún anime o manga? Ejemplo: 'autor One Piece' (Eiichiro Oda), 'autor Naruto' (Masashi Kishimoto)."
        elif "género" in tokens or "shonen" in tokens or "isekai" in tokens:
            respuesta = "¿Buscas recomendaciones por género? Ejemplo: 'recomienda isekai', 'recomienda shonen', 'recomienda romance'."
        elif "manga" in tokens:
            respuesta = "¿Te interesa leer manga? Puedes encontrar recomendaciones como 'Berserk', 'Monster', 'Vagabond', 'One Piece', 'Naruto', 'Dragon Ball', 'Jujutsu Kaisen', 'Chainsaw Man'."
        elif "película" in tokens:
            respuesta = "Algunas películas recomendadas: 'Your Name', 'A Silent Voice', 'El viaje de Chihiro', 'Weathering With You', 'La tumba de las luciérnagas', 'Paprika', 'Perfect Blue'."
        elif "capítulo" in tokens or "episodio" in tokens:
            respuesta = "¿Quieres saber cuántos episodios tiene un anime? Ejemplo: 'episodios One Piece', 'capítulos Naruto'."
        elif "studio" in tokens:
            respuesta = "Algunos estudios famosos: MAPPA, Ufotable, Madhouse, Bones, Toei Animation, Studio Ghibli, Wit Studio, CloverWorks, Sunrise, Pierrot."
        elif "crunchyroll" in tokens or "netflix" in tokens:
            respuesta = "Puedes ver anime en plataformas como Crunchyroll, Netflix, Amazon Prime Video, HIDIVE, AnimeFLV, AnimeID."
        elif "anime" in tokens:
            respuesta = "¡Me encanta el anime! Puedes preguntarme por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, etc."
        elif "naruto" in tokens:
            respuesta = "Naruto es un anime muy popular sobre ninjas. ¿Quieres saber más sobre sus personajes o historia?"
        elif "one piece" in tokens:
            respuesta = "One Piece trata sobre piratas y aventuras. ¿Te gustaría saber más sobre Luffy o la historia?"
        elif "dragon ball" in tokens:
            respuesta = "Dragon Ball es famoso por sus batallas épicas. ¿Quieres saber más sobre Goku o los villanos?"
        else:
            respuesta = "¿Quieres hablar de algún anime en particular o analizar una frase? Puedes preguntar por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, etc."
        return respuesta

    # Conversación genérica
    if len(tokens) <= 10:
        respuesta = "¡Interesante! ¿Quieres que te recomiende un anime, hablar de algún personaje, o necesitas ayuda con algo más?"
    else:
        respuesta = "¡Gracias por tu mensaje! Si quieres recomendaciones, escribe palabras como 'anime', 'recomienda', 'personaje', etc."

    return respuesta