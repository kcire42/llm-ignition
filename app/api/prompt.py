from fastapi import APIRouter
from LLM_Integration.LLMPrompt import getLLMResponse

questionRouter = APIRouter(prefix='/ask')

@questionRouter.post('/')
async def ask_question(prompt: str):
    answer = getLLMResponse(prompt)
    return {"answer": answer}