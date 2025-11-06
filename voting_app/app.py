from flask import Flask, render_template, request
import psycopg2
from datetime import datetime

app = Flask(__name__)

import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "votes_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "123456")


def get_connection():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/vote", methods=["POST"])
def vote():
    option = request.form["option"]
    now = datetime.now()

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE vote_table SET vote_number = vote_number + 1, last_vote = %s WHERE name = %s;",
            (now, option),
        )
        conn.commit()
        cur.close()
        conn.close()
        app.logger.info(f"{now} - Voted for {option}")
        return f"<h3>You voted for {option}!</h3><a href='/'>Back</a>"
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return f"<h3>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6110, debug=True)
