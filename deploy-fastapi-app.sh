#!/bin/bash

set -euo pipefail

##############################
# 安全部署 fastapi-app 容器（含自动回退）
# 用法: sudo deploy-fastapi-app.sh <镜像完整TAG>
##############################

APP_NAME="fastapi-app"
NETWORK_NAME="monitor"
HEALTH_URL="http://localhost:8000/health"
HEALTH_RETRIES=10
HEALTH_DELAY=3
BACKUP_CONTAINER="${APP_NAME}-backup"
DOCKER="/usr/bin/docker"
CURL="/usr/bin/curl"
LOG_FILE="/var/log/deploy-app.log"

touch "$LOG_FILE"
chmod 600 "$LOG_FILE"
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    # 写入独立日志文件
    echo "$msg" >> "$LOG_FILE"
    # 同时继续写入系统日志（用于审计）
    /usr/bin/logger -t deploy-app "$*"
}

# ============ 参数严格校验 ============
if [ $# -ne 1 ]; then
    log "错误: 需要传入镜像 TAG"
    exit 1
fi

IMAGE_TAG="$1"
# 只拒绝包含常见 Shell 注入字符的字符串，其余镜像标签放行
if echo "$IMAGE_TAG" | grep -q '[;&$`|*?(){}!<>\\'\'"]' ; then
    log "错误: 镜像 TAG 包含危险字符，禁止执行"
    exit 1
fi

log "===== 开始部署应用，镜像: $IMAGE_TAG ====="

# 拉取镜像
log "拉取新镜像..."
$DOCKER pull "$IMAGE_TAG"

# 确保监控网络存在（用于 Prometheus/Grafana 连通）
if ! $DOCKER network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    log "创建 Docker 网络: $NETWORK_NAME"
    $DOCKER network create "$NETWORK_NAME"
fi

log "检查并清理可能冲突的旧容器..."

#  清理之前部署失败的残留容器（status=Created/Exited/Dead）
FAILED_CONTAINER_ID=$($DOCKER ps -aq --filter "name=^${APP_NAME}$" --filter "status=created" --filter "status=exited" --filter "status=dead" 2>/dev/null || true)
if [ -n "$FAILED_CONTAINER_ID" ]; then
    log "发现残留的失败容器: $FAILED_CONTAINER_ID，强制移除..."
    $DOCKER rm -f "$FAILED_CONTAINER_ID" 2>/dev/null || true
fi

#  检查是否已有同名容器在运行，如果有，则停止并重命名为备份
RUNNING_CONTAINER_ID=$($DOCKER ps -q --filter "name=^${APP_NAME}$" || true)
if [ -n "$RUNNING_CONTAINER_ID" ]; then
    log "停止并备份当前运行的容器: $RUNNING_CONTAINER_ID"
    # 清理可能存在的旧备份容器
    $DOCKER rm -f "$BACKUP_CONTAINER" 2>/dev/null || true
    # 停止当前容器
    $DOCKER stop "$APP_NAME" >/dev/null || true
    # 重命名为备份容器
    $DOCKER rename "$APP_NAME" "$BACKUP_CONTAINER" || {
        log "重命名容器失败，强制移除后继续"
        $DOCKER rm -f "$APP_NAME" 2>/dev/null || true
    }
fi

#  最后确认，8000端口当前没有被占用（双重保险）
if ss -tuln | grep -q ':8000'; then
    log "警告: 8000端口仍被占用，尝试清理..."
    # 查找并强制移除占用8000端口的其他容器（非我们的目标容器）
    PORT_CONTAINER_ID=$($DOCKER ps -q --filter "publish=8000")
    if [ -n "$PORT_CONTAINER_ID" ]; then
        log "移除占用8000端口的容器: $PORT_CONTAINER_ID"
        $DOCKER rm -f "$PORT_CONTAINER_ID" 2>/dev/null || true
    fi
fi

# 启动新容器（只读根文件系统、限制内存、非特权，加入监控网络）
log "启动新容器..."
$DOCKER run -d \
    --name "$APP_NAME" \
    --network "$NETWORK_NAME" \
    --restart unless-stopped \
    -p 8000:8000 \
    --memory 256m \
    --read-only \
    --tmpfs /tmp \
    "$IMAGE_TAG"

# 健康检查
log "等待健康检查通过 (最多 ${HEALTH_RETRIES} 次)..."
SUCCESS=false
for i in $(seq 1 $HEALTH_RETRIES); do
    if $CURL -sSf "$HEALTH_URL" > /dev/null 2>&1; then
        log "新容器健康检查通过"
        SUCCESS=true
        break
    fi
    log "健康检查未通过，重试 $i/$HEALTH_RETRIES ..."
    sleep $HEALTH_DELAY
done

# 根据健康检查结果决定后续动作
if $SUCCESS; then
    log "部署成功，清理备份容器"
    $DOCKER rm -f "$BACKUP_CONTAINER" 2>/dev/null || true
else
    log "错误: 新容器健康检查失败，开始自动回退..."
    $DOCKER stop "$APP_NAME" || true
    $DOCKER rm "$APP_NAME" || true
    if $DOCKER inspect "$BACKUP_CONTAINER" >/dev/null 2>&1; then
        # 回退时需要把备份容器加回监控网络
        $DOCKER rename "$BACKUP_CONTAINER" "$APP_NAME"
        $DOCKER network connect "$NETWORK_NAME" "$APP_NAME" 2>/dev/null || true
        $DOCKER start "$APP_NAME"
        log "回退成功，旧容器已恢复运行"
    else
        log "严重: 没有备份容器可用，服务中断！"
        exit 1
    fi
fi

log "===== 部署流程结束 ====="
