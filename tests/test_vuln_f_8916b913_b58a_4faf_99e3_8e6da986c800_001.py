

def test_sql_injection_login_bypass(tmp_path, monkeypatch):
    import sqlite3
    import os

    # Set up a temporary test database
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret123')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use our test database
    import sqlite3 as sqlite3_module
    original_connect = sqlite3_module.connect
    monkeypatch.setattr(sqlite3_module, "connect", lambda db: original_connect(db_path))

    # Import app and set up test client
    import app as app_module
    app_module.app.config["TESTING"] = True
    client = app_module.app.test_client()

    # Attempt SQL injection bypass
    response = client.post("/login", data={
        "username": "' OR '1'='1' --",
        "password": "anything"
    })
    assert b"Login successful!" not in response.data, "SQL injection bypass should not succeed"
    assert b"Invalid username or password" in response.data, "Should return invalid credentials message"

    # Verify legitimate login still works
    response_valid = client.post("/login", data={
        "username": "admin",
        "password": "secret123"
    })
    assert b"Login successful!" in response_valid.data, "Valid credentials should still work"