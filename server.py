# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

import socket
from shared import *


def wait_for_clients(port):
    # setup socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    print("server is ready to receive")

    # wait for msg
    msg, addr = s.recvfrom(2048)

    # process if read request
    if msg[0:2] == RRQ:
        # input 01filename0, extract filename -> filename
        filename = extract_null_terminated_string(msg)
        print(filename)
        file = None
        try:
            # check if filename exists
            file = open(filename, 'rb')
        except FileNotFoundError:
            print("file not found")
            # create file not found error
            err_str = "filename does not correspond to a file saved on the server, try again"
            err_msg = ERROR + Error.FILE_NOT_FOUND + err_str.encode() + NULL
            s.sendto(err_msg, addr)
            return

        # if filename exists, gather up to 508 bytes and send them on over, increment block_num and continue as the
        # ACKs come in
        block_num = 1
        data_bytes = file.read(508)
        while data_bytes:
            block_num_bytes = short_to_bytes(block_num)
            data_msg = DATA + block_num_bytes + data_bytes
            s.sendto(data_msg, addr)
            # wait for sent data to be ACKnowledged
            msg, addr = s.recvfrom(2048)
            print(msg)
            if msg == ACK + block_num_bytes:
                block_num += 1
                data_bytes = file.read(508)
            else:
                continue

    # process if write request
    if msg[0:2] == WRQ:
        # todo: check if file already exists
        # make / send ack
        block_num = 0
        ack_msg = ACK + short_to_bytes(block_num)
        s.sendto(ack_msg, addr)
        # wait for more data
        while True:
            msg, addr = s.recvfrom(2048)
            # take the data and print it for now then keep responding with acks
            ack_msg = ACK + msg[2:4]
            s.sendto(ack_msg, addr)
            print(msg)
            if len(msg) < 512:
                break


if __name__ == '__main__':
    args = setup_args()
    wait_for_clients(args.server_port)
