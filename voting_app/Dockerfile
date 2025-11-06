# 使用官方 Python 轻量镜像（兼容 Apple M 芯片）
FROM python:3.10-slim

# 设置容器内的工作目录
WORKDIR /app

# 将当前目录下所有文件复制进容器
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 使用的端口
EXPOSE 6110

# 设置环境变量（供 Flask 连接数据库）
ENV DB_HOST=db \
    DB_NAME=votes \
    DB_USER=postgres \
    DB_PASS=pass

# 容器启动时执行的命令
CMD ["python", "app.py"]
