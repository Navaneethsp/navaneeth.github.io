from flask import Flask, request
from markupsafe import escape
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("mydb.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    if request.method == "POST":
        conn.execute("INSERT INTO users (name) VALUES (?)", (request.form["name"],))
        conn.commit()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    items = "".join(f"<li>{escape(r[1])}</li>" for r in rows)
    return f"""
        <h1>Users</h1>
        <form method="post">
            <input name="name" placeholder="Enter name" required>
            <button>Add</button>
        </form>
        <ul>{items}</ul>
    """

if __name__ == "__main__":
    app.run(debug=True)