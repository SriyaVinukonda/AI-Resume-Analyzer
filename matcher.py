import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------
# CLEAN TEXT
# --------------------
def clean(text):
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


# --------------------
# EXPERIENCE SCORE
# --------------------
def experience_score(text):
    text = text.lower()

    duration = re.search(r"\d+\s*(year|years|month|months)", text)
    job_words = re.search(
        r"(intern|internship|experience|worked|employment|company|organization)",
        text
    )

    if not duration and not job_words:
        return 0

    score = 50
    if duration:
        score += 30
    if job_words:
        score += 30

    return min(score, 100)


# --------------------
# SKILL MATCH
# --------------------
def skill_score(resume, jd):
    tfidf = TfidfVectorizer(stop_words="english")
    vec = tfidf.fit_transform([resume, jd])
    return round(cosine_similarity(vec[0:1], vec[1:2])[0][0] * 100, 2)


# --------------------
# KEYWORD MATCH
# --------------------
def keyword_score(resume, jd):
    r = set(clean(resume).split())
    j = set(clean(jd).split())
    if not j:
        return 0
    return round(len(r & j) / len(j) * 100, 2)


# --------------------
# MISSING KEYWORDS (ATS-GRADE)
# --------------------
def missing_keywords(resume, jd):
    resume_words = set(clean(resume).split())
    jd_words = set(clean(jd).split())

    important = [
        w for w in jd_words
        if len(w) > 3 and w not in resume_words
    ]

    return sorted(list(set(important)))[:25]


# --------------------
# SECTION SCORES
# --------------------
def section_scores(resume):
    text = resume.lower()

    return {
        "experience": experience_score(text),
        "education": 100 if "education" in text else 40,
        "skills": 100 if "skills" in text else 50,
        "projects": 88 if "project" in text else 50,
        "certifications": 90 if "certification" in text else 30
    }


# --------------------
# FINAL ATS SCORE (ENHANCV STYLE)
# --------------------
def ats_score(resume, jd):
    resume_c = clean(resume)
    jd_c = clean(jd)

    skill = skill_score(resume_c, jd_c)
    keyword = keyword_score(resume_c, jd_c)
    experience = experience_score(resume)

    # Enhancv-style weighted formula
    overall = round(
        0.5 * skill +
        0.4 * keyword +
        0.3 * experience,
        2
    )

    section_scores_dict = {
        "Skills Match": skill,
        "Keyword Match": keyword,
        "Experience": experience
    }

    return overall, section_scores_dict
