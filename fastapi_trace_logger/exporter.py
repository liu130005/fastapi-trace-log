import logging
from typing import Optional

from fastapi_trace_logger.common import TraceContext
from fastapi_trace_logger.config import Config

try:
    from jaeger_client import Config as JaegerConfig
    from jaeger_client.tracer import Tracer
except ImportError:
    JaegerConfig = None
    Tracer = None
    logging.getLogger(__name__).warning("jaeger_client not installed. JaegerExporter will be disabled.")


class JaegerExporter:
    """
    Exports trace context data to Jaeger tracing system.
    Uses jaeger-client library to send spans to Jaeger agent.
    """

    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.tracer: Optional[Tracer] = None
        if JaegerConfig is not None:
            self._initialize_tracer()
        else:
            self.logger.error("JaegerExporter cannot initialize: jaeger_client not available.")

    def _initialize_tracer(self) -> None:
        """Initialize Jaeger tracer with configuration from environment."""
        try:
            jaeger_config = JaegerConfig(
                config={
                    "sampler": {"type": "const", "param": 1},
                    "local_agent": {
                        "reporting_host": self.config.JAEGER_HOST,
                        "reporting_port": self.config.JAEGER_PORT,
                    },
                    "logging": True,
                },
                service_name="fastapi-trace-service",
                validate=True,
            )
            self.tracer = jaeger_config.initialize_tracer()
            self.logger.info(
                f"JaegerExporter initialized with host={self.config.JAEGER_HOST}, "
                f"port={self.config.JAEGER_PORT}"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Jaeger tracer: {e}")
            self.tracer = None

    def export(self, trace_context: TraceContext) -> None:
        """
        Export trace context spans to Jaeger.
        This method is synchronous and should be called in a thread pool if used in async context.

        Args:
            trace_context: TraceContext instance containing spans to export
        """
        if not self.tracer:
            self.logger.warning("Jaeger tracer not initialized, skipping export")
            return

        try:
            # Create root span for the entire trace
            root_span = self.tracer.start_span(
                operation_name="http_request",
                tags={
                    "trace_id": trace_context.trace_id,
                    "parent_span_id": trace_context.parent_span_id,
                },
            )

            # Export each span in the trace context
            for span_data in trace_context.spans:
                child_span = self.tracer.start_span(
                    operation_name=span_data["name"],
                    child_of=root_span,
                    tags={
                        "span_id": span_data["span_id"],
                    },
                )

                # Set duration if available
                if span_data.get("duration") is not None:
                    child_span.log_kv({"event": "duration", "value": span_data["duration"]})

                # Finish the child span
                child_span.finish()

            # Finish the root span
            root_span.finish()

            self.logger.debug(f"Exported trace {trace_context.trace_id} with {len(trace_context.spans)} spans")

        except Exception as e:
            self.logger.error(f"Failed to export trace {trace_context.trace_id} to Jaeger: {e}")
