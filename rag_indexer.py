import os 
import chromadb
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from ignition_gateway_scripts.LLM_Integration.config import CHROMA_API_URL, CHROMA_COLLECTION_NAME, REQUEST_TIMEOUT_SECONDS, LLM_HOST, CHROMA_PORT


# =========================
# CONFIGURACIÓN GENERAL
# =========================

# Ruta donde se encuentran los documentos PDF que se van a indexar
DOCS_PATH = './docs_to_index/'

# Modelo de embeddings a utilizar (Sentence Transformers)
# all-MiniLM-L6-v2 es ligero, rápido y muy usado para RAG
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'


# =========================
# FUNCIÓN PRINCIPAL
# =========================

def index_documents():
    """
    Carga documentos PDF desde un directorio,
    los divide en fragmentos (chunks),
    genera embeddings
    y los indexa en una base vectorial Chroma.
    """

    # ---- CARGA DE DOCUMENTOS ----
    print("Loading documents from:", DOCS_PATH)

    # DirectoryLoader recorre el directorio y subdirectorios
    # y carga únicamente archivos PDF usando PyPDFLoader
    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    # Cargar los documentos en memoria
    documents = loader.load()

    # Validación: si no hay documentos, se termina el proceso
    if not documents:
        print("No documents found to index.")
        return
    
    print(f"Loaded {len(documents)} documents.")

    # ---- DIVISIÓN DEL TEXTO EN CHUNKS ----
    # Se divide el texto para que los embeddings tengan contexto manejable
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # Tamaño máximo de cada fragmento
        chunk_overlap=120,      # Texto compartido entre fragmentos
        separators=["\n\n", "\n", " ", "", "."]  # Orden de separación
    )

    # Genera los fragmentos a partir de los documentos originales
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    # ---- CREACIÓN DE EMBEDDINGS ----
    print("Creating embeddings using model:", EMBEDDING_MODEL_NAME)

    try:
        # Inicializa el modelo de embeddings
        embedding_model = SentenceTransformerEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )
    except Exception as e:
        print("Error creating embedding model:", e)
        return
    
    print("Embeddings created successfully.")

    # ---- CONEXIÓN A CHROMA ----
    print("Connecting to Chroma vector store at:", CHROMA_API_URL)

    from chromadb.utils import embedding_functions
    from chromadb import Settings

    try:
        # Cliente HTTP para conectarse a Chroma (servidor externo)
        chroma_client = chromadb.HttpClient(
            host=LLM_HOST,
            port=CHROMA_PORT
        )

        # Intenta eliminar la colección existente
        # (útil para reindexar desde cero)
        try:
            chroma_client.delete_collection(
                name=CHROMA_COLLECTION_NAME
            )
            print(f"Deleted existing collection: {CHROMA_COLLECTION_NAME}")
        except Exception:
            # Si no existe la colección, se ignora el error
            pass

        # ---- INDEXACIÓN EN CHROMA ----
        vector_store = Chroma.from_documents(
            documents=chunks,                   # Fragmentos de texto
            embedding=embedding_model,          # Modelo de embeddings
            collection_name=CHROMA_COLLECTION_NAME,
            client=chroma_client
        )

        print(f"✅ SUCCESS: Indexed {len(chunks)} chunks into Chroma.")

    except Exception as e:
        print("Error connecting to Chroma or indexing documents:", e)
        return


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    index_documents()
    print("Document indexing completed.")