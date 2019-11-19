import struct
from threading import Thread
from time import sleep

from helper import get_obstacle

import paho.mqtt.client as mqtt

from config import BROKER_IP, BROKER_PORT, FOLLOWER_ID, DELAY_TURN
from control_api.api import *

command_switcher = {
    0: stop,
    1: move_forward,
    2: rotate_left,
    3: rotate_right,
    4: move_backward
}

class Follower(object):
    def __init__(self):
        self.last_operation = -1
        self.client = mqtt.Client()
    def on_message(self, client, userdata, msg):
        payload = struct.unpack('hhi', msg.payload)
        print("Action: {} ID: {} TIME: {}".format(Actions(payload[0]).name, payload[1], payload[2]))
        control_func = command_switcher.get(payload[0], '')
        # if true, follower need to first move forward to the turning point of the leader before turing.
        if DELAY_TURN:
            if payload[0] in [2, 3]:
                stop(*payload[1:])
                self.last_dist = get_distance(payload[1])
                print("Distance with front car is {}".format(self.last_dist))
                self.last_operation = control_func
                self.last_sec = payload[2]
            else:
                if payload[0] == 1:
                    # if leader moved forward after a turn, follower need to move forward first to the turning point and
                    # then makes the turn.
                    if self.last_operation in [rotate_right, rotate_left]:
                        print("Last operation was a turn")
                        forward_sec = (10 + self.last_dist) / 7 + 1
                        print("Need to move forward for {} seconds".format(forward_sec))
                        move_forward(payload[1], int(forward_sec))
                        # move_forward_by_distance(payload[1], str(self.last_dist+10))
                        sleep(forward_sec - 1)
                        print("Now repeating last operation for {} sec".format(self.last_sec))
                        self.last_operation(payload[1], self.last_sec)
                        sleep(self.last_sec)
                control_func(*payload[1:])
        else:
            control_func(*payload[1:])


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("control")

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(BROKER_IP, BROKER_PORT, 1000)
        self.client.loop_forever()


# Init the connection with the server.
init_socket()
get_obstacle_thread = Thread(target=get_obstacle, args=(0.5, False))
get_obstacle_thread.start()
follower = Follower()
follower.run()
