"""健康检查路由。"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """健康检查接口。

    Returns:
        服务状态信息
    """
    return {"status": "healthy", "service": "fastapi-cicd-demo"}


@router.get("/health/ready")
async def readiness_check():
    """就绪检查接口。"""
    return {"status": "ready"}


@router.get("/health/live")
async def liveness_check():
    """存活检查接口。"""
    return {"status": "alive"}
