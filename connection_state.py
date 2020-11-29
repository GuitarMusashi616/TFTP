# Austin Williams
# Dr. Shawn Butler
# Computer Networks
# November 25, 2020

from shared import *
from config import *
from message import *
import os


class ConnectionState:
    """
    Abstract class for states of the Connection instance, all states must have a startup and handle method
    """
    def __init__(self, connection):
        self.connection = connection

    def startup(self):
        raise NotImplementedError

    def handle(self, msg, addr):
        raise NotImplementedError


class Open(ConnectionState):
    """
    Initial Connection State for new Connection, ready to start a download or an upload based on first message received.
    """
    def startup(self):
        pass  # todo: set variables back to None

    def handle(self, msg, addr):
        if msg[0:2] == RRQ:
            filename = extract_null_terminated_string(msg)

            if not os.path.exists(filename) or not os.access(filename, os.R_OK):
                err_msg = ErrorMessage(Error.FILE_NOT_FOUND, "filename does not exist or cannot be opened, try again")
                self.connection.output_queue.put((bytes(err_msg), addr))
                self.connection.state = Closed(self.connection)
                return

            self.connection.file = open(filename, 'rb')
            self.connection.block_num = 1
            self.connection.addr = addr
            self.connection.state = Upload(self.connection)

        elif msg[0:2] == WRQ:
            filename = extract_null_terminated_string(msg)
            if filename[:40] == '/home/A365/tftp_threads/dist/read_files/':
                filename = os.getcwd() + filename[39:]

            if os.path.exists(filename):
                err_msg = ErrorMessage(Error.ACCESS_VIOLATION, "filename already exists at destination")
                self.connection.output_queue.put((bytes(err_msg), addr))
                self.connection.state = Closed(self.connection)
                return

            self.connection.file = open(filename, 'wb')
            self.connection.block_num = 0
            self.connection.addr = addr
            self.connection.state = Download(self.connection)
        else:
            # ERRORs are handled by higher Connection layer
            err_msg = ErrorMessage(Error.UNKNOWN_TID, "Unknown TID, first packet must be a read or write request")
            self.connection.output_queue.put((bytes(err_msg), addr))
            self.connection.state = Closed(self.connection)


class Upload(ConnectionState):
    """
    State used while sending data to the client,
    Queues the next up to 512 bytes of the file
    Changes state to FinalUpload when less than 512 bytes remaining in file
    """
    def startup(self):
        data_bytes = self.connection.file.read(MAX_PACKET_SIZE-4)
        block_num_bytes = short_to_bytes(self.connection.block_num)
        data_msg = DATA + block_num_bytes + data_bytes
        self.connection.output_queue.put((data_msg, self.connection.addr))
        if len(data_msg) < MAX_PACKET_SIZE:
            self.connection.state = FinalUpload(self.connection)

    def handle(self, msg, addr):
        if msg == ACK + short_to_bytes(self.connection.block_num):
            self.connection.block_num += 1
            self.connection.state = Upload(self.connection)


class Download(ConnectionState):
    """
    State used while receiving data from the client,
    Checks the Ack's block num and saves the data to a file
    Changes state to FinalDownload when less than 512 bytes received
    """
    def startup(self):
        ack_msg = ACK + short_to_bytes(self.connection.block_num)
        self.connection.output_queue.put((ack_msg, self.connection.addr))
        self.connection.block_num += 1

    def handle(self, msg, addr):
        if msg and msg[2:4] == short_to_bytes(self.connection.block_num):
            self.connection.file.write(msg[4:])
            if len(msg) < MAX_PACKET_SIZE:
                self.connection.state = FinalDownload(self.connection)
            else:
                self.connection.state = Download(self.connection)


class FinalUpload(ConnectionState):
    """
    Accepts the final Ack and changes state to Closed to be deleted by the ConnectionDictionary
    """
    def startup(self):
        pass

    def handle(self, msg, addr):
        if msg == ACK + short_to_bytes(self.connection.block_num):
            self.connection.block_num += 1
            self.connection.file.close()
            self.connection.state = Closed(self.connection)


class FinalDownload(ConnectionState):
    """
    Sends the final Ack, closes the file, and changes state to Closed to be deleted by the ConnectionDictionary
    """
    def startup(self):
        ack_msg = ACK + short_to_bytes(self.connection.block_num)
        self.connection.output_queue.put((ack_msg, self.connection.addr))
        self.connection.block_num += 1
        self.connection.file.close()
        self.connection.state = Closed(self.connection)

    def handle(self, msg, addr):
        pass


class Closed(ConnectionState):
    """
    Gets deleted by the parent ConnectionDictionary layer
    """
    def startup(self):
        pass

    def handle(self, msg, addr):
        pass


