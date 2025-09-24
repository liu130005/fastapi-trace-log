## app/models/workflow.py
"""
Workflow data models for the AI Middleware Platform.

This module defines the data models for workflows, including their definitions,
execution status, and results. These models are used for both database storage
and API serialization.
"""

from typing import Dict, List, Any, Optional
from sqlalchemy import Column, String, Text, JSON
from pydantic import BaseModel, Field

from app.db.base import Base


class WorkflowDB(Base):
    """
    Database model for workflows.
    
    This model represents a workflow stored in the database with its definition
    and metadata.
    """
    
    __tablename__ = "workflows"
    
    workflow_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nodes = Column(JSON, nullable=False)  # List of node definitions
    edges = Column(JSON, nullable=False)  # List of edge definitions
    variables = Column(JSON, nullable=False)  # Dictionary of workflow variables


class WorkflowDefinition(BaseModel):
    """
    Schema for workflow definition.
    
    This schema defines the structure of a workflow definition, including its
    nodes, edges, and variables.
    """
    
    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    name: str = Field(..., description="Human-readable name of the workflow")
    nodes: List[Dict[str, Any]] = Field(
        ..., 
        description="List of node definitions in the workflow"
    )
    edges: List[Dict[str, Any]] = Field(
        ..., 
        description="List of edge definitions connecting nodes"
    )
    variables: Dict[str, Any] = Field(
        ..., 
        description="Dictionary of workflow variables"
    )
    
    class Config:
        orm_mode = True


class WorkflowSchema(WorkflowDefinition):
    """
    Schema for workflow representation in API responses.
    
    This schema extends the WorkflowDefinition with additional fields that
    may be needed for API responses.
    """
    pass


class WorkflowCreateSchema(BaseModel):
    """
    Schema for creating a new workflow.
    
    This schema defines the structure of data needed to create a new workflow.
    """
    
    name: str = Field(..., description="Human-readable name of the workflow")
    nodes: List[Dict[str, Any]] = Field(
        ..., 
        description="List of node definitions in the workflow"
    )
    edges: List[Dict[str, Any]] = Field(
        ..., 
        description="List of edge definitions connecting nodes"
    )
    variables: Dict[str, Any] = Field(
        ..., 
        description="Dictionary of workflow variables"
    )


class WorkflowUpdateSchema(BaseModel):
    """
    Schema for updating an existing workflow.
    
    This schema defines the structure of data needed to update an existing workflow.
    All fields are optional to allow partial updates.
    """
    
    name: Optional[str] = Field(None, description="Human-readable name of the workflow")
    nodes: Optional[List[Dict[str, Any]]] = Field(
        None, 
        description="List of node definitions in the workflow"
    )
    edges: Optional[List[Dict[str, Any]]] = Field(
        None, 
        description="List of edge definitions connecting nodes"
    )
    variables: Optional[Dict[str, Any]] = Field(
        None, 
        description="Dictionary of workflow variables"
    )


class WorkflowExecutionDB(Base):
    """
    Database model for workflow executions.
    
    This model represents a workflow execution stored in the database with its
    status and result.
    """
    
    __tablename__ = "workflow_executions"
    
    execution_id = Column(String, primary_key=True, index=True)
    workflow_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    result = Column(JSON, nullable=True)  # Execution result data


class WorkflowExecutionSchema(BaseModel):
    """
    Schema for workflow execution representation in API responses.
    
    This schema defines the structure of workflow execution data when it's sent
    to or received from API clients.
    """
    
    execution_id: str = Field(..., description="Unique identifier for the workflow execution")
    workflow_id: str = Field(..., description="Identifier of the workflow being executed")
    status: str = Field(..., description="Current status of the execution (e.g., running, completed, failed)")
    result: Optional[Dict[str, Any]] = Field(None, description="Result of the workflow execution")
    
    class Config:
        orm_mode = True

