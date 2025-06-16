from flask import Flask, render_template, request
import sqlite3
import datetime
import random

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def get_db_connection():
    # ✅ On Render, only /tmp is writable
    conn = sqlite3.connect("/tmp/meds.db")
    conn.row_factory = sqlite3.Row
    return conn

# Simulate auto vitals
def simulate_vitals():
    return {
        "Temperature": f"{round(random.uniform(36.5, 38.5), 1)} °C",
        "Heart Rate": f"{random.randint(60, 100)} bpm",
        "Blood Pressure": f"{random.randint(100, 130)}/{random.randint(70, 85)} mmHg",
        "Latitude": f"{round(random.uniform(-90, 90), 4)}",
        "Longitude": f"{round(random.uniform(-180, 180), 4)}"
    }

@app.route("/")
def home():
    vitals = simulate_vitals()
    return render_template("home.html", vitals=vitals)

@app.route("/check", methods=["POST"])
def check():
    symptoms = request.form.get("symptoms", "")
    temp = request.form.get("temperature")
    hr = request.form.get("heartrate")
    bp = request.form.get("bloodpressure")
    lat = request.form.get("latitude")
    lon = request.form.get("longitude")

    # Vitals for chart + display
    vitals = {
        "Temperature": temp + " °C" if temp else "N/A",
        "Heart Rate": hr + " bpm" if hr else "N/A",
        "Blood Pressure": bp if bp else "N/A",
        "Latitude": lat if lat else "N/A",
        "Longitude": lon if lon else "N/A",
    }

    # Smart medicine logic
    suggested_meds = []
    result = "You may have a mild condition. Please consult a doctor if symptoms persist."

    if "fever" in symptoms.lower():
        suggested_meds = [
            {"name": "Paracetamol", "dosage": "500mg every 6 hours"},
            {"name": "Ibuprofen", "dosage": "200mg twice daily"}
        ]
        result = "You may have a fever. Take medicine and consult a doctor if it persists."

    elif "cold" in symptoms.lower() or "cough" in symptoms.lower():
        suggested_meds = [
            {"name": "Cetirizine", "dosage": "10mg at bedtime"},
            {"name": "Cough Syrup", "dosage": "2 tsp thrice daily"}
        ]
        result = "You seem to have a cold or cough. Take rest and medication."

    elif "headache" in symptoms.lower():
        suggested_meds = [
            {"name": "Aspirin", "dosage": "300mg every 4-6 hours"},
        ]
        result = "You may have a headache. Stay hydrated."

    elif "pain" in symptoms.lower():
        suggested_meds = [
            {"name": "Ibuprofen", "dosage": "400mg every 6 hours"},
        ]
        result = "You may be experiencing body pain."

    # Save to database
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS diagnosis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT,
            temperature TEXT,
            heartrate TEXT,
            bloodpressure TEXT,
            latitude TEXT,
            longitude TEXT,
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
