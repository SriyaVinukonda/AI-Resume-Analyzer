import pdfplumber
import io

def extract_resume_text(upload_file):
    file_bytes = upload_file.file.read()
    text = ""

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.strip()
