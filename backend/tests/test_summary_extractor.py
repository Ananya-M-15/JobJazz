from app.services.summary_extractor import extract_summary


def test_summary_extraction():
    text = """
    Introduction

    Aspiring Software Engineer and Data Analyst with experience in Python,
    SQL, React, and Machine Learning.

    Education

    Manipal University Jaipur
    """

    result = extract_summary(text)

    assert "Aspiring Software Engineer" in result
    assert "Machine Learning" in result
    assert "Education" not in result