import pytest

from ai_compliance_agent.uploads import UploadValidationError, validate_upload


def test_rejects_extension_content_mismatch():
    with pytest.raises(UploadValidationError, match="not a PDF"):
        validate_upload("policy.pdf", b"plain text")


def test_accepts_text_document():
    assert validate_upload("policy.txt", b"change approval policy") == ".txt"