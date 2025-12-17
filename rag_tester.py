# rag_tester.py
import requests
import json
from ignition_gateway_scripts.LLM_Integration.config import CHROMA_API_URL, CHROMA_COLLECTION_NAME, REQUEST_TIMEOUT_SECONDS, LLM_HOST, CHROMA_PORT, OLLAMA_API_URL, MODEL_NAME

# Función para buscar contexto en ChromaDB
def buscar_contexto(query):
    print(f"\n[1] Buscando contexto relevante para: '{query}'...")
    
    search_url = f"{CHROMA_API_URL}/api/v1/collections/{CHROMA_COLLECTION_NAME}/query"
    
    payload = {
        "query_text": [query], 
        "n_results": 4, 
        "include": ["documents", "metadatas"] 
    }

    try:
        response = requests.post(
            search_url, 
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status() 

        results = response.json().get("documents", [[]])[0]
        contexto = "\n---\n".join(results)
        
        print(f"    ✅ Contexto recuperado: {len(results)} fragmentos.")
        return contexto
            
    except requests.exceptions.RequestException as e:
        print(f"    ❌ ERROR al conectar o consultar ChromaDB. Detalle: {e}")
        return None

# Función para generar la respuesta RAG
def generar_respuesta_rag(user_query):
    contexto = buscar_contexto(user_query)
    
    if not contexto:
        return "ERROR: Falló la recuperación del contexto desde ChromaDB."

    # Construcción del Prompt Aumentado
    system_prompt_template = (
        "Eres un asistente experto en sistemas SCADA. "
        "Responde a la siguiente pregunta del usuario **únicamente basándote en el contexto proporcionado** "
        "entre los delimitadores triples (---). Si la pregunta no puede ser respondida con la información "
        "proporcionada, indica que necesitas más información."
        "\n\n---CONTEXTO RELEVADO---\n"
        "{contexto}"
        "\n---FIN CONTEXTO---\n"
    )
    
    final_prompt = system_prompt_template.format(contexto=contexto) + \
                   f"\n\nPREGUNTA DEL USUARIO: {user_query}"

    print("\n[2] Enviando Prompt aumentado a Ollama...")
    
    ollama_payload = {
        "model": MODEL_NAME,
        "prompt": final_prompt,
        "stream": False, 
        "options": {"temperature": 0.1, "num_ctx": 4096}
    }
    
    try:
        response = requests.post(
            OLLAMA_API_URL, 
            data=json.dumps(ollama_payload),
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()

        result = response.json()
        print("    ✅ Respuesta recibida de Ollama.")
        return result.get("response", "Error: Respuesta LLM vacía.")

    except requests.exceptions.RequestException as e:
        print(f"    ❌ ERROR al conectar o consultar Ollama. Detalle: {e}")
        return "Error de Conexión a Ollama."

# --- EJEMPLO DE PRUEBA ---
if __name__ == "__main__":
    pregunta_de_prueba = "¿Cuál son las instrucciones para dividir?"
    
    print("\n==============================================")
    print(f"🌐 INICIANDO PRUEBA RAG para: {pregunta_de_prueba}")
    print("==============================================")
    
    respuesta = generar_respuesta_rag(pregunta_de_prueba)
    
    print("\n==============================================")
    print("🤖 RESPUESTA FINAL DEL LLM:")
    print("==============================================")
    print(respuesta)
    print("==============================================")