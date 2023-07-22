# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4

import struct

from ._symbolic_constants import ICMP_HEADER_FORMAT


def read_icmp_header(raw: bytes) -> dict:
    """Get information from raw ICMP header data.

    Args:
        raw: Bytes. Raw data of ICMP header.

    Returns:
        A map contains the infos from the raw header.
    """
    icmp_header_keys = ("type", "code", "checksum", "id", "seq")
    return dict(zip(icmp_header_keys, struct.unpack(ICMP_HEADER_FORMAT, raw)))
