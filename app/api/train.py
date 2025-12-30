from fastapi import APIRouter
from RAG.trainData import trainRagData

trainRouter = APIRouter(prefix='/train')

@trainRouter.post('/')
async def train_rag():
    trainRagData()
    return {"status": "RAG training completed."}