# 📂 Projet GED – Gestion Électronique de Documents
<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/8e492e15-ca49-458b-b9dc-3bb388a5e96e" />

<img width="1919" height="901" alt="image" src="https://github.com/user-attachments/assets/1a4574c1-81af-4716-888d-39ab272c543f" />

<img width="1912" height="904" alt="image" src="https://github.com/user-attachments/assets/a72f6def-ab0e-4ac8-b4b4-4b4a8478d05c" />



## 📖 Description
Ce projet est une application simple de **Gestion Électronique de Documents (GED)**.  
Il permet :
- L’**upload** de documents avec des métadonnées.
- L’**indexation automatique** (extraction du texte).
- La **recherche avancée** (par mot-clé, auteur ou métadonnées).
- Le **téléchargement** de documents.
- Une **authentification simple** avec JWT.
- Une **interface web** (HTML/JS) pour interagir avec le système.

---

## 🛠️ Technologies utilisées
- **Backend** : Python (FastAPI) + Oracle Database
- **Frontend** : HTML / JavaScript (fetch API)
- **Base de données** : Oracle SQL
- **Librairies principales** :
  - `fastapi`
  - `uvicorn`
  - `python-oracledb`
  - `python-jose`
  - `python-multipart`
  - `pytesseract` + `Pillow` (pour OCR)

---

## 📂 Structure du projet
'ged_project/'
backend/
  main.py # API FastAPI
  database.py # Connexion Oracle
  auth.py # Authentification JWT
  uploads/ # Stockage local des fichiers

 frontend/
  login.html # Page de connexion
  upload.html # Page d’upload
  search.html # Page de recherche

 tables.sql # Script SQL pour créer les tables
 README.md # Documentation
## ⚙️ Installation

### 1. Base de données Oracle
- Installer Oracle Database (ou utiliser une instance existante).
- Exécuter le script `tables.sql` dans SQL*Plus ou Oracle SQL Developer :
  ```sql
  @tables.sql

### 2. Installer Python et les dépendances
Créer un environnement virtuel :
  python -m venv venv

venv\Scripts\activate      # Windows
Installer les dépendances :
pip install fastapi uvicorn python-oracledb python-jose passlib[bcrypt] python-multipart pytesseract Pillow

### 3. Lancer le serveur FastAPI
uvicorn backend.main:app --reload
Le backend sera disponible sur :
👉 http://127.0.0.1:8000/docs

### 4. Lancer le frontend
Va dans le dossier frontend/ :
cd frontend
Lance un serveur HTTP Python (port 5500 par exemple) :
python -m http.server 5500
Ouvre ton navigateur et tape :
👉 http://127.0.0.1:5500/login.html

### 🔑 Utilisateurs par défaut
Créés automatiquement via tables.sql :
Admin :
username : admin
password : admin123

### 🚀 Améliorations possibles
Gestion des rôles (admin / user).
Version avec mots de passe hachés.
Stockage sur S3 ou autre cloud.
Interface plus moderne (React, Vue.js).



