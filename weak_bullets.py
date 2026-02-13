import re

ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "optimized",
    "analyzed", "created", "led", "improved", "managed"
]

# ❌ Lines that should NEVER be treated as bullets
IGNORE_PATTERNS = [
    r"@",                    # email
    r"\b\d{10}\b",            # phone number
    r"btech|b\.tech|degree|university|college|school",
    r"cgpa|gpa|grade|percentage|%",
    r"education",
    r"skills",
    r"certifications?",
    r"projects?",
    r"experience",
    r"summary",
    r"name",
]

def is_non_bullet(line: str) -> bool:
    text = line.lower().strip()

    # Too short to be a bullet
    if len(text.split()) < 4:
        return True

    # Headings or irrelevant info
    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


def analyze_weak_bullets(bullets: list[str]):
    results = []

    for b in bullets:
        if is_non_bullet(b):
            continue  # 🚫 skip name, college, email, grades, headings

        reasons = []

        # Too short
        if len(b.split()) < 8:
            reasons.append("Too short and lacks detail")

        # No action verb
        if not any(verb in b.lower() for verb in ACTION_VERBS):
            reasons.append("Missing strong action verb")

        # No numbers / metrics
        if not re.search(r"\d+|%|\$", b):
            reasons.append("No metrics or measurable impact")

        # Generic wording
        if any(word in b.lower() for word in ["responsible for", "worked on", "helped"]):
            reasons.append("Uses generic wording")

        if reasons:
            results.append({
                "bullet": b.strip(),
                "reasons": reasons
            })

    return results
