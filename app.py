# vulnerable_app.py
# Intentionally vulnerable Flask app: SQL injection example

from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('alice', 'password')")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return """
        <h2>Login</h2>
        <form action="/login" method="post">
            <input name="username" placeholder="Username">
            <input name="password" placeholder="Password" type="password">
            <button type="submit">Login</button>
        </form>
    """

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = """
        SELECT * FROM users
        WHERE username = ?
        AND password = ?
    """

    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful!"
    else:
        return "Invalid username or password."

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
# Add this at the bottom of app.py on test-scan-1 branch only
def get_admin(username):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM admins WHERE username = '{username}'"
    return conn.execute(query).fetchone()
# app.py — deliberately vulnerable for VulnScan testing
import sqlite3
import hashlib

# Vulnerability 1: SQL Injection
def get_user(user_id):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchone()

# Vulnerability 2: Hardcoded secret
SECRET_KEY = "hardcoded_secret_key_abc123"

# Vulnerability 3: Weak MD5 hashing
def hash_password(password: str) -> str:
    return hashlib.scrypt(password.encode(), salt=os.urandom(16), n=16384, r=8, p=1).hex()


# Vulnerability 4: Path traversal
def read_file(filename: str) -> str:
    path = f"/app/uploads/{filename}"
    with open(path) as f:
        return f.read()
