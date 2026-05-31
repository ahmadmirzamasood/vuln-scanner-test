# Add this at the bottom of app.py on test-scan-1 branch only
def get_admin(username):
    conn = sqlite3.connect("db.sqlite")
    query = f"SELECT * FROM admins WHERE username = '{username}'"
    return conn.execute(query).fetchone()
