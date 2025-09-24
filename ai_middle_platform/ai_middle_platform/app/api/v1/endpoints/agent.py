## app/api/v1/endpoints/agent.py
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4

from app.schemas.agent_schema import (
    AgentCreateSchema,
    AgentSchema,
    AgentUpdateSchema,
    AgentResponseSchema
)
from app.services.agent_runtime import AgentRuntime
from app.models.agent import AgentDB
from app.db.session import get_postgresql_session
from app.utils.logger import logger

router = APIRouter()

# Initialize agent runtime
agent_runtime = AgentRuntime()


@router.post("/", response_model=AgentSchema)
async def create_agent(agent: AgentCreateSchema) -> AgentSchema:
    """
    Create a new agent.
    
    Args:
        agent: Agent creation data
        
    Returns:
        Created agent
    """
    try:
        agent_id = str(uuid4())
        
        # Create database model
        db_agent = AgentDB(
            agent_id=agent_id,
            name=agent.name,
            system_prompt=agent.system_prompt,
            tools=agent.tools,
            memory={}  # Initialize with empty memory
        )
        
        # Save to database
        with get_postgresql_session() as db_session:
            db_session.add(db_agent)
            db_session.commit()
            db_session.refresh(db_agent)
        
        # Reload agents in runtime
        agent_runtime._load_agents()
        
        # Return schema model
        return AgentSchema(
            agent_id=db_agent.agent_id,
            name=db_agent.name,
            system_prompt=db_agent.system_prompt,
            tools=db_agent.tools,
            memory=db_agent.memory
        )
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create agent")


@router.get("/{agent_id}", response_model=AgentSchema)
async def get_agent(agent_id: str) -> AgentSchema:
    """
    Get an agent by ID.
    
    Args:
        agent_id: ID of the agent to retrieve
        
    Returns:
        Agent details
    """
    try:
        with get_postgresql_session() as db_session:
            db_agent = db_session.query(AgentDB).filter(
                AgentDB.agent_id == agent_id
            ).first()
            
            if not db_agent:
                raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
            
            return AgentSchema(
                agent_id=db_agent.agent_id,
                name=db_agent.name,
                system_prompt=db_agent.system_prompt,
                tools=db_agent.tools,
                memory=db_agent.memory
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agent")


@router.put("/{agent_id}", response_model=AgentSchema)
async def update_agent(agent_id: str, agent: AgentUpdateSchema) -> AgentSchema:
    """
    Update an agent.
    
    Args:
        agent_id: ID of the agent to update
        agent: Agent update data
        
    Returns:
        Updated agent
    """
    try:
        with get_postgresql_session() as db_session:
            db_agent = db_session.query(AgentDB).filter(
                AgentDB.agent_id == agent_id
            ).first()
            
            if not db_agent:
                raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
            
            # Update fields if provided
            if agent.name is not None:
                db_agent.name = agent.name
            if agent.system_prompt is not None:
                db_agent.system_prompt = agent.system_prompt
            if agent.tools is not None:
                db_agent.tools = agent.tools
            
            db_session.commit()
            db_session.refresh(db_agent)
            
            # Reload agents in runtime
            agent_runtime._load_agents()
            
            return AgentSchema(
                agent_id=db_agent.agent_id,
                name=db_agent.name,
                system_prompt=db_agent.system_prompt,
                tools=db_agent.tools,
                memory=db_agent.memory
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update agent")


@router.delete("/{agent_id}", response_model=bool)
async def delete_agent(agent_id: str) -> bool:
    """
    Delete an agent.
    
    Args:
        agent_id: ID of the agent to delete
        
    Returns:
        Deletion success
    """
    try:
        with get_postgresql_session() as db_session:
            db_agent = db_session.query(AgentDB).filter(
                AgentDB.agent_id == agent_id
            ).first()
            
            if not db_agent:
                raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
            
            db_session.delete(db_agent)
            db_session.commit()
            
            # Reload agents in runtime
            agent_runtime._load_agents()
            
            return True
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete agent")


@router.post("/{agent_id}/chat", response_model=AgentResponseSchema)
async def chat_with_agent(agent_id: str, message_data: dict) -> AgentResponseSchema:
    """
    Chat with an agent.
    
    Args:
        agent_id: ID of the agent to chat with
        message_data: Message data containing the user's message
        
    Returns:
        Agent response
    """
    try:
        message = message_data.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="Message field is required")
        
        agent_response = agent_runtime.process_message(agent_id, message)
        
        return AgentResponseSchema(
            response=agent_response.response,
            metadata=agent_response.metadata
        )
    except ValueError as e:
        logger.error(f"Error chatting with agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error chatting with agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to chat with agent")

