import re
from resume_generator import generate_enhanced_resume

ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "optimized",
    "trained", "deployed", "created", "analyzed", "automated",
    "led", "improved", "engineered", "integrated", "researched"
]

METRIC_PATTERN = re.compile(r"\b\d+%|\b\d+\+|\b\d+x|\b\d+\b")


def weak_bullets(resume_text: str):
    """
    Returns bullets/sentences that are weak:
    - No action verb
    - No metrics
    - Too short
    - Vague self-descriptions
    """

    lines = [
        l.strip()
        for l in resume_text.split("\n")
        if len(l.strip()) > 10
    ]

    weak = []

    for line in lines:
        lower = line.lower()

        # Skip headers / names
        if lower.isupper() or lower in ["about", "skills", "education", "projects", "experience"]:
            continue

        has_action = any(v in lower for v in ACTION_VERBS)
        has_metric = bool(METRIC_PATTERN.search(lower))
        word_count = len(lower.split())

        if (
            not has_action
            or not has_metric
            or word_count < 8
            or lower.startswith(("passionate", "interested", "eager", "learning"))
        ):
            weak.append(line)

    return weak[:10]  # limit for UI


# ✅ ADD THIS (very important)
def enhance_resume(resume_text: str, job_description: str):
    """
    Wrapper used by FastAPI.
    Calls Gemini-based resume enhancement.
    """
    return generate_enhanced_resume(resume_text, job_description)
