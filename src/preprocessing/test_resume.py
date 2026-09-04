from pathlib import Path
import sys


# ============================================================
# AI JOB READINESS ANALYZER
# RESUME TEST
# ============================================================

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Allow imports from project root
sys.path.insert(0, str(BASE_DIR))


from src.preprocessing.resume_parser import (
    extract_resume_text
)

from src.nlp.skill_extractor import (
    extract_skills,
    create_skill_vector
)


# ============================================================
# RESUME LOCATION
# ============================================================

RESUME = (
    BASE_DIR
    / "data"
    / "sample_resumes"
    / "test_resume.pdf"
)


# ============================================================
# START
# ============================================================

print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("RESUME ANALYSIS")
print("=" * 60)

print()

print("Resume path:")
print(RESUME)

print()


# ============================================================
# CHECK RESUME
# ============================================================

if not RESUME.exists():

    print("ERROR: Resume file not found.")

    print()

    print("Please put your resume here:")

    print(
        BASE_DIR
        / "data"
        / "sample_resumes"
    )

    print()

    print("Required filename:")
    print("test_resume.pdf")

    sys.exit(1)


# ============================================================
# EXTRACT TEXT
# ============================================================

try:

    text = extract_resume_text(
        RESUME
    )

except Exception as error:

    print("ERROR while reading resume:")
    print(error)

    sys.exit(1)


print("Resume text extracted successfully.")

print(
    f"Characters extracted: {len(text)}"
)


# ============================================================
# CHECK EXTRACTED TEXT
# ============================================================

if not text.strip():

    print()
    print("WARNING:")
    print("No text was extracted from the PDF.")

    print()
    print(
        "The PDF may be a scanned/image-based resume."
    )

    print(
        "We can add OCR later."
    )

    sys.exit(1)


# ============================================================
# EXTRACT SKILLS
# ============================================================

skills = extract_skills(
    text
)


print()
print("=" * 60)
print("DETECTED SKILLS")
print("=" * 60)


if skills:

    for skill in skills:

        print(
            f"✓ {skill}"
        )

else:

    print(
        "No skills detected."
    )


# ============================================================
# SKILL VECTOR
# ============================================================

vector = create_skill_vector(
    text
)


print()
print("=" * 60)
print("SKILL VECTOR")
print("=" * 60)


for skill, value in vector.items():

    print(
        f"{skill:25} : {value}"
    )


# ============================================================
# FINISH
# ============================================================

print()
print("=" * 60)
print("RESUME ANALYSIS COMPLETE")
print("=" * 60)