import os
from fastapi import FastAPI, UploadFile, File, Form
from backend.database import get_connection
from fastapi import FastAPI, UploadFile, File, Form, Query, Depends
from fastapi import Body
import json
from backend.extract_text import extract_text_from_file
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi import status

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth import create_access_token, get_user, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines (tu peux restreindre plus tard)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossier local pour sauvegarder les fichiers
UPLOAD_FOLDER = "backend/uploads"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...),
                       created_by: str = Form(...),
                        metadata: str = Form("{}"),
                        current_user: dict = Depends(get_current_user) ):
    try:
        created_by = current_user["username"]

        # 1. Sauvegarde du fichier sur disque
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        #exrtraire le texte
        extracted_text = extract_text_from_file(file_path, file.content_type)

        # 2. Enregistrement dans Oracle
        conn = get_connection()
        cur = conn.cursor()

        doc_id = cur.var(int)

        cur.execute("""
            INSERT INTO ged_documents (original_name, storage_path, content_type, size_bytes, created_by, full_text)
            VALUES (:1, :2, :3, :4, :5, :6)
            RETURNING doc_id INTO :7
        """, (
            file.filename,
            file_path,
            file.content_type,
            os.path.getsize(file_path),
            created_by,
            extracted_text,
            doc_id
        ))
        #conn.commit()

        #generated_id = doc_id.getvalue()
        generated_id = doc_id.getvalue()[0]

        try:
            meta_dict = json.loads(metadata)
            for key, value in meta_dict.items():
                cur.execute("""
                    INSERT INTO ged_metadata (doc_id, meta_key, meta_value)
                    VALUES (:1, :2, :3)
                """, (generated_id, key, str(value)))

        except Exception as meta_err:
            print("⚠️ Erreur métadonnées:", meta_err)


        conn.commit()
        cur.close()
        conn.close()
        

        return {"status": "success", "doc_id": generated_id, "filename": file.filename, "indexed_text_length": len(extracted_text)}

    except Exception as e:
        return {"status": "error", "message": str(e)}



##############################################""""

@app.get("/search")
async def search_documents(
    keyword: str = Query(None, description="Mot-clé à chercher dans le nom ou le contenu"),
    created_by: str = Query(None, description="Filtrer par créateur"),
    meta_key: str = Query(None, description="Clé de métadonnée"),
    meta_value: str = Query(None, description="Valeur de métadonnée")
):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Construire la requête SQL dynamiquement
        sql = """
            SELECT d.doc_id, d.original_name, d.created_by, d.created_at
            FROM ged_documents d
            LEFT JOIN ged_metadata m ON d.doc_id = m.doc_id
            WHERE 1=1
        """
        params = {}

        if keyword:
            sql += " AND (LOWER(original_name) LIKE :keyword OR LOWER(full_text) LIKE :keyword)"
            params["keyword"] = f"%{keyword.lower()}%"

        if created_by:
            sql += " AND created_by = :created_by"
            params["created_by"] = created_by

        if meta_key and meta_value:
            sql += " AND m.meta_key = :meta_key AND m.meta_value = :meta_value"
            params["meta_key"] = meta_key
            params["meta_value"] = meta_value

        cur.execute(sql, params)

        results = []
        for row in cur:
            results.append({
                "doc_id": row[0],
                "original_name": row[1],
                "created_by": row[2],
                "created_at": str(row[3])
            })

        cur.close()
        conn.close()

        if not results:
            return {"status": "not_found", "results": []}

        return {"status": "success", "results": results}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    
#download
################################################################
from fastapi.responses import FileResponse

@app.get("/download/{doc_id}")
async def download_document(doc_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Récupérer le chemin du fichier
        cur.execute("""
            SELECT original_name, storage_path 
            FROM ged_documents 
            WHERE doc_id = :id
        """, {"id": doc_id})
        
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return {"status": "error", "message": "Document introuvable"}

        filename, filepath = row

        # Vérifier si le fichier existe sur le disque
        if not os.path.exists(filepath):
            return {"status": "error", "message": "Fichier manquant sur le serveur"}

        # Retourner le fichier
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/octet-stream"
        )

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    ####################################






@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    print("DEBUG login input:", form_data.username, form_data.password)  # 🔍
    print("DEBUG login user:", user)

    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Nom d’utilisateur ou mot de passe incorrect ")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


