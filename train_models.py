import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("datasets/diabetes.csv")

columns_to_fix = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]

for col in columns_to_fix:
    data[col] = data[col].replace(
        0,
        data[col].median()
    )

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression":
    LogisticRegression(max_iter=1000),

    "SVM":
    SVC(kernel="rbf"),

    "Random Forest":
    RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
}

best_model = None
best_accuracy = 0

for name, model in models.items():

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        pred
    )

    print(name, ":", accuracy)

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model

joblib.dump(
    best_model,
    "models/diabetes_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

print("Best Accuracy:", best_accuracy)
print("Model Saved Successfully")