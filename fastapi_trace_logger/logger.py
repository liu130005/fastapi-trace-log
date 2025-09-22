# logger.py
import json
import logging
import threading

# Async context variable to hold current TraceContext instance (imported from trace_middleware)
from fastapi_trace_logger.trace_middleware import _trace_context_var
from .config import Config


class TraceLogger:
    """
    Custom logger that automatically injects trace_id and span_id into log records.
    Supports both structured (JSON) and traditional log formats based on configuration.
    """

    def __init__(self, logger_name: str = "fastapi_trace"):
        self.config = Config()
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # Avoid adding multiple handlers if logger already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = self._create_formatter()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.addFilter(self._trace_filter)

    def get_logger(self) -> logging.Logger:
        """Return configured logger instance."""
        return self.logger

    def _create_formatter(self):
        """Create appropriate formatter based on JSON logging configuration."""
        if self.config.is_json_log_enabled:
            return JsonFormatter(self.config.LOG_FORMAT)
        else:
            return TraceFormatter(self.config.LOG_FORMAT)

    def _trace_filter(self, record: logging.LogRecord) -> bool:
        """
        Filter that injects trace_id and span_id into log record.
        Returns True to allow log record to be processed.
        """
        # 添加线程信息
        record.thread = threading.get_ident()
        record.threadName = threading.current_thread().name

        try:
            trace_context = _trace_context_var.get()
            record.trace_id = trace_context.trace_id
            # Use last span's span_id if exists, else use parent_span_id
            current_span_id = "0"
            if trace_context.spans:
                # Get the most recently opened (and not yet closed) span
                for span in reversed(trace_context.spans):
                    if span.get("end_time") is None:
                        current_span_id = span["span_id"]
                        break
                else:
                    # If all spans are closed, use the last one
                    if trace_context.spans:
                        current_span_id = trace_context.spans[-1]["span_id"]
            else:
                current_span_id = trace_context.parent_span_id
            record.span_id = current_span_id
        except LookupError:
            # No trace context available
            record.trace_id = "N/A"
            record.span_id = "N/A"
        return True


class TraceFormatter(logging.Formatter):
    """
    Custom formatter that includes thread information in traditional log format.
    """

    def format(self, record):
        # 确保thread和threadName字段存在
        if not hasattr(record, 'thread'):
            record.thread = threading.get_ident()
        if not hasattr(record, 'threadName'):
            record.threadName = threading.current_thread().name
        return super().format(record)


class JsonFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in JSON format.
    Automatically includes trace_id and span_id when available.
    """

    def __init__(self, fmt: str = None):
        super().__init__(fmt)
        self.fmt = fmt

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string."""
        # 添加线程信息
        if not hasattr(record, 'thread'):
            record.thread = threading.get_ident()
        if not hasattr(record, 'threadName'):
            record.threadName = threading.current_thread().name

        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread_id": record.thread,
            "thread_name": record.threadName,
        }

        # Add trace context if available
        if hasattr(record, "trace_id"):
            log_entry["trace_id"] = record.trace_id
        if hasattr(record, "span_id"):
            log_entry["span_id"] = record.span_id

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False, separators=(',', ':'))
