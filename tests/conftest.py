"""pytest 全局配置和 fixture。"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """创建 FastAPI 测试客户端。

    使用 session 级别，整个测试会话只创建一次。
    """
    with TestClient(app) as c:
        yield c
