import os
import ctypes
import socket

# Load the shared library into c types.
lib_control = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "c-libraries/lib_control.so"))

libc = ctypes.CDLL(lib_control)

def init_socket():
    result = libc.init(1)
    print(result)    

def move_forward():
    libc.send_forward_time(1, 7, 5)

init_socket()
move_forward()