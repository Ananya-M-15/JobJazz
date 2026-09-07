from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.services.gemini_service import generate_ai_recommendations


match = MatchResult(
    overall_score=62.5,
    matched_required_skills=[
        "Python",
        "SQL",
    ],
    missing_required_skills=[
        "AWS",
    ],
    matched_preferred_skills=[
        "Docker",
    ],
    missing_preferred_skills=[
        "TensorFlow",
    ],
    keyword_matches=[
        "Python",
        "SQL",
        "Docker",
    ],
    keyword_gaps=[
        "AWS",
        "TensorFlow",
    ],
    experience_match=False,
    education_match=True,
)


skill_gap = SkillGapResult(
    strengths=[
        "Python",
        "SQL",
        "Docker",
    ],
    critical_gaps=[
        "AWS",
    ],
    preferred_gaps=[
        "TensorFlow",
    ],
    experience_gap=True,
    education_gap=False,
)


result = generate_ai_recommendations(
    match,
    skill_gap,
)

print(result.model_dump())