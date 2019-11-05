import os
import pprint
import pygame
import struct
from time import sleep

import paho.mqtt.client as mqtt

from control_api.api import *
from config import BROKER_IP, BROKER_PORT

LEADER_ID = 7

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
              
                os.system('clear')
                #Up
                if self.hat_data[self.HAT_1][1] == 1:
                    print("Up")
                    client.publish(topic="control", payload=struct.pack('hhi', 1, LEADER_ID, 0), qos=1, retain=False)
                    move_forward(LEADER_ID, 0)
                #Down    
                elif self.hat_data[self.HAT_1][1] == -1:
                    print("Down")
                    client.publish(topic="control", payload=struct.pack('hhi', 4, LEADER_ID, 0), qos=1, retain=False)
                    move_backward(LEADER_ID, 0)
                #Right
                elif self.hat_data[self.HAT_1][0] == 1:
                    print("Right")
                    client.publish(topic="control", payload=struct.pack('hhi', 3, LEADER_ID, 0), qos=1, retain=False)
                    rotate_right(LEADER_ID, 1)
                #Left
                elif self.hat_data[self.HAT_1][0] == -1:
                    print("Left")
                    client.publish(topic="control", payload=struct.pack('hhi', 2, LEADER_ID, 0), qos=1, retain=False)
                    rotate_left(LEADER_ID, 1)
                elif self.button_data[self.BUTTON_SQUARE] == True:
                    print("Stop")
                    client.publish(topic="control", payload=struct.pack('hhi', 0, LEADER_ID, 0), qos=1, retain=False)
                    stop(LEADER_ID, 0)

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("control")

if __name__ == "__main__":
    init_socket()
    client = mqtt.Client()
    client.connect(BROKER_IP, BROKER_PORT)
    leader = LeaderPS4()
    leader.init()
    leader.listen()
    #client.on_connect = on_connect
    #client.on_message = on_message
    #client.loop_forever()
