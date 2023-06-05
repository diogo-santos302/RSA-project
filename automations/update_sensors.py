import json
import time
import paho.mqtt.client as mqtt

# Configuration for the source broker
broker_address = "localhost"
broker_port = 1883
broker_topic = "sensor2"

# Create the source MQTT client
client = mqtt.Client()

# Define callback functions for source and destination clients
def on_message(client, userdata, message):
    # Callback function for handling messages received from the source broker
    payload = message.payload.decode()
    print(f"Received message: {payload}")
    data = json.loads(payload)
    if "temperature" in data:
        client.publish("sensor/temperature", data["temperature"])
    elif "door" in data:
        client.publish("sensor/door", data["door"])

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")

def on_publish(client, userdata, mid):
    # Callback function for handling successful publish to the destination broker
    print("Message published")

# Set the callback functions for source and destination clients
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish

# Connect and subscribe the source client to the source broker
client.connect(broker_address, broker_port)
client.subscribe(broker_topic)

# Start the loop for both clients
client.loop_start()

try:
    while True:
        # Main loop to keep the script running
        time.sleep(1)

except KeyboardInterrupt:
    # Stop the loop and disconnect the clients when interrupted
    client.loop_stop()
    client.disconnect()
