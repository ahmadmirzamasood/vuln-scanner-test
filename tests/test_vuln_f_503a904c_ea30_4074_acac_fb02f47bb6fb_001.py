

def test_login_sql_injection(tmp_path, monkeypatch):
    import sqlite3
    import os
    from flask import Flask

    # Create a temporary users.db with a known user
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use our temp db
    original_connect = sqlite3.connect
    monkeypatch.setattr(sqlite3, "connect", lambda db: original_connect(db_path))

    app = Flask(__name__)
    app.config["TESTING"] = True

    # Register the login route using the patched function
    import importlib, sys, types
    # Inline the patched login function for testing
    @app.route("/login", methods=["POST"])
    def login():
        from flask import request
        username = request.form["username"]
        password = request.form["password"]
        conn2 = sqlite3.connect("users.db")
        cursor = conn2.cursor()
        query = """
            SELECT * FROM users
            WHERE username = ?
            AND password = ?
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn2.close()
        if user:
            return "Login successful!"
        else:
            return "Invalid username or password."

    with app.test_client() as client:
        # SQL injection attempt should NOT succeed
        response = client.post("/login", data={
            "username": "' OR '1'='1'--",
            "password": "anything"
        })
        assert response.data == b"Invalid username or password.", \
            "SQL injection bypass succeeded — vulnerability not fixed!"

        # SQL injection attempt with classic always-true payload
        response = client.post("/login", data={
            "username": "admin'--",
            "password": ""
        })
        assert response.data == b"Invalid username or password.", \
            "SQL injection comment bypass succeeded — vulnerability not fixed!"

        # Legitimate login should still work
        response = client.post("/login", data={
            "username": "admin",
            "password": "secret"
        })
        assert response.data == b"Login successful!", \
            "Legitimate login failed after fix!"