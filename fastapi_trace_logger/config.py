# config.py
import os


class Config:
    """
    Configuration class that loads settings from environment variables.
    Provides strongly-typed, default-valued configuration options for the tracing system.
    """

    def __init__(self):
        self.load_from_env()

    def load_from_env(self):
        """Load configuration from environment variables with fallback defaults."""
        # HTTP header name for trace propagation
        self.TRACE_HEADER_NAME: str = os.getenv("TRACE_HEADER_NAME", "X-Trace-ID")

        # Log format template, supports {trace_id}, {parent_span_id} placeholders
        self.LOG_FORMAT: str = os.getenv(
            "LOG_FORMAT",
            "[%(asctime)s] [%(levelname)s] [thread=%(thread)d:%(threadName)s] [trace_id=%(trace_id)s] [span_id=%(span_id)s] %(message)s"
        )

        # Enable JSON-formatted logs
        self.ENABLE_JSON_LOG: bool = os.getenv("ENABLE_JSON_LOG", "false").lower() in ("true", "1", "yes")

        # Enable Jaeger exporter
        self.ENABLE_JAEGER: bool = os.getenv("ENABLE_JAEGER", "false").lower() in ("true", "1", "yes")

        # Jaeger agent host and port
        self.JAEGER_HOST: str = os.getenv("JAEGER_HOST", "localhost")
        self.JAEGER_PORT: int = int(os.getenv("JAEGER_PORT", "6831"))

    @property
    def is_jaeger_enabled(self) -> bool:
        """Helper property to check if Jaeger export is enabled."""
        return self.ENABLE_JAEGER

    @property
    def is_json_log_enabled(self) -> bool:
        """Helper property to check if JSON logging is enabled."""
        return self.ENABLE_JSON_LOG
