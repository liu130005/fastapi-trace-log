## app/utils/logger.py
"""
Logging utilities for the AI Middleware Platform.

This module provides a centralized logging system that can be used throughout
the application. It supports both console and file logging, with configurable
log levels and formatting.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

from app.core.config import config


class Logger:
    """
    Centralized logger for the AI Middleware Platform.
    
    This class provides methods for logging messages at different levels
    (info, error, debug) and handles both console and file output based
    on configuration.
    """
    
    def __init__(self) -> None:
        """Initialize the logger with configured settings."""
        self.logger = logging.getLogger("ai_middleware")
        self.logger.setLevel(getattr(logging, config.log_level.upper()))
        
        # Prevent adding multiple handlers if logger is already configured
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # File handler (if log file path is configured)
            if config.log_file_path:
                # Ensure the directory exists
                log_path = Path(config.log_file_path)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(config.log_file_path)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def info(self, message: str) -> None:
        """
        Log an informational message.
        
        Args:
            message: The message to log.
        """
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """
        Log an error message.
        
        Args:
            message: The message to log.
        """
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """
        Log a debug message.
        
        Args:
            message: The message to log.
        """
        self.logger.debug(message)
    
    def warning(self, message: str) -> None:
        """
        Log a warning message.
        
        Args:
            message: The message to log.
        """
        self.logger.warning(message)
    
    def log_execution(self, execution_id: str, data: dict) -> None:
        """
        Log execution-specific data.
        
        Args:
            execution_id: The ID of the execution being logged.
            data: The execution data to log.
        """
        self.info(f"Execution {execution_id}: {data}")


# Global logger instance
logger = Logger()

