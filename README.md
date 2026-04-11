# fastapi-cicd-demo
一个用于演示 CI/CD 流水线的 FastAPI 项目

项目结构
```
fastapi-cicd-demo/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          ← GitHub Actions 流水线（最后才写）
├── app/
│   ├── __init__.py
│   ├── main.py                ← FastAPI 入口
│   ├── routers/
│   │   ├── __init__.py
│   │   └── health.py          ← 健康检查路由
│   └── services/
│       ├── __init__.py
│       └── calculator.py      ← 业务逻辑（供测试用）
├── tests/
│   ├── __init__.py
│   ├── conftest.py            ← pytest 配置 & fixture
│   ├── test_health.py         ← 健康检查测试
│   └── test_calculator.py     ← 计算器测试
├── Dockerfile                 ← Docker 构建文件
├── docker-compose.yml         ← 本地开发用
├── requirements.txt           ← Python 依赖
├── pyproject.toml             ← 项目元数据 & 工具配置
├── .flake8                    ← flake8 配置
├── .dockerignore              ← Docker 构建排除文件
└── README.md

```

