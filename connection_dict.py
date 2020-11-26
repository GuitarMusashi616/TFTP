# Austin Williams
# Dr. Shawn Butler
# Computer Networks
# November 25, 2020

import threading
from connection import *


class ConnectionDict:
    def __init__(self, output_queue):
        self.dict = {}
        self.lock = threading.Lock()
        self.output_queue = output_queue

    def retrieve(self, addr):
        self.lock.acquire()
        if addr not in self.dict:
            self.dict[addr] = [Connection(self.output_queue), threading.Lock()]
        conn, conn_lock = self.dict[addr]
        self.lock.release()
        return conn, conn_lock

    def delete(self, addr):
        self.lock.acquire()
        assert addr in self.dict, "Address not in Connection Dictionary, cannot delete"
        del self.dict[addr]
        self.lock.release()

    def handle(self, msg, addr):
        conn, conn_lock = self.retrieve(addr)
        conn_lock.acquire()
        conn.handle(msg, addr)
        if isinstance(conn.state, Closed):
            self.delete(addr)
        conn_lock.release()
