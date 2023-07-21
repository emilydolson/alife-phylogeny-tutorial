# adapted from ping3
# https://github.com/kyan001/ping3/tree/v4.0.4


def checksum(source: bytes) -> int:
    """Calculates the checksum of the input bytes.

    RFC1071: https://tools.ietf.org/html/rfc1071
    RFC792: https://tools.ietf.org/html/rfc792

    Args:
        source: Bytes. The input to be calculated.

    Returns:
        int: Calculated checksum.
    """
    BITS = 16  # 16-bit long
    carry = 1 << BITS  # 0x10000
    result = sum(source[::2]) + (
        sum(source[1::2]) << (BITS // 2)
    )  # Even bytes (odd indexes) shift 1 byte to the left.
    while result >= carry:  # Ones' complement sum.
        result = sum(
            divmod(result, carry)
        )  # Each carry add to right most bit.
    return ~result & ((1 << BITS) - 1)  # Ensure 16-bit
