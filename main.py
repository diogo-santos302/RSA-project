import time
import paho.mqtt.client as mqtt
from scan_neighbours import scan_neighbours
from neighbours import neighbours, lock

broker_address = "localhost"
broker_port = 1883
topic = "sensor"

def publish_to_topic(pi_address: str, msg):
    pi_client = mqtt.Client()
    pi_client.connect(pi_address, broker_port)
    pi_client.publish(topic, msg.payload.decode())
    pi_client.disconnect()

def publish_message_to_all_neighbours(neighbours: list, msg):
    for pi_address in neighbours:
        if pi_address != broker_address:
            try:
                publish_to_topic(pi_address, msg)
            except socket.timeout:
                print(f"Socket timeout occurred. Unable to establish connection or receive data with {pi_address}")

def on_message(client, userdata, msg):
    print("Received MQTT message: ", msg.payload.decode())
    temp_neighbours = []
    with lock:
        temp_neighbours[:] = neighbours
    publish_message_to_all_neighbours(temp_neighbours, msg)
    
def subscribe_to_topic() -> mqtt.Client:
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    client.subscribe(topic)
    return client
    
def main():
    client: mqtt.Client = subscribe_to_topic()
    client.loop_start()

    try:
        while True:
            scan_neighbours(10)
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nExiting")

    client.loop_stop()

if __name__ == "__main__":
	main()
