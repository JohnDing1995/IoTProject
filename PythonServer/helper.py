import ctypes
import socket

lib = ctypes.CDLL("./libpycall_c.so")
def init_socket():
    bot_id = -1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
        s.bind(('', 5555))
        from pprint import pprint
        pprint(s)
        print("Bind succeed. listening")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            lib.create_packet.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char, POINTER(ctypes.c_char_p)]
            lib.send_forward_time(1, 7, 0)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

init_socket()