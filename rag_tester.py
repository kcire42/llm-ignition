import requests
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from ignition_gateway_scripts.LLM_Integration.config import CHROMA_COLLECTION_NAME, LLM_HOST, CHROMA_PORT, MODEL_NAME, OLLAMA_API_URL

def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]


def buscar_contexto(query):
    #print(f"Buscando contexto para la consulta: {query}")
    
    try:
        # Usamos el cliente oficial en lugar de requests manual para evitar el error 405
        chroma_client = chromadb.HttpClient(host=LLM_HOST, port=CHROMA_PORT)
        
        # Necesitamos el modelo de embedding para que Chroma sepa qué buscar
        embedding_model = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')
        
        vector_store = Chroma(
            client=chroma_client,
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=embedding_model
        )
        
        # Realizamos la búsqueda
        results = vector_store.similarity_search(query, k=3)
        
        contexto = "\n---\n".join([doc.page_content for doc in results])
        #print(f"    ✅ Contexto recuperado: {len(results)} fragmentos.")
        prompt = f"""
                You are a technical documentation assistant for Ignition Smart Factory.

                STRICT RULES:
                - Answer ONLY with concrete, actionable steps.
                - Use short, clear bullet points.
                - Do NOT explain sections, guides, or assumptions.
                - Do NOT mention document sections or numbers.
                - Do NOT add commentary or meta explanations.
                - Do NOT repeat the question.
                - Do NOT include information not present in the context.

                FORMAT:
                - Start directly with the steps.
                - Maximum 7 steps.
                - Each step must start with an action verb.

                Question:
                {query}

                Context:
                {contexto}

                Answer:
                """
        return ask_llm(prompt)

    except Exception as e:
        #print(f"ERROR al consultar ChromaDB: {e}")
        return 'Fail'

# --- EJEMPLO DE PRUEBA ---
if __name__ == "__main__":
    pregunta_de_prueba = "List the steps to create Zone Group tags in Ignition Smart Factory."
    
    print("\n==============================================")
    print(f"🌐 INICIANDO PRUEBA RAG para pregunta")
    print("==============================================")
    
    respuesta = buscar_contexto(pregunta_de_prueba)
    
    print("\n==============================================")
    print("🤖 RESPUESTA FINAL DEL LLM:")
    print("==============================================")
    print(respuesta)
    print("==============================================")