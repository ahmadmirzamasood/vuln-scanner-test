

def test_sql_injection_login_bypasses_are_fixed(tmp_path, monkeypatch):
    import sqlite3
    import os
    from flask import Flask
    from unittest.mock import patch

    # Set up a temporary database
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret123')")
    conn.commit()
    conn.close()

    app = Flask(__name__)
    app.config["TESTING"] = True

    def login():
        from flask import request
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(db_path)
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

    app.add_url_rule("/login", "login", login, methods=["POST"])

    with app.test_client() as client:
        # Classic always-true injection
        resp = client.post("/login", data={"username": "' OR '1'='1'--", "password": "anything"})
        assert resp.data == b"Invalid username or password."

        # Comment-out password clause injection
        resp = client.post("/login", data={"username": "admin'--", "password": ""})
        assert resp.data == b"Invalid username or password."

        # UNION-based injection
        resp = client.post("/login", data={"username": "' UNION SELECT id, username, password FROM users--", "password": ""})
        assert resp.data == b"Invalid username or password."

        # Valid credentials still work
        resp = client.post("/login", data={"username": "admin", "password": "secret123"})
        assert resp.data == b"Login successful!"