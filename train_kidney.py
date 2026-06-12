import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("datasets/kidney.csv")

# Remove ID
if "id" in df.columns:
    df.drop("id", axis=1, inplace=True)

# Fill Missing Values
for col in df.columns:

    if df[col].dtype == "object":

        df[col].fillna(
            df[col].mode()[0],
            inplace=True
        )

    else:

        df[col].fillna(
            df[col].median(),
            inplace=True
        )

# Encode All Object Columns
le = LabelEncoder()

for col in df.columns:

    if df[col].dtype == "object":

        df[col] = le.fit_transform(
            df[col].astype(str)
        )

X = df.drop(
    "classification",
    axis=1
)

y = df["classification"]

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

accuracy = accuracy_score(
    y_test,
    pred
)

print(
    "Kidney Accuracy:",
    accuracy
)

joblib.dump(
    model,
    "models/ckd_model.pkl"
)

joblib.dump(
    scaler,
    "models/ckd_scaler.pkl"
)

print("Kidney Model Saved")

