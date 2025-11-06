from flask import Flask, render_template
from psycopg2 import pool
import os

app = Flask(__name__)

# 从环境变量中读取数据库配置
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "votes-db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "123456")

try:
    conn_pool = pool.SimpleConnectionPool(
        1,          # 最小连接数
        10,         # 最大连接数
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    if conn_pool:
        app.logger.info("PostgreSQL connection pool created successfully.")
except Exception as e:
    app.logger.error(f"Error creating connection pool: {e}")
    raise

def get_connection():
    return conn_pool.getconn()

def release_connection(conn):
    conn_pool.putconn(conn)

@app.route("/")
def results():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, vote_number, last_vote FROM vote_table;")
        conn.commit()
        rows = cur.fetchall()
        cur.close()
        total = sum([r[1] for r in rows]) or 1
        data = []
        for name, num, last in rows:
            percent = f"{num / total * 100:.1f}%"
            data.append({"name": name, "num": num, "percent": percent, "last": last})

        return render_template("results.html", data=data, total=total)
    except Exception as e:
        app.logger.error(f"Database error: {e}")
    finally:
        if conn:
            release_connection(conn)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6111)
