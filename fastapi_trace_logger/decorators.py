## decorators.py
import functools
import time
from typing import Callable, Any, Optional
from .trace_middleware import get_current_trace_context


class PerformanceDecorator:
    """
    Decorator class for performance tracing of functions.
    Automatically creates and closes spans in the current trace context.
    Usage: @PerformanceDecorator().trace_span("operation_name")
    """

    def trace_span(self, name: str) -> Callable:
        """
        Decorator factory that returns a decorator to trace a function call as a span.
        
        Args:
            name: Name of the span to be created
            
        Returns:
            Decorator function that wraps the target function
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    trace_context = get_current_trace_context()
                    span = trace_context.new_span(name)
                except LookupError:
                    # No trace context available, execute function without tracing
                    return await func(*args, **kwargs)

                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    trace_context.close_span(span)

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    trace_context = get_current_trace_context()
                    span = trace_context.new_span(name)
                except LookupError:
                    # No trace context available, execute function without tracing
                    return func(*args, **kwargs)

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    trace_context.close_span(span)

            # Return appropriate wrapper based on whether function is async
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper

        return decorator


# Convenience instance for easier usage
performance_decorator = PerformanceDecorator()
trace_span = performance_decorator.trace_span


# Optional: If asyncio is not already imported, import it
import asyncio
