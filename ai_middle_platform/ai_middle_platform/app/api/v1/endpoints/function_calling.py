## app/api/v1/endpoints/function_calling.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.schemas.function_schema import FunctionSpecSchema, FunctionResponseSchema
from app.services.function_caller import FunctionCaller, FunctionSpec
from app.db.session import get_postgresql_session
from app.models.function import FunctionDB
from app.utils.logger import logger

router = APIRouter()

# Initialize function caller
function_caller = FunctionCaller()


@router.post("/", response_model=bool)
async def register_function(func_spec: FunctionSpecSchema) -> bool:
    """
    Register a new function.
    
    Args:
        func_spec: Function specification to register
        
    Returns:
        Registration success
    """
    try:
        # Convert schema to internal representation
        internal_func_spec = FunctionSpec(
            name=func_spec.name,
            description=func_spec.description,
            parameters=func_spec.parameters,
            callback_url=getattr(func_spec, "callback_url", None)
        )
        
        # Validate function specification
        if not function_caller.validate_function_spec(internal_func_spec):
            raise HTTPException(status_code=400, detail="Invalid function specification")
        
        # Save to database
        db_function = FunctionDB(
            name=func_spec.name,
            description=func_spec.description,
            parameters=func_spec.parameters,
            callback_url=getattr(func_spec, "callback_url", None)
        )
        
        with get_postgresql_session() as db_session:
            db_session.add(db_function)
            db_session.commit()
        
        # Reload functions in caller
        function_caller._load_functions()
        
        return True
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering function {func_spec.name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to register function")


@router.post("/{func_name}/call", response_model=FunctionResponseSchema)
async def call_function(func_name: str, parameters: Dict[str, Any]) -> FunctionResponseSchema:
    """
    Call a registered function.
    
    Args:
        func_name: Name of the function to call
        parameters: Parameters to pass to the function
        
    Returns:
        Function call result
    """
    try:
        result = function_caller.execute_function_call(func_name, parameters)
        
        return FunctionResponseSchema(
            result=result.result,
            status=result.status
        )
    except ValueError as e:
        logger.error(f"Error calling function {func_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error calling function {func_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to call function")

