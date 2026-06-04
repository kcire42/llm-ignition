from pydantic import BaseModel

class EmbeddingText(BaseModel):
    user_id : str
    text : str


class EmbeddingContext(BaseModel):
    context : str
    
