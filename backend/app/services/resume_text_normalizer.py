COMMON_RESUME_CORRECTIONS = {
    "Generative Al": "Generative AI",
    "generative al": "generative AI",
    "Artificial lntelligence": "Artificial Intelligence",
    "artificial lntelligence": "artificial intelligence",
    "Machine Leaming": "Machine Learning",
    "machine leaming": "machine learning",
    "Deep Leaming": "Deep Learning",
    "deep leaming": "deep learning",
    "Scikit leam": "Scikit-learn",
    "scikit leam": "scikit-learn",
}


def normalize_resume_text(text: str) -> str:
    if not text:
        return ""

    normalized = text

    for incorrect, correct in COMMON_RESUME_CORRECTIONS.items():
        normalized = normalized.replace(incorrect, correct)

    return normalized