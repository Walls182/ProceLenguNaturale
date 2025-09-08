from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_logic import responder, analizar_texto

app = Flask(__name__)
CORS(app)

# Estado de la conversación por sesión (simple, para demo)
estado = {'saludo': False, 'pregunta_estado': False}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    respuesta = responder(mensaje, estado)
    return jsonify({'respuesta': respuesta})

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