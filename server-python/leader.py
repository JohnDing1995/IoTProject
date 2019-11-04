import os
import ctypes
import socket
import paho.mqtt.client as paho

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

client = paho.Client()
client.on_connect = on_connect
client.connect("broker.mqttdashboard.com", 1883)

paho.Client(client_id="leader", clean_session=True, userdata=None, protocol=paho.MQTTv311)
client.connect(host="localhost", port=1883, keepalive=60, bind_address="")
client.loop_forever()