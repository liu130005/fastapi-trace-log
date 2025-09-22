# trace_middleware.py
import asyncio
import contextvars
import uuid

from starlette.types import ASGIApp, Receive, Scope, Send

from fastapi_trace_logger.common import TraceContext
from fastapi_trace_logger.config import Config
from fastapi_trace_logger.exporter import JaegerExporter

# Async context variable to hold current TraceContext instance
_trace_context_var: contextvars.ContextVar = contextvars.ContextVar("trace_context")


def get_current_trace_context() -> TraceContext:
    """Get current trace context from async context, raise LookupError if not set."""
    try:
        return _trace_context_var.get()
    except LookupError:
        raise LookupError("No trace context found in current async context")


class TraceMiddleware:
    """
    ASGI middleware that injects trace context into HTTP requests and propagates trace headers.
    Automatically exports trace data to Jaeger if enabled.
    Complies with ASGI specification and supports optional performance tracing.
    """

    def __init__(self, app: ASGIApp, enable_performance: bool = False):
        self.app = app
        self.enable_performance = enable_performance
        self.config = Config()
        self.exporter = (
            JaegerExporter(self.config) if self.config.is_jaeger_enabled else None
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # Extract trace_id and parent_span_id from headers
        headers = dict(scope.get("headers", []))
        trace_header_name = self.config.TRACE_HEADER_NAME.lower().encode()
        parent_header_name = b"x-parent-span-id"

        trace_id_bytes = headers.get(trace_header_name)
        parent_span_id_bytes = headers.get(parent_header_name)

        trace_id = (
            trace_id_bytes.decode() if trace_id_bytes else str(uuid.uuid4())
        )
        parent_span_id = (
            parent_span_id_bytes.decode() if parent_span_id_bytes else "0"
        )

        # Initialize trace context
        trace_context = TraceContext(trace_id=trace_id, parent_span_id=parent_span_id)
        token = _trace_context_var.set(trace_context)

        # Optionally auto-create root span for the HTTP request
        root_span = None
        if self.enable_performance:
            # HTTP请求的根span，父ID为从header中获取的parent_span_id
            root_span = trace_context.new_span("http_request", parent_span_id)

        # Wrap send to inject trace header and close root span
        async def wrapped_send(message):
            if message["type"] == "http.response.start":
                response_headers = message.get("headers", [])
                # Inject trace_id into response headers
                response_headers.append(
                    (trace_header_name, trace_context.trace_id.encode())
                )
                message["headers"] = response_headers

                # Close root span if performance tracing is enabled
                if self.enable_performance and root_span:
                    trace_context.close_span(root_span)

            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        except Exception:
            raise
        finally:
            # Export trace data if exporter is enabled and spans exist
            if self.exporter and trace_context.spans:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.exporter.export, trace_context)

            # Clean up context
            _trace_context_var.reset(token)
