"""Prometheus 指标定义与 FastAPI 集成。

使用 prometheus-fastapi-instrumentator 库自动收集 HTTP 请求指标，
同时暴露自定义业务指标。
"""

from prometheus_fastapi_instrumentator import Instrumentator

# 创建全局 instrumentator 实例
instrumentator = Instrumentator()


def setup_metrics(app):
    """在 FastAPI 应用上启用 Prometheus 指标收集。

    Args:
        app: FastAPI 应用实例
    """
    # 自动暴露 /metrics 端点并收集请求指标
    instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
