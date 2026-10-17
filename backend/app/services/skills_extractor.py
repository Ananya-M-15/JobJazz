import re

from app.utils.skill_vocabulary import SKILL_VOCABULARY

# Maintained for backward-compatibility if referenced elsewhere
SKILL_ALIASES = {
    alias.lower(): canonical
    for canonical, aliases in SKILL_VOCABULARY.items()
    for alias in aliases
}


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from resume text using the unified project SKILL_VOCABULARY.
    Ensures canonical naming, robust word-boundary matching, and parity with JD extraction.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = []

    for canonical_name, aliases in SKILL_VOCABULARY.items():
        for alias in aliases:
            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9+#])"
            )

            if re.search(pattern, text_lower):
                if canonical_name not in found_skills:
                    found_skills.append(canonical_name)
                break

    return found_skills