from flask import Flask, render_template, request, jsonify
import sqlite3, datetime, random

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def get_db_connection():
    conn = sqlite3.connect("../databases/meds.db")
    conn.row_factory = sqlite3.Row
    return conn

def generate_fake_vitals():
    return {
        "Temperature": f"{round(random.uniform(97.5, 99.5), 1)} °F",
        "Heart Rate": f"{random.randint(60, 100)} bpm",
        "Blood Pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)} mmHg",
        "Latitude": "28.6139",
        "Longitude": "77.2090"
    }

@app.route("/")
def home():
    vitals = generate_fake_vitals()
    return render_template("home.html", vitals=vitals)

@app.route("/vitals")
def get_vitals():
    return jsonify(generate_fake_vitals())

@app.route("/check", methods=["POST"])
def check():
    symptoms = request.form.get("symptoms", "")
    temp = request.form.get("temperature")
    hr = request.form.get("heartrate")
    bp = request.form.get("bloodpressure")
    lat = request.form.get("latitude")
    lon = request.form.get("longitude")

    vitals = {
        "Temperature": temp,
        "Heart Rate": hr,
        "Blood Pressure": bp,
        "Latitude": lat,
        "Longitude": lon,
    }

    result = "You may have a mild condition. Please consult a doctor if symptoms persist."
    suggested_meds = []

    if "fever" in symptoms.lower():
        suggested_meds = [
            {"name": "Paracetamol", "dosage": "500mg every 6 hours"},
            {"name": "Ibuprofen", "dosage": "200mg twice daily"}
        ]
    elif "cough" in symptoms.lower():
        suggested_meds = [{"name": "Cough Syrup", "dosage": "10ml twice daily"}]
    elif "headache" in symptoms.lower():
        suggested_meds = [{"name": "Aspirin", "dosage": "300mg once daily"}]

    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS diagnosis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT,
            temperature TEXT,
            heartrate TEXT,
            bloodpressure TEXT,
            latitude REAL,
            longitude REAL,
            timestamp TEXT
        )
    ''')
    conn.execute('''
        INSERT INTO diagnosis (symptoms, temperature, heartrate, bloodpressure, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symptoms, temp, hr, bp, lat, lon, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return render_template("result.html", result=result, vitals=vitals, medicines=suggested_meds)

if __name__ == "__main__":
    app.run(debug=True)
