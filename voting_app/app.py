from flask import Flask, render_template, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

import os

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "votes-db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "123456")


def get_connection():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():
    option = request.form["option"]
    real_option = "Cats" if option == "0" else "Dogs"
    now = datetime.now()
    ip = request.remote_addr

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
        conn.close()
        app.logger.info(f"[{now}]{ip} - Voted for {option}")
        return jsonify({"status": "success", "message": f"You voted for {option}!"}), 200
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6110, debug=True)
