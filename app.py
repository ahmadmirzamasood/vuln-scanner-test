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
    return hashlib.md5(password.encode()).hexdigest()

# Vulnerability 4: Path traversal
def read_file(filename: str) -> str:
    path = f"/app/uploads/{filename}"
    with open(path) as f:
        return f.read()
