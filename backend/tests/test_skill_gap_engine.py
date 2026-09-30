from app.models.match_result import MatchResult
from app.services.skill_gap_engine import calculate_skill_gap


def test_skill_gap_calculation():
    match_result = MatchResult(
        overall_score=48.81,
        matched_required_skills=[
            "Python",
            "SQL",
            "Machine Learning",
        ],
        missing_required_skills=[
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "REST APIs",
        ],
        matched_preferred_skills=[
            "Generative AI",
            "NLP",
            "Git",
            "GitHub",
        ],
        missing_preferred_skills=[
            "Docker",
            "AWS",
        ],
        keyword_matches=[
            "Python",
            "SQL",
            "Machine Learning",
            "Generative AI",
            "NLP",
            "Git",
            "GitHub",
        ],
        keyword_gaps=[
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "REST APIs",
            "Docker",
            "AWS",
        ],
        experience_match=False,
        education_match=True,
    )

    result = calculate_skill_gap(match_result)

    assert result.strengths == [
        "Python",
        "SQL",
        "Machine Learning",
        "Generative AI",
        "NLP",
        "Git",
        "GitHub",
    ]

    assert result.critical_gaps == [
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "REST APIs",
    ]

    assert result.preferred_gaps == [
        "Docker",
        "AWS",
    ]

    assert result.experience_gap is True
    assert result.education_gap is False


def test_empty_skill_gap():
    match_result = MatchResult(
        overall_score=100,
        matched_required_skills=["Python"],
        experience_match=True,
        education_match=True,
    )

    result = calculate_skill_gap(match_result)

    assert result.strengths == ["Python"]
    assert result.critical_gaps == []
    assert result.preferred_gaps == []
    assert result.experience_gap is False
    assert result.education_gap is False