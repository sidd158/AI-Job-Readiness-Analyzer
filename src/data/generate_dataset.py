import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AI JOB READINESS ANALYZER
# DATASET GENERATOR
# ============================================================

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# SKILLS
# ------------------------------------------------------------

skills = [
    "python",
    "sql",
    "excel",
    "power_bi",
    "statistics",
    "machine_learning",
    "tableau",
    "communication",
    "git",
    "data_visualization"
]


# ------------------------------------------------------------
# JOB ROLES
# ------------------------------------------------------------

job_roles = [
    "Data Analyst",
    "Data Scientist",
    "Business Analyst",
    "Python Developer",
    "ML Engineer"
]


# ------------------------------------------------------------
# GENERATE CANDIDATES
# ------------------------------------------------------------

num_candidates = 500

candidates = []

for i in range(1, num_candidates + 1):

    candidate_id = f"C{i:04d}"

    education = np.random.choice(
        [
            "B.Tech",
            "B.E",
            "B.Sc",
            "BCA",
            "MCA",
            "M.Tech"
        ]
    )

    experience = np.random.choice(
        [0, 0, 0, 1, 1, 2],
        p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10]
    )

    skill_values = {
        skill: np.random.choice(
            [0, 1],
            p=[0.35, 0.65]
        )
        for skill in skills
    }

    projects = np.random.randint(0, 6)

    internships = np.random.randint(0, 3)

    certifications = np.random.randint(0, 5)

    target_role = np.random.choice(job_roles)

    candidates.append({
        "candidate_id": candidate_id,
        "education": education,
        "experience": experience,
        **skill_values,
        "projects": projects,
        "internships": internships,
        "certifications": certifications,
        "target_role": target_role
    })


candidates_df = pd.DataFrame(candidates)


# ------------------------------------------------------------
# CALCULATE READINESS SCORE
# ------------------------------------------------------------

skill_columns = skills

candidates_df["skill_score"] = (
    candidates_df[skill_columns].sum(axis=1)
    / len(skill_columns)
) * 100


candidates_df["experience_score"] = (
    candidates_df["experience"].clip(upper=2)
    / 2
) * 100


candidates_df["project_score"] = (
    candidates_df["projects"].clip(upper=5)
    / 5
) * 100


candidates_df["internship_score"] = (
    candidates_df["internships"].clip(upper=2)
    / 2
) * 100


candidates_df["certification_score"] = (
    candidates_df["certifications"].clip(upper=4)
    / 4
) * 100


# ------------------------------------------------------------
# FINAL READINESS SCORE
# ------------------------------------------------------------

candidates_df["readiness_score"] = (
    candidates_df["skill_score"] * 0.55
    + candidates_df["experience_score"] * 0.10
    + candidates_df["project_score"] * 0.15
    + candidates_df["internship_score"] * 0.10
    + candidates_df["certification_score"] * 0.10
)


# Add small randomness so the ML problem is realistic

noise = np.random.normal(
    loc=0,
    scale=5,
    size=num_candidates
)

candidates_df["readiness_score"] += noise

candidates_df["readiness_score"] = (
    candidates_df["readiness_score"]
    .clip(0, 100)
    .round(2)
)


# ------------------------------------------------------------
# READINESS CATEGORY
# ------------------------------------------------------------

def classify_readiness(score):

    if score >= 75:
        return "Ready"

    elif score >= 55:
        return "Needs Improvement"

    else:
        return "Not Ready"


candidates_df["readiness_category"] = (
    candidates_df["readiness_score"]
    .apply(classify_readiness)
)


# ------------------------------------------------------------
# JOB SELECTED
# ------------------------------------------------------------

selection_probability = (
    candidates_df["readiness_score"] / 100
)

random_values = np.random.random(num_candidates)

candidates_df["job_selected"] = (
    random_values < selection_probability
).astype(int)


# ------------------------------------------------------------
# REMOVE INTERMEDIATE COLUMNS
# ------------------------------------------------------------

candidates_df.drop(
    columns=[
        "skill_score",
        "experience_score",
        "project_score",
        "internship_score",
        "certification_score"
    ],
    inplace=True
)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

output_file = RAW_DIR / "candidates.csv"

candidates_df.to_csv(
    output_file,
    index=False
)


print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("DATASET GENERATION COMPLETE")
print("=" * 60)

print()

print(f"Rows created: {len(candidates_df)}")

print()

print("Columns:")
print(list(candidates_df.columns))

print()

print("Readiness distribution:")
print(
    candidates_df["readiness_category"]
    .value_counts()
)

print()

print(f"Saved to:")
print(output_file)

print()

print(candidates_df.head())