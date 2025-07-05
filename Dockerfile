FROM ghcr.io/hassio-addons/base-python:latest

COPY tuya_mqtt_doorbell.py /app/tuya_mqtt_doorbell.py

CMD ["python3", "/app/tuya_mqtt_doorbell.py"]
