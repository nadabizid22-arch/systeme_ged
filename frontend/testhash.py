import bcrypt

hashed = b"$2b$12$OftozshXZ2G8/HiOrxT4.e2bKDVQ/f8nbWg3Eg9SmWzrersh88u9O"
password = b"admin123"  # teste avec le mot de passe que tu penses

if bcrypt.checkpw(password, hashed):
    print("Mot de passe correct ✅")
else:
    print("Mot de passe incorrect ❌")