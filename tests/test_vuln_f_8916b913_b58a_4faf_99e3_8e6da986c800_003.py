

def test_debug_mode_disabled():
    """Ensure the Flask app is not running in debug mode."""
    import app as application
    assert application.app.debug is False, "Flask debug mode must be disabled in production"

def test_get_admin_no_sql_injection(tmp_path, monkeypatch):
    """Ensure get_admin uses parameterized queries and is not vulnerable to SQL injection."""
    import sqlite3
    import inspect
    import app as application

    # Check that the source does not contain f-string SQL construction for get_admin
    source = inspect.getsource(application.get_admin)
    assert "f\"" not in source and "f'" not in source, "get_admin must not use f-strings for SQL"
    assert "?" in source, "get_admin must use parameterized queries"

    # Functional test: SQL injection payload should not return unexpected results
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE admins (username TEXT, password TEXT)")
    conn.execute("INSERT INTO admins VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

    monkeypatch.setattr("sqlite3.connect", lambda _: sqlite3.connect(db_path))
    # This injection payload would return rows if vulnerable
    result = application.get_admin("' OR '1'='1")
    assert result is None, "SQL injection payload must not return rows"