## main.py
"""
Main application entry point for the AI Middleware Platform.

This module initializes and starts the FastAPI application server,
configuring all routes, middleware, and dependencies required for
the AI Middleware Platform to operate.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config
from app.db.session import db_manager
from app.api.v1.endpoints import ai_service, workflow, agent, function_calling
from app.utils.logger import logger


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance.
    """
    # Initialize FastAPI app
    app = FastAPI(
        title="AI Middleware Platform",
        description="A platform for managing AI models, workflows, agents, and function calling",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(
        ai_service.router,
        prefix="/api/v1/ai",
        tags=["AI Services"]
    )
    
    app.include_router(
        workflow.router,
        prefix="/api/v1/workflows",
        tags=["Workflows"]
    )
    
    app.include_router(
        agent.router,
        prefix="/api/v1/agents",
        tags=["Agents"]
    )
    
    app.include_router(
        function_calling.router,
        prefix="/api/v1/functions",
        tags=["Function Calling"]
    )
    
    # Create database tables
    db_manager.create_postgresql_tables()
    
    return app


def main() -> None:
    """
    Main function to start the AI Middleware Platform server.
    
    This function initializes the application and starts the Uvicorn server
    with the configured settings.
    """
    logger.info("Starting AI Middleware Platform")
    
    # Create the FastAPI app
    app = create_app()
    
    # Start the Uvicorn server
    try:
        uvicorn.run(
            app,
            host=config.api_host,
            port=config.api_port,
            log_level=config.log_level.lower()
        )
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down gracefully")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
    finally:
        # Close database connections
        db_manager.close_connections()
        logger.info("AI Middleware Platform shutdown complete")


if __name__ == "__main__":
    main()

