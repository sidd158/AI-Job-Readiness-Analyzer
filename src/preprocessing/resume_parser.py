import fitz
from docx import Document
from pathlib import Path


# ============================================================
# RESUME PARSER
# Supports PDF and DOCX
# ============================================================


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    text = []

    document = fitz.open(file_path)

    for page in document:
        page_text = page.get_text()

        if page_text:
            text.append(page_text)

    document.close()

    return "\n".join(text)


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX resume.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(
                paragraph.text.strip()
            )

    return "\n".join(paragraphs)


def extract_resume_text(file_path):
    """
    Automatically detect PDF/DOCX and extract text.
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(file_path)

    elif extension == ".docx":

        return extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please use PDF or DOCX."
        )


if __name__ == "__main__":

    print("=" * 60)
    print("RESUME TEXT EXTRACTION")
    print("=" * 60)

    print("\nThis module supports:")
    print("1. PDF")
    print("2. DOCX")