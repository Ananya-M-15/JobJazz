from app.services.certification_extractor import extract_certifications


def test_certification_extraction():
    text = """
    Certifications

    NPTEL: Data Structures & Algorithms
    NPTEL: Design & Analysis of Algorithms
    NPTEL: Machine Learning
    NPTEL: Deep Learning
    Python: Python Essentials
    Microsoft Azure: Azure Certification
    Red Hat: Operating Systems
    Cisco: Computer Networks

    """

    result = extract_certifications(text)

    assert len(result) == 8

    names = [cert.name for cert in result]

    assert "Data Structures & Algorithms" in names
    assert "Machine Learning" in names
    assert "Deep Learning" in names
    assert "Azure Certification" in names
    assert "Computer Networks" in names