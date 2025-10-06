"""
Módulo de análisis de sentimientos usando pysentimiento
Analiza el sentimiento del usuario para adaptar las respuestas del chatbot
"""

try:
    from pysentimiento import create_analyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False
    print("⚠️ pysentimiento no está instalado. Ejecuta: pip install pysentimiento")

class SentimentAnalyzer:
    """
    Clase para analizar el sentimiento de los mensajes del usuario.
    """
    
    def __init__(self):
        """Inicializa el analizador de sentimientos."""
        if SENTIMENT_AVAILABLE:
            try:
                self.analyzer = create_analyzer(task="sentiment", lang="es")
                self.enabled = True
                print("✅ Analizador de sentimientos cargado correctamente")
            except Exception as e:
                self.enabled = False
                print(f"⚠️ Error al cargar el analizador: {e}")
        else:
            self.enabled = False
            self.analyzer = None
    
    def analyze(self, texto):
        """
        Analiza el sentimiento de un texto.
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            dict: {
                'sentimiento': 'POS'|'NEG'|'NEU',
                'probabilidades': {'POS': 0.x, 'NEG': 0.x, 'NEU': 0.x},
                'confianza': float,
                'descripcion': str
            }
        """
        if not self.enabled or not texto:
            return {
                'sentimiento': 'NEU',
                'probabilidades': {'POS': 0.33, 'NEG': 0.33, 'NEU': 0.34},
                'confianza': 0.0,
                'descripcion': 'neutral'
            }
        
        try:
            resultado = self.analyzer.predict(texto)
            sentimiento = resultado.output
            probas = resultado.probas
            
            # Obtener la confianza (probabilidad máxima)
            confianza = max(probas.values())
            
            # Descripción del sentimiento
            descripciones = {
                'POS': 'positivo',
                'NEG': 'negativo',
                'NEU': 'neutral'
            }
            
            return {
                'sentimiento': sentimiento,
                'probabilidades': probas,
                'confianza': confianza,
                'descripcion': descripciones.get(sentimiento, 'neutral')
            }
        
        except Exception as e:
            print(f"Error al analizar sentimiento: {e}")
            return {
                'sentimiento': 'NEU',
                'probabilidades': {'POS': 0.33, 'NEG': 0.33, 'NEU': 0.34},
                'confianza': 0.0,
                'descripcion': 'neutral'
            }
    
    def get_response_tone(self, sentimiento_analizado):
        """
        Determina el tono de respuesta apropiado según el sentimiento del usuario.
        
        Args:
            sentimiento_analizado (dict): Resultado del análisis de sentimiento
            
        Returns:
            str: Tono de respuesta ('empático', 'entusiasta', 'neutral')
        """
        sentimiento = sentimiento_analizado['sentimiento']
        confianza = sentimiento_analizado['confianza']
        
        if confianza < 0.5:
            return 'neutral'
        
        tonos = {
            'NEG': 'empático',
            'POS': 'entusiasta',
            'NEU': 'neutral'
        }
        
        return tonos.get(sentimiento, 'neutral')
    
    def generar_mensaje_empatico(self, sentimiento_analizado):
        """
        Genera un mensaje empático según el sentimiento detectado.
        
        Args:
            sentimiento_analizado (dict): Resultado del análisis
            
        Returns:
            str: Mensaje empático o None si no aplica
        """
        sentimiento = sentimiento_analizado['sentimiento']
        confianza = sentimiento_analizado['confianza']
        
        # Solo si la confianza es alta
        if confianza < 0.6:
            return None
        
        mensajes = {
            'NEG': [
                "Noto que podrías estar un poco frustrado. 💙 ",
                "Entiendo que esto puede ser complicado. ",
                "Percibo cierta preocupación. Estoy aquí para ayudarte. "
            ],
            'POS': [
                "¡Me encanta tu entusiasmo! 😊 ",
                "¡Qué emoción poder compartir esto contigo! ",
                "¡Genial que te interese este tema! "
            ]
        }
        
        import random
        if sentimiento in mensajes:
            return random.choice(mensajes[sentimiento])
        
        return None


# Instancia global del analizador
_sentiment_analyzer = None

def get_sentiment_analyzer():
    """Obtiene la instancia global del analizador de sentimientos."""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer


# Función de utilidad para análisis rápido
def analizar_sentimiento(texto):
    """
    Función de utilidad para analizar el sentimiento de un texto.
    
    Args:
        texto (str): Texto a analizar
        
    Returns:
        dict: Resultado del análisis
    """
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze(texto)


if __name__ == "__main__":
    # Pruebas del módulo
    print("=== Prueba del Analizador de Sentimientos ===\n")
    
    analyzer = SentimentAnalyzer()
    
    textos_prueba = [
        "Me encanta aprender sobre inteligencia artificial",
        "Esto es muy complicado y frustrante",
        "¿Qué es el James Webb?",
        "Eres inútil y no me ayudas en nada",
        "Gracias por la información"
    ]
    
    for texto in textos_prueba:
        resultado = analyzer.analyze(texto)
        tono = analyzer.get_response_tone(resultado)
        mensaje = analyzer.generar_mensaje_empatico(resultado)
        
        print(f"Texto: '{texto}'")
        print(f"Sentimiento: {resultado['descripcion']} ({resultado['sentimiento']})")
        print(f"Confianza: {resultado['confianza']:.2%}")
        print(f"Tono de respuesta: {tono}")
        if mensaje:
            print(f"Mensaje empático: {mensaje}")
        print(f"Probabilidades: {resultado['probabilidades']}")
        print("-" * 60)
