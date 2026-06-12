import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv("datasets/stroke.csv")

# Remove ID
df.drop("id", axis=1, inplace=True)

# Fill Missing BMI
df["bmi"].fillna(
    df["bmi"].median(),
    inplace=True
)

# Encode Categorical Columns
categorical_cols = [
    "gender",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status"
]

le = LabelEncoder()

for col in categorical_cols:
    df[col] = le.fit_transform(
        df[col]
    )

# Features and Target
X = df.drop("stroke", axis=1)
y = df["stroke"]

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
    "Stroke Accuracy:",
    accuracy
)

# Save
joblib.dump(
    model,
    "models/stroke_model.pkl"
)

joblib.dump(
    scaler,
    "models/stroke_scaler.pkl"
)

print("Stroke Model Saved")

