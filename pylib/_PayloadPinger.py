# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4

import errno
import itertools as it
import random
import socket
import typing
import zlib

import typing_extensions

from ._ping import receive_one_ping, send_one_ping


class PayloadPinger:

    sock: socket.socket
    seq_counter: typing.Generator

    def __init__(self: "PayloadPinger") -> None:
        self.seq_counter = it.count()
        try:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
            )
        except PermissionError as err:
            if err.errno == errno.EPERM:  # [Errno 1] Operation not permitted
                self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP
                )
            else:
                raise err

    def __del__(self: "PayloadPinger") -> None:
        self.sock.close

    def send(
        self: "PayloadPinger",
        dest_addr: str,
        payload: typing_extensions.Buffer,
    ) -> float:
        """
        Dispatch one ping to destination address.

        Args:
            dest_addr: The destination address, can be an IP address or a domain name. Ex. "192.168.1.1"/"example.com"
            payload: The ICMP packet payload payload.

        Returns:
            The delay in seconds/milliseconds, False on error and None on timeout.

        Raises:
            PingError: Any PingError will raise again if `ping3.EXCEPTIONS` is True.
        """

        # with sock:
        icmp_id = (
            zlib.crc32(str(random.random()).encode()) & 0xFFFF
        )  # to avoid icmp_id collision.
        send_one_ping(
            sock=self.sock,
            dest_addr=dest_addr,
            icmp_id=icmp_id,
            seq=next(self.seq_counter),
            payload=payload,
        )

    def read(self: "PayloadPinger") -> typing_extensions.Buffer:
        return receive_one_ping(sock=self.sock)
