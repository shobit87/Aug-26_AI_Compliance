from io import BytesIO

from docx import Document

from ai_compliance_agent.exports import corrected_docx_bytes


def test_corrected_docx_is_valid_and_nonblank():
    content = corrected_docx_bytes("Corrected policy content")
    document = Document(BytesIO(content))
    assert content.startswith(b"PK")
    assert "Corrected policy content" in " ".join(p.text for p in document.paragraphs)