from shared import *


class Message:
    def __init__(self, opcode):
        assert 1 <= opcode <= 5, 'opcode must be between 1-5'
        self.opcode = opcode

    def __bytes__(self):
        raise NotImplementedError


class ReadRequest(Message):
    def __init__(self, filename, mode):
        super().__init__(1)
        self.filename = filename
        self.mode = mode

    def __bytes__(self):
        return short_to_bytes(self.opcode) + self.filename.encode() + NULL + self.mode.encode() + NULL


class WriteRequest(Message):
    def __init__(self, filename, mode):
        super().__init__(2)
        self.filename = filename
        self.mode = mode

    def __bytes__(self):
        return short_to_bytes(self.opcode) + self.filename.encode() + NULL + self.mode.encode() + NULL


class DataMessage(Message):
    def __init__(self, block_num, content):
        super().__init__(3)
        self.block_num = block_num
        self.content = content

    def __bytes__(self):
        return short_to_bytes(self.opcode) + short_to_bytes(self.block_num) + self.content


class AckMessage(Message):
    def __init__(self, block_num):
        super().__init__(4)
        self.block_num = block_num

    def __bytes__(self):
        return short_to_bytes(self.opcode) + short_to_bytes(self.block_num)


class ErrorMessage(Message):
    def __init__(self, error_code, error_msg):
        super().__init__(5)
        self.error_code = error_code
        self.error_msg = error_msg

    def __bytes__(self):
        return short_to_bytes(self.opcode) + short_to_bytes(self.error_code) + self.error_msg.encode() + NULL