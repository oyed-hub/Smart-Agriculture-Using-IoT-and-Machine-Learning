import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("Fertilizer Prediction.csv")

print("Columns:", df.columns)

# Rename columns to clean names
df = df.rename(columns={
    "Temparature": "temperature",
    "Humidity ": "humidity",
    "Moisture": "soil_moisture",
    "Soil Type": "soil_type",
    "Crop Type": "crop",
    "Fertilizer Name": "fertilizer"
})

# Features & target
X = df[["temperature", "humidity", "soil_moisture", "crop", "soil_type", "Nitrogen", "Phosphorous", "Potassium"]]
y = df["fertilizer"]

# Encode categorical columns
crop_encoder = LabelEncoder()
soil_encoder = LabelEncoder()
fertilizer_encoder = LabelEncoder()

X["crop"] = crop_encoder.fit_transform(X["crop"])
X["soil_type"] = soil_encoder.fit_transform(X["soil_type"])
y_enc = fertilizer_encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

# Hyperparameter tuning for >95% accuracy
params = {
    "n_estimators": [200, 300, 500],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5]
}

rf = RandomForestClassifier(random_state=42)
grid = GridSearchCV(rf, params, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_

# Evaluate
y_pred = best_model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("🔥 Fertilizer Model Accuracy:", acc)
print("Best Params:", grid.best_params_)

# Save models
joblib.dump(best_model, "fertilizer_model.pkl")
joblib.dump(crop_encoder, "fertilizer_crop_encoder.pkl")
joblib.dump(soil_encoder, "fertilizer_soil_encoder.pkl")
joblib.dump(fertilizer_encoder, "fertilizer_label_encoder.pkl")

print("✅ Fertilizer Model Trained & Saved Successfully")
