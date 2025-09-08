import nltk
import spacy

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
    return nltk.word_tokenize(texto.lower())

def analizar_texto(texto):
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

def show_analysis(analisis):
    if isinstance(analisis, str):
        return analisis
    tabla = "Análisis lingüístico:\n"
    tabla += "Palabra\tLema\tPOS\tEtiqueta\tDependencia\n"
    tabla += "-" * 60 + "\n"
    for token in analisis:
        tabla += f"{token['texto']:8}\t{token['lema']:8}\t{token['pos']:8}\t{token['tag']:8}\t{token['dependencia']:12}\n"
    return tabla

def responder(mensaje, estado):
    tokens = obtener_tokens(mensaje)
    respuesta = ""
    analisis = None

    # Lógica de conversación
    if not estado['saludo']:
        if "hola" in tokens:
            estado['saludo'] = True
            estado['pregunta_estado'] = True
            respuesta = "Hola, ¿cómo estás?"
        else:
            respuesta = "Primero tienes que saludarme con 'hola'."
    else:
        if estado['pregunta_estado']:
            if any(palabra in tokens for palabra in ["bien", "mal", "regular", "excelente", "feliz", "triste"]):
                estado['pregunta_estado'] = False
                if "bien" in tokens or "excelente" in tokens or "feliz" in tokens:
                    respuesta = "¡Me alegra que estés bien! ¿En qué puedo ayudarte?"
                elif "mal" in tokens or "triste" in tokens:
                    respuesta = "Lo siento mucho. Espero que te sientas mejor pronto."
                else:
                    respuesta = "Entendido. ¿En qué puedo ayudarte?"
            else:
                respuesta = "Por favor respóndeme, ¿cómo estás?"
        elif mensaje.lower().startswith("analizar:"):
            texto_analizar = mensaje[9:].strip()
            if texto_analizar:
                analisis = analizar_texto(texto_analizar)
                respuesta = show_analysis(analisis)
            else:
                respuesta = "Por favor escribe algo después de 'analizar:'"
        elif any(palabra in tokens for palabra in ["adios", "chao", "hasta luego", "nos vemos"]):
            respuesta = "Adiós, ¡hasta luego! Fue un gusto conversar contigo."
        elif any(palabra in tokens for palabra in [
            "anime", "naruto", "one piece", "dragon ball", "recomienda", "personaje", "opening", "ending", "temporada",
            "autor", "género", "manga", "película", "shonen", "isekai", "waifu", "husbando", "villano", "protagonista",
            "capítulo", "episodio", "studio", "crunchyroll", "netflix"
        ]):
            if "recomienda" in tokens or "recomendar" in tokens:
                respuesta = (
                    "Claro, Te recomiendo ver 'Fullmetal Alchemist', 'Attack on Titan', "
                    "'Jujutsu Kaisen', 'Demon Slayer', 'Spy x Family', 'Mob Psycho 100', "
                    "'Chainsaw Man', 'Death Note', 'My Hero Academia', 'Haikyuu!!', 'One Piece', "
                    "'Naruto', 'Dragon Ball', 'Bleach', 'Kimetsu no Yaiba', 'Tokyo Ghoul', "
                    "...otros títulos..."
                )
            elif "personaje" in tokens or "protagonista" in tokens or "villano" in tokens or "waifu" in tokens or "husbando" in tokens:
                respuesta = "¿De qué anime quieres saber sobre un personaje? Ejemplo: 'personaje Naruto', 'villano One Piece', 'waifu Demon Slayer'."
            elif "opening" in tokens:
                respuesta = "Algunos openings famosos son: 'Guren no Yumiya' (Attack on Titan), 'Unravel' (Tokyo Ghoul), 'Blue Bird' (Naruto), 'Cha-La Head-Cha-La' (Dragon Ball Z), 'Again' (Fullmetal Alchemist Brotherhood). ¿Quieres analizar la letra de alguno?"
            elif "ending" in tokens:
                respuesta = "Algunos endings populares: 'Secret Base' (Anohana), 'Wind' (Naruto), 'Lost in Paradise' (Jujutsu Kaisen), 'Kimi no Shiranai Monogatari' (Bakemonogatari). ¿Quieres analizar la letra de alguno?"
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
                respuesta = "¡Me encanta el anime! Puedes preguntarme por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, etc. También puedo analizar frases de anime, solo escribe 'analizar: tu frase'."
            elif "naruto" in tokens:
                respuesta = "Naruto es un anime muy popular sobre ninjas. ¿Quieres analizar una frase de Naruto? Ejemplo: 'analizar: El dolor es mi amigo'."
            elif "one piece" in tokens:
                respuesta = "One Piece trata sobre piratas y aventuras. ¿Te gustaría analizar una cita de Luffy? Ejemplo: 'analizar: ¡Seré el rey de los piratas!'."
            elif "dragon ball" in tokens:
                respuesta = "Dragon Ball es famoso por sus batallas épicas. ¿Quieres analizar una frase de Goku? Ejemplo: 'analizar: ¡Kamehameha!'."
            else:
                respuesta = "¿Quieres hablar de algún anime en particular o analizar una frase? Puedes preguntar por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, etc."
        else:
            respuesta = f"Entendí: '{mensaje}'"
            if len(tokens) <= 10:
                respuesta += "\n¿Quieres que analice lingüísticamente tu mensaje? (escribe 'analizar: tu mensaje')"

    return respuesta