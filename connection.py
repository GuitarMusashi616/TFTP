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
        """
        If Error: shut down the connection (if client port is new then creates and destroys same connection)
        Else: pass the message and address down to the Connection's State
        """
        if msg[0:2] == ERROR:
            if self.file:
                self.file.close()
            self.state = Closed(self)
            return
        self.state.handle(msg, addr)

    @property
    def state(self):
        """
        Makes state a public property used by the Connection's State instances to swap states
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        When Changing state the State's startup method is called
        """
        self._state = value
        self.startup()



