from fastapi import APIRouter
from app.api.models import *

embeddingRouter = APIRouter(prefix='/embedding')

@embeddingRouter.post('/')
async def create_embedding(request: EmbeddingText):
    pass


@embeddingRouter.get('/context')
async def get_embedding_context(request: EmbeddingContext):
    pass




