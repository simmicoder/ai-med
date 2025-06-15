from flask import Flask, render_template, request
import sqlite3
import datetime
import os
import random

# Flask setup
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Database path handling
basedir = os.path.abspath(os.path.dirname(__file__))
def get_db_connection():
    db_path = os.path.join(basedir, '..', 'databases', 'meds.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Simulate vitals
def simulate_vitals():
    return {
        "temperature": str(round(random.uniform(36.5, 38.5), 1)),
        "heartrate": str(random.randint(70, 100)),
        "bloodpressure": f"{random.randint(110, 130)}/{random.randint(70, 90)}"
    }

# Home route
@app.route("/")
def home():
    auto_vitals = simulate_vitals()
    return render_template("home.html", vitals=auto_vitals)

# Diagnosis route
@app.route("/check", methods=["POST"])
def check():
    symptoms = request.form.get("symptoms", "")
    temp = request.form.get("temperature")
    hr = request.form.get("heartrate")
    bp = request.form.get("bloodpressure")
    lat = request.form.get("latitude")
    lon = request.form.get("longitude")

    vitals = {
        "Temperature": temp + " °C" if temp else "N/A",
        "Heart Rate": hr + " bpm" if hr else "N/A",
        "Blood Pressure": bp if bp else "N/A",
        "Latitude": lat if lat else "N/A",
        "Longitude": lon if lon else "N/A",
    }

    # Basic logic for demo diagnosis
    result = "You may have a mild condition. Please consult a doctor if symptoms persist."
    suggested_meds = []
    if "fever" in symptoms.lower():
        suggested_meds = [
            {"name": "Paracetamol", "dosage": "500mg every 6 hours"},
            {"name": "Ibuprofen", "dosage": "200mg twice daily"}
        ]
    elif "cough" in symptoms.lower():
        suggested_meds = [
            {"name": "Cough Syrup", "dosage": "10ml thrice daily"},
            {"name": "Cetirizine", "dosage": "10mg at night"}
        ]

    # Save to database
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

# Run app
if __name__ == "__main__":
    app.run(debug=True)
