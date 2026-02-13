from text_cleaner import clean_text

# Expandable skill database
SKILLS_DB = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "nlp", "computer vision", "tensorflow", "pytorch", "streamlit",
    "flask", "django", "aws", "docker", "kubernetes",
    "data analysis", "pandas", "numpy", "scikit-learn",
    "react", "javascript", "html", "css", "git"
]


def extract_skills(text):
    text = clean_text(text)
    found = []

    for skill in SKILLS_DB:
        if skill in text:
            found.append(skill)

    return sorted(list(set(found)))
