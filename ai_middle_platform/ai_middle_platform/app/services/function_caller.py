## app/services/function_caller.py
"""
Function Calling service for the AI Middleware Platform.

This module implements the FunctionCaller class which is responsible for
validating, executing, and managing function calls. It provides a unified
interface for interacting with external functions and handles callback
mechanisms.
"""

from typing import Dict, Any, Optional
import json
import time
import requests
from urllib.parse import urljoin

from app.utils.logger import logger
from app.utils.monitor import monitor
from app.db.session import get_postgresql_session
from app.models.function import FunctionDB


class FunctionResult:
    """
    Represents the result of a function call.
    
    This class encapsulates the outcome of executing a function, including
    the result data and execution status.
    """
    
    def __init__(self, result: Any, status: str = "success") -> None:
        """
        Initialize the function result.
        
        Args:
            result: The result data from the function execution
            status: Status of the function execution (default: "success")
        """
        self.result = result
        self.status = status


class FunctionSpec:
    """
    Represents a function specification.
    
    This class defines the structure of a function that can be registered
    and called through the FunctionCaller.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        callback_url: Optional[str] = None
    ) -> None:
        """
        Initialize the function specification.
        
        Args:
            name: Name of the function
            description: Description of what the function does
            parameters: Parameter schema for the function
            callback_url: Optional URL to call when function completes
        """
        self.name = name
        self.description = description
        self.parameters = parameters
        self.callback_url = callback_url


class FunctionCaller:
    """
    Service for managing and executing function calls in the AI Middleware Platform.
    
    This class is responsible for validating function specifications, executing
    function calls, and handling callback mechanisms. It provides a unified
    interface for integrating with external functions.
    """
    
    def __init__(self) -> None:
        """Initialize the function caller."""
        self.registered_functions: Dict[str, FunctionSpec] = {}
        self._load_functions()
    
    def _load_functions(self) -> None:
        """Load all registered functions from the database."""
        logger.info("Loading registered functions from database")
        
        try:
            with get_postgresql_session() as db_session:
                db_functions = db_session.query(FunctionDB).all()
                
                # For each function in the database, create a FunctionSpec and add it to the registry
                for db_function in db_functions:
                    func_spec = FunctionSpec(
                        name=db_function.name,
                        description=db_function.description,
                        parameters=db_function.parameters,
                        callback_url=db_function.callback_url
                    )
                    self.registered_functions[db_function.name] = func_spec
                
                logger.info(f"Successfully loaded {len(self.registered_functions)} functions")
        except Exception as e:
            logger.error(f"Failed to load functions: {str(e)}")
            self.registered_functions = {}
    
    def validate_function_spec(self, func_spec: FunctionSpec) -> bool:
        """
        Validate a function specification.
        
        Args:
            func_spec: The function specification to validate
            
        Returns:
            True if the specification is valid, False otherwise
        """
        try:
            # Check that required fields are present
            if not func_spec.name:
                logger.error("Function specification missing name")
                return False
            
            if not func_spec.description:
                logger.error("Function specification missing description")
                return False
            
            if not isinstance(func_spec.parameters, dict):
                logger.error("Function specification parameters must be a dictionary")
                return False
            
            # Validate that parameters have a schema
            for param_name, param_schema in func_spec.parameters.items():
                if not isinstance(param_schema, dict):
                    logger.error(f"Parameter '{param_name}' schema must be a dictionary")
                    return False
                if "type" not in param_schema:
                    logger.error(f"Parameter '{param_name}' schema must include a 'type'")
                    return False
            
            # Additional validation could be added here
            logger.info(f"Function specification for '{func_spec.name}' is valid")
            return True
            
        except Exception as e:
            logger.error(f"Error validating function specification: {str(e)}")
            return False
    
    def execute_function_call(self, func_name: str, parameters: Dict[str, Any]) -> FunctionResult:
        """
        Execute a registered function with the given parameters.
        
        Args:
            func_name: Name of the function to execute
            parameters: Parameters to pass to the function
            
        Returns:
            Result of the function execution
            
        Raises:
            ValueError: If the function is not found or validation fails
        """
        start_time = time.time()
        
        try:
            if func_name not in self.registered_functions:
                raise ValueError(f"Function '{func_name}' is not registered")
            
            func_spec = self.registered_functions[func_name]
            logger.info(f"Executing function '{func_name}'")
            
            # Validate parameters against function specification
            for param_name, param_value in parameters.items():
                if param_name not in func_spec.parameters:
                    logger.warning(f"Unexpected parameter '{param_name}' for function '{func_name}'")
            
            # In a real implementation, this would actually call the function
            # For now, we'll return a mock result
            result_data = {
                "function": func_name,
                "parameters": parameters,
                "result": f"Mock result from function {func_name}",
                "timestamp": time.time()
            }
            
            result = FunctionResult(result=result_data)
            
            duration = time.time() - start_time
            monitor.record_api_call(f"execute_function_{func_name}", duration, "success")
            
            logger.info(f"Successfully executed function '{func_name}'")
            
            # Handle callback if defined
            if func_spec.callback_url:
                self.handle_callback(func_spec.callback_url, result_data)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            monitor.record_api_call(f"execute_function_{func_name}", duration, "failure")
            logger.error(f"Failed to execute function '{func_name}': {str(e)}")
            raise
    
    def handle_callback(self, callback_url: str, data: Dict[str, Any]) -> bool:
        """
        Handle a callback by sending data to the specified URL.
        
        Args:
            callback_url: URL to send the callback data to
            data: Data to send in the callback
            
        Returns:
            True if callback was successful, False otherwise
        """
        try:
            logger.info(f"Sending callback to {callback_url}")
            
            # Send POST request with JSON data
            response = requests.post(
                callback_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30  # 30 second timeout
            )
            
            response.raise_for_status()  # Raise an exception for bad status codes
            
            logger.info(f"Successfully sent callback to {callback_url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send callback to {callback_url}: {str(e)}")
            return False
    
    def generate_openapi_spec(self) -> Dict[str, Any]:
        """
        Generate an OpenAPI specification for all registered functions.
        
        Returns:
            OpenAPI specification as a dictionary
        """
        try:
            # Create base OpenAPI structure
            openapi_spec = {
                "openapi": "3.0.0",
                "info": {
                    "title": "AI Middleware Function Calling API",
                    "version": "1.0.0",
                    "description": "API for calling registered functions in the AI Middleware Platform"
                },
                "paths": {},
                "components": {
                    "schemas": {}
                }
            }
            
            # Add paths for each registered function
            for func_name, func_spec in self.registered_functions.items():
                # Create path for the function
                path = f"/functions/{func_name}/call"
                openapi_spec["paths"][path] = {
                    "post": {
                        "summary": func_spec.description,
                        "operationId": f"call{func_name.capitalize()}",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "parameters": {
                                                "type": "object",
                                                "description": "Function parameters"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Function call result",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "result": {
                                                    "type": "object",
                                                    "description": "Function result data"
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Execution status"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            
            logger.info("Generated OpenAPI specification for registered functions")
            return openapi_spec
            
        except Exception as e:
            logger.error(f"Failed to generate OpenAPI specification: {str(e)}")
            return {}

