
import json
import sqlite3
from datetime import datetime

import paho.mqtt.client as mqtt

# =========================
# MQTT SETTINGS
# =========================

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "hvac/energy/sensors"

# =========================
# SQLITE DATABASE
# =========================

DB_NAME = "hvac_data.db"

def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature REAL,
                humidity REAL,
                occupancy INTEGER,
                hvac_power REAL
            )
        """)
        conn.commit()

# =========================
# SAVE SENSOR DATA
# =========================

def save_data(data):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO sensor_data
            (timestamp, temperature, humidity,
             occupancy, hvac_power)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            float(data["temperature"]),
            float(data["humidity"]),
            int(data["occupancy"]),
            float(data["hvac_power"])
        ))
        conn.commit()

    print("Saved to SQLite:", data)

# =========================
# MQTT CALLBACKS
# =========================

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker!")
        client.subscribe(TOPIC)
        print("Subscribed to:", TOPIC)
    else:
        print("Connection failed:", reason_code)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))

        required = [
            "temperature",
            "humidity",
            "occupancy",
            "hvac_power"
        ]

        if not all(key in data for key in required):
            print("Invalid sensor data:", data)
            return

        save_data(data)

    except Exception as e:
        print("Error processing data:", e)

# =========================
# MAIN PROGRAM
# =========================

if __name__ == "__main__":

    create_database()

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    client.on_connect = on_connect
    client.on_message = on_message

    print("Starting MQTT Receiver...")
    print("Connecting to MQTT broker...")

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_forever()

    except Exception as e:
        print("MQTT Error:", e)