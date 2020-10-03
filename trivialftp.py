# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

import socket
from shared import *
import os
from multithreaded import send, send_only_once


def download(s: socket.socket, args: argparse.Namespace) -> None:
    """Initiates a read request, records incoming data and responds with acks until file is constructed

    :param s: the UDP socket connected to the server
    :param args: the argparser object with the ip, ports, and filename fields
    """
    inbox = []

    # make / send read request
    rrq_msg = RRQ + args.filename.encode() + NULL + 'netascii'.encode() + NULL
    send(s, args, rrq_msg, inbox)

    # setup file to write to
    while os.path.exists(args.filename):
        # todo: support no file extension files
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

            # if data length less than 512 bytes then stop otherwise loop
            ack_msg = ACK + received[2:4]

            if len(received) < 516:
                print("sending only once")
                send_only_once(s, args, ack_msg)
                break

            # send ack
            if send(s, args, ack_msg, inbox):
                break  # increment block_num

            block_num = (block_num + 1) % 65536
        elif received and received[0:2] == ERROR:
            raise Error()
        else:
            ack_msg = ACK + received[2:4]
            if send(s, args, ack_msg, inbox):
                break
    f.close()


def upload(s: socket.socket, args: argparse.Namespace) -> None:
    """Initiates a write request, transmits data while acks are received until file is fully transferred

    :param s: the UDP socket connected to the server
    :param args: the argparser object with the ip, ports, and filename fields
    """
    inbox = []

    # find file from args.filename
    file = None
    try:
        # check if args.filename exists
        file = open(args.filename, 'rb')
    except FileNotFoundError:
        print("file not found, try again")

    # make / send write request
    wrq_msg = WRQ + args.filename.encode() + NULL + 'netascii'.encode() + NULL
    send(s, args, wrq_msg, inbox)

    # wait for acks while sending data
    block_num = 0
    data_bytes = file.read(512)
    msg = None
    data_msg = None
    while True:
        if inbox:
            msg = inbox.pop(0)

        if msg and msg[0:2] == ACK and bytes_to_short(msg[2], msg[3]) == block_num:
            block_num = (block_num + 1) % 65536
            data_msg = DATA + short_to_bytes(block_num) + data_bytes
            if len(data_bytes) < 512:
                send_only_once(s, args, data_msg)
                break
            if send(s, args, data_msg, inbox):
                break
            data_bytes = file.read(512)
        elif msg and msg[0:2] == ERROR:
            raise Error()
        else:
            print('resend')
            if not data_msg:
                print("aint gonna work")
            if send(s, args, data_msg, inbox):
                break


if __name__ == '__main__':
    args = setup_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', args.port))

    if args.mode == 'r':
        download(s, args)
    elif args.mode == 'w':
        upload(s, args)
    s.close()

# python3 /home/A365/tftp/tester.py -f trivialftp.py
