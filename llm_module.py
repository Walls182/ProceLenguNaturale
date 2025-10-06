"""
Módulo de integración con modelo LLM Gemma de Google
Genera respuestas más naturales y contextuales usando el modelo Gemma-2b-it
"""

import os

try:
    from huggingface_hub import login
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("⚠️ transformers o huggingface_hub no están instalados.")
    print("Ejecuta: pip install transformers huggingface_hub torch")


class GemmaLLM:
    """
    Clase para interactuar con el modelo Gemma-2b-it de Google.
    Genera respuestas contextuales y naturales.
    """
    
    def __init__(self, hf_token=None, model_name="google/gemma-2b-it", load_on_init=False):
        """
        Inicializa el modelo Gemma.
        
        Args:
            hf_token (str): Token de HuggingFace (opcional si está en env)
            model_name (str): Nombre del modelo a cargar
            load_on_init (bool): Si cargar el modelo inmediatamente
        """
        self.model_name = model_name
        self.hf_token = hf_token or os.getenv('HUGGINGFACE_TOKEN')
        self.model = None
        self.tokenizer = None
        self.enabled = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if not LLM_AVAILABLE:
            print("⚠️ Dependencias de LLM no disponibles")
            return
        
        if load_on_init:
            self.load_model()
    
    def load_model(self):
        """Carga el modelo y tokenizer de HuggingFace."""
        if not LLM_AVAILABLE:
            print("⚠️ No se pueden cargar las dependencias de LLM")
            return False
        
        try:
            print(f"🔄 Cargando modelo {self.model_name}...")
            
            # Login a HuggingFace si hay token
            if self.hf_token:
                login(self.hf_token)
                print("✅ Autenticado en HuggingFace")
            
            # Cargar tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_auth_token=self.hf_token if self.hf_token else None
            )
            
            # Cargar modelo
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                use_auth_token=self.hf_token if self.hf_token else None,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            self.enabled = True
            print(f"✅ Modelo cargado en {self.device}")
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar el modelo: {e}")
            self.enabled = False
            return False
    
    def generar_respuesta(self, prompt, max_length=200, temperature=0.7, top_p=0.9):
        """
        Genera una respuesta usando el modelo Gemma.
        
        Args:
            prompt (str): Prompt de entrada
            max_length (int): Longitud máxima de la respuesta
            temperature (float): Control de creatividad (0.0-1.0)
            top_p (float): Muestreo nucleus (0.0-1.0)
            
        Returns:
            str: Respuesta generada o None si hay error
        """
        if not self.enabled:
            return None
        
        try:
            # Tokenizar entrada
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            # Generar respuesta
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decodificar respuesta
            respuesta = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Limpiar el prompt de la respuesta
            if respuesta.startswith(prompt):
                respuesta = respuesta[len(prompt):].strip()
            
            return respuesta
            
        except Exception as e:
            print(f"Error al generar respuesta: {e}")
            return None
    
    def generar_respuesta_cientifica(self, tema, pregunta_usuario, contexto=None):
        """
        Genera una respuesta científica específica usando el modelo.
        
        Args:
            tema (str): Tema científico (IA, espacio, medicina, etc.)
            pregunta_usuario (str): Pregunta del usuario
            contexto (str): Contexto adicional opcional
            
        Returns:
            str: Respuesta generada
        """
        # Construir prompt especializado
        prompt = f"""Eres un asistente experto en ciencia y tecnología. Responde de manera clara, precisa y académica.

Tema: {tema}
Pregunta del usuario: {pregunta_usuario}
"""
        
        if contexto:
            prompt += f"\nContexto adicional: {contexto}\n"
        
        prompt += "\nRespuesta:"
        
        return self.generar_respuesta(prompt, max_length=250, temperature=0.6)
    
    def mejorar_respuesta(self, respuesta_base, sentimiento_usuario=None):
        """
        Mejora una respuesta base usando el modelo LLM.
        
        Args:
            respuesta_base (str): Respuesta original del chatbot
            sentimiento_usuario (str): Sentimiento del usuario (POS/NEG/NEU)
            
        Returns:
            str: Respuesta mejorada
        """
        tono = {
            'POS': 'entusiasta y motivador',
            'NEG': 'empático y comprensivo',
            'NEU': 'profesional y claro'
        }.get(sentimiento_usuario, 'profesional y claro')
        
        prompt = f"""Mejora esta respuesta de chatbot sobre ciencia y tecnología.
Debe ser {tono}, concisa y mantener el contenido técnico.

Respuesta original:
{respuesta_base}

Respuesta mejorada:"""
        
        respuesta_mejorada = self.generar_respuesta(prompt, max_length=300, temperature=0.5)
        
        # Si falla o es demasiado corta, devolver la original
        if not respuesta_mejorada or len(respuesta_mejorada) < 20:
            return respuesta_base
        
        return respuesta_mejorada
    
    def unload_model(self):
        """Descarga el modelo de la memoria."""
        if self.model:
            del self.model
            del self.tokenizer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.model = None
            self.tokenizer = None
            self.enabled = False
            print("✅ Modelo descargado de la memoria")


# Instancia global del modelo
_gemma_llm = None

def get_gemma_llm(auto_load=False):
    """
    Obtiene la instancia global del modelo Gemma.
    
    Args:
        auto_load (bool): Si cargar el modelo automáticamente
        
    Returns:
        GemmaLLM: Instancia del modelo
    """
    global _gemma_llm
    if _gemma_llm is None:
        _gemma_llm = GemmaLLM(load_on_init=auto_load)
    return _gemma_llm


# Función de utilidad para generación rápida
def generar_respuesta_llm(prompt, max_length=200):
    """
    Función de utilidad para generar respuestas rápidas.
    
    Args:
        prompt (str): Prompt de entrada
        max_length (int): Longitud máxima
        
    Returns:
        str: Respuesta generada o None
    """
    llm = get_gemma_llm()
    if not llm.enabled:
        llm.load_model()
    
    return llm.generar_respuesta(prompt, max_length=max_length)


if __name__ == "__main__":
    # Pruebas del módulo
    print("=== Prueba del Módulo LLM Gemma ===\n")
    print("⚠️ NOTA: El modelo requiere ~5GB de RAM y puede tardar en cargar\n")
    
    # Crear instancia sin cargar
    llm = GemmaLLM(load_on_init=False)
    
    if not LLM_AVAILABLE:
        print("❌ Dependencias no disponibles. Instala: pip install transformers huggingface_hub torch")
        exit(1)
    
    respuesta = input("¿Deseas cargar el modelo para pruebas? (s/n): ")
    
    if respuesta.lower() == 's':
        if llm.load_model():
            print("\n--- Prueba 1: Respuesta científica ---")
            respuesta = llm.generar_respuesta_cientifica(
                tema="Inteligencia Artificial",
                pregunta_usuario="¿Qué es ChatGPT?",
                contexto="El usuario está aprendiendo sobre IA"
            )
            print(f"Respuesta: {respuesta}\n")
            
            print("--- Prueba 2: Mejora de respuesta ---")
            base = "ChatGPT es un modelo de lenguaje. Fue creado por OpenAI."
            mejorada = llm.mejorar_respuesta(base, sentimiento_usuario='POS')
            print(f"Original: {base}")
            print(f"Mejorada: {mejorada}\n")
        else:
            print("❌ No se pudo cargar el modelo")
    else:
        print("Pruebas canceladas")
