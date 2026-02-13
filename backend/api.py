from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from resume_parser import extract_resume_text
from resume_generator import generate_enhanced_resume
from pdf_generator import generate_resume_pdf

from matcher import ats_score, missing_keywords
from enhancer import weak_bullets
from weak_bullets import analyze_weak_bullets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DOWNLOAD ENHANCED RESUME PDF ----------
@app.post("/download")
async def download_resume(
    resume: UploadFile = File(...),
    jd: str = Form(...)
):
    resume_text = extract_resume_text(resume)
    enhanced_resume = generate_enhanced_resume(resume_text, jd)

    pdf_path = generate_resume_pdf(enhanced_resume)

    return FileResponse(
        pdf_path,
        filename="Enhanced_Resume.pdf",
        media_type="application/pdf"
    )

# ---------- ANALYZE RESUME ----------
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd: str = Form(...)
):
    resume_text = extract_resume_text(resume)

    overall_score, section_scores_data = ats_score(resume_text, jd)

    return {
        "overall_score": overall_score,
        "section_scores": section_scores_data,
        "missing_keywords": missing_keywords(resume_text, jd),
        "weak_bullets": analyze_weak_bullets(weak_bullets(resume_text)),
        "improved_resume": generate_enhanced_resume(resume_text, jd)
    }
