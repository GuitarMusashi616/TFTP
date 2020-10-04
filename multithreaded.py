# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

# multithreaded.py
# module used to send multiple messages while receiving messages at the same time


from shared import *
import socket
from threading import Thread, Event
from time import sleep


def wait_for_result(s: socket.socket, connection_event: Event, inbox: list):
    """used by the thread to listen for data sent by the server

    :param s: the UDP socket connected to the server
    :param connection_event: the thread event that signals when it is time to stop sending the same message to the server
    :param inbox: a list that is used to store incoming messages
    """
    msg = None
    addr = None
    while not msg:
        try:
            msg, addr = s.recvfrom(516)
        except ConnectionResetError:
            continue

    connection_event.set()
    # print("received " + str(msg[:5]))
    inbox.append((msg, addr))
    return


def spam_rrq(s: socket.socket, args: argparse.Namespace, connection_event: Event, msg: bytes):
    """Used by the thread to resend a message until the server provides a valid response

    :param s: the UDP socket connected to the server
    :param args: the argparser object with the ip, ports, and filename fields
    :param connection_event: the thread event that signals when it is time to stop sending the same message to the server
    :param msg: the message sent to the server

    """
    while not connection_event.is_set():
        # print("sending " + str(msg))
        s.sendto(msg, (args.ip, args.server_port))
        sleep(1)


def send(s: socket.socket, args: argparse.Namespace, msg: bytes, inbox: list) -> bool:
    """Opens up a thread to listen to the server and a thread to send a message over and over, returns True if a
    response is not received within 10 seconds

    :param s: the UDP socket connected to the server
    :param args: the argparser object with the ip, ports, and filename fields
    :param msg: the message sent to the server
    :param inbox: a list that is used to store incoming messages
    """
    connection_event = Event()

    t1 = Thread(target=wait_for_result, args=(s, connection_event, inbox))
    t2 = Thread(target=spam_rrq, args=(s, args, connection_event, msg))

    t1.start()
    t2.start()

    t1.join(10)

    if not connection_event.is_set():
        # raise ConnectionError("Took longer than 20 seconds")
        print("Connection took longer than 10 seconds")
        return True


def send_only_once(s: socket.socket, args: argparse.Namespace, msg: bytes):
    """Does not wait for response from server, used for sending the final message to the server"""
    s.sendto(msg, (args.ip, args.server_port))

