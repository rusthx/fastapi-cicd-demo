"""FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health

app = FastAPI(
    title="FastAPI CI/CD Demo",
    description="一个用于演示 CI/CD 流水线的 FastAPI 项目",
    version="0.1.0",
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router)


@app.get("/")
async def root():
    """根路径。"""
    return {
        "message": "Welcome to FastAPI CI/CD Demo",
        "docs": "/docs",
    }
