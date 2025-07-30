FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 复制到容器中
COPY requirements.txt .

# 在容器内安装所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将应用代码复制到容器中
COPY . .

# 创建数据目录
RUN mkdir -p /app/www/zip /app/www/unzip /app/www/output /app/www/array

# 暴露 Flask 默认端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]