"""
Script de inicio rápido para el Chatbot de Ciencia y Tecnología v3.0
Verifica dependencias, muestra configuración e inicia el chatbot
"""

import sys
import os

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...\n")
    
    missing = []
    dependencies = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'nltk': 'NLTK',
        'spacy': 'spaCy',
    }
    
    optional = {
        'pysentimiento': 'pysentimiento (Análisis de Sentimientos)',
        'transformers': 'transformers (Modelo LLM)',
        'torch': 'PyTorch (Modelo LLM)',
    }
    
    # Verificar dependencias básicas
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NO INSTALADO")
            missing.append(module)
    
    print("\n📦 Dependencias opcionales:")
    # Verificar dependencias opcionales
    for module, name in optional.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"⚠️  {name} - No instalado (opcional)")
    
    if missing:
        print(f"\n❌ Faltan dependencias básicas: {', '.join(missing)}")
        print("\n💡 Instala con: pip install " + " ".join(missing))
        return False
    
    return True


def check_spacy_model():
    """Verifica que el modelo de español de spaCy esté instalado."""
    print("\n🔍 Verificando modelo de spaCy...")
    try:
        import spacy
        nlp = spacy.load("es_core_news_sm")
        print("✅ Modelo es_core_news_sm instalado")
        return True
    except OSError:
        print("❌ Modelo es_core_news_sm NO instalado")
        print("\n💡 Instala con: python -m spacy download es_core_news_sm")
        return False


def download_nltk_data():
    """Descarga datos necesarios de NLTK."""
    print("\n📥 Verificando datos de NLTK...")
    import nltk
    
    try:
        nltk.data.find('tokenizers/punkt')
        print("✅ Datos de NLTK disponibles")
    except LookupError:
        print("📥 Descargando datos de NLTK...")
        nltk.download('punkt')
        nltk.download('wordnet')
        print("✅ Datos descargados")


def show_config():
    """Muestra la configuración actual."""
    print("\n" + "="*60)
    print("⚙️  CONFIGURACIÓN DEL CHATBOT")
    print("="*60)
    
    try:
        from config import print_config
        print_config()
    except ImportError:
        print("⚠️  Archivo config.py no encontrado")
        print("Usando configuración por defecto")


def create_env_file():
    """Crea archivo .env si no existe."""
    if not os.path.exists('.env'):
        print("\n📝 Creando archivo .env...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Archivo .env creado desde .env.example")
            print("💡 Edita .env para configurar el chatbot")
        else:
            with open('.env', 'w') as f:
                f.write("# Configuración del chatbot\n")
                f.write("OPERATION_MODE=sentiment\n")
                f.write("DEBUG_MODE=False\n")
            print("✅ Archivo .env creado con configuración básica")
    else:
        print("\n✅ Archivo .env existe")


def start_chatbot():
    """Inicia el chatbot."""
    print("\n" + "="*60)
    print("🚀 INICIANDO CHATBOT")
    print("="*60)
    print("\n💡 El chatbot estará disponible en: http://localhost:5000")
    print("💡 Para detenerlo, presiona Ctrl+C")
    print("\n" + "="*60 + "\n")
    
    # Importar y ejecutar backend
    try:
        from backend import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot detenido. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error al iniciar el chatbot: {e}")
        print("\n💡 Verifica que todas las dependencias estén instaladas")


def main():
    """Función principal."""
    print("="*60)
    print("🤖 CHATBOT DE CIENCIA Y TECNOLOGÍA v3.0")
    print("="*60)
    
    # 1. Verificar dependencias
    if not check_dependencies():
        print("\n❌ Faltan dependencias. Instálalas e intenta de nuevo.")
        sys.exit(1)
    
    # 2. Verificar modelo de spaCy
    if not check_spacy_model():
        print("\n❌ Falta el modelo de spaCy. Instálalo e intenta de nuevo.")
        sys.exit(1)
    
    # 3. Descargar datos de NLTK
    download_nltk_data()
    
    # 4. Crear archivo .env
    create_env_file()
    
    # 5. Mostrar configuración
    show_config()
    
    # 6. Preguntar si iniciar
    print("\n" + "="*60)
    respuesta = input("\n¿Iniciar el chatbot? (s/n): ").lower()
    
    if respuesta == 's' or respuesta == 'si' or respuesta == 'yes' or respuesta == 'y':
        start_chatbot()
    else:
        print("\n👋 Chatbot no iniciado. Ejecuta este script cuando estés listo.")
        print("\n💡 Para iniciar manualmente: python backend.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Instalación cancelada. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
