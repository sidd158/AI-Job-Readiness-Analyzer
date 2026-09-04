import fitz


def extract_text_from_pdf(uploaded_file):
    try:
        pdf_bytes = uploaded_file.getvalue()

        doc = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in doc:
            text += page.get_text("text") + "\n"

        doc.close()

        return text.strip()

    except Exception as e:
        return f"PDF_ERROR: {e}"