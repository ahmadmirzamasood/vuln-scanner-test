

def test_sql_injection_login_bypass(tmp_path, monkeypatch):
    import sqlite3
    import os
    from unittest.mock import patch, MagicMock

    # Create a temporary test database
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'securepassword123')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use our test database
    original_connect = sqlite3.connect
    def patched_connect(path, **kwargs):
        return original_connect(db_path, **kwargs)

    with patch("sqlite3.connect", side_effect=patched_connect):
        import importlib
        import app as app_module

        test_client = app_module.app.test_client()

        # Test 1: Classic OR-based bypass should NOT succeed
        response = test_client.post("/login", data={
            "username": "' OR '1'='1'--",
            "password": "anything"
        })
        assert b"Login successful!" not in response.data, \
            "SQL injection bypass should not grant access"
        assert b"Invalid username or password" in response.data, \
            "Should return invalid credentials for injection attempt"

        # Test 2: Comment-out password check should NOT succeed
        response = test_client.post("/login", data={
            "username": "admin'--",
            "password": "wrongpassword"
        })
        assert b"Login successful!" not in response.data, \
            "SQL injection comment bypass should not grant access"

        # Test 3: Legitimate login SHOULD succeed
        response = test_client.post("/login", data={
            "username": "admin",
            "password": "securepassword123"
        })
        assert b"Login successful!" in response.data, \
            "Legitimate credentials should grant access"

        # Test 4: Wrong password should NOT succeed
        response = test_client.post("/login", data={
            "username": "admin",
            "password": "wrongpassword"
        })
        assert b"Login successful!" not in response.data, \
            "Wrong password should not grant access"