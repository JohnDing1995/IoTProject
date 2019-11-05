import ctypes
import os
from enum import Enum

lib_control = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../c-libraries/lib_control.so"))

libc = ctypes.CDLL(lib_control)



class Actions(Enum):
    STOP = 0
    FORWARD = 1
    LEFT = 2
    RIGHT = 3
    BACK = 4


def move_forward(target: int, seconds: int):
    libc.send_forward_time(1, target, seconds)

def move_backward(target: int, seconds: int):
    libc.send_reverse_time(1, target, seconds)

def stop(target: int, seconds:int):
    libc.stop_bot(1, target)

def rotate_left(target: int, seconds: int):
    libc.send_rotate_left(1, target, seconds)

def rotate_right(target: int, seconds: int):
    libc.send_rotate_right(1, target, seconds)

def init_socket():
    result = libc.init(1)
    print(result)

def get_distance(target: int) -> int:

    result = libc.get_obstacle_data(1, target, 3)
    return result

