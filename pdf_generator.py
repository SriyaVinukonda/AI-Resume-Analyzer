from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
import re
import html
import unicodedata

def normalize_text(text: str) -> str:
    """
    Convert Unicode text to safe ASCII for ReportLab
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return text



def _clean_text(text: str) -> str:
    """
    Clean LLM output so ReportLab never crashes
    """
    text = html.escape(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # remove markdown bold
    text = re.sub(r"[`_]", "", text)
    return text


def generate_resume_pdf(resume_text: str, output_path="enhanced_resume.pdf"):
    """
    Generate a modern, ATS-friendly resume PDF
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # ---------- Custom Styles ----------
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=18,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        textColor=HexColor("#1f2937"),
        spaceAfter=8,
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor("#4b5563"),
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=HexColor("#f59e0b"),  # yellow-orange accent
        spaceBefore=14,
        spaceAfter=6,
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=11,
        fontName="Helvetica-Bold",
        textColor=HexColor("#111827"),
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=HexColor("#1f2937"),
        spaceAfter=6,
    )

    story = []

    section_keywords = {
        "summary", "objective", "experience", "education", "skills",
        "projects", "certifications", "achievements", "profile"
    }

    resume_text = normalize_text(resume_text)
    lines = resume_text.split("\n")


    for i, raw_line in enumerate(lines):
        line = _clean_text(raw_line.strip())

        if not line:
            story.append(Spacer(1, 8))
            continue

        lower = line.lower()

        # Name (top of resume)
        if i < 3 and (raw_line.isupper() or len(raw_line.split()) <= 4):
            story.append(Paragraph(line, title_style))
            continue

        # Contact info
        if "@" in line or re.search(r"\d{10}|\d{3}[-.\s]\d{3}", line):
            story.append(Paragraph(line, contact_style))
            continue

        # Section headings
        if lower in section_keywords or raw_line.isupper():
            story.append(Paragraph(line.upper(), heading_style))
            continue

        # Bullet points
        if raw_line.startswith(("•", "-", "*")):
            bullet = raw_line.lstrip("•-* ").strip()
            story.append(Paragraph(f"• {bullet}", body_style))
            continue

        # Subheadings (company | role | duration)
        if "|" in raw_line and len(raw_line) < 120:
            story.append(Paragraph(line, subheading_style))
            continue

        # Normal text
        story.append(Paragraph(line, body_style))

    doc.build(story)
    return output_path
