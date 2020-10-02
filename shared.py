import argparse
import re

RRQ = b'\x00\x01'
WRQ = b'\x00\x02'
DATA = b'\x00\x03'
ACK = b'\x00\x04'
ERROR = b'\x00\x05'
NULL = b'\x00'


class Error:
    NOT_DEFINED = b'\x00\x00'
    FILE_NOT_FOUND = b'\x00\x01'
    ACCESS_VIOLATION = b'\x00\x02'
    DISK_FULL = b'\x00\x03'
    ILLEGAL_OPERATION = b'\x00\x04'
    UNKNOWN_TID = b'\x00\x05'
    FILE_EXISTS = b'\x00\x06'
    NO_SUCH_USER = b'\x00\x07'


def setup_args():
    parser = argparse.ArgumentParser(description='send files reliably over UDP')

    parser.add_argument('-a', action='store', dest='ip',
                        help='specify ip address')

    parser.add_argument('-sp', action='store', dest='server_port', type=within_port_numbers,
                    help='specify server port number')

    parser.add_argument('-f', action='store', dest='filename',
                        help='specify name of file to download / upload')

    parser.add_argument('-p', action='store', dest='port', type=within_port_numbers,
                        help='specify port number')

    parser.add_argument('-m', action='store', dest='mode',
                        help='r = read from server, w = write to server')

    return parser.parse_args()


def within_port_numbers(string):
    value = None
    try:
        value = int(string)
    except ValueError:
        raise ValueError("port/server_port must be an integer")

    if value < 5000:
        raise ValueError("port/server_port must be a value higher than 5000")
    return value


def extract_filename(byte_msg, str_start=2):
    filename = ''
    for byte in byte_msg[str_start:]:
        if byte == 0:
            break
        filename += chr(byte)
    return filename


def short_to_bytes(short):
    assert 0 <= short <= 65535
    return bytes([short // 256, short % 256])


def bytes_to_short(msb, lsb):
    assert 0 <= lsb <= 255
    assert 0 <= msb <= 255
    return msb*256 + lsb


def increment_filename(filename):
    assert type(filename) == str
    strs = filename.split('.')
    if len(strs) != 2:
        raise ValueError('filename must have exactly 1 file extension')

    num = strs[0]

    lst = re.findall(r"\((\d+)\)", num)
    if lst:
        integer = int(lst[0])
        return re.sub(r"\((\d+)\)", '('+str(integer + 1)+')', num) + '.' + strs[1]
    else:
        return num + '(1).' + strs[1]
