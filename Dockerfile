# ========== 构建阶段 ==========
FROM python:3.10-slim AS builder

WORKDIR /build

# 先复制依赖文件，利用 Docker 缓存层
COPY requirements.txt .

# 安装依赖到指定目录
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ========== 运行阶段 ==========
FROM python:3.10-slim AS runtime

WORKDIR /app

# 从构建阶段复制已安装的依赖
COPY --from=builder /install /usr/local

# 复制应用代码
COPY app/ ./app/

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
