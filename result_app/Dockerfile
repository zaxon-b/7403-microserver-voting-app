FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6111

# 设置环境变量（供 Flask 连接数据库）
ENV DB_HOST=db \
    DB_NAME=votes \
    DB_USER=postgres \
    DB_PASS=pass

CMD ["python", "app.py"]
