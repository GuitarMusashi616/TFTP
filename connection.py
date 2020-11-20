from connection_state import *


class Connection:
    """
    A message processor and responder that remembers the state of the connection for a unique client port
    """
    def __init__(self):
        self.state = NotInitialized(self)
        self.type = None
        self.client_port = None
        self.file_path = None

    def handle(self, msg, addr):
        self.state.handle(msg, addr)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value



