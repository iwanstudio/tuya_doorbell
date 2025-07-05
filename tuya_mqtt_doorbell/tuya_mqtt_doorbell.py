import json
import time
import paho.mqtt.client as mqtt
from tinytuya import OutletDevice

CONFIG_PATH = "/data/options.json"

# Wczytaj dane konfiguracyjne
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

mqtt_broker = config.get("mqtt_broker")
mqtt_port = int(config.get("mqtt_port", 1883))
mqtt_username = config.get("mqtt_username")
mqtt_password = config.get("mqtt_password")
device_id = config.get("device_id")
device_local_key = config.get("device_local_key")

# Konfiguracja klienta MQTT
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

print("Połączono z MQTT brokerem")

# Konfiguracja urządzenia Tuya
device = OutletDevice(device_id, "192.168.3.1", device_local_key)
device.set_version(3.3)

print("Połączono z urządzeniem Tuya")

def main_loop():
    while True:
        try:
            data = device.status()
            if data:
                dps = data.get("dps", {})
                if "1" in dps and dps["1"] == True:
                    print("Dzwonek został wciśnięty!")
                    client.publish("tuya/doorbell", "pressed", qos=0, retain=False)
                    time.sleep(5)
        except Exception as e:
            print("Błąd:", e)
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
