import re


def calculate_text_quality(text: str) -> dict:
    """
    Estimate whether extracted text is usable for resume analysis.

    This is a heuristic quality check, not a perfect classifier.
    """

    if not text or not text.strip():
        return {
            "quality": "poor",
            "score": 0,
            "character_count": 0,
            "word_count": 0,
            "alphabetic_ratio": 0.0,
            "garbled_ratio": 0.0,
        }

    stripped_text = text.strip()

    character_count = len(stripped_text)

    words = re.findall(
        r"\b[\w+#.-]+\b",
        stripped_text,
    )

    word_count = len(words)

    alphabetic_characters = sum(
        character.isalpha()
        for character in stripped_text
    )

    visible_characters = sum(
        not character.isspace()
        for character in stripped_text
    )

    alphabetic_ratio = (
        alphabetic_characters / visible_characters
        if visible_characters
        else 0.0
    )

    garbled_characters = sum(
        character in "�□"
        for character in stripped_text
    )

    garbled_ratio = (
        garbled_characters / character_count
        if character_count
        else 0.0
    )

    # Basic heuristic scoring.
    score = 100

    if character_count < 100:
        score -= 50
    elif character_count < 300:
        score -= 20

    if word_count < 20:
        score -= 30
    elif word_count < 50:
        score -= 10

    if alphabetic_ratio < 0.30:
        score -= 30
    elif alphabetic_ratio < 0.50:
        score -= 10

    if garbled_ratio > 0.05:
        score -= 40
    elif garbled_ratio > 0.01:
        score -= 20

    score = max(0, min(score, 100))

    if score >= 70:
        quality = "good"
    elif score >= 40:
        quality = "fair"
    else:
        quality = "poor"

    return {
        "quality": quality,
        "score": score,
        "character_count": character_count,
        "word_count": word_count,
        "alphabetic_ratio": round(alphabetic_ratio, 3),
        "garbled_ratio": round(garbled_ratio, 3),
    }
    