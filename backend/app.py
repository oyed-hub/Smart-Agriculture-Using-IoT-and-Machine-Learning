from flask import Flask, request, jsonify, send_from_directory, session, redirect
import os, json
import joblib
import pandas as pd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "frontend"))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_JSON = os.path.join(BASE_DIR, "users.json")
SENSOR_FILE = os.path.join(DATA_DIR, "latest_sensor.json")

os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "smartcrop-secret"

# -------- Load ML Models --------
crop_model = joblib.load("model.pkl")
disease_model = joblib.load("model_xgb.pkl")
label_encoder = joblib.load("label_encoder.pkl")
fert_model = joblib.load("fertilizer_model.pkl")
fert_soil_encoder = joblib.load("fertilizer_soil_encoder.pkl")

# -------- Utils --------
def read_users():
    return json.load(open(USERS_JSON)) if os.path.exists(USERS_JSON) else {}

def write_users(data):
    json.dump(data, open(USERS_JSON, "w"), indent=2)

def auth_required():
    return bool(session.get("user"))

# -------- Pages --------
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/login")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/register")
def register_page():
    return send_from_directory(FRONTEND_DIR, "register.html")

@app.route("/dashboard")
def dashboard():
    if not auth_required():
        return redirect("/login")
    return send_from_directory(BASE_DIR, "index.html")  # backend dashboard

# -------- Auth APIs --------
@app.route("/api/register", methods=["POST"])
def register():
    d = request.json
    users = read_users()

    if d["phone"] in users:
        return jsonify({"error": "User already exists"}), 400

    users[d["phone"]] = {"password": d["password"]}
    write_users(users)
    session["user"] = d["phone"]
    return jsonify({"ok": True, "redirect": "/dashboard"})

@app.route("/api/login", methods=["POST"])
def login():
    d = request.json
    users = read_users()

    if d["phone"] not in users or users[d["phone"]]["password"] != d["password"]:
        return jsonify({"error": "Invalid login"}), 401

    session["user"] = d["phone"]
    return jsonify({"ok": True, "redirect": "/dashboard"})

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/me")
def me():
    return jsonify({"authenticated": auth_required()})

# -------- IoT Sensor API --------
@app.route("/api/sensor-update", methods=["POST"])
def sensor_update():
    data = request.json
    json.dump(data, open(SENSOR_FILE, "w"), indent=2)
    return jsonify({"ok": True})

@app.route("/data/latest")
def latest():
    if not os.path.exists(SENSOR_FILE):
        return jsonify({})
    return jsonify(json.load(open(SENSOR_FILE)))

# -------- CSV Upload --------
@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():
    f = request.files["file"]
    df = pd.read_csv(f)
    df.to_csv(os.path.join(DATA_DIR, "uploaded.csv"), index=False)
    return jsonify({"ok": True, "rows": len(df)})

# -------- Smart Advisory --------
@app.route("/api/smart-advisory", methods=["POST"])
def smart_advisory():
    d = request.json

    crop = crop_model.predict([[d["soil_moisture"], d["temperature"], d["humidity"]]])[0]

    disease_encoded = disease_model.predict([[d["temperature"], d["humidity"], d["soil_moisture"], d["rainfall"], d["pesticide_index"]]])[0]
    disease = label_encoder.inverse_transform([disease_encoded])[0]

    soil_enc = fert_soil_encoder.transform([d["soil_type"]])[0]
    fertilizer = fert_model.predict([[d["temperature"], d["humidity"], d["soil_moisture"], soil_enc]])[0]

    latest_data = json.load(open(SENSOR_FILE)) if os.path.exists(SENSOR_FILE) else {}
    latest_data["predicted_crop"] = crop
    latest_data["disease_info"] = [{"name": disease, "pesticide": fertilizer, "dosage": "As per label"}]
    json.dump(latest_data, open(SENSOR_FILE, "w"), indent=2)

    return jsonify({
        "recommended_crop": crop,
        "predicted_disease": disease,
        "recommended_fertilizer": fertilizer
    })

if __name__ == "__main__":
    app.run(debug=True)
