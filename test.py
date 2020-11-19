import pytest
import threading
import socket
import random
import time
from queue import Queue
from shared import *


def single_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_port = 54321
    port = random.randint(5000, 6000)
    s.bind(('', port))
    s.sendto(b'TestTestTest', ('127.0.0.1', server_port))


def single_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_port = 54321
    s.bind(('', server_port))

    msg, addr = s.recvfrom(2048)
    assert msg == b'TestTestTest'


def test_client_access():
    t1 = threading.Thread(target=single_server)
    t2 = threading.Thread(target=single_client)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def setup_server(server_port=54321):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', server_port))
    s.settimeout(3)
    return s


def server_to_queue(s, queue, queue_lock):
    messages = 5
    while messages:
        msg, addr = s.recvfrom(2048)
        queue_lock.acquire()
        queue.append(msg)
        queue_lock.release()
        messages -= 1
    print("shutting down")


def queue_to_client(queue, queue_lock):
    messages = 100
    while messages:
        time.sleep(.1)
        queue_lock.acquire()
        if queue:
            print(queue.pop())
        queue_lock.release()
        messages -= 1


def test_locking():
    s = setup_server()
    queue = []
    queue_lock = threading.Lock()
    t1 = threading.Thread(target=server_to_queue, args=(s, queue, queue_lock))
    t2 = threading.Thread(target=queue_to_client, args=(queue, queue_lock))
    t3 = threading.Thread(target=server_to_queue, args=(s, queue, queue_lock))
    t4 = threading.Thread(target=server_to_queue, args=(s, queue, queue_lock))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    for _ in range(15):
        threading.Thread(target=single_client).start()


def server_to_file(s):
    with open("text.txt", 'w') as file:
        while True:
            msg, addr = s.recvfrom(2048)
            file.write(str(msg))
            file.write(' - ')
            file.write(str(addr))
            file.write('\n')


if __name__ == "__main__":
    args = setup_args()
    s = setup_server(args.server_port)
    server_to_file(s)
    # threading.Thread(target=server_to_file, args=(s,)).start()
