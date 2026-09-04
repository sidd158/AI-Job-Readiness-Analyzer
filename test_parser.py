import fitz


pdf_path = "test_resume.pdf"


document = fitz.open(pdf_path)

text = ""

for page in document:
    text += page.get_text("text") + "\n"

document.close()


print("=" * 60)
print("EXTRACTED RESUME TEXT")
print("=" * 60)

print(text)

print("=" * 60)