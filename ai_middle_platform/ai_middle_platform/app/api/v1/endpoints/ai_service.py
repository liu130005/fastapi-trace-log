## app/api/v1/endpoints/ai_service.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas.ai_service_schema import AIModelSchema, ModelStatus
from app.services.ai_service_manager import AIServiceManager
from app.utils.logger import logger

router = APIRouter()

# Initialize AI service manager
ai_service_manager = AIServiceManager()


@router.get("/models", response_model=List[AIModelSchema])
async def list_models() -> List[AIModelSchema]:
    """
    List all available AI models.
    
    Returns:
        List of AI models
    """
    try:
        models = ai_service_manager.load_models()
        return [AIModelSchema(
            model_id=model.model_id,
            name=model.name,
            provider=model.provider,
            capabilities=model.capabilities,
            config=model.config
        ) for model in models.values()]
    except Exception as e:
        logger.error(f"Error listing AI models: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve AI models")


@router.get("/models/{model_id}", response_model=AIModelSchema)
async def get_model_info(model_id: str) -> AIModelSchema:
    """
    Get information about a specific AI model.
    
    Args:
        model_id: ID of the model to retrieve
        
    Returns:
        Information about the requested AI model
    """
    try:
        models = ai_service_manager.load_models()
        if model_id not in models:
            raise HTTPException(status_code=404, detail=f"Model with ID {model_id} not found")
        
        model = models[model_id]
        return AIModelSchema(
            model_id=model.model_id,
            name=model.name,
            provider=model.provider,
            capabilities=model.capabilities,
            config=model.config
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving model info for {model_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model information")


@router.post("/models/{model_id}/invoke", response_model=dict)
async def invoke_model(model_id: str, input_data: dict) -> dict:
    """
    Invoke an AI model with the given input data.
    
    Args:
        model_id: ID of the model to invoke
        input_data: Input data for the model
        
    Returns:
        Result from the model invocation
    """
    try:
        result = ai_service_manager.invoke_model(model_id, input_data)
        return result
    except ValueError as e:
        logger.error(f"Error invoking model {model_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error invoking model {model_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to invoke model")

