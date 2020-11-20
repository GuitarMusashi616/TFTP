from shared import *


class ConnectionState:
    def __init__(self, connection):
        self.connection = connection


class NotInitialized(ConnectionState):
    """
    Initial Connection State for new Connection, yet to decide whether the connection to client will be a download or upload
    """
    def handle(self, msg, addr):
        if msg[0:2] == RRQ:
            self.connection.type = 'Upload'
            self.connection.state = SendData(self)

        elif msg[0:2] == WRQ:
            self.connection.type = 'Download'
            self.connection.state = ReceiveData(self)







        # Server Upload States


class SendData(ConnectionState):
    def handle(self, msg, addr):
        pass





class WaitForAck(ConnectionState):
    pass


class Shutdown(ConnectionState):
    pass


class ReceiveData(ConnectionState):
    pass

# Server Download States

