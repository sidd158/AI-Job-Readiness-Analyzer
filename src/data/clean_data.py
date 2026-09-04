import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AI JOB READINESS ANALYZER
# DATA CLEANING
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "raw" / "candidates.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "cleaned_candidates.csv"


print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("DATA CLEANING")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")


# ------------------------------------------------------------
# 2. DISPLAY BASIC INFORMATION
# ------------------------------------------------------------

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 3. CHECK DUPLICATES
# ------------------------------------------------------------

duplicate_count = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicate_count}")

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")


# ------------------------------------------------------------
# 4. CHECK MISSING VALUES
# ------------------------------------------------------------

print("\nMissing values:")

missing = df.isnull().sum()

print(missing[missing > 0])

if missing.sum() == 0:
    print("No missing values found.")


# ------------------------------------------------------------
# 5. CLEAN TEXT COLUMNS
# ------------------------------------------------------------

text_columns = [
    "candidate_id",
    "education",
    "target_role",
    "readiness_category"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )


# ------------------------------------------------------------
# 6. CLEAN NUMERIC COLUMNS
# ------------------------------------------------------------

numeric_columns = [
    "experience",
    "python",
    "sql",
    "excel",
    "power_bi",
    "statistics",
    "machine_learning",
    "tableau",
    "communication",
    "git",
    "data_visualization",
    "projects",
    "internships",
    "certifications",
    "readiness_score",
    "job_selected"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ------------------------------------------------------------
# 7. HANDLE NUMERIC MISSING VALUES
# ------------------------------------------------------------

for column in numeric_columns:

    if column in df.columns:

        if df[column].isnull().sum() > 0:

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )


# ------------------------------------------------------------
# 8. FIX BINARY SKILL VALUES
# ------------------------------------------------------------

binary_columns = [
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

for column in binary_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .round()
            .clip(0, 1)
            .astype(int)
        )


# ------------------------------------------------------------
# 9. FIX COUNTER VARIABLES
# ------------------------------------------------------------

counter_columns = [
    "experience",
    "projects",
    "internships",
    "certifications"
]

for column in counter_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .round()
            .clip(lower=0)
            .astype(int)
        )


# ------------------------------------------------------------
# 10. FIX READINESS SCORE
# ------------------------------------------------------------

if "readiness_score" in df.columns:

    df["readiness_score"] = (
        df["readiness_score"]
        .clip(0, 100)
        .round(2)
    )


# ------------------------------------------------------------
# 11. FIX JOB SELECTED
# ------------------------------------------------------------

if "job_selected" in df.columns:

    df["job_selected"] = (
        df["job_selected"]
        .round()
        .clip(0, 1)
        .astype(int)
    )


# ------------------------------------------------------------
# 12. RECREATE READINESS CATEGORY
# ------------------------------------------------------------

def classify_readiness(score):

    if score >= 75:
        return "Ready"

    elif score >= 55:
        return "Needs Improvement"

    else:
        return "Not Ready"


df["readiness_category"] = (
    df["readiness_score"]
    .apply(classify_readiness)
)


# ------------------------------------------------------------
# 13. FINAL MISSING VALUE CHECK
# ------------------------------------------------------------

print("\nMissing values after cleaning:")

remaining_missing = df.isnull().sum()

if remaining_missing.sum() == 0:

    print("No missing values.")

else:

    print(
        remaining_missing[
            remaining_missing > 0
        ]
    )


# ------------------------------------------------------------
# 14. FINAL DUPLICATE CHECK
# ------------------------------------------------------------

print(
    f"\nDuplicate rows after cleaning: "
    f"{df.duplicated().sum()}"
)


# ------------------------------------------------------------
# 15. SAVE CLEAN DATA
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 16. SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)

print(f"Final rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nReadiness distribution:")

print(
    df["readiness_category"]
    .value_counts()
)

print("\nJob selection distribution:")

print(
    df["job_selected"]
    .value_counts()
)

print("\nSaved file:")

print(OUTPUT_FILE)