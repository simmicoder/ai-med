from flask import Flask, render_template, request
import sqlite3
import datetime
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def get_db_connection():
    db_path = "/tmp/meds.db"
    
    # Create DB and table if not exists (for first-time deploys)
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
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
        conn.commit()
        conn.close()
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("home.html", vitals={})

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

    result = "You may have a mild condition. Please consult a doctor if symptoms persist."
    suggested_meds = [
        {"name": "Paracetamol", "dosage": "500mg every 6 hours"},
        {"name": "Ibuprofen", "dosage": "200mg twice daily"}
    ] if "fever" in symptoms.lower() else []

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO diagnosis (symptoms, temperature, heartrate, bloodpressure, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symptoms, temp, hr, bp, lat, lon, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return render_template("result.html", result=result, vitals=vitals, medicines=suggested_meds)

if __name__ == "__main__":
    app.run(debug=True)
