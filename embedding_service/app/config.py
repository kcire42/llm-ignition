import os 
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent



class Settings:
    PROJECT_NAME: str = "Embedding Service"
    PROJECT_VERSION: str = "1.0.0"
    MODEL_WHISPER: str = "small"
    LLM_SERVICE_URL: str = "http://embedding_service:8000/embedding/"
    #DATA_DIR: Path = Path(os.getenv("DATA_PATH", BASE_DIR / "app" / "Youtube_Extractor" / "data"))
    #MODELS_DIR: Path = Path(os.getenv("MODELS_PATH", BASE_DIR / "app" / "Youtube_Extractor" / "models"))
    MODELS_EMBEDDINGS_REGISTRY = {
        "all-MiniLM-L6-v2": {"max_tokens": 256, "chars_per_token": 4},
        "Gemini Embedding 1B": {"max_tokens": 512, "chars_per_token": 4},
        "Gemini Embedding 2B": {"max_tokens": 512, "chars_per_token": 4},
    }
settings = Settings()

