#!/bin/bash
# stop.sh - 停止 newflask 项目

echo "������ 正在停止 newflask-app 容器..."
docker stop newflask-app
echo "✅ 容器已停止"
