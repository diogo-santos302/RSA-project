import time
import paho.mqtt.client as mqtt

# Configuration for the source broker
source_broker_address = "localhost"
source_broker_port = 1883
source_broker_topic = "sensor"

# Configuration for the destination broker
destination_broker_address = "10.1.1.2"
destination_broker_port = 1883
destination_broker_topic = "sensor"

# Create the source MQTT client
source_client = mqtt.Client()

# Create the destination MQTT client
destination_client = mqtt.Client()

# Define callback functions for source and destination clients
def on_source_message(client, userdata, message):
    # Callback function for handling messages received from the source broker
    payload = message.payload.decode()
    print(f"Received from source: {payload}")

    # Publish the message to the destination broker
    destination_client.publish(destination_broker_topic, payload)

def on_source_connect(client, userdata, flags, rc):
    print("Connected to local broker")
    client.subscribe("sensor")

def on_destination_connect(client, userdata, flags, rc):
    # Callback function for handling connection to the destination broker
    print("Connected to destination broker")
    client.subscribe("sensor")

def on_destination_publish(client, userdata, mid):
    # Callback function for handling successful publish to the destination broker
    print("Message published to destination")

def on_destination_message(client, userdata, msg):
    print("Received message: ", msg.payload.decode())
    source_client.publish("sensor2", msg.payload.decode())

# Set the callback functions for source and destination clients
source_client.on_message = on_source_message
destination_client.on_connect = on_destination_connect
destination_client.on_message = on_destination_message

# Connect and subscribe the source client to the source broker
source_client.connect(source_broker_address, source_broker_port)
source_client.subscribe(source_broker_topic)

# Connect the destination client to the destination broker
destination_client.connect(destination_broker_address, destination_broker_port)

# Start the loop for both clients
source_client.loop_start()
destination_client.loop_start()

try:
    while True:
        # Main loop to keep the script running
        time.sleep(1)

except KeyboardInterrupt:
    # Stop the loop and disconnect the clients when interrupted
    source_client.loop_stop()
    destination_client.loop_stop()
    source_client.disconnect()
    destination_client.disconnect()
