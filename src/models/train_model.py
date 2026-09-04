from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# AI JOB READINESS ANALYZER
# MODEL TRAINING
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_candidates.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_FILE = (
    MODEL_DIR
    / "job_selection_model.pkl"
)


# ============================================================
# START
# ============================================================

print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("MACHINE LEARNING MODEL TRAINING")
print("=" * 60)


# ============================================================
# CHECK DATASET
# ============================================================

if not DATA_FILE.exists():

    print()
    print("ERROR: Dataset not found.")
    print()
    print("Expected file:")
    print(DATA_FILE)
    print()
    print("Check your data\\processed folder.")

    raise SystemExit(1)


# ============================================================
# LOAD DATA
# ============================================================

print()
print("Loading dataset...")

df = pd.read_csv(DATA_FILE)

print(
    f"Dataset shape: {df.shape}"
)

print()
print("Columns:")

print(
    df.columns.tolist()
)


# ============================================================
# TARGET
# ============================================================

TARGET = "job_selected"


if TARGET not in df.columns:

    print()
    print(
        f"ERROR: Target column '{TARGET}' "
        "was not found."
    )

    print()
    print("Available columns:")

    print(
        df.columns.tolist()
    )

    raise SystemExit(1)


# ============================================================
# FEATURES
# ============================================================

requested_features = [

    "education",
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

    "target_role",

    "readiness_score"
]


# ============================================================
# USE ONLY EXISTING FEATURES
# ============================================================

features = [
    column
    for column in requested_features
    if column in df.columns
]


missing_features = [
    column
    for column in requested_features
    if column not in df.columns
]


print()
print("Features used:")

print(features)


if missing_features:

    print()
    print("Features not found:")

    print(missing_features)


if len(features) == 0:

    print()
    print("ERROR: No usable features found.")

    raise SystemExit(1)


# ============================================================
# PREPARE DATA
# ============================================================

X = df[features].copy()

y = df[TARGET].copy()


# ============================================================
# CLEAN TARGET
# ============================================================

if y.dtype == "object":

    y = (
        y.astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "yes": 1,
            "no": 0,
            "selected": 1,
            "not selected": 0,
            "true": 1,
            "false": 0
        })
    )


y = pd.to_numeric(
    y,
    errors="coerce"
)


# Remove invalid target rows

valid_rows = y.notna()

X = X.loc[valid_rows].copy()

y = y.loc[valid_rows].astype(int)


# ============================================================
# CLEAN FEATURES
# ============================================================

categorical_features = []

numerical_features = []


for column in features:

    if X[column].dtype == "object":

        categorical_features.append(
            column
        )

    else:

        numerical_features.append(
            column
        )


# Fill missing numerical values

for column in numerical_features:

    X[column] = pd.to_numeric(
        X[column],
        errors="coerce"
    )

    X[column] = X[column].fillna(
        X[column].median()
    )


# Fill missing categorical values

for column in categorical_features:

    X[column] = (
        X[column]
        .fillna("Unknown")
        .astype(str)
    )


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

print()
print("Target distribution:")

print(
    y.value_counts()
)


if y.nunique() < 2:

    print()
    print(
        "ERROR: Target must contain "
        "at least two classes."
    )

    raise SystemExit(1)


# ============================================================
# PREPROCESSOR
# ============================================================

transformers = []


if categorical_features:

    transformers.append(

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        )
    )


if numerical_features:

    transformers.append(

        (
            "numerical",

            "passthrough",

            numerical_features
        )
    )


preprocessor = ColumnTransformer(
    transformers=transformers
)


# ============================================================
# RANDOM FOREST
# ============================================================

classifier = RandomForestClassifier(

    n_estimators=200,

    max_depth=10,

    min_samples_split=5,

    random_state=42,

    class_weight="balanced"
)


# ============================================================
# PIPELINE
# ============================================================

model = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            classifier
        )
    ]
)


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

try:

    X_train, X_test, y_train, y_test = (
        train_test_split(

            X,

            y,

            test_size=0.20,

            random_state=42,

            stratify=y
        )
    )

except ValueError:

    X_train, X_test, y_train, y_test = (
        train_test_split(

            X,

            y,

            test_size=0.20,

            random_state=42
        )
    )


print()
print(
    f"Training rows: {len(X_train)}"
)

print(
    f"Testing rows: {len(X_test)}"
)


# ============================================================
# TRAIN
# ============================================================

print()
print("Training Random Forest...")

model.fit(
    X_train,
    y_train
)

print(
    "Training completed."
)


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(
    X_test
)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print()
print("=" * 60)

print(
    f"MODEL ACCURACY: "
    f"{accuracy * 100:.2f}%"
)

print("=" * 60)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print()
print("Classification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print()
print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_FILE
)


print()
print("=" * 60)

print("MODEL SAVED SUCCESSFULLY")

print("=" * 60)

print()
print(
    MODEL_FILE
)

print()
print("Training complete.")