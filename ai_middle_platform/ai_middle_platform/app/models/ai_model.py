## app/models/ai_model.py
"""
AI Model data models for the AI Middleware Platform.

This module defines the data models for AI models, including their capabilities,
configuration, and invocation interface. These models are used for both database
storage and API serialization.
"""

from typing import Dict, List, Any, Optional
from sqlalchemy import Column, String, Text, JSON
from pydantic import BaseModel, Field

from app.db.base import Base


class AIModelDB(Base):
    """
    Database model for AI models.
    
    This model represents an AI model stored in the database with its configuration
    and capabilities.
    """
    
    __tablename__ = "ai_models"
    
    model_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    capabilities = Column(JSON, nullable=False)  # List of strings
    config = Column(JSON, nullable=False)  # Configuration dictionary


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

