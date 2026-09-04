from pathlib import Path
import sys

# ============================================================
# AI JOB READINESS ANALYZER
# SKILL GAP ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE_DIR))

from src.matching.job_requirements import get_job_requirements


def calculate_skill_gap(candidate_skills, job_role):

    required_skills = set(
        get_job_requirements(job_role)
    )

    candidate_skills = set(
        candidate_skills
    )

    matched_skills = (
        required_skills
        & candidate_skills
    )

    missing_skills = (
        required_skills
        - candidate_skills
    )

    extra_skills = (
        candidate_skills
        - required_skills
    )

    total_required = len(
        required_skills
    )

    matched_count = len(
        matched_skills
    )

    if total_required > 0:

        match_percentage = (
            matched_count
            / total_required
        ) * 100

    else:

        match_percentage = 0

    return {
        "job_role": job_role,

        "required_skills": sorted(
            required_skills
        ),

        "matched_skills": sorted(
            matched_skills
        ),

        "missing_skills": sorted(
            missing_skills
        ),

        "extra_skills": sorted(
            extra_skills
        ),

        "match_percentage": round(
            match_percentage,
            2
        )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    candidate_skills = [
        "python",
        "sql",
        "excel",
        "pandas",
        "numpy",
        "git"
    ]

    job_role = "Data Analyst"

    result = calculate_skill_gap(
        candidate_skills,
        job_role
    )

    print("=" * 60)
    print("AI JOB READINESS ANALYZER")
    print("SKILL GAP ANALYSIS")
    print("=" * 60)

    print(
        f"\nJob Role: {result['job_role']}"
    )

    print(
        f"Match Score: "
        f"{result['match_percentage']}%"
    )

    print("\nRequired Skills:")

    for skill in result["required_skills"]:
        print(f"  • {skill}")

    print("\nMatched Skills:")

    for skill in result["matched_skills"]:
        print(f"  ✓ {skill}")

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:
        print(f"  ✗ {skill}")

    print("\nAdditional Skills:")

    for skill in result["extra_skills"]:
        print(f"  + {skill}")

    print("\n" + "=" * 60)