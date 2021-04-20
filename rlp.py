import struct
from typing import Union, List, Tuple, TypeVar


Item = Union[bytes, List["Item"]]


def encode(value: Item) -> bytes:
    if isinstance(value, bytes):
        if len(value) == 1 and value[0] < 0x80:
            return value
        elif len(value) <= 55:
            return bytes([0x80 + len(value)]) + value
        else:
            len_enc = _encode_int64(len(value))
            return bytes([0xb7 + len(len_enc)]) + len_enc + value
    elif isinstance(value, list):
        encoded_list = b"".join(encode(item) for item in value)
        if len(encoded_list) <= 55:
            return bytes([0xc0 + len(encoded_list)]) + encoded_list
        else:
            len_enc = _encode_int64(len(encoded_list))
            return bytes([0xf7 + len(len_enc)]) + len_enc + encoded_list
    else:
        raise ValueError(f"Unsupported type: {type(value)}")


def decode(data: bytes) -> Item:
    return _decode_item(data)[0]


def _decode_list(data: bytes) -> Item:
    result = []
    remainder = data
    while remainder:
        item, remainder = _decode_item(remainder)
        result.append(item)
    return result


def _decode_item(data: bytes) -> Tuple[Item, bytes]:
    if data[0] < 0xc0:
        if data[0] < 0x80:
            return (data[:1], data[1:])
        elif data[0] < 0xb7:
            length = data[0] - 0x80
            return (data[1:length+1], data[length+1:])
        else:
            enc_length = data[0] - 0xb7
            length = _decode_int64(data[1:enc_length+1])
            return (data[enc_length+1:enc_length+length+1], data[enc_length+length+1:])
    else:
        if data[0] < 0xf7:
            length = data[0] - 0xc0
            return (_decode_list(data[1:length+1]), data[length+1:])
        else:
            enc_length = data[0] - 0xf7
            length = _decode_int64(data[1:enc_length+1])
            return (_decode_list(data[enc_length+1:enc_length+length+1]), data[enc_length+length+1:])


def _encode_int64(value: int) -> bytes:
    """Encodes an int64 in big-endian stripping leading zeros."""
    return struct.pack(">Q", value).lstrip(b"\x00")


def _decode_int64(data: bytes) -> int:
    """Decodes an int64 from big-endian with stripped leading zeros."""
    return struct.unpack(">Q", (8 - len(data)) * b'\x00' + data)[0]


