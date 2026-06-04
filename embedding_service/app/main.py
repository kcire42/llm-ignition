from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from shared.logger_config import setup_logger


app = FastAPI()
Instrumentator().instrument(app).expose(app) # Instrumentar el router para Prometheus

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para procesar cada solicitud HTTP."""
    response = await call_next(request)
    
    # Ahora esto funcionará perfecto sin romper el formato
    logger.info(f"Request: {request.method} {request.url} - Response status: {response.status_code}")
    
    return response