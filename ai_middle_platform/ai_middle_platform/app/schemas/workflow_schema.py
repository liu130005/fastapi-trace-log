## app/schemas/workflow_schema.py
"""
Workflow schemas for the AI Middleware Platform.

This module defines the Pydantic schemas for workflow operations,
including workflow creation, updating, retrieval, and execution.
These schemas are used for API request/response validation and serialization.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


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

