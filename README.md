# 🤖 Chatbot de Ciencia y Tecnología v3.0

Chatbot inteligente especializado en noticias y avances de ciencia y tecnología, con **análisis de sentimientos** y capacidades de **IA generativa** opcionales.

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Características Principales

### 🎯 **Funcionalidades Base**
- ✅ Conversación inteligente sobre ciencia y tecnología
- ✅ 6 categorías de temas: IA, Espacio, Computación, Medicina, Energía, Blockchain
- ✅ Validación de entrada y guía contextual
- ✅ Sistema de memoria conversacional
- ✅ Respuestas estructuradas con formato

### 🧠 **Análisis de Sentimientos** (NUEVO en v3.0)
- ✅ Detección automática de emociones (POS/NEG/NEU)
- ✅ Respuestas empáticas adaptadas al estado emocional
- ✅ Confianza y probabilidades del análisis
- ✅ Tono adaptativo según el sentimiento

### 🤖 **IA Generativa** (Opcional - v3.0)
- ✅ Integración con modelo Gemma-2b-it de Google
- ✅ Generación de respuestas naturales y contextuales
- ✅ Mejora automática de respuestas base
- ✅ Adaptación al sentimiento del usuario

---

## 🚀 Instalación Rápida

### Opción 1: Instalación Básica (Recomendada)
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ProceLenguNaturale.git
cd ProceLenguNaturale

# Instalar dependencias básicas
pip install flask flask-cors nltk spacy pysentimiento python-dotenv

# Descargar modelo de español para spaCy
python -m spacy download es_core_news_sm

# Configurar variables de entorno
copy .env.example .env

# Ejecutar
python backend.py
```

### Opción 2: Instalación Completa (con LLM)
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Descargar modelo de español
python -m spacy download es_core_news_sm

# Configurar token de HuggingFace en .env
# Editar .env y agregar: HUGGINGFACE_TOKEN=tu_token_aqui

# Ejecutar
python backend.py
```

---

## 📋 Requisitos

### Básico (Modo `sentiment`)
- Python 3.8+
- 2GB RAM
- Conexión a internet (descarga inicial de modelos)

### Completo (Modo `llm` o `hybrid`)
- Python 3.8+
- 8GB RAM (mínimo 5GB)
- GPU con CUDA (recomendado)
- Token de HuggingFace

---

## ⚙️ Configuración

### Modos de Operación

Edita `config.py` o la variable `OPERATION_MODE` en `.env`:

| Modo | Descripción | Requisitos | Recomendado |
|------|-------------|------------|-------------|
| `basic` | Solo respuestas predefinidas | Bajo | Desarrollo |
| `sentiment` | Con análisis de sentimientos | Medio | ✅ **Producción** |
| `llm` | Generación con IA avanzada | Alto | Investigación |
| `hybrid` | Todo combinado | Alto | Máxima calidad |

### Variables de Entorno (.env)

```bash
# Modo de operación
OPERATION_MODE=sentiment

# Token de HuggingFace (solo si usas LLM)
HUGGINGFACE_TOKEN=tu_token_aqui

# Debug
DEBUG_MODE=False
VERBOSE_LOGGING=False
```

---

## 🎮 Uso

### Iniciar el Backend
```bash
python backend.py
```

El servidor estará disponible en: `http://localhost:5000`

### Probar Módulos Individuales

#### Análisis de Sentimientos
```bash
python sentiment_analyzer.py
```

#### Modelo LLM
```bash
python llm_module.py
```

#### Ver Configuración
```bash
python config.py
```

### API Endpoints

#### POST /chat
Envía un mensaje al chatbot

**Request:**
```json
{
  "mensaje": "Hola, cuéntame sobre inteligencia artificial"
}
```

**Response:**
```json
{
  "respuesta": "¡Hola! 👋 Bienvenido...",
  "tema_actual": "Inteligencia Artificial",
  "estado_conversacion": "activo",
  "sentimiento": {
    "tipo": "positivo",
    "confianza": 95.5
  },
  "temas_discutidos": ["Inteligencia Artificial"],
  "num_mensajes": 1
}
```

#### POST /analisis
Analiza lingüísticamente un texto

**Request:**
```json
{
  "mensaje": "La inteligencia artificial es fascinante"
}
```

---

## 📁 Estructura del Proyecto

```
ProceLenguNaturale/
│
├── backend.py                 # Servidor Flask
├── chatbot_logic.py          # Lógica conversacional principal
├── sentiment_analyzer.py     # Módulo de análisis de sentimientos
├── llm_module.py            # Módulo de IA generativa (Gemma)
├── config.py                # Configuración centralizada
│
├── requirements.txt         # Dependencias del proyecto
├── .env.example            # Template de variables de entorno
├── README.md               # Este archivo
├── MEJORAS_CHATBOT.md      # Documentación detallada de mejoras
│
└── frontend/
    ├── index.html          # Interfaz web
    ├── styles.css          # Estilos
    ├── app.js             # JavaScript del frontend
    └── bg.jpg             # Imagen de fondo
```

---

## 🧪 Ejemplos de Conversación

### Ejemplo 1: Sentimiento Positivo
```
👤 Usuario: ¡Hola! Me encanta aprender sobre IA
🤖 Bot: ¡Genial que te interese este tema! ¡Hola! 👋 Bienvenido...
      [Análisis: Positivo 98%]

👤 Usuario: Cuéntame sobre ChatGPT
🤖 Bot: ¡Me encanta tu entusiasmo! 😊 **ChatGPT y GPT** 🤖
      Son modelos de lenguaje desarrollados por OpenAI...
```

### Ejemplo 2: Sentimiento Negativo
```
👤 Usuario: Esto es muy confuso, no entiendo
🤖 Bot: Lamento que no estés en tu mejor momento. 💙
      Quizás un descubrimiento fascinante te anime...
      [Análisis: Negativo 87%]

👤 Usuario: Explícame de forma simple
🤖 Bot: Entiendo que esto puede ser complicado. 
      **Inteligencia Artificial** 🧠
      [Respuesta simplificada...]
```

### Ejemplo 3: Conversación Completa
```
👤 Usuario: Hola
🤖 Bot: ¡Hola! 👋 Bienvenido al chatbot de ciencia y tecnología.
      [Muestra menú de temas]

👤 Usuario: Quiero saber sobre el espacio
🤖 Bot: **Astronomía y Exploración Espacial** 🌌
      [Información sobre el tema]

👤 Usuario: ¿Qué es el James Webb?
🤖 Bot: **Telescopio Espacial James Webb** 🔭
      El James Webb ha revolucionado la astronomía...

👤 Usuario: ¡Increíble! Gracias
🤖 Bot: ¡De nada! 😊 Me alegra ayudarte con Exploración Espacial.
      ¿Hay otro tema que te gustaría explorar?
```

---

## 🎓 Temas Disponibles

### 🤖 Inteligencia Artificial
- Modelos de lenguaje (ChatGPT, GPT-4, Claude)
- Robótica y automatización
- Machine Learning y Deep Learning
- Aplicaciones de IA en medicina

### 🚀 Exploración Espacial
- Telescopio James Webb
- Misiones a Marte (Perseverance, Curiosity)
- SpaceX y cohetes reutilizables
- Exoplanetas y búsqueda de vida

### 💻 Computación
- Computación cuántica
- Procesadores avanzados
- Semiconductores y chips
- Arquitecturas de hardware

### 🧬 Medicina y Biotecnología
- CRISPR y edición genética
- Terapias génicas
- Tratamientos contra el cáncer
- Medicina personalizada

### ⚡ Energía y Clima
- Fusión nuclear
- Energías renovables (solar, eólica)
- Baterías avanzadas
- Cambio climático

### 🔗 Blockchain y Web3
- Criptomonedas (Bitcoin, Ethereum)
- DeFi y contratos inteligentes
- NFTs y propiedad digital
- Realidad Virtual y Aumentada

---

## 🔧 Desarrollo

### Agregar Nuevos Temas

Edita `chatbot_logic.py`:

```python
# En la función responder(), agregar nuevo bloque:
if any(palabra in tokens for palabra in ["nuevo", "tema", "keywords"]):
    estado['ultimo_tema'] = "Nuevo Tema"
    respuesta = (
        "**Nuevo Tema** 🎯\n\n"
        "Información sobre el nuevo tema...\n\n"
        "¿Te gustaría saber más sobre...?"
    )
    return respuesta
```

### Personalizar Análisis de Sentimientos

Edita `config.py`:

```python
SENTIMENT_CONFIG = {
    'enabled': True,
    'min_confidence': 0.7,  # Ajustar umbral (0.0-1.0)
    'adapt_tone': True,
}
```

### Activar/Desactivar LLM

Edita `config.py`:

```python
LLM_CONFIG = {
    'enabled': True,  # Cambiar a True
    'auto_load': False,  # True para cargar al inicio
    'use_for_enhancement': True,  # Mejora respuestas
}
```

---

## 📊 Rendimiento

### Benchmarks (Intel i5, 8GB RAM)

| Modo | Tiempo de Respuesta | Uso de RAM | CPU |
|------|-------------------|------------|-----|
| basic | ~50ms | 200MB | 5% |
| sentiment | ~150ms | 500MB | 10% |
| llm (CPU) | ~2-5s | 3GB | 80% |
| llm (GPU) | ~500ms | 5GB | 20% |

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **Tu Nombre** - Desarrollo inicial

---

## 🙏 Agradecimientos

- [pysentimiento](https://github.com/pysentimiento/pysentimiento) - Análisis de sentimientos
- [HuggingFace](https://huggingface.co/) - Modelos de IA
- [Google Gemma](https://ai.google.dev/gemma) - Modelo LLM
- [spaCy](https://spacy.io/) - Procesamiento de lenguaje natural
- [Flask](https://flask.palletsprojects.com/) - Framework web

---

## 📞 Soporte

¿Problemas o preguntas?

- 📧 Email: tu@email.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/ProceLenguNaturale/issues)
- 📖 Docs: Ver `MEJORAS_CHATBOT.md`

---

## 🔮 Roadmap

- [ ] Sistema de sesiones múltiples
- [ ] Base de datos para historial
- [ ] API REST completa
- [ ] Interfaz web mejorada
- [ ] Más idiomas (inglés, portugués)
- [ ] Integración con APIs de noticias reales
- [ ] Sistema de recomendaciones personalizadas
- [ ] Deploy en la nube (Heroku, AWS)

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐**

Hecho con ❤️ y mucho ☕

</div>
