import sys
import nltk
import spacy
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QSplitter, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QColor

# Descargar recursos de NLTK (solo primera vez)
try:
    nltk.download("punkt")
    nltk.download("punkt_tab")
except:
    pass

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except:
    print("Error: No se pudo cargar el modelo de spaCy")
    nlp = None

class ChatBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.saludo = False
        self.pregunta_estado = False
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('ChatBot Lingüístico')
        self.setGeometry(100, 100, 900, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter para dividir la ventana
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel de chat
        chat_frame = QFrame()
        chat_frame.setFrameStyle(QFrame.StyledPanel)
        chat_layout = QVBoxLayout(chat_frame)
        
        # Área de chat
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 11))
        chat_layout.addWidget(QLabel("Conversación:"))
        chat_layout.addWidget(self.chat_display)
        
        # Área de entrada
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu mensaje aquí...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        chat_layout.addLayout(input_layout)
        
        # Panel de análisis
        analysis_frame = QFrame()
        analysis_frame.setFrameStyle(QFrame.StyledPanel)
        analysis_layout = QVBoxLayout(analysis_frame)
        
        self.analysis_display = QTextEdit()
        self.analysis_display.setReadOnly(True)
        self.analysis_display.setFont(QFont("Courier", 10))
        analysis_layout.addWidget(QLabel("Análisis Lingüístico:"))
        analysis_layout.addWidget(self.analysis_display)
        
        # Añadir paneles al splitter
        splitter.addWidget(chat_frame)
        splitter.addWidget(analysis_frame)
        splitter.setSizes([600, 300])
        
        main_layout.addWidget(splitter)
        
        # Mostrar mensaje inicial
        self.add_message("ChatBot", "Hola, ¿cómo estás Walter Alejandro? Debes saludarme con 'hola' para que empecemos a hablar.", False)
    
    def add_message(self, sender, message, is_user=True):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Formatear mensaje
        if is_user:
            formatted_message = f"<p><b>{sender}:</b> {message}</p>"
            self.chat_display.append(formatted_message)
        else:
            formatted_message = f"<p style='color:#0066CC;'><b>{sender}:</b> {message}</p>"
            self.chat_display.append(formatted_message)
        
        # Auto-scroll
        self.chat_display.ensureCursorVisible()
    
    def show_analysis(self, analisis):
        if isinstance(analisis, str):
            self.analysis_display.setText(analisis)
            return
        
        tabla = "Análisis lingüístico:\n"
        tabla += "Palabra\t\tLema\t\tPOS\t\tEtiqueta\tDependencia\n"
        tabla += "-" * 60 + "\n"
        
        for token in analisis:
            tabla += f"{token['texto']:8}\t{token['lema']:8}\t{token['pos']:8}\t{token['tag']:8}\t{token['dependencia']:12}\n"
        
        self.analysis_display.setText(tabla)
    
    def obtener_tokens(self, texto):
        return nltk.word_tokenize(texto.lower())
    
    def analizar_texto(self, texto):
        if nlp is None:
            return "Error: Modelo de spaCy no cargado"
        
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
    
    def send_message(self):
        entrada = self.input_field.text().strip()
        if not entrada:
            return
        
        # Añadir mensaje del usuario al chat
        self.add_message("Tú", entrada, True)
        self.input_field.clear()
        
        # Procesar mensaje
        tokens = self.obtener_tokens(entrada)

        if not self.saludo:
            if "hola" in tokens:
                self.saludo = True
                self.pregunta_estado = True
                self.add_message("ChatBot", "Hola, ¿cómo estás?", False)
            else:
                self.add_message("ChatBot", "Primero tienes que saludarme con 'hola'.", False)
        
        else:
            if self.pregunta_estado:
                if any(palabra in tokens for palabra in ["bien", "mal", "regular", "excelente", "feliz", "triste"]):
                    self.pregunta_estado = False
                    if "bien" in tokens or "excelente" in tokens or "feliz" in tokens:
                        self.add_message("ChatBot", "¡Me alegra que estés bien! ¿En qué puedo ayudarte?", False)
                    elif "mal" in tokens or "triste" in tokens:
                        self.add_message("ChatBot", "Lo siento mucho. Espero que te sientas mejor pronto.", False)
                    else:
                        self.add_message("ChatBot", "Entendido. ¿En qué puedo ayudarte?", False)
                else:
                    self.add_message("ChatBot", "Por favor respóndeme, ¿cómo estás?", False)
            
            elif entrada.lower().startswith("analizar:"):
                texto_analizar = entrada[9:].strip()
                if texto_analizar:
                    analisis = self.analizar_texto(texto_analizar)
                    self.show_analysis(analisis)
                else:
                    self.add_message("ChatBot", "Por favor escribe algo después de 'analizar:'", False)
            
            elif any(palabra in tokens for palabra in ["adios", "chao", "hasta luego", "nos vemos"]):
                self.add_message("ChatBot", "Adiós, ¡hasta luego! Fue un gusto conversar contigo.", False)
                # Podrías añadir un delay y cerrar la aplicación
                
            elif any(palabra in tokens for palabra in ["anime", "naruto", "one piece", "dragon ball", "recomienda", "personaje", "opening", "ending", "temporada", "autor", "género", "manga", "película", "shonen", "isekai", "waifu", "husbando", "villano", "protagonista", "capítulo", "episodio", "studio", "crunchyroll", "netflix"]):
                if "recomienda" in tokens or "recomendar" in tokens:
                    self.add_message("ChatBot", (
    "Claro, Te recomiendo ver 'Fullmetal Alchemist', 'Attack on Titan', "
    "'Jujutsu Kaisen', 'Demon Slayer', 'Spy x Family', 'Mob Psycho 100', "
    "'Chainsaw Man', 'Death Note', 'My Hero Academia', 'Haikyuu!!', 'One Piece', "
    "'Naruto', 'Dragon Ball', 'Bleach', 'Kimetsu no Yaiba', 'Tokyo Ghoul', "
    "...otros títulos..."
), False)
                elif "personaje" in tokens or "protagonista" in tokens or "villano" in tokens or "waifu" in tokens or "husbando" in tokens:
                    self.add_message("ChatBot", "¿De qué anime quieres saber sobre un personaje? Ejemplo: 'personaje Naruto', 'villano One Piece', 'waifu Demon Slayer'.", False)
                elif "opening" in tokens:
                    self.add_message("ChatBot", "Algunos openings famosos son: 'Guren no Yumiya' (Attack on Titan), 'Unravel' (Tokyo Ghoul), 'Blue Bird' (Naruto), 'Cha-La Head-Cha-La' (Dragon Ball Z), 'Again' (Fullmetal Alchemist Brotherhood). ¿Quieres analizar la letra de alguno?", False)
                elif "ending" in tokens:
                    self.add_message("ChatBot", "Algunos endings populares: 'Secret Base' (Anohana), 'Wind' (Naruto), 'Lost in Paradise' (Jujutsu Kaisen), 'Kimi no Shiranai Monogatari' (Bakemonogatari). ¿Quieres analizar la letra de alguno?", False)
                elif "temporada" in tokens:
                    self.add_message("ChatBot", "¿Te gustaría saber cuántas temporadas tiene un anime? Ejemplo: 'temporada My Hero Academia'.", False)
                elif "autor" in tokens:
                    self.add_message("ChatBot", "¿Quieres saber el autor de algún anime o manga? Ejemplo: 'autor One Piece' (Eiichiro Oda), 'autor Naruto' (Masashi Kishimoto).", False)
                elif "género" in tokens or "shonen" in tokens or "isekai" in tokens:
                    self.add_message("ChatBot", "¿Buscas recomendaciones por género? Ejemplo: 'recomienda isekai', 'recomienda shonen', 'recomienda romance'.", False)
                elif "manga" in tokens:
                    self.add_message("ChatBot", "¿Te interesa leer manga? Puedes encontrar recomendaciones como 'Berserk', 'Monster', 'Vagabond', 'One Piece', 'Naruto', 'Dragon Ball', 'Jujutsu Kaisen', 'Chainsaw Man'.", False)
                elif "película" in tokens:
                    self.add_message("ChatBot", "Algunas películas recomendadas: 'Your Name', 'A Silent Voice', 'El viaje de Chihiro', 'Weathering With You', 'La tumba de las luciérnagas', 'Paprika', 'Perfect Blue'.", False)
                elif "capítulo" in tokens or "episodio" in tokens:
                    self.add_message("ChatBot", "¿Quieres saber cuántos episodios tiene un anime? Ejemplo: 'episodios One Piece', 'capítulos Naruto'.", False)
                elif "studio" in tokens:
                    self.add_message("ChatBot", "Algunos estudios famosos: MAPPA, Ufotable, Madhouse, Bones, Toei Animation, Studio Ghibli, Wit Studio, CloverWorks, Sunrise, Pierrot.", False)
                elif "crunchyroll" in tokens or "netflix" in tokens:
                    self.add_message("ChatBot", "Puedes ver anime en plataformas como Crunchyroll, Netflix, Amazon Prime Video, HIDIVE, AnimeFLV, AnimeID.", False)
                elif "anime" in tokens:
                    self.add_message("ChatBot", "¡Me encanta el anime! Puedes preguntarme por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, etc. También puedo analizar frases de anime, solo escribe 'analizar: tu frase'.", False)
                elif "naruto" in tokens:
                    self.add_message("ChatBot", "Naruto es un anime muy popular sobre ninjas. ¿Quieres analizar una frase de Naruto? Ejemplo: 'analizar: El dolor es mi amigo'.", False)
                elif "one piece" in tokens:
                    self.add_message("ChatBot", "One Piece trata sobre piratas y aventuras. ¿Te gustaría analizar una cita de Luffy? Ejemplo: 'analizar: ¡Seré el rey de los piratas!'.", False)
                elif "dragon ball" in tokens:
                    self.add_message("ChatBot", "Dragon Ball es famoso por sus batallas épicas. ¿Quieres analizar una frase de Goku? Ejemplo: 'analizar: ¡Kamehameha!'.", False)
                else:
                    self.add_message("ChatBot", "¿Quieres hablar de algún anime en particular o analizar una frase? Puedes preguntar por recomendaciones, personajes, openings, endings, películas, géneros, estudios, autores, temporadas, episodios, plataformas, manga, waifus, husbando, villanos, protagonistas, etc.", False)
                
            else:
                self.add_message("ChatBot", f"Entendí: '{entrada}'", False)
                
                # Ofrecer análisis lingüístico
                if len(tokens) <= 10:
                    self.add_message("ChatBot", "¿Quieres que analice lingüísticamente tu mensaje? (escribe 'analizar: tu mensaje')", False)

def main():
    app = QApplication(sys.argv)
    chatbot = ChatBotGUI()
    chatbot.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()