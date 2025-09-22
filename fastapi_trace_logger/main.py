# main.py
import asyncio
import os

from fastapi import FastAPI

from fastapi_trace_logger.config import Config
from fastapi_trace_logger.logger import TraceLogger
from fastapi_trace_logger.trace_middleware import TraceMiddleware, get_current_trace_context

# Initialize global logger
trace_logger = TraceLogger().get_logger()
config = Config()

# Create FastAPI application
app = FastAPI(
    title="FastAPI Trace Example",
    description="An example FastAPI application with automatic trace_id injection and performance tracing",
    version="1.0.0"
)

# Add TraceMiddleware to the application
# enable_performance=True to auto-create spans for HTTP requests
app.add_middleware(TraceMiddleware, enable_performance=True)


@app.get("/")
async def root():
    trace_logger.info("Handling root endpoint request")
    # 模拟一些处理时间
    await asyncio.sleep(0.1)
    return {"message": "Hello World with tracing!"}


@app.get("/health")
async def health_check():
    trace_logger.info("Health check requested")

    # 记录开始测试
    trace_logger.info("开始执行测试函数")
    await test_trace_logger()
    # 记录结束测试
    trace_logger.info("测试函数执行完成")

    return {"status": "healthy"}


# 在 main.py 中
async def test_trace_logger():
    trace_context = get_current_trace_context()
    # 无需手动获取父span ID
    span = trace_context.new_span("test_span")
    trace_logger.info("Testing trace logger")
    await asyncio.sleep(3)
    trace_context.close_span(span)
    trace_logger.info("test_span 已关闭")
    trace_logger.info(f"当前trace上下文: {trace_context.to_dict()}")


# For development only - auto start server if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "true").lower() in ("true", "1", "yes"),
        log_level="info"
    )
