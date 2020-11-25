from shared import *
import os


class ConnectionState:
    def __init__(self, connection):
        self.connection = connection

    def startup(self):
        raise NotImplementedError

    def handle(self, msg, addr):
        raise NotImplementedError


class Open(ConnectionState):
    """
    Initial Connection State for new Connection, yet to decide whether the connection to client will be a download or upload
    """
    def startup(self):
        pass  # todo: set variables back to None

    def handle(self, msg, addr):
        if msg[0:2] == RRQ:
            filename = extract_null_terminated_string(msg)

            if not os.path.exists(filename):  # todo: replace with try except
                err_str = "filename does not correspond to a file saved on the server, try again"
                err_msg = ERROR + Error.FILE_NOT_FOUND + err_str.encode() + NULL
                self.connection.output_queue.put((err_msg, addr))
                self.connection.state = Closed(self.connection)
                return

            self.connection.type = 'Upload'
            self.connection.file = open(filename, 'rb')
            self.connection.block_num = 1
            self.connection.addr = addr
            self.connection.state = Upload(self.connection)

        elif msg[0:2] == WRQ:
            filename = extract_null_terminated_string(msg)
            # if os.path.exists(filename):
            #     err_str = "filename already exists at destination"
            #     err_msg = ERROR + Error.ACCESS_VIOLATION + err_str.encode() + NULL
            #     self.connection.output_queue.put((err_msg, addr))
            #     self.connection.state = Closed(self.connection)
            #     return

            self.connection.type = 'Download'
            self.connection.file = open(filename, 'wb')
            self.connection.block_num = 0
            self.connection.addr = addr
            self.connection.state = Download(self.connection)


class Upload(ConnectionState):
    def startup(self):
        data_bytes = self.connection.file.read(512)
        block_num_bytes = short_to_bytes(self.connection.block_num)
        data_msg = DATA + block_num_bytes + data_bytes
        self.connection.output_queue.put((data_msg, self.connection.addr))
        if len(data_msg) < 516:
            self.connection.state = FinalUpload(self.connection)

    def handle(self, msg, addr):
        if msg == ACK + short_to_bytes(self.connection.block_num):
            self.connection.block_num += 1
            self.connection.state = Upload(self.connection)


class Download(ConnectionState):
    def startup(self):
        ack_msg = ACK + short_to_bytes(self.connection.block_num)
        self.connection.output_queue.put((ack_msg, self.connection.addr))
        self.connection.block_num += 1

    def handle(self, msg, addr):
        if msg and msg[2:4] == short_to_bytes(self.connection.block_num):
            self.connection.file.write(msg[4:])
            if len(msg) < 516:
                self.connection.state = FinalDownload(self.connection)
            else:
                self.connection.state = Download(self.connection)


class FinalUpload(ConnectionState):
    def startup(self):
        pass

    def handle(self, msg, addr):
        if msg == ACK + short_to_bytes(self.connection.block_num):
            self.connection.block_num += 1
            self.connection.state = Closed(self.connection)


class FinalDownload(ConnectionState):
    def startup(self):
        ack_msg = ACK + short_to_bytes(self.connection.block_num)
        self.connection.output_queue.put((ack_msg, self.connection.addr))
        self.connection.block_num += 1
        self.connection.file.close()
        self.connection.state = Closed(self.connection)

    def handle(self, msg, addr):
        pass


class Closed(ConnectionState):
    def startup(self):
        pass

    def handle(self, msg, addr):
        pass


class WaitForAck(ConnectionState):
    pass


class Shutdown(ConnectionState):
    pass

