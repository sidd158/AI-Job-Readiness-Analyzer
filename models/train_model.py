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
# MACHINE LEARNING MODEL
# ============================================================


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("MACHINE LEARNING MODEL")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_FILE)

print(
    f"Dataset shape: {df.shape}"
)


# ------------------------------------------------------------
# TARGET
# ------------------------------------------------------------

TARGET = "job_selected"


# ------------------------------------------------------------
# FEATURES
# ------------------------------------------------------------

features = [
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


X = df[features]

y = df[TARGET]


# ------------------------------------------------------------
# DISPLAY TARGET DISTRIBUTION
# ------------------------------------------------------------

print("\nTarget distribution:")

print(
    y.value_counts()
)


# ------------------------------------------------------------
# CATEGORICAL FEATURES
# ------------------------------------------------------------

categorical_features = [
    "education",
    "target_role"
]


# ------------------------------------------------------------
# NUMERICAL FEATURES
# ------------------------------------------------------------

numerical_features = [
    column
    for column in features
    if column not in categorical_features
]


# ------------------------------------------------------------
# PREPROCESSOR
# ------------------------------------------------------------

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        ),

        (
            "numerical",

            "passthrough",

            numerical_features
        )
    ]
)


# ------------------------------------------------------------
# RANDOM FOREST
# ------------------------------------------------------------

classifier = RandomForestClassifier(

    n_estimators=200,

    max_depth=10,

    min_samples_split=5,

    random_state=42,

    class_weight="balanced"
)


# ------------------------------------------------------------
# PIPELINE
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# TRAIN TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining rows:")
print(len(X_train))

print("\nTesting rows:")
print(len(X_test))


# ------------------------------------------------------------
# TRAIN
# ------------------------------------------------------------

print("\nTraining Random Forest...")

model.fit(
    X_train,
    y_train
)


print("Training completed.")


# ------------------------------------------------------------
# PREDICTION
# ------------------------------------------------------------

y_pred = model.predict(
    X_test
)


# ------------------------------------------------------------
# ACCURACY
# ------------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n" + "=" * 60)

print(
    f"MODEL ACCURACY: "
    f"{accuracy * 100:.2f}%"
)

print("=" * 60)


# ------------------------------------------------------------
# CLASSIFICATION REPORT
# ------------------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ------------------------------------------------------------
# CONFUSION MATRIX
# ------------------------------------------------------------

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ------------------------------------------------------------
# SAVE MODEL
# ------------------------------------------------------------

joblib.dump(
    model,
    MODEL_FILE
)


print("\nModel saved successfully:")

print(
    MODEL_FILE
)


print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETE")
print("=" * 60)