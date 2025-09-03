from auth import get_password_hash
from database import get_connection

username = "admin"
password = "admin123"
role = "admin"

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    INSERT INTO ged_users (username, password_hash, role)
    VALUES (:1, :2, :3)
""", (username, get_password_hash(password), role))

conn.commit()
cur.close()
conn.close()

print("✅ Utilisateur créé :", username)
