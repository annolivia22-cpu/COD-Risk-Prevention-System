
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# Project paths
DATA_PATH = Path("data/orders_sample.csv")
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "risk_model.pkl"

# Create model directory if missing
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Original dataset:", df.shape)

# Clean status
df["final_status"] = (
    df["final_status"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Remove exact duplicate rows
df = df.drop_duplicates()

# Keep only completed orders
df = df[
    df["final_status"].isin(["DELIVERED", "RTO"])
].copy()

# Target variable
df["rto"] = (
    df["final_status"] == "RTO"
).astype(int)

# Features available before shipping
numeric_features = [
    "order_value",
    "num_items",
    "customer_prior_orders",
    "customer_prior_rto"
]

categorical_features = [
    "city",
    "state",
    "utm_source",
    "courier"
]

X = df[numeric_features + categorical_features]
y = df["rto"]

# Keep the same customer in only one split
groups = df["phone"].fillna("UNKNOWN").astype(str)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(X, y, groups)
)

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

print("Training orders:", len(X_train))
print("Testing orders:", len(X_test))

# Numeric preprocessing
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

# Categorical preprocessing
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Combine preprocessing
preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Random Forest model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42
    ))
])

# Train model
print("\nTraining model...")

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]

# Evaluation
print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, predictions))

print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print(
    "\nROC AUC:",
    round(roc_auc_score(y_test, probabilities), 3)
)

# Save model
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print("Location:", MODEL_PATH)
