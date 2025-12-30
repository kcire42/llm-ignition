import os 

ENV = os.getenv('APP','local')
# ====================
# OLLAMA
# ===================
OLLAMA_HOST = os.getenv('OLLAMA_HOST','localhost' if ENV == 'local' else 'ollama')
OLLAMA_PORT = int(os.getenv('OLLAMA_PORT',11434))
MODEL_NAME = os.getenv('MODEL_NAME','phi3:mini')
OLLAMA_API_URL = f'http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate'


#===================
#EMBEDDINGS
#==================
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME','all-MiniLM-L6-v2')

#===================
#CHROMA
#===================

CHROMA_HOST = os.getenv('CHROMA_HOST','localhost' if ENV == 'local' else 'chroma')
CHROMA_PORT = int(os.getenv('OLLAMA_PORT',11743))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME","Knowledgebase")
CHROMA_API_URL = f'http://{OLLAMA_HOST}:{CHROMA_PORT}'


#=================
#RUNTIME
#================
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", 90))