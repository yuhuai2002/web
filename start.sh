#!/bin/bash
# start.sh - 一键启动 newflask 项目

echo "������ 正在启动 newflask 项目..."

# 进入项目目录
cd /home/ubuntu/gyd/qianyi/flaskProject-trans

# 启动或创建容器
docker run -d --name newflask-app -p 8000:5000 -v newflask_volume:/app/www newflask || docker start newflask-app

# 显示状态
echo "������ 容器状态："
docker ps | grep newflask-app

echo "������ 最近日志："
docker logs newflask-app | tail -10

echo "✅ 服务已启动，访问：http://<你的服务器IP>:8000"
