import os
import pytesseract
import pdfplumber
from docx import Document
from PIL import Image

# Définir le chemin vers Tesseract si nécessaire (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_file(filepath, content_type):
    text = ""

    try:
        # Cas 1 : PDF (texte ou image)
        if content_type == "application/pdf":
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            # Si rien trouvé (probablement image scannée), OCR
            if not text.strip():
                text = pytesseract.image_to_string(Image.open(filepath))

        # Cas 2 : Images
        elif content_type.startswith("image/"):
            text = pytesseract.image_to_string(Image.open(filepath))

        # Cas 3 : Word
        elif content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            doc = Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"

        # Cas 4 : Texte brut
        elif content_type.startswith("text/"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

    except Exception as e:
        print(f"⚠️ Erreur extraction texte: {e}")

    return text.strip()
