import json
import paho.mqtt.client as mqtt
import time
import logging

_LOGGER = logging.getLogger(__name__)

# Wczytanie konfiguracji z options.json
def load_config():
    try:
        with open('/data/options.json') as f:
            options = json.load(f)
        return options
    except Exception as e:
        _LOGGER.error(f"Failed to load options.json: {e}")
        return None

# Callback przy połączeniu MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        _LOGGER.info("Connected to MQTT broker successfully")
        # Subskrybuj temat (dopasuj temat do swojego urządzenia)
        client.subscribe("tuya/doorbell/event")
    else:
        _LOGGER.error(f"Failed to connect to MQTT broker, return code {rc}")

# Callback przy otrzymaniu wiadomości MQTT
def on_message(client, userdata, msg):
    _LOGGER.info(f"Received MQTT message on topic {msg.topic}: {msg.payload.decode()}")

    # Tutaj możesz dodać własną logikę np. wywołanie powiadomienia itp.

def main():
    options = load_config()
    if not options:
        _LOGGER.error("No configuration found, exiting")
        return

    mqtt_conf = options.get('mqtt', {})
    device_conf = options.get('device', {})

    mqtt_broker = mqtt_conf.get('broker')
    mqtt_port = mqtt_conf.get('port', 1883)
    mqtt_username = mqtt_conf.get('username')
    mqtt_password = mqtt_conf.get('password')

    device_id = device_conf.get('id')
    local_key = device_conf.get('local_key')

    if not all([mqtt_broker, mqtt_username, mqtt_password, device_id, local_key]):
        _LOGGER.error("Missing MQTT or device configuration parameters")
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
            # Tutaj możesz dodać logikę do komunikacji z urządzeniem Tuya,
            # np. odczytywanie stanu, wysyłanie komend itp.
            time.sleep(1)
    except KeyboardInterrupt:
        _LOGGER.info("Stopping Tuya MQTT Doorbell")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
