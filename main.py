import socket
import time
import paho.mqtt.client as mqtt
from arp import get_connected_devices

broker_address = "localhost"
broker_port = 1883
topic = "sensor"
ip_range = "10.1.1.0/24"

def publish_to_topic(pi_address: str, msg):
    pi_client = mqtt.Client()
    pi_client.connect(pi_address, broker_port)
    pi_client.publish(topic, msg.payload.decode())
    pi_client.disconnect()

def publish_message_to_all_neighbours(msg):
    neighbours: list = get_connected_devices(ip_range, 1)
    for ip_address in neighbours:
        print(f"Relaying message to {ip_address}")
        try:
            publish_to_topic(ip_address, msg)
        except socket.timeout:
            print(f"Socket timeout occurred. Unable to establish connection or receive data with {ip_address}")

def on_message(client, userdata, msg):
    print("Received MQTT message: ", msg.payload.decode())
    publish_message_to_all_neighbours(msg)
    
def subscribe_to_topic() -> mqtt.Client:
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    client.subscribe(topic)
    return client
    
def main():
    client: mqtt.Client = subscribe_to_topic()
    client.loop_start()
    print("Started loop")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting")

    client.loop_stop()

if __name__ == "__main__":
	main()
