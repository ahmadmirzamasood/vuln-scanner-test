

def test_sql_injection_login_bypass(tmp_path, monkeypatch):
    import sqlite3
    import os
    from unittest.mock import patch, MagicMock

    # Create a temporary test database
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret123')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use our test database
    original_connect = sqlite3.connect
    def mock_connect(db_name):
        return original_connect(db_path)
    
    import app
    with patch("sqlite3.connect", side_effect=mock_connect):
        with app.app.test_client() as client:
            # Test 1: SQL injection with comment bypass should NOT succeed
            response = client.post("/login", data={
                "username": "admin' --",
                "password": "anything"
            })
            assert b"Login successful!" not in response.data, \
                "SQL injection comment bypass should not grant access"

            # Test 2: OR 1=1 bypass should NOT succeed
            response = client.post("/login", data={
                "username": "' OR '1'='1' --",
                "password": "anything"
            })
            assert b"Login successful!" not in response.data, \
                "OR 1=1 SQL injection should not grant access"

            # Test 3: Valid credentials SHOULD succeed
            response = client.post("/login", data={
                "username": "admin",
                "password": "secret123"
            })
            assert b"Login successful!" in response.data, \
                "Valid credentials should grant access"

            # Test 4: Wrong password should NOT succeed
            response = client.post("/login", data={
                "username": "admin",
                "password": "wrongpassword"
            })
            assert b"Login successful!" not in response.data, \
                "Wrong password should not grant access"