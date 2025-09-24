## app/core/config.py
from typing import Optional
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """
    Configuration settings for the AI Middleware Platform.
    
    This class defines all the configuration parameters needed for the application,
    including API settings, database connections, Redis configuration, and logging.
    """
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="Host for the API server")
    api_port: int = Field(default=8000, description="Port for the API server")
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/ai_middleware",
        description="PostgreSQL database connection URL"
    )
    mongodb_url: str = Field(
        default="mongodb://localhost:27017/ai_middleware",
        description="MongoDB connection URL"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    
    # Security Configuration
    secret_key: str = Field(
        default="your-secret-key-here",
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(
        default="HS256",
        description="Algorithm used for JWT token encoding"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Expiration time for access tokens in minutes"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    log_file_path: Optional[str] = Field(
        default=None,
        description="Path to the log file (if not set, logs to console)"
    )
    
    # AI Model Configuration
    model_cache_expiration: int = Field(
        default=3600,
        description="Cache expiration time for AI models in seconds"
    )
    
    # Workflow Configuration
    workflow_execution_timeout: int = Field(
        default=300,
        description="Maximum execution time for workflows in seconds"
    )
    
    # Monitoring Configuration
    monitoring_enabled: bool = Field(
        default=True,
        description="Enable or disable performance monitoring"
    )
    
    class Config:
        env_prefix = "AI_MIDDLEWARE_"
        case_sensitive = False

# Create a global instance of the configuration
config = Config()

