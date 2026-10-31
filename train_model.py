
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
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

# Load data
df = pd.read_csv("data/orders_sample.csv")

# Standardise status
df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)

# Remove exact duplicate rows
df = df.drop_duplicates()

# Keep only orders with known outcomes
df = df[df["final_status"].isin(["DELIVERED", "RTO"])].copy()

# Create target
df["rto"] = (df["final_status"] == "RTO").astype(int)

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

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Preprocessing
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Model
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

# Train
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("ROC AUC:", roc_auc_score(y_test, probabilities))

# Save model
joblib.dump(model, "models/risk_model.pkl")

print("\nModel trained and saved successfully!")
