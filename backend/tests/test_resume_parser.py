from app.services.resume_parser import parse_resume_text


def test_complete_resume_profile():
    text = """
    Ananya Maheshwari
    Jaipur
    ananyamaheshwari72@gmail.com
    +91 9828308428

    Introduction

    Aspiring Software Engineer and Data Analyst with experience in Python,
    SQL, React, and Machine Learning.

    Education

    Aug 2023 - July 2027
    Manipal University Jaipur
    B.Tech in Computer Science Engineering (AI & ML)

    2015 - 2023
    Jindal Vidya Mandir
    Senior Secondary Education (Class V - XII)

    Experience

    Feb 2024 - Apr 2025
    Senior Coordinator (Curations)
    IEEE WIE
    Coordinated technical events and cross-functional teams.

    Projects

    EduCaps
    Built a micro-learning platform using React and Django.

    Certifications

    NPTEL: Machine Learning
    """

    result = parse_resume_text(text)

    assert result.name == "Ananya Maheshwari"
    assert result.email == "ananyamaheshwari72@gmail.com"
    assert result.phone == "+91 9828308428"
    assert result.location == "Jaipur"

    assert result.summary != ""
    assert "Software Engineer" in result.summary

    assert len(result.education) == 2
    assert result.education[0].institution == "Manipal University Jaipur"

    assert len(result.experience) == 1
    assert result.experience[0].company == "IEEE WIE"

    assert len(result.projects) >= 1
    assert result.projects[0].name == "EduCaps"

    assert len(result.certifications) >= 1