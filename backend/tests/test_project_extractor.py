from app.services.project_extractor import extract_projects


def test_project_extraction():
    text = """
    Projects

    EduCaps
    Built a micro-learning platform with responsive UI,
    progress tracking, and gamified learning.
    Developed using React, Django, MongoDB, HTML, and CSS.

    Fuel Forge
    Developed a machine learning-based fuel optimization system
    using neural networks.
    Built an interactive React interface.

    Certifications
    """

    result = extract_projects(text)

    assert len(result) >= 2

    names = [project.name for project in result]

    assert "EduCaps" in names
    assert "Fuel Forge" in names