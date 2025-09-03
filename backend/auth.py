from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.database import get_connection

# Config JWT
SECRET_KEY = "supersecretkey"   # ⚠️ change-la dans ton vrai projet
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Schéma d’authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Récupérer un utilisateur depuis Oracle
def get_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password, role FROM ged_users WHERE username = :u", {"u": username})
    row = cur.fetchone()
    cur.close()
    conn.close()
    print(">> DEBUG get_user:", row) # 👈 ça va s’afficher dans le terminal
    if row:
        return {"username": row[0], "password": row[1], "role": row[2]}
    return None

# Générer un JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Vérifier le token et retourner l'utilisateur
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    return user
