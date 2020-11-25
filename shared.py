# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

# shared.py
# module that is utilized by both server and client

import argparse
import re

RRQ = b'\x00\x01'
WRQ = b'\x00\x02'
DATA = b'\x00\x03'
ACK = b'\x00\x04'
ERROR = b'\x00\x05'
NULL = b'\x00'


class Error:
    """
    Used to compare error codes in bytes
    """
    NOT_DEFINED = b'\x00\x00'
    FILE_NOT_FOUND = b'\x00\x01'
    ACCESS_VIOLATION = b'\x00\x02'
    DISK_FULL = b'\x00\x03'
    ILLEGAL_OPERATION = b'\x00\x04'
    UNKNOWN_TID = b'\x00\x05'
    FILE_EXISTS = b'\x00\x06'
    NO_SUCH_USER = b'\x00\x07'


def setup_args() -> argparse.Namespace:
    """
    Utilizes argparser to setup and return arguments
    """
    parser = argparse.ArgumentParser(description='send files reliably over UDP')

    parser.add_argument('-a', action='store', dest='ip',
                        help='specify ip address', required=False)

    parser.add_argument('-sp', action='store', dest='server_port', type=within_port_numbers,
                        help='specify server port number', required=False)

    parser.add_argument('-f', action='store', dest='filename',
                        help='specify name of file to download / upload', required=False)

    parser.add_argument('-p', action='store', dest='port', type=within_port_numbers,
                        help='specify port number', required=False)

    parser.add_argument('-m', action='store', dest='mode', required=False, choices=['r', 'w'],
                        help='r = read from server, w = write to server')

    parser.add_argument('-k', action='store', dest='random', required=False,
                        help='no idea')

    return parser.parse_args()


def within_port_numbers(string: str) -> int:
    """
    Used within argparser to filter out the port and server_port arguments

    :param string: The string representation of the port or server_port argument
    """
    value = None
    try:
        value = int(string)
    except ValueError:
        raise ValueError("port/server_port must be an integer")

    if value < 5000 or value > 65535:
        raise ValueError("port/server_port must be a value higher than 5000")
    return value


def extract_null_terminated_string(byte_msg: bytes, str_start: int = 2) -> str:
    """
    Extracts a null terminated string from bytes

    :param byte_msg: a bytes type with a bunch of ascii char bytes followed by a null byte
    :param str_start: which byte index to start searching on
    """
    string = ''
    for byte in byte_msg[str_start:]:
        if byte == 0:
            break
        string += chr(byte)
    return string


def short_to_bytes(short: int):
    """
    Takes a number between 0 and 65535 and returns a 2 byte representation

    :param short: integer between 0-65535
    """

    assert 0 <= short <= 65535
    return bytes([short // 256, short % 256])


def bytes_to_short(msb: bytes, lsb: bytes) -> int:
    """Takes 2 bytes and returns an integer between 0-65535

    :param msb: the most significant byte
    :param lsb: the least significant byte
    """

    assert 0 <= lsb <= 255
    assert 0 <= msb <= 255
    return msb*256 + lsb


def increment_filename(filename: str) -> str:
    """
    Appends a (n+1) to the end of an existing file ie text(1).txt

    :param filename: the name of the file
    """
    assert type(filename) == str
    strs = filename.split('.')
    ending = ''
    if len(strs) > 2:
        raise ValueError('filename can only have up to 1 file extension')

    if len(strs) == 2:
        ending = '.' + strs[1]

    num = strs[0]

    lst = re.findall(r"\((\d+)\)", num)
    if lst:
        integer = int(lst[0])
        return re.sub(r"\((\d+)\)", '(' + str(integer + 1) + ')', num) + ending
    else:
        return num + '(1)' + ending
