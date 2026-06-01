import sqlite3
import hashlib
import os
import subprocess

SECRET_KEY = "sk-prod-abc123-hardcoded"
DB_PASSWORD = "admin123"

def get_user(user_id):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchone()

def login(username, password):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return conn.execute(query).fetchone()

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def read_file(filename: str) -> str:
    path = f"/app/uploads/{filename}"
    with open(path) as f:
        return f.read()

def run_command(user_input: str):
    os.system(f"ls {user_input}")

def ping(host: str):
    subprocess.call(f"ping {host}", shell=True)
