import struct
from time import sleep

from control_api.api import get_distance, stop
from config import QOS, LEADER_ID, FOLLOWER_ID
from paho.mqtt.client import Client

def get_obstacle(interval_seconds: float, is_leader, mqtt: Client=None):

    while True:
        if get_distance(LEADER_ID if is_leader else FOLLOWER_ID) <= 5:
            if is_leader:
                mqtt.publish(topic="control", payload=struct.pack('hhi', 0, FOLLOWER_ID, 0), qos=QOS,
                               retain=False)
                stop(LEADER_ID, 0)
            else:
                stop(FOLLOWER_ID, 0)
        sleep(interval_seconds)
