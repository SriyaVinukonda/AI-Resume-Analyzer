import streamlit as st

from resume_parser import extract_resume_text
from matcher import split_sections, section_score, missing_keywords, overall_score
from enhancer import (
    weak_bullets,
    weak_action_verbs,
    improvement_suggestions,
    skill_roadmap
)
from skill_extractor import extract_skills

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Checker",
    layout="wide"
)

# ---------------- CUSTOM CSS (GRADIENT) ----------------
st.markdown("""
<style>
/* Full background gradient */
.stApp {
    background: linear-gradient(135deg, #fff3b0, #ffb703);
}

/* Center card */
.main-card {
    background: white;
    padding: 2.5rem;
    border-radius: 18px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

/* Headings */
h1 {
    color: #ff8c00;
    font-weight: 800;
}
h2, h3 {
    color: #fb8500;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #ffb703, #fb8500);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    border: none;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #ffb703, #fb8500);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="main-card">
<h1 style='text-align:center;'>Is your resume good enough?</h1>
<h4 style='text-align:center;color:#555;'>
A free and fast AI resume checker doing crucial checks to ensure your resume is ready
to perform and get you interview callbacks.
</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- UPLOAD SECTION ----------------
with st.container():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        resume_file = st.file_uploader(
            "📄 Drop your resume here or choose a file",
            type=["pdf", "docx"]
        )

    st.caption("PDF & DOCX only • Max 2MB")

    jd_text = st.text_area(
        "📌 Paste Job Description",
        height=200,
        placeholder="Paste the job description here..."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN LOGIC ----------------
if resume_file and jd_text:
    resume_file.seek(0)
    resume_text = extract_resume_text(resume_file)

    if len(resume_text) < 100:
        st.error("❌ Resume text could not be read properly.")
    else:
        # -------- DETECTED SKILLS --------
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)

        st.header("🧠 Detected Skills")
        skills = extract_skills(resume_text)

        if skills:
            st.success(", ".join(skills))
        else:
            st.warning("No recognizable skills detected.")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------- SECTION SCORES --------
        sections = split_sections(resume_text)
        scores = [
            section_score(sections["skills"], jd_text),
            section_score(sections["experience"], jd_text),
            section_score(sections["education"], jd_text),
            section_score(sections["projects"], jd_text)
        ]
        final_score = overall_score(scores)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)

        st.header("📊 Resume Performance")
        st.metric("Overall ATS Score", f"{final_score}%")
        st.progress(final_score / 100)

        cols = st.columns(4)
        names = ["Skills", "Experience", "Education", "Projects"]
        for i in range(4):
            with cols[i]:
                st.subheader(names[i])
                st.progress(scores[i] / 100)
                st.write(f"{scores[i]}%")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------- GAPS & FEEDBACK --------
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)

        st.header("❌ Missing Keywords")
        missing = missing_keywords(resume_text, jd_text)
        if missing:
            st.error(", ".join(missing[:20]))
        else:
            st.success("No major keyword gaps 🎉")

        st.header("✍ Bullet Point Quality")
        weak = weak_bullets(resume_text)
        if weak:
            for w in weak[:5]:
                st.warning(w)
        else:
            st.success("Strong bullet points detected 💪")

        st.header("⚠ Action Verb Analysis")
        verbs = weak_action_verbs(resume_text)
        if verbs:
            st.warning("Weak verbs used: " + ", ".join(verbs))
        else:
            st.success("Strong action verbs used 🎯")

        st.header("🛠 Improvement Suggestions")
        for s in improvement_suggestions(missing):
            st.info(s)

        st.header("📈 Skill Gap Roadmap")
        for r in skill_roadmap(missing):
            st.success(r)

        st.markdown("</div>", unsafe_allow_html=True)
