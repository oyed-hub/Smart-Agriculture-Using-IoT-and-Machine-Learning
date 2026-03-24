import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("disease_data.csv")
print("Columns:", df.columns)

# 2️⃣ Target (disease)
le = LabelEncoder()
y = le.fit_transform(df["disease"])

# 3️⃣ Features (ONLY columns that exist in your CSV)
X = df[["temperature", "humidity", "soil_moisture", "rainfall", "ph"]]

# 4️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5️⃣ Pipeline: Scaling + Logistic Regression
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("lr", LogisticRegression(max_iter=5000))
])

# 6️⃣ Hyperparameter tuning
param_grid = {
    "lr__C": [0.1, 1, 5, 10, 50]
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

# 7️⃣ Accuracy
acc = best_model.score(X_test, y_test)
print("🔥 Accuracy:", acc)
print("Best Params:", grid.best_params_)

# 8️⃣ Save model
joblib.dump(best_model, "disease_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("✅ Disease Model Trained & Saved Successfully")
