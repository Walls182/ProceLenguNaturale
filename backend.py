from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_logic import responder, analizar_texto

try:
    from config import CHATBOT_CONFIG, print_config
    print_config()
except ImportError:
    CHATBOT_CONFIG = {'nombre': 'SciTech Bot', 'version': '3.0'}
    print("⚠️ Archivo config.py no encontrado, usando configuración por defecto")

app = Flask(__name__)
CORS(app)

# Estado de la conversación por sesión (mejorado con sentimientos)
estado = {
    'saludo': False,
    'ultimo_tema': None,
    'temas_discutidos': [],
    'analisis_sentimiento': None,
    'contador_mensajes': 0
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    
    # Validación básica
    if not mensaje:
        return jsonify({'respuesta': 'Por favor, escribe un mensaje.'}), 400
    
    # Incrementar contador de mensajes
    estado['contador_mensajes'] += 1
    
    try:
        respuesta = responder(mensaje, estado)
        
        # Preparar respuesta con metadata
        response_data = {
            'respuesta': respuesta,
            'tema_actual': estado.get('ultimo_tema'),
            'estado_conversacion': 'activo' if estado['saludo'] else 'sin_saludo',
            'temas_discutidos': estado.get('temas_discutidos', []),
            'num_mensajes': estado['contador_mensajes']
        }
        
        # Agregar análisis de sentimiento si está disponible
        if estado.get('analisis_sentimiento'):
            sentiment = estado['analisis_sentimiento']
            response_data['sentimiento'] = {
                'tipo': sentiment.get('descripcion', 'neutral'),
                'confianza': round(sentiment.get('confianza', 0) * 100, 1)
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error en el chatbot: {e}")
        return jsonify({
            'respuesta': 'Lo siento, ocurrió un error. ¿Podrías reformular tu pregunta?',
            'error': str(e) if CHATBOT_CONFIG.get('debug', False) else 'Error interno'
        }), 500

@app.route('/analisis', methods=['POST'])
def analisis():
    data = request.get_json()
    texto = data.get('mensaje', '')
    resultado = analizar_texto(texto)
    return jsonify({'analisis': resultado})

@app.route('/')
def home():
    return "Backend PLN activo. Usa /chat para procesar mensajes."

if __name__ == '__main__':
    app.run(debug=True)