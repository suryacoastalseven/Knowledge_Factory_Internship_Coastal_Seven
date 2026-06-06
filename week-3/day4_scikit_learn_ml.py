# ==========================================
# DAY 4 - SCIKIT LEARN COMPLETE PRACTICE
# Regression + Classification + Evaluation
# ==========================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression
)

from sklearn.tree import DecisionTreeClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    mean_squared_error,
    r2_score
)

from sklearn.pipeline import Pipeline

from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

from sklearn.impute import SimpleImputer

print("=" * 70)
print("DAY 4 - SCIKIT LEARN")
print("=" * 70)

# =========================================================
# PART 1 - LINEAR REGRESSION
# =========================================================

print("\n")
print("=" * 70)
print("PART 1 : LINEAR REGRESSION")
print("=" * 70)

# Hours Studied -> Marks

regression_df = pd.DataFrame({
    "Hours_Studied": [1,2,3,4,5,6,7,8,9,10],
    "Marks": [30,40,45,55,60,70,75,85,90,95]
})

X = regression_df[["Hours_Studied"]]
y = regression_df["Marks"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

predictions = linear_model.predict(X_test)

print("\nActual Marks:")
print(y_test.values)

print("\nPredicted Marks:")
print(np.round(predictions, 2))

print("\nR2 Score:")
print(r2_score(y_test, predictions))

print("\nMSE:")
print(mean_squared_error(y_test, predictions))

print("\nPrediction for 12 Study Hours:")
print(
    linear_model.predict([[12]])[0]
)

# =========================================================
# PART 2 - CLASSIFICATION DATASET
# =========================================================

print("\n")
print("=" * 70)
print("PART 2 : CLASSIFICATION")
print("=" * 70)

students = pd.DataFrame({

    "Hours_Studied":
        [1,2,3,4,5,6,7,8,2,5,7,9,3,6,8,10],

    "Attendance":
        [50,60,70,80,90,95,85,88,55,78,90,92,68,84,87,98],

    "Department":
        [
            "CSE","ECE","CSE","MECH",
            "CSE","ECE","MECH","CSE",
            "ECE","MECH","CSE","ECE",
            "MECH","CSE","ECE","CSE"
        ],

    "Pass":
        [
            0,0,0,1,
            1,1,1,1,
            0,1,1,1,
            0,1,1,1
        ]
})

print("\nDataset:")
print(students.head())

X = students[
    [
        "Hours_Studied",
        "Attendance",
        "Department"
    ]
]

y = students["Pass"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

# =========================================================
# COLUMN TRANSFORMER
# =========================================================

numeric_features = [
    "Hours_Studied",
    "Attendance"
]

categorical_features = [
    "Department"
]

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="mean")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder()
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
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
    ]
)

# =========================================================
# LOGISTIC REGRESSION
# =========================================================

print("\n")
print("=" * 70)
print("LOGISTIC REGRESSION")
print("=" * 70)

logistic_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            LogisticRegression()
        )
    ]
)

logistic_pipeline.fit(
    X_train,
    y_train
)

pred = logistic_pipeline.predict(
    X_test
)

print("\nPredictions:")
print(pred)

print("\nAccuracy:")
print(
    accuracy_score(y_test, pred)
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        pred
    )
)

print("\nPrecision:")
print(
    precision_score(
        y_test,
        pred
    )
)

print("\nRecall:")
print(
    recall_score(
        y_test,
        pred
    )
)

print("\nF1 Score:")
print(
    f1_score(
        y_test,
        pred
    )
)

# =========================================================
# DECISION TREE
# =========================================================

print("\n")
print("=" * 70)
print("DECISION TREE")
print("=" * 70)

tree_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            DecisionTreeClassifier(
                random_state=42
            )
        )
    ]
)

tree_pipeline.fit(
    X_train,
    y_train
)

tree_pred = tree_pipeline.predict(
    X_test
)

print("\nAccuracy:")
print(
    accuracy_score(
        y_test,
        tree_pred
    )
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        tree_pred
    )
)

# =========================================================
# KNN
# =========================================================

print("\n")
print("=" * 70)
print("KNN")
print("=" * 70)

knn_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            KNeighborsClassifier(
                n_neighbors=3
            )
        )
    ]
)

knn_pipeline.fit(
    X_train,
    y_train
)

knn_pred = knn_pipeline.predict(
    X_test
)

print("\nAccuracy:")
print(
    accuracy_score(
        y_test,
        knn_pred
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        knn_pred
    )
)

# =========================================================
# FIT / PREDICT / SCORE DEMO
# =========================================================

print("\n")
print("=" * 70)
print("FIT / PREDICT / SCORE")
print("=" * 70)

demo_model = LogisticRegression()

processed_X_train = preprocessor.fit_transform(
    X_train
)

processed_X_test = preprocessor.transform(
    X_test
)

demo_model.fit(
    processed_X_train,
    y_train
)

demo_predictions = demo_model.predict(
    processed_X_test
)

score = demo_model.score(
    processed_X_test,
    y_test
)

print("\nPredictions:")
print(demo_predictions)

print("\nScore:")
print(score)

# =========================================================
# NEW STUDENT PREDICTION
# =========================================================

print("\n")
print("=" * 70)
print("NEW STUDENT PREDICTION")
print("=" * 70)

new_student = pd.DataFrame({
    "Hours_Studied": [8],
    "Attendance": [90],
    "Department": ["CSE"]
})

result = logistic_pipeline.predict(
    new_student
)

print("\nStudent Details:")
print(new_student)

print("\nPrediction:")

if result[0] == 1:
    print("PASS")
else:
    print("FAIL")

print("\n")
print("=" * 70)
print("DAY 4 COMPLETED SUCCESSFULLY")
print("=" * 70)