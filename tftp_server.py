# Austin Williams
# Dr. Shawn Butler
# Computer Networks
# November 25, 2020

import socket
import threading
from connection_dict import ConnectionDict
from message import *
from config import *
from queue import Queue


def setup_server(server_port=54321):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', server_port))
    s.settimeout(TIMEOUT)
    return s


def put_msgs_in_queue(input_queue, sock):
    """
    Listens to incoming messages for socket
    Puts messages into the thread safe queue
    """
    is_open = True
    shutdown_msg = ReadRequest('shutdown.txt')
    while is_open:
        try:
            new_msg, new_addr = sock.recvfrom(MAX_PACKET_SIZE)
        except (ConnectionResetError, socket.timeout):
            print('No more new messages')
            break
        else:
            if new_msg == bytes(shutdown_msg):
                is_open = False
            input_queue.put((new_msg, new_addr))
            if VERBOSE:
                print("{} from {} added to input queue".format(new_msg[:10], new_addr))


def process_msgs(input_queue, conn_dict):
    """
    Takes messages from input queue,
    Passes message to Connection Dictionary which passes message to Connection
    Connection passes message to Connection State.
    Connection State puts response in output queue
    """
    while True:
        msg, addr = input_queue.get()
        conn_dict.handle(msg, addr)
        input_queue.task_done()
        if VERBOSE:
            print("{} from {} processed, reply sent to output queue".format(msg[:10], addr))


def send_whenever(output_queue, sock):
    """Thread that waits for messages then sends them once they enter the output queue"""
    while True:
        msg, addr = output_queue.get()
        sock.sendto(msg, addr)
        output_queue.task_done()
        if VERBOSE:
            print("{} to {} sent from output queue".format(msg[:10], addr))


def start_threaded_server(server_port):
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

    sock.close()


if __name__ == "__main__":
    args = setup_args()
    start_threaded_server(args.server_port)
