## trace_middleware.py
import asyncio
import contextvars
import uuid
import time
from typing import Awaitable, Callable, Dict, Any, Optional
from starlette.types import ASGIApp, Receive, Scope, Send

from .config import Config
from .exporter import JaegerExporter


class TraceContext:
    """
    Trace context manager for storing trace_id, parent_span_id and performance spans.
    Uses contextvars for async-safe context propagation.
    """

    def __init__(self, trace_id: Optional[str] = None, parent_span_id: Optional[str] = None):
        self.trace_id: str = trace_id or str(uuid.uuid4())
        self.parent_span_id: str = parent_span_id or "0"
        self.start_time: float = time.time()
        self.spans: list = []

    def new_span(self, name: str) -> Dict[str, Any]:
        """Create and register a new span."""
        span = {
            "name": name,
            "span_id": str(uuid.uuid4()),
            "start_time": time.time(),
            "end_time": None,
            "duration": None,
        }
        self.spans.append(span)
        return span

    def close_span(self, span: Dict[str, Any]) -> None:
        """Mark a span as completed and calculate duration."""
        span["end_time"] = time.time()
        span["duration"] = span["end_time"] - span["start_time"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace context to dictionary for export."""
        return {
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "start_time": self.start_time,
            "duration": time.time() - self.start_time,
            "spans": self.spans,
        }


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
            root_span = trace_context.new_span("http_request")

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
