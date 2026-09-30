from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_recommendation_api_falls_back_when_ai_fails(
    monkeypatch,
):
    from app.api.routes import recommendations

    def fake_ai_recommendations(
        match_result,
        skill_gap,
    ):
        raise RuntimeError("Gemini unavailable")

    monkeypatch.setattr(
        recommendations,
        "generate_ai_recommendations",
        fake_ai_recommendations,
    )

    payload = {
        "match_result": {
            "overall_score": 48.81,
            "matched_required_skills": [
                "Python",
                "SQL",
            ],
            "missing_required_skills": [
                "Pandas",
            ],
            "matched_preferred_skills": [
                "Git",
            ],
            "missing_preferred_skills": [
                "Docker",
            ],
            "keyword_matches": [
                "Python",
                "SQL",
                "Git",
            ],
            "keyword_gaps": [
                "Pandas",
                "Docker",
            ],
            "experience_match": False,
            "education_match": True,
        },
        "skill_gap": {
            "strengths": [
                "Python",
                "SQL",
                "Git",
            ],
            "critical_gaps": [
                "Pandas",
            ],
            "preferred_gaps": [
                "Docker",
            ],
            "experience_gap": True,
            "education_gap": False,
        },
    }

    response = client.post(
        "/recommendations/generate",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "fallback"
    assert "recommendations" in data
    assert data["recommendations"]["recommendations"]