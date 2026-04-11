"""健康检查接口测试。"""


class TestHealthEndpoint:
    """健康检查相关测试集合。"""

    def test_root_returns_welcome(self, client):
        """测试根路径返回欢迎信息。"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to FastAPI CI/CD Demo"
        assert "/docs" in data["docs"]

    def test_health_check_returns_healthy(self, client):
        """测试健康检查返回 healthy 状态。"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "fastapi-cicd-demo"

    def test_readiness_check_returns_ready(self, client):
        """测试就绪检查返回 ready 状态。"""
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"

    def test_liveness_check_returns_alive(self, client):
        """测试存活检查返回 alive 状态。"""
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"


class TestNotFound:
    """404 相关测试。"""

    def test_nonexistent_path_returns_404(self, client):
        """测试不存在的路径返回 404。"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
