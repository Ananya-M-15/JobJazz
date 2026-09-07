import re

from app.utils.skill_vocabulary import SKILL_VOCABULARY


def extract_skills_from_text(text: str) -> list[str]:
    if not text:
        return []

    text_lower = text.lower()

    found_skills = []

    for skill, aliases in SKILL_VOCABULARY.items():
        for alias in aliases:
            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9+#])"
            )

            if re.search(pattern, text_lower):
                found_skills.append(skill)
                break

    return found_skills


def extract_job_skills(
    required_text: str,
    preferred_text: str,
) -> tuple[list[str], list[str]]:

    required_skills = extract_skills_from_text(
        required_text
    )

    preferred_skills = extract_skills_from_text(
        preferred_text
    )

    return required_skills, preferred_skills