import os
import pprint
import pygame
import struct
from time import sleep

import paho.mqtt.client as mqtt

from control_api.api import *
from config import BROKER_IP, BROKER_PORT

LEADER_ID = 6
FOLLOWER_ID = 7
QOS = 2


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("control")


def on_publish(client, userdata, mid):
    print("published")


def on_disconnect(client, userdata, rc):
    print("client disconnected ok")


class LeaderPS4(object):

    controller = None
    button_data = None
    hat_data = None

    # Labels for DS4 controller hats (Only one hat control)
    HAT_1 = 0
    BUTTON_SQUARE = 3

    def init(self):
        """Initialize the joystick components"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.button_data = {}
        self.hat_data = {}
        
        # Assign initial data values
        # Hats are initialized to 0
        for i in range(self.controller.get_numhats()): 
            self.hat_data[i] = (0, 0)
        # Buttons are initialized to False
        for i in range(self.controller.get_numbuttons()): 
            self.button_data[i] = False
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_publish = on_publish
        self.client.on_disconnect = on_disconnect
        self.client.connect(BROKER_IP, BROKER_PORT)

    def listen(self):
        """Listen for events to happen"""
        
        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False

                #Up
                if self.hat_data[self.HAT_1][1] == 1:
                    print("Up")
                    self.client.publish(topic="control", payload=struct.pack('hhi', 1, FOLLOWER_ID, 0), qos=QOS,
                                        retain=False)
                    move_forward(LEADER_ID, 0)
                    sleep(0.5)
                #Down    
                elif self.hat_data[self.HAT_1][1] == -1:
                    print("Down")
                    self.client.publish(topic="control", payload=struct.pack('hhi', 4, FOLLOWER_ID, 0), qos=QOS,
                                        retain=False)
                    move_backward(LEADER_ID, 0)
                    sleep(0.5)
                #Right
                elif self.hat_data[self.HAT_1][0] == 1:
                    print("Left")
                    self.client.publish(topic="control", payload=struct.pack('hhi', 3, FOLLOWER_ID, 2), qos=QOS,
                                        retain=False)
                    rotate_left(LEADER_ID, 2)
                    sleep(0.5)
                #Left
                elif self.hat_data[self.HAT_1][0] == -1:
                    print("Right")
                    self.client.publish(topic="control", payload=struct.pack('hhi', 2, FOLLOWER_ID, 2), qos=QOS,
                                        retain=False)
                    rotate_right(LEADER_ID, 2)
                    sleep(0.5)
                elif self.button_data[self.BUTTON_SQUARE] == True:
                    print("Stop")
                    self.client.publish(topic="control", payload=struct.pack('hhi', 0, FOLLOWER_ID, 0), qos=QOS,
                                        retain=False)
                    stop(LEADER_ID, 0)
                    sleep(0.5)




if __name__ == "__main__":
    init_socket()
    leader = LeaderPS4()
    leader.init()
    leader.listen()
