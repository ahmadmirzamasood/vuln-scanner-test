

def test_sql_injection_login_fixed(tmp_path, monkeypatch):
    import sqlite3
    import os
    from unittest.mock import patch, MagicMock

    # Create a temp DB with a known user
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use our temp DB
    original_connect = sqlite3.connect
    def patched_connect(name, *args, **kwargs):
        if name == "users.db":
            return original_connect(db_path, *args, **kwargs)
        return original_connect(name, *args, **kwargs)

    with patch("sqlite3.connect", side_effect=patched_connect):
        import app
        client = app.app.test_client()

        # SQL injection attempt: OR '1'='1'
        response = client.post("/login", data={
            "username": "' OR '1'='1'--",
            "password": "anything"
        })
        assert b"Login successful" not in response.data, "SQLi bypass should not succeed"
        assert b"Invalid username or password" in response.data

        # SQL injection attempt: bypass password check
        response = client.post("/login", data={
            "username": "admin'--",
            "password": ""
        })
        assert b"Login successful" not in response.data, "Password bypass SQLi should not succeed"
        assert b"Invalid username or password" in response.data

        # Legitimate login should still work
        response = client.post("/login", data={
            "username": "admin",
            "password": "secret"
        })
        assert b"Login successful" in response.data, "Valid credentials should work"