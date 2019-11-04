import enum
import os
import ctypes
import socket
import paho.mqtt.client as mqtt
import struct

from control_api.api import move_forward, init_socket, Actions

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("control")


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

init_socket()
move_forward(7, 2)
