import paho.mqtt.client as mqtt
import json
import random
import time

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "hvac/energy/sensors"

client = mqtt.Client()

client.connect(BROKER, PORT, 60)

print("MQTT Sensor Simulator Started...")
print(f"Publishing to: {TOPIC}")

while True:
    data = {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "occupancy": random.randint(0, 20),
        "hvac_power": round(random.uniform(1.5, 5.0), 2)
    }

    message = json.dumps(data)

    client.publish(TOPIC, message)

    print("Published:", message)

    time.sleep(5)