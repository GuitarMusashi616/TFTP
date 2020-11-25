# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

import socket
from shared import *
from message import *


def wait_for_clients(port):
    # setup socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    print("server is ready to receive")

    # wait for msg
    msg, addr = s.recvfrom(2048)
    print(msg)

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

write_request_msgs = [
        b'\x00\x02text.txt\x00netascii\x00',
        b'\x00\x03\x00\x01from django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.mo',
        b'\x00\x03\x00\x02dels import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom d',
        b'\x00\x03\x00\x03jango.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, Licens',
        b'\x00\x03\x00\x04ingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Catego',
        b'\x00\x03\x00\x05ry, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, Ver',
        b'\x00\x03\x00\x06ificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\n\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntry\r\nv\r\nfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Indu',
        b'\x00\x03\x00\x07stry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Projec',
        b'\x00\x03\x00\x08t, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .mo',
        b'\x00\x03\x00\tdels import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import url',
        b'\x00\x03\x00\nencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.uti',
        b'\x00\x03\x00\x0bls.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r',
        b'\x00\x03\x00\x0c\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html i',
        b'\x00\x03\x00\rmport format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom d',
        b'\x00\x03\x00\x0ejango.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models imp',
        b'\x00\x03\x00\x0fort LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contrib.admin.models import LogEntryfrom django.utils.html import format_html\r\n\r\nfrom django.utils.http import urlencode\r\n\r\nfrom .models import Project, File, Tag, Industry, Client, Employee, VerificationLevel, Category, FileType, LicensingAgreement\r\n\r\nfrom django.contri',
        b'\x00\x03\x00\x10b.admin.models import LogEntry\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n',
    ]

read_request_msgs = [
        b'\x00\x01text.txt\x00netascii\x00',
        b'\x00\x04\x00\x01',
        b'\x00\x04\x00\x02',
        b'\x00\x04\x00\x03',
        b'\x00\x04\x00\x04',
        b'\x00\x04\x00\x05',
        b'\x00\x04\x00\x06',
        b'\x00\x04\x00\x07',
        b'\x00\x04\x00\x08',
        b'\x00\x04\x00\x09',
        b'\x00\x04\x00\x0a',
        b'\x00\x04\x00\x0b',
        b'\x00\x04\x00\x0c',
        b'\x00\x04\x00\x0d',
        b'\x00\x04\x00\x0e',
        b'\x00\x04\x00\x0f',
        b'\x00\x04\x00\x10',
    ]


def send_examples_for_test(msgs_to_send=write_request_msgs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 12345))
    s.settimeout(1000)

    while msgs_to_send:
        msg = msgs_to_send.pop(0)
        s.sendto(msg, ('127.0.0.1', 54321))
        new_msg, new_addr = s.recvfrom(516)
        print(new_msg, new_addr)
    s.close()


def send_examples_from_file(filename='example_client.txt'):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 12345))
        with open(filename, 'r') as file:
            for line in file.readlines():
                msg = bytes(line.strip())
                s.sendto(msg, ('127.0.0.1', 54321))


if __name__ == '__main__':
    # args = setup_args()
    # wait_for_clients(54321)
    send_examples_for_test(read_request_msgs)
