# common.py
import time
import uuid
from typing import Optional, Any, Dict


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

    def new_span(self, name: str, parent_span_id: Optional[str] = None) -> Dict[str, Any]:
        """Create and register a new span with parent-child relationship."""
        # 如果没有显式指定parent_span_id，则自动获取当前活跃的span作为父span
        if parent_span_id is None:
            parent_span_id = self._get_current_active_span_id()

        span = {
            "name": name,
            "span_id": str(uuid.uuid4()),
            "parent_span_id": parent_span_id,
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

    def _get_current_active_span_id(self) -> str:
        """
        获取当前活跃的span ID作为新span的父ID
        """
        # 查找最近创建但尚未关闭的span
        for span in reversed(self.spans):
            if span.get("end_time") is None:
                return span["span_id"]
        # 如果没有未关闭的span，则使用trace context的parent_span_id
        return self.parent_span_id
