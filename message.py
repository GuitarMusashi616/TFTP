# Austin Williams
# Shawn Butler
# Computer Networks
# 2 October 2020

# message.py
# module to create Message objects used to send to server

from shared import *


class Message:
    """
    Abstract class for all message instances
    """
    def __init__(self, opcode: int):
        assert 1 <= opcode <= 5, 'opcode must be between 1-5'
        self.opcode = opcode

    def __bytes__(self):
        raise NotImplementedError


class ReadRequest(Message):
    """
    Used to quickly construct a read request
    """
    def __init__(self, filename: str, mode: str = 'netascii'):
        super().__init__(1)
        self.filename = filename
        self.mode = mode

    def __bytes__(self):
        return short_to_bytes(self.opcode) + self.filename.encode() + NULL + self.mode.encode() + NULL


class WriteRequest(Message):
    """
    Used to quickly construct a write request
    """
    def __init__(self, filename: str, mode: str = 'netascii'):
        super().__init__(2)
        self.filename = filename
        self.mode = mode

    def __bytes__(self):
        return short_to_bytes(self.opcode) + self.filename.encode() + NULL + self.mode.encode() + NULL


class DataMessage(Message):
    """
    Used to quickly construct a data message
    """
    def __init__(self, block_num: int, content: bytes):
        super().__init__(3)
        self.block_num = block_num
        self.content = content

    def __bytes__(self):
        return short_to_bytes(self.opcode) + short_to_bytes(self.block_num) + self.content


class AckMessage(Message):
    """
    Used to quickly construct an ack message
    """
    def __init__(self, block_num: int):
        super().__init__(4)
        self.block_num = block_num

    def __bytes__(self):
        return short_to_bytes(self.opcode) + short_to_bytes(self.block_num)


class ErrorMessage(Message):
    """
    Used to quickly construct an error request
    """
    def __init__(self, error_code: int, error_msg: str):
        super().__init__(5)
        self.error_code = error_code
        self.error_msg = error_msg

    def __bytes__(self):
        return short_to_bytes(self.opcode) + short_to_bytes(self.error_code) + self.error_msg.encode() + NULL