import pytest
import threading
import socket
import random
import time
import os
from queue import Queue
from shared import *
from message import *
from connection import *
from connection_dict import *
from concurrent.futures import ThreadPoolExecutor

TIMEOUT = 3
VERBOSE = False


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
    s.settimeout(TIMEOUT)
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
    with open("text.txt", 'a') as file:
        while True:
            msg, addr = s.recvfrom(2048)
            file.write(str(msg))
            file.write(' - ')
            file.write(str(addr))
            file.write('\n')


def main_server_to_file():
    args = setup_args()
    os.remove("text.txt")
    s = setup_server(args.server_port)
    server_to_file(s)


def test_connection_state():
    read_request, addr_1 = bytes()
    write_request, addr_2 = bytes()
    msg_1, addr_1 = bytes()
    msg_2, addr_2 = bytes()

    client_1 = Connection()
    client_2 = Connection()

    client_1.handle(msg_1, addr_1)  # processes msg and responds to the client, sends data and waits for acks
    client_2.handle(msg_2, addr_2)  # sends ack and waits for more data


def test_single_connection_with_server():
    args = setup_args()
    client_1 = Connection()

    with setup_server(args.server_port) as s:
        while True:
            msg, addr = s.recvfrom(2048)
            client_1.handle(msg, addr)


def test_init_state_transition():
    msg_1 = ReadRequest('text.txt', 'netascii')
    addr_1 = ('127.0.0.1', 12345)

    client_1 = Connection()
    client_1.handle(bytes(msg_1), addr_1)

    assert client_1.type == "Upload"
    assert isinstance(client_1.state, Upload)


def handle_msgs(input_queue, output_queue, client_dict, client_dict_lock):
    while input_queue.queue:
        msg, addr = input_queue.get()
        print(msg, addr)

        client_dict_lock.acquire()
        if addr not in client_dict:
            client_dict[addr] = [Connection(output_queue), threading.Lock()]
        connection, connection_lock = client_dict[addr]
        client_dict_lock.release()

        connection_lock.acquire()
        connection.handle(msg, addr)
        connection_lock.release()


def send_responses(output_queue, input_queue, sock):
    while output_queue.queue:
        msg, addr = output_queue.get()
        print(msg, addr)
        sock.sendto(msg, addr)

        new_msg, new_addr = sock.recvfrom(2048)
        input_queue.put((new_msg, addr))


def test_read_doing_stuff():
    sock = setup_server()

    addr_1 = ('127.0.0.1', 22345)
    addr_2 = ('127.0.0.1', 32345)
    addr_3 = ('127.0.0.1', 42345)

    output_queue = Queue()
    input_queue = Queue()
    input_queue.put((bytes(ReadRequest('text.txt')), addr_1))
    input_queue.put((bytes(WriteRequest('text.txt')), addr_2))
    input_queue.put((bytes(ReadRequest('text.txt')), addr_3))

    # spin up new thread whenever new client port is found
    client_dict = {}
    client_dict_lock = threading.Lock()

    handle_msgs(input_queue, output_queue, client_dict, client_dict_lock)
    send_responses(output_queue, input_queue, sock)
    print(input_queue.queue)


def test_threads():
    sock = setup_server()

    output_queue = Queue()
    input_queue = Queue()

    t_receive = threading.Thread(target=put_msgs_in_queue, args=(input_queue, sock), daemon=True)
    t_receive.start()

    # spin up new thread whenever new client port is found
    client_dict = {}
    client_dict_lock = threading.Lock()

    handle_msgs(input_queue, output_queue, client_dict, client_dict_lock)
    send_responses(output_queue, input_queue, sock)

    print(input_queue.queue)


def put_msgs_in_queue(input_queue, sock):
    while True:
        try:
            new_msg, new_addr = sock.recvfrom(516)
        except (ConnectionResetError, socket.timeout):
            print('No more new messages')
            break
        else:
            input_queue.put((new_msg, new_addr))
            # print(f"{new_msg[:10]} from {new_addr} added to input queue")
            if VERBOSE:
                print("{} from {} added to input queue".format(new_msg[:10], new_addr))


def move_from_input_to_output(input_queue, output_queue):
    while True:
        msg, addr = input_queue.get()
        output_queue.put((msg, addr))
        input_queue.task_done()
        if VERBOSE:
            print("{} from {} moved to output queue".format(msg[:10], addr))
        # print(f"{msg[:10]} from {addr} moved to output queue")


def process_msgs(input_queue, conn_dict):
    while True:
        msg, addr = input_queue.get()
        conn_dict.handle(msg, addr)
        input_queue.task_done()
        if VERBOSE:
            print("{} from {} processed, reply sent to output queue".format(msg[:10], addr))
        # print(f"{msg[:10]} from {addr} processed, reply sent to output queue")


def send_whenever(output_queue, sock):
    """Thread that waits for messages then sends them once they enter the output queue"""
    while True:
        msg, addr = output_queue.get()
        sock.sendto(msg, addr)
        output_queue.task_done()
        if VERBOSE:
            print("{} to {} sent from output queue".format(msg[:10], addr))


def test_input_and_output_sending(server_port):
    """Make thread that sends whenever a message is received"""
    sock = setup_server(server_port)

    output_queue = Queue()
    input_queue = Queue()

    conn_dict = ConnectionDict(output_queue)

    t_receive = threading.Thread(target=put_msgs_in_queue, args=(input_queue, sock), daemon=True)
    t_process = threading.Thread(target=process_msgs, args=(input_queue, conn_dict), daemon=True)
    t_send = threading.Thread(target=send_whenever, args=(output_queue, sock), daemon=True)

    t_receive.start()
    t_process.start()
    t_send.start()

    t_receive.join()
    t_process.join()
    t_send.join()


def test_duo_connection():
    """Two Connection instances talking to each other"""
    input_queue = Queue()
    output_queue = Queue()

    conn_1 = Connection(output_queue)
    conn_2 = Connection(input_queue)

    msg, addr = bytes(WriteRequest('text.txt')), ('127.0.0.1', 12345)
    input_queue.put((msg, addr))

    new_msg, new_addr = bytes(ReadRequest('text.txt')), ('127.0.0.1', 12345)
    conn_2.handle(new_msg, new_addr)

    while True:
        msg, addr = input_queue.get(timeout=3)
        print(msg[:10], addr)
        conn_1.handle(msg, addr)

        new_msg, new_addr = output_queue.get(timeout=3)
        print(new_msg[:10], new_addr)
        conn_2.handle(new_msg, new_addr)


if __name__ == "__main__":
    args = setup_args()
    # args.server_port = 54321
    test_input_and_output_sending(args.server_port)
