## app/schemas/ai_service_schema.py
"""
AI Service schemas for the AI Middleware Platform.

This module defines the Pydantic schemas for AI service operations,
including model listing, model information retrieval, and model invocation.
These schemas are used for API request/response validation and serialization.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class AIModelSchema(BaseModel):
    """
    Pydantic schema for AI model representation in API responses.
    
    This schema defines the structure of AI model data when it's sent to or
    received from API clients.
    """
    
    model_id: str = Field(..., description="Unique identifier for the AI model")
    name: str = Field(..., description="Human-readable name of the AI model")
    provider: str = Field(..., description="Provider of the AI model (e.g., OpenAI, Hugging Face)")
    capabilities: List[str] = Field(
        ..., 
        description="List of capabilities supported by this model"
    )
    config: Dict[str, Any] = Field(
        ..., 
        description="Configuration parameters for the AI model"
    )
    
    class Config:
        orm_mode = True


class ModelStatus(BaseModel):
    """
    Schema for representing the status of an AI model.
    
    This schema is used to communicate the current status of a model,
    including its availability and health.
    """
    
    model_id: str = Field(..., description="Unique identifier for the AI model")
    status: str = Field(..., description="Current status of the model (e.g., available, loading, error)")
    details: Optional[str] = Field(None, description="Additional details about the model status")
    
    class Config:
        orm_mode = True

