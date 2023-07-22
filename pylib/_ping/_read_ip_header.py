# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4

from ._symbolic_constants import IP_HEADER_FORMAT


def read_ip_header(raw: bytes) -> dict:
    """Get information from raw IP header data.

    Args:
        raw: Bytes. Raw data of IP header.

    Returns:
        A map contains the infos from the raw header.
    """

    def stringify_ip(ip: int) -> str:
        return ".".join(
            str(ip >> offset & 0xFF) for offset in (24, 16, 8, 0)
        )  # str(ipaddress.ip_address(ip))

    ip_header_keys = (
        "version",
        "tos",
        "len",
        "id",
        "flags",
        "ttl",
        "protocol",
        "checksum",
        "src_addr",
        "dest_addr",
    )
    ip_header = dict(zip(ip_header_keys, struct.unpack(IP_HEADER_FORMAT, raw)))
    ip_header["src_addr"] = stringify_ip(ip_header["src_addr"])
    ip_header["dest_addr"] = stringify_ip(ip_header["dest_addr"])
    return ip_header
