import ctypes
import re
import socket
from _ctypes import POINTER
from time import sleep

from subprocess import Popen, PIPE

import pexpect

class Control():
    def connect(self):
        self.child = pexpect.spawn('./tcpserver 1')
        self.child.expect('Waiting for bots to connect', timeout=99999999)
        print(self.child.before.decode("utf-8"))
        self.child.expect('Enter Bot ID to send the packet',timeout=99999999)
        string_with_id = self.child.before.decode("utf-8")
        print(string_with_id)
        self.car_id = re.search(r'<(.*?)>',string_with_id).group(1)

    def move_forward(self, time=0):
        self.child.sendline(self.car_id)
        self.child.expect('Waiting for user input', timeout=99999999)
        print(self.child.before.decode("utf-8"))

        self.child.sendline('1')
        print('Moving forward')
        sleep(time)


    def stop(self):
        self.child.expect('Enter Bot ID to send the packet', timeout=99999999)
        self.child.sendline(self.car_id)
        self.child.expect('Waiting for user input', timeout=99999999)
        print(self.child.before.decode("utf-8"))
        self.child.sendline('7')
        print('Stop')

# control = Control()
# control.connect()
# control.move_forward(2)
# control.stop()
# control.move_forward(2)
# control.stop()
# control.move_forward(2)
# control.stop()
# control.move_forward(2)
# control.stop()
# control.move_forward(2)
# control.stop()
# control.move_forward(2)
# control.stop()
# control.move_forward(2)
# control.stop()


# init()