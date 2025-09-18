## main.py
import os
import logging
from fastapi import FastAPI
from .trace_middleware import TraceMiddleware
from .logger import TraceLogger
from .config import Config

# Initialize global logger
trace_logger = TraceLogger().get_logger()
config = Config()

# Create FastAPI application
app = FastAPI(
    title="FastAPI Trace Example",
    description="An example FastAPI application with automatic trace_id injection and performance tracing",
    version="1.0.0"
)

# Add TraceMiddleware to the application
# enable_performance=True to auto-create spans for HTTP requests
app.add_middleware(TraceMiddleware, enable_performance=True)

# Example route to demonstrate tracing
@app.get("/")
async def root():
    trace_logger.info("Handling root endpoint request")
    return {"message": "Hello World with tracing!"}

@app.get("/health")
async def health_check():
    trace_logger.info("Health check requested")
    return {"status": "healthy"}

# For development only - auto start server if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "true").lower() in ("true", "1", "yes"),
        log_level="info"
    )
