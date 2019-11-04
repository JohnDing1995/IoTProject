import struct

import paho.mqtt.client as mqtt

from config import BROKER_IP, BROKER_PORT
from control_api.api import move_forward, init_socket, Actions, stop, move_backward, rotate_left, rotate_right

command_switcher = {
    0: stop,
    1: move_forward,
    2: rotate_left,
    3: rotate_right,
    4: move_backward
}


def on_message(client, userdata, msg):
    payload = struct.unpack('hhi', msg.payload)
    print("Action: {} ID: {} TIME: {}".format(Actions(payload[0]).name, payload[1], payload[2]))
    control_func = command_switcher.get(payload[0], '')
    control_func(*payload[1:])


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("control")


# Init the connection with the server.
init_socket()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_IP, BROKER_PORT, 60)

client.loop_forever()
