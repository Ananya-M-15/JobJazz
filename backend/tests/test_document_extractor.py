from app.services.document_extractor import extract_document_text


def test_empty_document_rejected():
    try:
        extract_document_text(b"", "pdf")
        assert False
    except ValueError:
        assert True