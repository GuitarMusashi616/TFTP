# Austin Williams
# Dr. Shawn Butler
# Computer Networks
# November 25, 2020

import pytest
from message import *
from queue import Queue
from connection import *


@pytest.fixture
def client_upload():
    return [
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


@pytest.fixture
def client_download():
    return [
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


def test_packet_types():
    rrq = ReadRequest('text.txt')
    wrq = WriteRequest('text.txt')
    dm = DataMessage(1, b'Lorem Ipsum Dolor')
    ack = AckMessage(1)
    err = ErrorMessage(Error.FILE_NOT_FOUND, 'File not found')

    assert bytes(rrq) == b'\x00\x01text.txt\x00netascii\x00'
    assert bytes(wrq) == b'\x00\x02text.txt\x00netascii\x00'
    assert bytes(dm) == b'\x00\x03\x00\x01Lorem Ipsum Dolor'
    assert bytes(ack) == b'\x00\x04\x00\x01'
    assert bytes(err) == b'\x00\x05\x00\x01File not found\x00'


@pytest.mark.parametrize("filename", [b'text.txt', 12])
@pytest.mark.parametrize("block_num", [b'read.csv', 10000, 'string'])
@pytest.mark.parametrize("byte_str", ['', 12345, 'file'])
def test_packet_types_2(filename, block_num, byte_str):
    with pytest.raises(TypeError):
        rrq = ReadRequest(filename)
        wrq = WriteRequest(filename)
        dm = DataMessage(block_num, b'123')
        ack = AckMessage(block_num)
        err = ErrorMessage(Error.FILE_NOT_FOUND, filename)

    with pytest.raises(TypeError):
        dm = DataMessage(1, byte_str)
        err = ErrorMessage(byte_str, 'File not found')


def test_download_output(client_download):
    input_queue = Queue()
    output_queue = Queue()
    addr = ('127.0.0.1', 12345)
    for packet in client_download:
        input_queue.put((packet, addr))

    conn = Connection(output_queue)
    assert isinstance(conn.state, Open)

    conn.handle(*input_queue.get())
    assert isinstance(conn.state, Upload)

    while input_queue.queue:
        conn.handle(*input_queue.get())


def test_upload_output(client_upload):
    input_queue = Queue()
    output_queue = Queue()
    addr = ('127.0.0.1', 12345)
    for packet in client_upload:
        input_queue.put((packet, addr))

    conn = Connection(output_queue)
    assert isinstance(conn.state, Open)

    conn.handle(*input_queue.get())
    assert isinstance(conn.state, Closed)  # File exists, close connection








