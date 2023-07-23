# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4

import socket
import struct
import time

import typing_extensions

from ._checksum import checksum
from ._enums import *
from ._symbolic_constants import *


def send_one_ping(
    sock: socket,
    dest_addr: str,
    icmp_id: int,
    seq: int,
    payload: typing_extensions.Buffer,
) -> bool:
    """Sends one ping to the given destination.

    ICMP Header (bits): type (8), code (8), checksum (16), id (16), sequence (16)
    ICMP Payload: time (double), data
    ICMP Wikipedia: https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol

    Args:
        sock: Socket.
        dest_addr: The destination address, can be an IP address or a domain name. Ex. "192.168.1.1"/"example.com"
        icmp_id: ICMP packet id. Calculated from Process ID and Thread ID.
        seq: ICMP packet sequence, usually increases from 0 in the same process.
        size: The ICMP packet payload size in bytes. Note this is only for the payload part.

    Raises:
        HostUnkown: If destination address is a domain name and cannot resolved.
    """
    try:
        dest_addr = socket.gethostbyname(
            dest_addr
        )  # Domain name will translated into IP address, and IP address leaves unchanged.
    except socket.gaierror as err:
        # raise errors.HostUnknown(dest_addr=dest_addr) from err
        return False
    pseudo_checksum = (
        0  # Pseudo checksum is used to calculate the real checksum.
    )
    icmp_header = struct.pack(
        ICMP_HEADER_FORMAT,
        IcmpType.ECHO_REQUEST,
        ICMP_DEFAULT_CODE,
        pseudo_checksum,
        icmp_id,
        seq,
    )
    icmp_payload = struct.pack(ICMP_TIME_FORMAT, time.time()) + payload
    real_checksum = checksum(
        icmp_header + icmp_payload
    )  # Calculates the checksum on the dummy header and the icmp_payload.
    # Don't know why I need socket.htons() on real_checksum since ICMP_HEADER_FORMAT already in Network Bytes Order (big-endian)
    icmp_header = struct.pack(
        ICMP_HEADER_FORMAT,
        IcmpType.ECHO_REQUEST,
        ICMP_DEFAULT_CODE,
        socket.htons(real_checksum),
        icmp_id,
        seq,
    )  # Put real checksum into ICMP header.
    packet = icmp_header + icmp_payload
    sock.sendto(
        packet, (dest_addr, 0)
    )  # addr = (ip, port). Port is 0 respectively the OS default behavior will be used.
    return True
