import time
import threading
import tinytuya
import paho.mqtt.client as mqtt
import yaml

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

MQTT_HOST = config["mqtt"]["host"]
MQTT_PORT = config["mqtt"].get("port", 1883)
MQTT_USER = config["mqtt"]["username"]
MQTT_PASS = config["mqtt"]["password"]

DEVICE_ID = config["tuya"]["device_id"]
LOCAL_KEY = config["tuya"]["local_key"]

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {rc}")

mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

print("Logging into Tuya Cloud...")
c = tinytuya.Cloud(
    apiRegion="eu",
    apiKey="",       # Leave empty if using localKey only
    apiSecret="",    # Leave empty if using localKey only
    username="",     # Leave empty if using localKey only
    password=""      # Leave empty if using localKey only
)

device = tinytuya.OutletDevice(DEVICE_ID, '', LOCAL_KEY)
device.set_version(3.3)

def poll_loop():
    last_state = None
    while True:
        data = device.status()
        if 'dps' in data:
            doorbell_state = data['dps'].get('door_bell', None)
            if doorbell_state != last_state:
                print(f"Doorbell state changed: {doorbell_state}")
                mqtt_client.publish("tuya/doorbell/pressed", str(doorbell_state).lower())
                last_state = doorbell_state
        time.sleep(1)

poll_loop()
