import sqlite3
import jwt

def get_user(user_id):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchone()

SECRET_KEY = "hardcoded_secret_key_123"

def create_token(user_id):
    return jwt.encode({"sub": user_id}, SECRET_KEY)
