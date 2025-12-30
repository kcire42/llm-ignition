from fastapi import FastAPI, Request
from app.api.prompt import questionRouter
from app.api.train import trainRouter
import logging

app = FastAPI()

app.include_router(questionRouter)
app.include_router(trainRouter)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para procesar cada solicitud HTTP."""
    logger = logging.getLogger("uvicorn.access")
    response = await call_next(request)
    logger.info(f"Request: {request.method} {request.url} - Response status: {response.status_code}")
    return response