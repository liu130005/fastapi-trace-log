## app/api/v1/endpoints/workflow.py
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4

from app.schemas.workflow_schema import (
    WorkflowCreateSchema,
    WorkflowSchema,
    WorkflowUpdateSchema,
    WorkflowExecutionSchema
)
from app.services.workflow_engine import WorkflowEngine
from app.models.workflow import WorkflowDB
from app.db.session import get_postgresql_session
from app.utils.logger import logger

router = APIRouter()

# Initialize workflow engine
workflow_engine = WorkflowEngine()


@router.post("/", response_model=WorkflowSchema)
async def create_workflow(workflow: WorkflowCreateSchema) -> WorkflowSchema:
    """
    Create a new workflow.
    
    Args:
        workflow: Workflow creation data
        
    Returns:
        Created workflow
    """
    try:
        workflow_id = str(uuid4())
        
        # Create database model
        db_workflow = WorkflowDB(
            workflow_id=workflow_id,
            name=workflow.name,
            nodes=workflow.nodes,
            edges=workflow.edges,
            variables=workflow.variables
        )
        
        # Save to database
        with get_postgresql_session() as db_session:
            db_session.add(db_workflow)
            db_session.commit()
            db_session.refresh(db_workflow)
        
        # Return schema model
        return WorkflowSchema(
            workflow_id=db_workflow.workflow_id,
            name=db_workflow.name,
            nodes=db_workflow.nodes,
            edges=db_workflow.edges,
            variables=db_workflow.variables
        )
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create workflow")


@router.get("/{workflow_id}", response_model=WorkflowSchema)
async def get_workflow(workflow_id: str) -> WorkflowSchema:
    """
    Get a workflow by ID.
    
    Args:
        workflow_id: ID of the workflow to retrieve
        
    Returns:
        Workflow details
    """
    try:
        with get_postgresql_session() as db_session:
            db_workflow = db_session.query(WorkflowDB).filter(
                WorkflowDB.workflow_id == workflow_id
            ).first()
            
            if not db_workflow:
                raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
            
            return WorkflowSchema(
                workflow_id=db_workflow.workflow_id,
                name=db_workflow.name,
                nodes=db_workflow.nodes,
                edges=db_workflow.edges,
                variables=db_workflow.variables
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve workflow")


@router.put("/{workflow_id}", response_model=WorkflowSchema)
async def update_workflow(workflow_id: str, workflow: WorkflowUpdateSchema) -> WorkflowSchema:
    """
    Update a workflow.
    
    Args:
        workflow_id: ID of the workflow to update
        workflow: Workflow update data
        
    Returns:
        Updated workflow
    """
    try:
        with get_postgresql_session() as db_session:
            db_workflow = db_session.query(WorkflowDB).filter(
                WorkflowDB.workflow_id == workflow_id
            ).first()
            
            if not db_workflow:
                raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
            
            # Update fields if provided
            if workflow.name is not None:
                db_workflow.name = workflow.name
            if workflow.nodes is not None:
                db_workflow.nodes = workflow.nodes
            if workflow.edges is not None:
                db_workflow.edges = workflow.edges
            if workflow.variables is not None:
                db_workflow.variables = workflow.variables
            
            db_session.commit()
            db_session.refresh(db_workflow)
            
            return WorkflowSchema(
                workflow_id=db_workflow.workflow_id,
                name=db_workflow.name,
                nodes=db_workflow.nodes,
                edges=db_workflow.edges,
                variables=db_workflow.variables
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update workflow")


@router.delete("/{workflow_id}", response_model=bool)
async def delete_workflow(workflow_id: str) -> bool:
    """
    Delete a workflow.
    
    Args:
        workflow_id: ID of the workflow to delete
        
    Returns:
        Deletion success
    """
    try:
        with get_postgresql_session() as db_session:
            db_workflow = db_session.query(WorkflowDB).filter(
                WorkflowDB.workflow_id == workflow_id
            ).first()
            
            if not db_workflow:
                raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
            
            db_session.delete(db_workflow)
            db_session.commit()
            
            return True
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete workflow")


@router.post("/{workflow_id}/execute", response_model=WorkflowExecutionSchema)
async def execute_workflow(workflow_id: str, input_data: dict) -> WorkflowExecutionSchema:
    """
    Execute a workflow.
    
    Args:
        workflow_id: ID of the workflow to execute
        input_data: Input data for the workflow execution
        
    Returns:
        Workflow execution result
    """
    try:
        execution_result = workflow_engine.execute_workflow(workflow_id, input_data)
        
        return WorkflowExecutionSchema(
            execution_id=execution_result.execution_id,
            workflow_id=execution_result.workflow_id,
            status=execution_result.status,
            result=execution_result.result
        )
    except ValueError as e:
        logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to execute workflow")

