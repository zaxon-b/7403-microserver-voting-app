from flask import Flask, render_template, request, jsonify
from psycopg2 import pool
from datetime import datetime
import os

app = Flask(__name__)

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

# ===== Flask 路由 =====
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/vote", methods=["POST"])
def vote():
    option = request.form["option"]
    real_option = "Cats" if option == "0" else "Dogs"
    now = datetime.now()
    ip = request.remote_addr

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO vote_table (name, vote_number, last_vote)
            VALUES (%s, 1, %s)
            ON CONFLICT (name) DO UPDATE
            SET 
              vote_number = vote_table.vote_number + EXCLUDED.vote_number,
              last_vote = EXCLUDED.last_vote;
            """,
            (real_option, now),
        )
        conn.commit()
        cur.close()
        app.logger.info(f"[{now}] {ip} - Voted for {real_option}")
        return jsonify({"status": "success", "message": f"You voted for {real_option}!"}), 200
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            release_connection(conn)

# ===== 应用启动 =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6110, debug=True)
