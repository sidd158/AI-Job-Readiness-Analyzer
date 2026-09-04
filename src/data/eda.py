import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# AI JOB READINESS ANALYZER
# EXPLORATORY DATA ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_candidates.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# BASIC INFORMATION
# ------------------------------------------------------------

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nStatistics:")
print(df.describe())


# ------------------------------------------------------------
# EDUCATION DISTRIBUTION
# ------------------------------------------------------------

print("\nEducation Distribution:")

print(
    df["education"]
    .value_counts()
)


# ------------------------------------------------------------
# TARGET ROLE DISTRIBUTION
# ------------------------------------------------------------

print("\nTarget Role Distribution:")

print(
    df["target_role"]
    .value_counts()
)


# ------------------------------------------------------------
# READINESS DISTRIBUTION
# ------------------------------------------------------------

print("\nReadiness Distribution:")

print(
    df["readiness_category"]
    .value_counts()
)


# ------------------------------------------------------------
# AVERAGE READINESS
# ------------------------------------------------------------

print("\nAverage Readiness Score:")

print(
    round(
        df["readiness_score"].mean(),
        2
    )
)


# ------------------------------------------------------------
# JOB SELECTION RATE
# ------------------------------------------------------------

selection_rate = (
    df["job_selected"].mean()
    * 100
)

print("\nJob Selection Rate:")

print(
    round(selection_rate, 2),
    "%"
)


# ------------------------------------------------------------
# SKILL ANALYSIS
# ------------------------------------------------------------

skill_columns = [
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


skill_percentages = (
    df[skill_columns]
    .mean()
    .sort_values(ascending=False)
    * 100
)


print("\nSkill Availability (%):")

print(
    skill_percentages.round(2)
)


# ------------------------------------------------------------
# GRAPH 1
# READINESS DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

df["readiness_category"].value_counts().plot(
    kind="bar"
)

plt.title(
    "Candidate Readiness Distribution"
)

plt.xlabel("Readiness Category")

plt.ylabel("Number of Candidates")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "readiness_distribution.png"
)

plt.show()


# ------------------------------------------------------------
# GRAPH 2
# SKILL AVAILABILITY
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

skill_percentages.plot(
    kind="bar"
)

plt.title(
    "Candidate Skill Availability"
)

plt.xlabel("Skill")

plt.ylabel("Candidates (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "skill_availability.png"
)

plt.show()


# ------------------------------------------------------------
# GRAPH 3
# JOB ROLE DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

df["target_role"].value_counts().plot(
    kind="bar"
)

plt.title(
    "Target Job Role Distribution"
)

plt.xlabel("Job Role")

plt.ylabel("Candidates")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "job_role_distribution.png"
)

plt.show()


# ------------------------------------------------------------
# GRAPH 4
# READINESS SCORE
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

df["readiness_score"].plot(
    kind="hist",
    bins=20
)

plt.title(
    "Readiness Score Distribution"
)

plt.xlabel("Readiness Score")

plt.ylabel("Number of Candidates")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "readiness_score_distribution.png"
)

plt.show()


print("\nEDA completed successfully.")

print("\nGraphs saved to:")

print(OUTPUT_DIR)