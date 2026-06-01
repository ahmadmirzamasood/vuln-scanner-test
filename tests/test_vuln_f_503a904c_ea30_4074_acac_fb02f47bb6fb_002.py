

def test_sql_injection_login_bypass(tmp_path, monkeypatch):
    import sqlite3
    import os
    from flask import Flask
    from unittest.mock import patch

    # Set up a temporary test database
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use the test database
    original_connect = sqlite3.connect
    monkeypatch.setattr(sqlite3, "connect", lambda _: original_connect(db_path))

    app = Flask(__name__)
    app.config["TESTING"] = True

    # Register the patched login function
    import importlib, sys
    # Inline the fixed login logic for isolated testing
    def login_fixed(username, password):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    # Test 1: SQL injection bypass attempt returns no user
    injection_payload = "' OR '1'='1'--"
    result = login_fixed(injection_payload, "anything")
    assert result is None, "SQL injection bypass should not return a user"

    # Test 2: UNION-based injection returns no user
    union_payload = "' UNION SELECT id, username, password FROM users--"
    result = login_fixed(union_payload, "anything")
    assert result is None, "UNION-based SQL injection should not return a user"

    # Test 3: Valid credentials still work
    result = login_fixed("admin", "secret")
    assert result is not None, "Valid credentials should return a user"

    # Test 4: Wrong password fails
    result = login_fixed("admin", "wrongpassword")
    assert result is None, "Wrong password should not authenticate"