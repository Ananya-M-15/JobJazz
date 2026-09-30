from app.models.match_result import MatchResult
from app.models.skill_gap import SkillGapResult
from app.services.recommendation_engine import (
    generate_recommendations,
)


def test_deterministic_recommendations():
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
        experience_match=False,
        education_match=True,
    )

    skill_gap = SkillGapResult(
        strengths=[
            "Python",
            "SQL",
            "Machine Learning",
            "Generative AI",
            "NLP",
            "Git",
            "GitHub",
        ],
        critical_gaps=[
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "REST APIs",
        ],
        preferred_gaps=[
            "Docker",
            "AWS",
        ],
        experience_gap=True,
        education_gap=False,
    )

    result = generate_recommendations(
        match_result,
        skill_gap,
    )

    assert len(result.recommendations) == 7

    recommendation_skills = [
        recommendation.skill
        for recommendation in result.recommendations
    ]

    assert "Scikit-learn" in recommendation_skills
    assert "Pandas" in recommendation_skills
    assert "NumPy" in recommendation_skills
    assert "REST APIs" in recommendation_skills
    assert "Docker" in recommendation_skills
    assert "AWS" in recommendation_skills
    assert "Experience" in recommendation_skills

    high_priority = [
        recommendation.skill
        for recommendation in result.recommendations
        if recommendation.priority == "High"
    ]

    assert "Scikit-learn" in high_priority
    assert "Pandas" in high_priority
    assert "NumPy" in high_priority
    assert "REST APIs" in high_priority
    assert "Experience" in high_priority

    medium_priority = [
        recommendation.skill
        for recommendation in result.recommendations
        if recommendation.priority == "Medium"
    ]

    assert "Docker" in medium_priority
    assert "AWS" in medium_priority

    assert result.overall_advice != ""


def test_recommendation_action_for_known_skill():
    match_result = MatchResult(
        overall_score=50,
        missing_required_skills=["Pandas"],
    )

    skill_gap = SkillGapResult(
        critical_gaps=["Pandas"],
    )

    result = generate_recommendations(
        match_result,
        skill_gap,
    )

    assert len(result.recommendations) == 1
    assert result.recommendations[0].skill == "Pandas"
    assert result.recommendations[0].priority == "High"
    assert "Pandas" in result.recommendations[0].action


def test_no_gap_produces_no_recommendations():
    match_result = MatchResult(
        overall_score=100,
        experience_match=True,
        education_match=True,
    )

    skill_gap = SkillGapResult(
        strengths=["Python", "SQL"],
    )

    result = generate_recommendations(
        match_result,
        skill_gap,
    )

    assert result.recommendations == []
    assert result.overall_advice != ""