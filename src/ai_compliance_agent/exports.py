"""Generate portable document artifacts without storing user content permanently."""

from __future__ import annotations

from io import BytesIO

from docx import Document


def corrected_docx_bytes(text: str) -> bytes:
    document = Document()
    document.add_heading("Corrected Compliance Document", level=1)
    for block in text.split("\n\n"):
        cleaned = block.strip()
        if cleaned:
            document.add_paragraph(cleaned)
    output = BytesIO()
    document.save(output)
    return output.getvalue()
