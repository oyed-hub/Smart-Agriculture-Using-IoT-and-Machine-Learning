import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("Crop_recommendation_with_soil_moisture.csv")

print("Columns:", df.columns)

# 2️⃣ Select features (ONLY what you have from sensors)
X = df[["soil_moisture", "temperature", "humidity"]]
y = df["label"]   # crop name

# 3️⃣ Encode target crop labels
le_crop = LabelEncoder()
y_encoded = le_crop.fit_transform(y)

# 4️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# 5️⃣ Train Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

# 6️⃣ Accuracy check
acc = model.score(X_test, y_test)
print("Crop Model Accuracy:", acc)

# 7️⃣ Save model + encoder
joblib.dump(model, "crop_model.pkl")
joblib.dump(le_crop, "crop_label_encoder.pkl")

print("✅ Crop Recommendation Model Saved!")
