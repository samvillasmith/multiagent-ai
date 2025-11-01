from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from typing import List 
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings 
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="Multiagent")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request for model: {request.model}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model")
    
    try: 
        response = get_response_from_ai_agents(
            request.model_name,
            request.system_prompt,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Successfully got response from AI agent {request.model_name}")

        return {"response": response}
    
    except Exception as e:
        logger.error("An error occurred during response generation")
        raise HTTPException(status_code=500, detail=str(CustomException("Error generating response", e)))