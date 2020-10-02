from shared import *
import socket
from threading import Thread, Event
from time import sleep


def wait_for_result(s, args, connection_event, inbox):
    msg = None
    while not msg:
        try:
            msg = s.recv(516)
        except ConnectionResetError:
            continue

    connection_event.set()
    # print("received " + str(msg[:5]))
    inbox.append(msg)
    return


def spam_rrq(s, args, connection_event, msg):
    while not connection_event.is_set():
        # print("sending " + str(msg))
        s.sendto(msg, (args.ip, args.server_port))
        sleep(1)


def send(s, args, msg, inbox):
    connection_event = Event()

    t1 = Thread(target=wait_for_result, args=(s, args, connection_event, inbox))
    t2 = Thread(target=spam_rrq, args=(s, args, connection_event, msg))

    t1.start()
    t2.start()

    t1.join(10)

    if not connection_event.is_set():
        # raise ConnectionError("Took longer than 20 seconds")
        print("Connection took longer than 10 seconds")
        return True


def send_only_once(s, args, msg):
    s.sendto(msg, (args.ip, args.server_port))


if __name__ == '__main__':
    args = setup_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', args.port))
    inbox = []
    msg = b'\x00\x01' + args.filename.encode() + b'\x00netascii\x00'
    send(s, args, msg, inbox)
