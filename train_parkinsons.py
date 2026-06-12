import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv("datasets/parkinsons.csv")

# Remove Name Column
df.drop("name", axis=1, inplace=True)

# Features and Target
X = df.drop("status", axis=1)
y = df["status"]

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

accuracy = accuracy_score(y_test, pred)

print("Parkinson's Accuracy:", accuracy)

# Save
joblib.dump(
    model,
    "models/parkinsons_model.pkl"
)

joblib.dump(
    scaler,
    "models/parkinsons_scaler.pkl"
)

print("Parkinson's Model Saved")

