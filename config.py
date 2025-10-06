"""
Archivo de configuración para el chatbot de ciencia y tecnología
Contiene configuraciones para análisis de sentimientos y modelo LLM
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ========== CONFIGURACIÓN GENERAL ==========
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
VERBOSE_LOGGING = os.getenv('VERBOSE_LOGGING', 'False').lower() == 'true'

# ========== ANÁLISIS DE SENTIMIENTOS ==========
SENTIMENT_CONFIG = {
    'enabled': True,  # Activar/desactivar análisis de sentimientos
    'min_confidence': 0.6,  # Confianza mínima para aplicar respuestas empáticas
    'adapt_tone': True,  # Adaptar tono de respuesta según sentimiento
}

# ========== MODELO LLM (GEMMA) ==========
LLM_CONFIG = {
    'enabled': False,  # Activar/desactivar modelo LLM (requiere recursos)
    'auto_load': False,  # Cargar modelo al iniciar (consume memoria)
    'model_name': 'google/gemma-2b-it',
    'hf_token': os.getenv('HUGGINGFACE_TOKEN'),  # Token desde variable de entorno
    'generation_params': {
        'max_length': 250,
        'temperature': 0.7,
        'top_p': 0.9,
    },
    'use_for_enhancement': False,  # Usar LLM para mejorar respuestas base
}

# ========== MODOS DE OPERACIÓN ==========
OPERATION_MODE = os.getenv('OPERATION_MODE', 'hybrid')  # 'basic', 'sentiment', 'llm', 'hybrid'

# Configuración según modo
MODE_SETTINGS = {
    'basic': {
        'sentiment': False,
        'llm': False,
        'description': 'Modo básico con respuestas predefinidas'
    },
    'sentiment': {
        'sentiment': True,
        'llm': False,
        'description': 'Modo con análisis de sentimientos'
    },
    'llm': {
        'sentiment': False,
        'llm': True,
        'description': 'Modo con generación LLM (requiere GPU)'
    },
    'hybrid': {
        'sentiment': True,
        'llm': False,  # Desactivado por defecto (requiere recursos)
        'description': 'Modo híbrido: sentimientos + respuestas base'
    }
}

# Aplicar configuración del modo
current_mode = MODE_SETTINGS.get(OPERATION_MODE, MODE_SETTINGS['hybrid'])
SENTIMENT_CONFIG['enabled'] = current_mode['sentiment']
LLM_CONFIG['enabled'] = current_mode['llm']

# ========== CONFIGURACIÓN DEL CHATBOT ==========
CHATBOT_CONFIG = {
    'nombre': 'SciTech Bot',
    'version': '3.0',
    'idioma': 'es',
    'max_historial': 50,  # Máximo de mensajes en historial
    'timeout_sesion': 1800,  # 30 minutos en segundos
}

# ========== TEMAS CIENTÍFICOS ==========
TEMAS_DISPONIBLES = {
    'ia': {
        'nombre': 'Inteligencia Artificial',
        'emoji': '🤖',
        'keywords': ['ia', 'ai', 'inteligencia', 'artificial', 'chatgpt', 'robot']
    },
    'espacio': {
        'nombre': 'Exploración Espacial',
        'emoji': '🚀',
        'keywords': ['espacio', 'nasa', 'marte', 'james webb', 'spacex']
    },
    'computacion': {
        'nombre': 'Computación',
        'emoji': '💻',
        'keywords': ['cuántica', 'quantum', 'computación', 'procesador', 'chip']
    },
    'medicina': {
        'nombre': 'Medicina y Biotecnología',
        'emoji': '🧬',
        'keywords': ['medicina', 'crispr', 'genética', 'cáncer', 'adn']
    },
    'energia': {
        'nombre': 'Energía y Clima',
        'emoji': '⚡',
        'keywords': ['energía', 'fusión', 'nuclear', 'batería', 'solar']
    },
    'blockchain': {
        'nombre': 'Blockchain y Web3',
        'emoji': '🔗',
        'keywords': ['blockchain', 'bitcoin', 'crypto', 'nft', 'web3']
    }
}

# ========== MENSAJES DEL SISTEMA ==========
SYSTEM_MESSAGES = {
    'bienvenida': (
        f"¡Hola! 👋 Bienvenido a {CHATBOT_CONFIG['nombre']} v{CHATBOT_CONFIG['version']}\n\n"
        "Soy tu asistente especializado en ciencia y tecnología.\n"
        "Modo actual: " + current_mode['description']
    ),
    'despedida': "¡Hasta pronto! Gracias por usar el chatbot de ciencia y tecnología. 👋",
    'error_generico': "Ocurrió un error. Por favor, intenta reformular tu pregunta.",
}

# ========== LOGGING ==========
LOG_CONFIG = {
    'log_sentiments': DEBUG_MODE,
    'log_llm_calls': DEBUG_MODE,
    'log_errors': True,
}

# ========== LÍMITES Y RESTRICCIONES ==========
LIMITS = {
    'max_message_length': 1000,
    'min_message_length': 2,
    'max_tokens_llm': 300,
    'rate_limit_messages': 100,  # Mensajes por sesión
}


def get_config_summary():
    """Retorna un resumen de la configuración actual."""
    return {
        'modo': OPERATION_MODE,
        'descripcion': current_mode['description'],
        'sentiment_enabled': SENTIMENT_CONFIG['enabled'],
        'llm_enabled': LLM_CONFIG['enabled'],
        'chatbot': CHATBOT_CONFIG,
    }


def print_config():
    """Imprime la configuración actual del sistema."""
    print("=" * 60)
    print(f"🤖 {CHATBOT_CONFIG['nombre']} v{CHATBOT_CONFIG['version']}")
    print("=" * 60)
    print(f"Modo de operación: {OPERATION_MODE}")
    print(f"Descripción: {current_mode['description']}")
    print(f"Análisis de sentimientos: {'✅ Activado' if SENTIMENT_CONFIG['enabled'] else '❌ Desactivado'}")
    print(f"Modelo LLM: {'✅ Activado' if LLM_CONFIG['enabled'] else '❌ Desactivado'}")
    print(f"Debug: {'✅' if DEBUG_MODE else '❌'}")
    print("=" * 60)


if __name__ == "__main__":
    # Mostrar configuración cuando se ejecuta el archivo
    print_config()
    print("\nResumen de configuración:")
    import json
    print(json.dumps(get_config_summary(), indent=2, ensure_ascii=False))
