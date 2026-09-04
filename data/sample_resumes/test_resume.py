from pathlib import Path

from resume_parser import extract_resume_text

import sys

sys.path.append(
    str(
        Path(__file__).resolve().parents[2]
    )
)

from src.nlp.skill_extractor import (
    extract_skills,
    create_skill_vector
)


# ============================================================
# RESUME TEST
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RESUME = (
    BASE_DIR
    / "data"
    / "sample_resumes"
    / "test_resume.pdf"
)


print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("RESUME ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# EXTRACT TEXT
# ------------------------------------------------------------

text = extract_resume_text(
    RESUME
)


print("\nResume text extracted.")

print(
    f"Characters extracted: {len(text)}"
)


# ------------------------------------------------------------
# EXTRACT SKILLS
# ------------------------------------------------------------

skills = extract_skills(
    text
)


print("\nDetected Skills:")

if skills:

    for skill in skills:

        print(
            f"✓ {skill}"
        )

else:

    print(
        "No skills detected."
    )


# ------------------------------------------------------------
# CREATE VECTOR
# ------------------------------------------------------------

vector = create_skill_vector(
    text
)


print("\nSkill Vector:")

for skill, value in vector.items():

    print(
        f"{skill:20} : {value}"
    )


print("\n" + "=" * 60)
print("RESUME ANALYSIS COMPLETE")
print("=" * 60)