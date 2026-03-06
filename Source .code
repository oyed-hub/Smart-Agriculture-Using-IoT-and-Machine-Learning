from flask import Flask, request, jsonify, send_from_directory, session, redirect
import os, json
import joblib
import pandas as pd
import uuid
import datetime
import random
import requests
from azure.cosmos import CosmosClient

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "frontend"))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_JSON = os.path.join(BASE_DIR, "users.json")

os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "smartcrop-secret"

# -------- Fast2SMS CONFIG --------
FAST2SMS_API_KEY = "7Jy9tV0jmT3xi395Y9y0Nm1cibZaSK9Yi91dIZPnwpbzLvZHwuJroU6XQ6Pd"
otp_store = {}

# -------- Azure Cosmos DB --------
COSMOS_URI = "https://smartcropcosmos.documents.azure.com:443/"
COSMOS_KEY = "BWkBVrpwVC5D0KzPPOfhXuZJnzRMNhwV1QBmWQqvGwf62xnz6hE59nP2m7pbWfyYFCLx00VjRJqxACDbQKdJ2Q=="

cosmos_client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)

database = cosmos_client.get_database_client("sensorDB")
container = database.get_container_client("sensorData")


# -------- Load ML Models --------
crop_model = joblib.load("model.pkl")
disease_model = joblib.load("model_xgb.pkl")
label_encoder = joblib.load("label_encoder.pkl")
fert_model = joblib.load("fertilizer_model.pkl")
fert_soil_encoder = joblib.load("fertilizer_soil_encoder.pkl")


# -------- Utils --------
def read_users():
    if not os.path.exists(USERS_JSON):
        return {}
    return json.load(open(USERS_JSON))


def write_users(data):
    json.dump(data, open(USERS_JSON, "w"), indent=2)


def auth_required():
    return bool(session.get("user"))


# -------- OTP SEND API --------
@app.route("/api/send-otp", methods=["POST"])
def send_otp():

    data = request.json
    phone = data.get("phone")

    otp = str(random.randint(100000,999999))
    otp_store[phone] = otp

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",
        "message": f"Your SmartCrop OTP is {otp}",
        "language": "english",
        "numbers": phone
    }

    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    print("FAST2SMS RESPONSE:", response.text)

    return jsonify({"status":"otp_sent"})


# -------- OTP VERIFY API --------
@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():

    data = request.json
    phone = data.get("phone")
    otp = data.get("otp")

    if otp_store.get(phone) == otp:
        return jsonify({"verified": True})

    return jsonify({"verified": False})


# -------- Save sensor data to Azure --------
def save_sensor_data(data):

    item = {
        "id": str(uuid.uuid4()),
        "device_id": data.get("device_id", "farm_sensor_1"),
        "soil_moisture": data.get("soil_moisture"),
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "soil_type": data.get("soil_type"),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    container.create_item(body=item)


# -------- Get latest sensor data --------
def get_latest_sensor():

    query = "SELECT TOP 1 * FROM c ORDER BY c.timestamp DESC"

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    if not items:
        return None

    return items[0]


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
    return send_from_directory(BASE_DIR, "index.html")


# -------- Auth APIs --------
@app.route("/api/register", methods=["POST"])
def register():

    d = request.json
    users = read_users()

    username = d["username"]

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = {
        "password": d["password"],
        "phone": d["phone"]
    }

    write_users(users)

    session["user"] = username

    return jsonify({"ok": True, "redirect": "/dashboard"})


@app.route("/api/login", methods=["POST"])
def login():

    d = request.json
    users = read_users()

    username = d["username"]

    if username not in users:
        return jsonify({"error": "User not found"}), 401

    if users[username]["password"] != d["password"]:
        return jsonify({"error": "Invalid password"}), 401

    session["user"] = username

    return jsonify({"ok": True, "redirect": "/dashboard"})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me")
def me():

    if not auth_required():
        return jsonify({"authenticated": False})

    username = session.get("user")
    users = read_users()

    user_data = users.get(username, {})

    return jsonify({
        "authenticated": True,
        "user": {
            "name": username,
            "phone": user_data.get("phone", "")
        }
    })


# -------- IoT Sensor API --------
@app.route("/api/sensor-update", methods=["POST"])
def sensor_update():

    data = request.json

    save_sensor_data(data)

    return jsonify({"status": "stored_in_azure"})


@app.route("/data/latest")
def latest():

    latest = get_latest_sensor()

    if not latest:
        return jsonify({})

    return jsonify({
        "soil_moisture": latest.get("soil_moisture"),
        "temperature": latest.get("temperature"),
        "humidity": latest.get("humidity"),
        "soil_type": latest.get("soil_type")
    })


# -------- CSV Upload --------
@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():

    f = request.files["file"]
    df = pd.read_csv(f)

    df.to_csv(os.path.join(DATA_DIR, "uploaded.csv"), index=False)

    return jsonify({
        "ok": True,
        "rows": len(df)
    })


# -------- Smart Advisory --------
@app.route("/api/smart-advisory", methods=["POST"])
def smart_advisory():

    d = request.json

    crop = crop_model.predict(
        [[d["soil_moisture"], d["temperature"], d["humidity"]]]
    )[0]

    disease_encoded = disease_model.predict(
        [[d["temperature"], d["humidity"], d["soil_moisture"],
          d["rainfall"], d["pesticide_index"]]]
    )[0]

    disease = label_encoder.inverse_transform([disease_encoded])[0]

    soil_enc = fert_soil_encoder.transform([d["soil_type"]])[0]

    fertilizer = fert_model.predict(
        [[d["temperature"], d["humidity"], d["soil_moisture"], soil_enc]]
    )[0]

    return jsonify({
        "recommended_crop": crop,
        "predicted_disease": disease,
        "recommended_fertilizer": fertilizer
    })


if __name__ == "__main__":
    app.run(debug=True)
