import struct

import paho.mqtt.client as mqtt

from config import BROKER_IP, BROKER_PORT

broker_url = "0.0.0.0"
broker_port = 1883

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("control")


client = mqtt.Client()
client.connect(BROKER_IP, BROKER_PORT)
client.publish(topic="control", payload=struct.pack('hhi', 1, 7, 2), qos=1, retain=False)
client.on_connect = on_connect
#client.on_message = on_message
client.loop_forever()
