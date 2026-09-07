from app.services.experience_extractor import extract_experience


def test_experience_extraction():
    text = """
    Experience

    Feb 2024 - Apr 2025
    Senior Coordinator (Curations)
    IEEE WIE
    Coordinated technical events, sponsorship outreach, and cross-functional teams.

    May 2026 - July 2026
    Tech Intern
    HomeSkool
    Contributed to platform development by working on backend integration,
    database operations, debugging, and feature enhancements.

    Projects
    """

    result = extract_experience(text)

    assert len(result) == 2

    assert result[0].company == "IEEE WIE"
    assert result[0].role == "Senior Coordinator (Curations)"
    assert result[0].start_date == "Feb 2024"
    assert result[0].end_date == "Apr 2025"
    assert "technical events" in result[0].description

    assert result[1].company == "HomeSkool"
    assert result[1].role == "Tech Intern"
    assert result[1].start_date == "May 2026"
    assert result[1].end_date == "July 2026"
    assert "backend integration" in result[1].description