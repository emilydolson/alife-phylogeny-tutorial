# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4

IP_HEADER_FORMAT = "!BBHHHBBHII"
ICMP_HEADER_FORMAT = "!BBHHH"  # According to netinet/ip_icmp.h. !=network byte order(big-endian), B=unsigned char, H=unsigned short
ICMP_TIME_FORMAT = "!d"  # d=double
SOCKET_SO_BINDTODEVICE = 25  # socket.SO_BINDTODEVICE

__all__ = [
    "IP_HEADER_FORMAT",
    "ICMP_HEADER_FORMAT",
    "ICMP_TIME_FORMAT",
    "SOCKET_SO_BINDTODEVICE",
]
