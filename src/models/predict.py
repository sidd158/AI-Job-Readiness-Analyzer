from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# AI JOB READINESS ANALYZER
# JOB SELECTION PREDICTION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "models"
    / "job_selection_model.pkl"
)


print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("JOB SELECTION PREDICTION")
print("=" * 60)


# ============================================================
# CHECK MODEL
# ============================================================

if not MODEL_FILE.exists():

    print()
    print("ERROR: Model not found.")
    print()
    print("Run:")
    print("python src\\models\\train_model.py")

    raise SystemExit(1)


# ============================================================
# LOAD MODEL
# ============================================================

print()
print("Loading trained model...")

model = joblib.load(
    MODEL_FILE
)

print("Model loaded successfully.")


# ============================================================
# CANDIDATE
# ============================================================

candidate = {

    "education": "B.Tech",

    "experience": 0,

    "python": 1,

    "sql": 1,

    "excel": 1,

    "power_bi": 1,

    "statistics": 1,

    "machine_learning": 0,

    "tableau": 0,

    "communication": 1,

    "git": 1,

    "data_visualization": 1,

    "projects": 3,

    "internships": 1,

    "certifications": 2,

    "target_role": "Data Analyst",

    "readiness_score": 72.5
}


# ============================================================
# DATAFRAME
# ============================================================

candidate_df = pd.DataFrame(
    [candidate]
)


# ============================================================
# GET TRAINING FEATURES
# ============================================================

try:

    preprocessor = (
        model.named_steps["preprocessor"]
    )

    transformers = (
        preprocessor.transformers_
    )

except Exception as error:

    print()
    print("ERROR reading model preprocessing:")
    print(error)

    raise SystemExit(1)


# ============================================================
# MAKE SURE CANDIDATE HAS ALL TRAINING COLUMNS
# ============================================================

training_columns = []

for transformer in transformers:

    if len(transformer) < 3:
        continue

    columns = transformer[2]

    if isinstance(columns, str):
        columns = [columns]

    training_columns.extend(
        list(columns)
    )


# Remove duplicates

training_columns = list(
    dict.fromkeys(
        training_columns
    )
)


# ============================================================
# ADD MISSING COLUMNS
# ============================================================

for column in training_columns:

    if column not in candidate_df.columns:

        candidate_df[column] = 0


# ============================================================
# KEEP ONLY TRAINING COLUMNS
# ============================================================

candidate_df = candidate_df[
    training_columns
]


# ============================================================
# FIX DATA TYPES
# ============================================================

for column in candidate_df.columns:

    if candidate_df[column].dtype == "object":

        candidate_df[column] = (
            candidate_df[column]
            .fillna("Unknown")
            .astype(str)
        )

    else:

        candidate_df[column] = pd.to_numeric(
            candidate_df[column],
            errors="coerce"
        )

        candidate_df[column] = (
            candidate_df[column]
            .fillna(0)
        )


# ============================================================
# PREDICTION
# ============================================================

print()
print("Running prediction...")


prediction = model.predict(
    candidate_df
)[0]


probabilities = model.predict_proba(
    candidate_df
)[0]


# ============================================================
# PROBABILITY
# ============================================================

classes = model.classes_

probability_map = dict(
    zip(
        classes,
        probabilities
    )
)


selection_probability = (
    probability_map.get(1, 0)
)


# ============================================================
# RESULT
# ============================================================

print()
print("=" * 60)
print("PREDICTION RESULT")
print("=" * 60)

print()

print(
    "Target Role:",
    candidate["target_role"]
)

print(
    "Readiness Score:",
    candidate["readiness_score"]
)

print()

if prediction == 1:

    print(
        "Prediction: LIKELY TO BE SELECTED"
    )

else:

    print(
        "Prediction: NEEDS IMPROVEMENT"
    )

print()

print(
    f"Selection Probability: "
    f"{selection_probability * 100:.2f}%"
)

print()

print("=" * 60)
print("PREDICTION COMPLETE")
print("=" * 60)