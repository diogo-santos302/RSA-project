import time
import paho.mqtt.client as mqtt

# Configuration for the broker
broker_address = "localhost"
broker_port = 1883
broker_topic = "automation/alarm"
SECRET_KEY = "alarm" # MUST MATCH PAYLOAD INSIDE HOME ASSISTANT AUTOMATION TRIGGER

# Create the MQTT client
client = mqtt.Client()

# Define callback functions for the client
def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe("sensor/door")

def on_message(client, userdata, message):
    # Callback function for handling messages received from the broker
    payload = message.payload.decode()
    print(f"Received message: {payload}")
    # Check the values of temperature and smoke
    if  payload == "on":
        # Send a message to the automation topic
        client.publish(broker_topic, SECRET_KEY)

def on_publish(client, userdata, mid):
    # Callback function for handling successful publish to the broker
    print("Message published")

# Set the callback functions for the client
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect the client to the broker
client.connect(broker_address, broker_port)

# Start the loop for the client
client.loop_start()

try:
    while True:
        # Main loop to keep the script running
        time.sleep(5)
except KeyboardInterrupt:
    # Stop the loop and disconnect the client when interrupted
    client.loop_stop()
    client.disconnect()
    
