# Austin Williams
# Dr. Shawn Butler
# Computer Networks
# November 25, 2020

from connection_state import *


class Connection:
    """
    A message processor and responder that remembers the state of the connection for a unique client port
    """
    def __init__(self, output_queue):
        self.state = Open(self)
        self.file = None
        self.addr = None
        self.block_num = None
        self.output_queue = output_queue

    def startup(self):
        self.state.startup()

    def handle(self, msg, addr):
        self.state.handle(msg, addr)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.startup()



