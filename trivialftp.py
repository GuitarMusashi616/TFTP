# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

import socket
from shared import *
from message import *
import os
from multithreaded import send, send_only_once


def download(s: socket.socket, args: argparse.Namespace) -> None:
    """Initiates a read request, records incoming data and responds with acks until file is constructed

    :param s: the UDP socket connected to the server
    :param args: the argparser object with the ip, ports, and filename fields
    """
    # setup incoming messages
    inbox = []

    # make / send read request
    rrq_msg = ReadRequest(args.filename, 'netascii')
    send(s, args, bytes(rrq_msg), inbox)

    # setup file to write to
    while os.path.exists(args.filename):
        args.filename = increment_filename(args.filename)

    f = open(args.filename, "wb")

    block_num = 1
    received = None
    while True:
        # wait for response, try 3 times, if timeout try again
        if inbox:
            received = inbox.pop(0)

        # query response, if data and block_num==1++ then ack, continue acking until data < 512
        if received and received[0:2] == DATA and bytes_to_short(received[2], received[3]) == block_num:
            # save contents
            f.write(received[4:])

            ack_msg = AckMessage(bytes_to_short(received[2], received[3]))

            # if data length less than 512 bytes then stop otherwise loop
            if len(received) < 516:
                print("sending only once")
                send_only_once(s, args, bytes(ack_msg))
                break

            # send ack
            if send(s, args, bytes(ack_msg), inbox):
                break

            # increment block_num
            block_num = (block_num + 1) % 65536

        elif received and received[0:2] == ERROR:
            # handle errors
            raise Error()

        else:
            # resend last ack
            ack_msg = AckMessage(bytes_to_short(received[2], received[3]))
            if send(s, args, ack_msg, inbox):
                break
    f.close()


def upload(s: socket.socket, args: argparse.Namespace) -> None:
    """Initiates a write request, transmits data while acks are received until file is fully transferred

    :param s: the UDP socket connected to the server
    :param args: the argparser object with the ip, ports, and filename fields
    """
    # setup incoming messages
    inbox = []

    # find file from args.filename
    file = None
    try:
        file = open(args.filename, 'rb')
    except FileNotFoundError:
        print("file not found, try again")

    # make / send write request
    wrq_msg = WriteRequest(args.filename, 'netascii')
    send(s, args, bytes(wrq_msg), inbox)

    # wait for acks while sending data
    block_num = 0
    data_bytes = file.read(512)
    msg = None
    data_msg = None
    while True:
        # pop latest message
        if inbox:
            msg = inbox.pop(0)

        # if message is ACK
        if msg and msg[0:2] == ACK and bytes_to_short(msg[2], msg[3]) == block_num:
            block_num = (block_num + 1) % 65536
            data_msg = DataMessage(block_num, data_bytes)

            if len(data_bytes) < 512:
                send_only_once(s, args, bytes(data_msg))
                break
            if send(s, args, bytes(data_msg), inbox):
                break
            data_bytes = file.read(512)

        # else if msg is ERROR
        elif msg and msg[0:2] == ERROR:
            raise Error()

        # otherwise resend last data msg
        else:
            if send(s, args, bytes(data_msg), inbox):
                break


if __name__ == '__main__':
    # setup the args and the socket
    args = setup_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', args.port))

    # if r then read request, if w then write request
    if args.mode == 'r':
        download(s, args)
    elif args.mode == 'w':
        upload(s, args)
    s.close()

# python3 /home/A365/tftp/tester.py -f trivialftp.py
