# decorators.py
import asyncio
import functools
from typing import Callable, Any, Optional

from fastapi_trace_logger.trace_middleware import get_current_trace_context


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

        # 在 decorators.py 中
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    trace_context = get_current_trace_context()
                    # 无需手动获取父span ID，new_span会自动处理
                    span = trace_context.new_span(name)
                except LookupError:
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
                    # 获取当前活跃的span作为父span
                    parent_span_id = self._get_current_span_id(trace_context)
                    span = trace_context.new_span(name, parent_span_id)
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

    def _get_current_span_id(self, trace_context) -> Optional[str]:
        """
        获取当前活跃的span ID作为新span的父ID
        """
        # 查找最近创建但尚未关闭的span
        for span in reversed(trace_context.spans):
            if span.get("end_time") is None:
                return span["span_id"]
        # 如果没有未关闭的span，则使用trace context的parent_span_id
        return trace_context.parent_span_id


# Convenience instance for easier usage
performance_decorator = PerformanceDecorator()
trace_span = performance_decorator.trace_span
