"""Shared upload validation for API and Streamlit entry points."""

from __future__ import annotations

from pathlib import Path


MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_SUFFIXES = {".pdf", ".docx", ".txt", ".md"}


class UploadValidationError(ValueError):
    pass


def validate_upload(filename: str, data: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise UploadValidationError("Supported file types are PDF, DOCX, TXT, and MD.")
    if not data:
        raise UploadValidationError("The uploaded file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise UploadValidationError("The uploaded file exceeds the 10 MB limit.")
    if suffix == ".pdf" and not data.startswith(b"%PDF-"):
        raise UploadValidationError("The file extension is PDF but its content is not a PDF.")
    if suffix == ".docx" and not data.startswith(b"PK"):
        raise UploadValidationError("The file extension is DOCX but its content is not a DOCX archive.")
    return suffix
