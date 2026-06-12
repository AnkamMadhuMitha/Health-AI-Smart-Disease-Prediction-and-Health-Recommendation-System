import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("datasets/lung_cancer.csv")

# Encode Gender
le = LabelEncoder()
df["GENDER"] = le.fit_transform(df["GENDER"])

# Encode Target
df["LUNG_CANCER"] = le.fit_transform(
    df["LUNG_CANCER"]
)

X = df.drop("LUNG_CANCER", axis=1)
y = df["LUNG_CANCER"]

scaler = StandardScaler()

X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print(
    "Lung Cancer Accuracy:",
    accuracy
)

joblib.dump(
    model,
    "models/lung_cancer_model.pkl"
)

joblib.dump(
    scaler,
    "models/lung_cancer_scaler.pkl"
)

print("Lung Cancer Model Saved")

