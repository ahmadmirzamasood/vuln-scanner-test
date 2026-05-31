# test_app.py — deliberately vulnerable for testing
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchone()

SECRET_KEY = "hardcoded_secret_123"
