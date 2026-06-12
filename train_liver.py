import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv("datasets/liver.csv")

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

# Encode Gender
le = LabelEncoder()

df["Gender"] = le.fit_transform(
    df["Gender"]
)

# Features and Target
X = df.drop(
    "Dataset",
    axis=1
)

y = df["Dataset"]

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

# Model
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
    "Liver Accuracy:",
    accuracy
)

joblib.dump(
    model,
    "models/liver_model.pkl"
)

joblib.dump(
    scaler,
    "models/liver_scaler.pkl"
)

print("Liver Model Saved")

