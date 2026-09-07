from app.services.contact_extractor import extract_contact_information


def test_contact_information():
    text = """
    Ananya Maheshwari
    Jaipur
    ananyamaheshwari72@gmail.com
    +91 9828308428
    """

    result = extract_contact_information(text)

    assert result["name"] == "Ananya Maheshwari"
    assert result["email"] == "ananyamaheshwari72@gmail.com"
    assert result["phone"] == "+91 9828308428"
    assert result["location"] == "Jaipur"