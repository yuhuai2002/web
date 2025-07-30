#!/bin/bash
# start.sh - 一键启动 newflask 项目（每次启动都重建镜像）

echo "������ 正在启动 newflask 项目..."

# 进入项目目录
cd /home/ubuntu/gyd/qianyi/flaskProject-trans

# 1. 停止并删除旧容器
echo "������ 停止并删除旧容器..."
docker stop newflask-app > /dev/null 2>&1 || true
docker rm newflask-app > /dev/null 2>&1 || true

# 2. 删除旧镜像
echo "������️  删除旧镜像..."
docker rmi newflask > /dev/null 2>&1 || true

# 3. 重新构建镜像（关键：包含最新的代码）
echo "������ 正在构建 Docker 镜像..."
docker build -t newflask . || { echo "❌ 镜像构建失败"; exit 1; }

# 4. 运行新容器
echo "������ 正在运行新容器..."
docker run -d \
           --name newflask-app \
           -p 8000:5000 \
           -v newflask_volume:/app/www \
           newflask || { echo "❌ 容器运行失败"; exit 1; }

# 显示状态
echo "������ 容器状态："
docker ps | grep newflask-app

echo "������ 最近日志："
docker logs newflask-app | tail -10

echo "✅ 服务已启动，访问：http://<你的服务器IP>:8000"
