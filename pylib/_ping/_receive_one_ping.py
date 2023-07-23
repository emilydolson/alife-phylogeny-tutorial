# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4

import os
import platform
import select
import socket
import struct
import typing

import typing_extensions

from ._enums import *
from ._read_icmp_header import read_icmp_header
from ._symbolic_constants import *


def receive_one_ping(
    sock: socket,
) -> typing.Optional[typing_extensions.Buffer]:
    """Receives the ping from the socket.

    IP Header (bits): version (8), type of service (8), length (16), id (16), flags (16), time to live (8), protocol (8), checksum (16), source ip (32), destination ip (32).
    ICMP Packet (bytes): IP Header (20), ICMP Header (8), ICMP Payload (*).
    Ping Wikipedia: https://en.wikipedia.org/wiki/Ping_(networking_utility)
    ToS (Type of Service) in IP header for ICMP is 0. Protocol in IP header for ICMP is 1.

    Args:
        sock: The same socket used for send the ping.
        seq: ICMP packet sequence. Sent packet sequence should be identical with received packet sequence.
        timeout: Timeout in seconds.

    Returns:
        The delay in seconds or None on timeout.

    Raises:
        TimeToLiveExpired: If the Time-To-Live in IP Header is not large enough for destination.
        TimeExceeded: If time exceeded but Time-To-Live does not expired.
        DestinationHostUnreachable: If the destination host is unreachable.
        DestinationUnreachable: If the destination is unreachable.
    """
    has_ip_header = (
        (os.name != "posix")
        or (platform.system() == "Darwin")
        or (sock.type == socket.SOCK_RAW)
    )  # No IP Header when unprivileged on Linux.
    if has_ip_header:
        ip_header_slice = slice(0, struct.calcsize(IP_HEADER_FORMAT))  # [0:20]
        icmp_header_slice = slice(
            ip_header_slice.stop,
            ip_header_slice.stop + struct.calcsize(ICMP_HEADER_FORMAT),
        )  # [20:28]
    else:
        icmp_header_slice = slice(
            0, struct.calcsize(ICMP_HEADER_FORMAT)
        )  # [0:8]
    for __ in range(5):
        timeout = 0.1
        selected = select.select(
            [
                sock,
            ],
            [],
            [],
            timeout,
        )  # Wait until sock is ready to read or time is out.
        if selected[0] == []:  # Timeout
            return None
        # time_recv = time.time()
        # _debug("Received time: {} ({}))".format(time.ctime(time_recv), time_recv))
        recv_data, addr = sock.recvfrom(
            1500
        )  # Single packet size limit is 65535 bytes, but usually the network packet limit is 1500 bytes.
        icmp_header_raw, icmp_payload_raw = (
            recv_data[icmp_header_slice],
            recv_data[icmp_header_slice.stop :],
        )
        icmp_header = read_icmp_header(icmp_header_raw)
        if (
            not has_ip_header
        ):  # When unprivileged on Linux, ICMP ID is rewrited by kernel.
            icmp_id = sock.getsockname()[
                1
            ]  # According to https://stackoverflow.com/a/14023878/4528364
        if icmp_header["type"] == IcmpType.TIME_EXCEEDED:
            continue
        if icmp_header["type"] == IcmpType.DESTINATION_UNREACHABLE:
            continue
        if icmp_header["id"]:
            if (
                icmp_header["type"] == IcmpType.ECHO_REQUEST
            ):  # filters out the ECHO_REQUEST itself.
                continue
            if icmp_header["type"] == IcmpType.ECHO_REPLY:
                # time_sent = struct.unpack(ICMP_TIME_FORMAT, icmp_payload_raw[0:struct.calcsize(ICMP_TIME_FORMAT)])[0]
                # time_recv - time_sent
                return icmp_payload_raw[struct.calcsize(ICMP_TIME_FORMAT) :]

        return None
    return None
