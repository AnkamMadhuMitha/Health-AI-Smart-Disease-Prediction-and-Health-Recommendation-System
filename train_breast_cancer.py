import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv(
    "datasets/breast_cancer.csv"
)

# Remove Unnecessary Columns
df.drop(
    ["id", "Unnamed: 32"],
    axis=1,
    inplace=True
)

# Encode Diagnosis
le = LabelEncoder()

df["diagnosis"] = le.fit_transform(
    df["diagnosis"]
)

# Features and Target
X = df.drop(
    "diagnosis",
    axis=1
)

y = df["diagnosis"]

# Scaling
scaler = StandardScaler()

X = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    pred
)

print(
    "Breast Cancer Accuracy:",
    accuracy
)

# Save
joblib.dump(
    model,
    "models/breast_cancer_model.pkl"
)

joblib.dump(
    scaler,
    "models/breast_cancer_scaler.pkl"
)

print("Breast Cancer Model Saved")

