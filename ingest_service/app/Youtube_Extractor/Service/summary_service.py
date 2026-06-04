import httpx
import logging
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_summary_from_llm(transcription_text: str):
    """Envía la transcripción al LLM Service para obtener un resumen."""
    async with httpx.AsyncClient(timeout=60.0) as client: # Timeout largo por ser un LLM
        try:
            response = await client.post(settings.LLM_SERVICE_URL, json={"text": transcription_text,"llm_resource": True })
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"✅ Respuesta del LLM Service: {data}")
            return data.get("text")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Error del LLM Service: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error de conexión con LLM Service: {e}")
            return None
    