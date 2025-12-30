import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from LLM_Integration.config import CHROMA_COLLECTION_NAME, CHROMA_HOST, CHROMA_PORT, EMBEDDING_MODEL_NAME

_embedding_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def getdocContext(prompt: str) -> str:
    try:
        # Create an HTTP client to connect to the ChromaDB service
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        # Initialize the Chroma vector store with the existing collection
        # and the embedding model used during indexing
        vector_store = Chroma(
            client=chroma_client,
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=_embedding_model
        )
        # Perform a similarity search to retrieve the top-k most relevant documents
        results = vector_store.similarity_search(prompt, k=3)
        # Concatenate the retrieved document contents into a single context string
        docContext = "\n---\n".join([doc.page_content for doc in results])
        return docContext

    except Exception as e:
        print(f"Error retrieving document context: {e}")
        return ""
