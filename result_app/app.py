from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# 从环境变量中读取数据库配置
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "votes-db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "123456")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

@app.route("/")
def results():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, vote_number, last_vote FROM vote_table;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    total = sum([r[1] for r in rows]) or 1
    data = []
    for name, num, last in rows:
        percent = f"{num / total * 100:.1f}%"
        data.append({"name": name, "num": num, "percent": percent, "last": last})

    return render_template("results.html", data=data, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6111)
