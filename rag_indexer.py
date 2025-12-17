import os 
import chromadb
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from ignition_gateway_scripts.LLM_Integration.config import CHROMA_API_URL, CHROMA_COLLECTION_NAME, REQUEST_TIMEOUT_SECONDS, LLM_HOST, CHROMA_PORT


DOCS_PATH = './docs_to_index/'
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'



def index_documents():
    print("Loading documents from:", DOCS_PATH)

    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    if not documents:
        print("No documents found to index.")
        return
    
    print(f"Loaded {len(documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", "","."]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    print("Creating embeddings using model:", EMBEDDING_MODEL_NAME)

    try:
        embedding_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    except Exception as e:
        print("Error creating embedding model:", e)
        return
    
    print("Embeddings created successfully.")

    print("Connecting to Chroma vector store at:", CHROMA_API_URL)

    from chromadb.utils import embedding_functions
    from chromadb import Settings

    try:
        chroma_client = chromadb.HttpClient(
            host=LLM_HOST,
            port=CHROMA_PORT
        )
        try:
            chroma_client.delete_collection(name=CHROMA_COLLECTION_NAME)
            print(f"Deleted existing collection: {CHROMA_COLLECTION_NAME}")
        except Exception:
            pass
        
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME,
            client = chroma_client
        )

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=sentence_transformer_ef,
            collection_name=CHROMA_COLLECTION_NAME,
            client=chroma_client
        )

        print(f"Indexed {len(chunks)} document chunks into Chroma collection: {CHROMA_COLLECTION_NAME}")

    except Exception as e:
        print("Error connecting to Chroma or indexing documents:", e)
        return
    
if __name__ == "__main__":
    index_documents()
    print("Document indexing completed.")


