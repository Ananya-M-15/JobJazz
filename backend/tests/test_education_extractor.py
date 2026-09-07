from app.services.education_extractor import extract_education


def test_education_extraction():
    text = """
    Education

    Aug 2023 - July 2027
    Manipal University Jaipur
    B.Tech in Computer Science Engineering (AI & ML)

    Coursework: Machine Learning, CN, OS, NLP

    2015 - 2023
    Jindal Vidya Mandir
    Senior Secondary Education (Class V - XII)

    Technical Skills
    """

    result = extract_education(text)

    assert len(result) == 2

    assert result[0].institution == "Manipal University Jaipur"
    assert result[0].degree == "B.Tech"
    assert result[0].field_of_study == "Computer Science Engineering (AI & ML)"
    assert result[0].start_date == "Aug 2023"
    assert result[0].end_date == "July 2027"

    assert result[1].institution == "Jindal Vidya Mandir"
    assert result[1].degree == "Senior Secondary Education (Class V - XII)"
    assert result[1].start_date == "2015"
    assert result[1].end_date == "2023"