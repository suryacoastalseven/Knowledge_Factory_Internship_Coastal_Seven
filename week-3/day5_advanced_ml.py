# =====================================================
# DAY 5 - ADVANCED MACHINE LEARNING
# Random Forest, SVM, XGBoost
# Feature Engineering
# Cross Validation
# GridSearchCV
# Feature Importance
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    GridSearchCV
)

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    OneHotEncoder
)

from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

# =====================================================
# CREATE SAMPLE DATASET
# =====================================================

np.random.seed(42)

n = 200

df = pd.DataFrame({

    "Hours_Studied":
        np.random.randint(1, 11, n),

    "Attendance":
        np.random.randint(50, 101, n),

    "Assignments":
        np.random.randint(1, 11, n),

    "Department":
        np.random.choice(
            ["CSE", "ECE", "MECH"],
            n
        )
})

# Target Column

df["Pass"] = np.where(

    (
        df["Hours_Studied"] * 5
        + df["Attendance"] * 0.5
        + df["Assignments"] * 2
    ) > 70,

    1,
    0
)

print("=" * 60)
print("DATASET")
print("=" * 60)

print(df.head())

# =====================================================
# FEATURES / TARGET
# =====================================================

X = df.drop("Pass", axis=1)
y = df["Pass"]

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

numeric_features = [

    "Hours_Studied",
    "Attendance",
    "Assignments"
]

categorical_features = [

    "Department"
]

# StandardScaler

numeric_transformer = Pipeline([

    (
        "imputer",
        SimpleImputer(strategy="mean")
    ),

    (
        "scaler",
        StandardScaler()
    )
])

# One Hot Encoding

categorical_transformer = Pipeline([

    (
        "imputer",
        SimpleImputer(strategy="most_frequent")
    ),

    (
        "encoder",
        OneHotEncoder()
    )
])

preprocessor = ColumnTransformer([

    (
        "num",
        numeric_transformer,
        numeric_features
    ),

    (
        "cat",
        categorical_transformer,
        categorical_features
    )
])

# =====================================================
# RANDOM FOREST
# =====================================================

print("\n")
print("=" * 60)
print("RANDOM FOREST")
print("=" * 60)

rf_pipeline = Pipeline([

    ("preprocessor", preprocessor),

    (
        "model",
        RandomForestClassifier(
            random_state=42
        )
    )
])

rf_pipeline.fit(

    X_train,
    y_train
)

rf_pred = rf_pipeline.predict(

    X_test
)

rf_accuracy = accuracy_score(

    y_test,
    rf_pred
)

print(
    "Accuracy:",
    round(rf_accuracy, 4)
)

print(
    classification_report(
        y_test,
        rf_pred
    )
)

# =====================================================
# SVM
# =====================================================

print("\n")
print("=" * 60)
print("SVM")
print("=" * 60)

svm_pipeline = Pipeline([

    (
        "preprocessor",
        preprocessor
    ),

    (
        "model",
        SVC()
    )
])

svm_pipeline.fit(

    X_train,
    y_train
)

svm_pred = svm_pipeline.predict(

    X_test
)

svm_accuracy = accuracy_score(

    y_test,
    svm_pred
)

print(
    "Accuracy:",
    round(svm_accuracy, 4)
)

# =====================================================
# CROSS VALIDATION
# =====================================================

print("\n")
print("=" * 60)
print("CROSS VALIDATION")
print("=" * 60)

cv_scores = cross_val_score(

    rf_pipeline,

    X,
    y,

    cv=5
)

print(
    "Scores:",
    cv_scores
)

print(
    "Average:",
    cv_scores.mean()
)

# =====================================================
# GRID SEARCH
# =====================================================

print("\n")
print("=" * 60)
print("GRID SEARCH")
print("=" * 60)

param_grid = {

    "model__n_estimators":
        [10, 50, 100],

    "model__max_depth":
        [3, 5, 10, None]
}

grid = GridSearchCV(

    rf_pipeline,

    param_grid,

    cv=5,

    scoring="accuracy"
)

grid.fit(X_train, y_train)

print(
    "Best Parameters:"
)

print(
    grid.best_params_
)

print(
    "\nBest Score:"
)

print(
    grid.best_score_
)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

print("\n")
print("=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

# Preprocess

X_processed = preprocessor.fit_transform(X)

feature_names = (

    numeric_features +

    list(

        preprocessor
        .named_transformers_["cat"]
        .named_steps["encoder"]
        .get_feature_names_out(
            categorical_features
        )
    )
)

rf_model = RandomForestClassifier(
    random_state=42
)

rf_model.fit(

    X_processed,
    y
)

importances = rf_model.feature_importances_

importance_df = pd.DataFrame({

    "Feature":
        feature_names,

    "Importance":
        importances
})

importance_df = (

    importance_df
    .sort_values(
        "Importance",
        ascending=False
    )
)

print(
    importance_df
)

# =====================================================
# FEATURE IMPORTANCE PLOT
# =====================================================

plt.figure(
    figsize=(10, 5)
)

plt.bar(

    importance_df["Feature"],

    importance_df["Importance"]
)

plt.title(
    "Feature Importance"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.show()

# =====================================================
# MINMAX SCALER DEMO
# =====================================================

print("\n")
print("=" * 60)
print("MINMAX SCALER DEMO")
print("=" * 60)

sample = pd.DataFrame({

    "Salary":
        [30000, 50000, 70000, 100000]
})

scaler = MinMaxScaler()

scaled = scaler.fit_transform(
    sample
)

print("Original")

print(sample)

print("\nScaled")

print(scaled)

# =====================================================
# XGBOOST (OPTIONAL)
# =====================================================

try:

    from xgboost import XGBClassifier

    print("\n")
    print("=" * 60)
    print("XGBOOST")
    print("=" * 60)

    xgb_pipeline = Pipeline([

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            XGBClassifier(
                eval_metric="logloss"
            )
        )
    ])

    xgb_pipeline.fit(
        X_train,
        y_train
    )

    xgb_pred = xgb_pipeline.predict(
        X_test
    )

    print(
        "Accuracy:",
        accuracy_score(
            y_test,
            xgb_pred
        )
    )

except Exception:

    print(
        "\nXGBoost not installed."
    )

    print(
        "Install using:"
    )

    print(
        "pip install xgboost"
    )

# =====================================================
# MODEL COMPARISON
# =====================================================

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

comparison = pd.DataFrame({

    "Model":
        [
            "Random Forest",
            "SVM"
        ],

    "Accuracy":
        [
            rf_accuracy,
            svm_accuracy
        ]
})

print(comparison)

print("\nDAY 5 COMPLETED SUCCESSFULLY")