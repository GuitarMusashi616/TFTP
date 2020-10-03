# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

# trivialftp.py
# main program used to download and upload files to a tftp server

import socket
from shared import *
from message import *
import os
from multithreaded import send, send_only_once


def is_legit(msg: bytes) -> bool:
    """Returns True if msg is legitimate (no wrong opcode etc)

    :param msg: The bytes that are sent from the server
    """
    try:
        assert msg[0] == 0 and 1 <= msg[1] <= 5, 'opcode must be between 1-5'

        if msg[0:2] == RRQ or msg[0:2] == WRQ:
            assert list(msg[2:]).count(0) == 2
            assert msg[-10:0] == b'\x00netascii\x00'

        if msg[0:2] == DATA:
            assert len(msg) <= 516

        if msg[0:2] == ACK:
            assert len(msg) == 4

        if msg[0:2] == ERROR:
            assert msg[2] == 0 and 0 <= msg[3] <= 7
            assert list(msg[4:]).count(0) == 1

    except AssertionError:
        return False
    return True


def read_error(error_msg: bytes):
    """Used to print the received server error message

    :param error_msg: bytes sent from the server whose opcode is 5
    """
    if is_legit(error_msg):
        if error_msg[2:4] == Error.NOT_DEFINED:
            print("Server Error: Undefined")
        elif error_msg[2:4] == Error.FILE_NOT_FOUND:
            print("Server Error: File Not Found")
        elif error_msg[2:4] == Error.ACCESS_VIOLATION:
            print("Server Error: Access Violation")
        elif error_msg[2:4] == Error.DISK_FULL:
            print("Server Error: Disk Full")
        elif error_msg[2:4] == Error.ILLEGAL_OPERATION:
            print("Server Error: Illegal Operation")
        elif error_msg[2:4] == Error.UNKNOWN_TID:
            print("Server Error: Unknown Transfer ID")
        elif error_msg[2:4] == Error.FILE_EXISTS:
            print("Server Error: File Exists")
        elif error_msg[2:4] == Error.NO_SUCH_USER:
            print("Server Error: No Such User")
        string = extract_null_terminated_string(error_msg, 4)
        if string:
            print("Error Message: ", end='')
            print(string)
    else:
        print("Unreadable Server Error")


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
            read_error(received)
            raise Error()

        else:
            # resend last ack
            ack_msg = AckMessage(bytes_to_short(received[2], received[3]))
            if send(s, args, bytes(ack_msg), inbox):
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

        # if msg is ack then send next data packet
        if msg and msg[0:2] == ACK and bytes_to_short(msg[2], msg[3]) == block_num:
            block_num = (block_num + 1) % 65536
            data_msg = DataMessage(block_num, data_bytes)

            if len(data_bytes) < 512:
                send_only_once(s, args, bytes(data_msg))
                break
            if send(s, args, bytes(data_msg), inbox):
                break
            data_bytes = file.read(512)

        # if msg is error then Error
        elif msg and msg[0:2] == ERROR:
            read_error(msg)
            raise Error()

        # otherwise resend last data msg
        else:
            if send(s, args, bytes(data_msg), inbox):
                break
    file.close()


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
