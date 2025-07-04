import json
import paho.mqtt.client as mqtt
import time
import logging

_LOGGER = logging.getLogger(__name__)

def load_config():
    try:
        with open('/data/options.json') as f:
            options = json.load(f)
        return options
    except Exception as e:
        _LOGGER.error(f"Failed to load options.json: {e}")
        return None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        _LOGGER.info("Connected to MQTT broker successfully")
        client.subscribe("tuya/doorbell/event")  # Dopasuj temat do swojego urządzenia
    else:
        _LOGGER.error(f"Failed to connect to MQTT broker, return code {rc}")

def on_message(client, userdata, msg):
    _LOGGER.info(f"Received MQTT message on topic {msg.topic}: {msg.payload.decode()}")
    # Dodaj tutaj obsługę wiadomości, np. powiadomienia w HA

def main():
    options = load_config()
    if not options:
        _LOGGER.error("No configuration found, exiting")
        return

    mqtt_broker = options.get('mqtt_broker')
    mqtt_port = options.get('mqtt_port', 1883)
    mqtt_username = options.get('mqtt_username')
    mqtt_password = options.get('mqtt_password')
    device_id = options.get('device_id')
    device_local_key = options.get('device_local_key')

    if not all([mqtt_broker, mqtt_username, mqtt_password, device_id, device_local_key]):
        _LOGGER.error("Missing required configuration parameters")
        return

    _LOGGER.info(f"Starting Tuya MQTT Doorbell for device {device_id}")

    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
    except Exception as e:
        _LOGGER.error(f"Could not connect to MQTT broker: {e}")
        return

    client.loop_start()

    try:
        while True:
            # Tutaj możesz dopisać logikę komunikacji z urządzeniem Tuya
            time.sleep(1)
    except KeyboardInterrupt:
        _LOGGER.info("Stopping Tuya MQTT Doorbell")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
