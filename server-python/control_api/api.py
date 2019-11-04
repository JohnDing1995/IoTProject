import ctypes
import os

lib_control = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../c-libraries/lib_control.so"))

libc = ctypes.CDLL(lib_control)

def move_forward(target: int, seconds: int):
    libc.send_forward_time(1, target, seconds)

def init_socket():
    result = libc.init(1)
    print(result)
