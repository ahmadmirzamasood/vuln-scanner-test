

def test_sql_injection_login_fixed(tmp_path, monkeypatch):
    import sqlite3
    import os

    # Set up a temporary test database
    db_path = str(tmp_path / "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

    # Patch sqlite3.connect to use the temp db
    original_connect = sqlite3.connect
    monkeypatch.setattr(sqlite3, "connect", lambda _: original_connect(db_path))

    # Import app and set up test client
    import app as flask_app
    flask_app.app.config["TESTING"] = True
    client = flask_app.app.test_client()

    # Test classic OR-based SQLi bypass
    response = client.post("/login", data={"username": "' OR '1'='1'--", "password": "anything"})
    assert b"Login successful!" not in response.data, "SQLi bypass should not succeed"

    # Test comment-based SQLi bypass
    response = client.post("/login", data={"username": "admin'--", "password": ""})
    assert b"Login successful!" not in response.data, "Comment-based SQLi bypass should not succeed"

    # Test that legitimate credentials still work
    response = client.post("/login", data={"username": "admin", "password": "secret"})
    assert b"Login successful!" in response.data, "Legitimate login should succeed"