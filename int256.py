class Int256:
    __slots__ = ("_bytes_value",)

    def __init__(self, bytes_value: bytes):
        if len(bytes_value) != 32:
            raise ValueError("bytes_value must be 256bit number.")
        self._bytes_value = bytes_value

    def __bytes__(self):
        return self._bytes_value

    def __repr__(self):
        return str(self.unsigned)

    @property
    def signed(self):
        return int.from_bytes(self._bytes_value, "big", signed=True)

    @property
    def unsigned(self):
        return int.from_bytes(self._bytes_value, "big", signed=False)

    def add(self, other: "Int256") -> "Int256":
        return from_int((self.unsigned + other.unsigned) % 2**256)

    def mul(self, other: "Int256") -> "Int256":
        return from_int((self.unsigned * other.unsigned) % 2**256)

    def sub(self, other: "Int256") -> "Int256":
        return from_int((self.unsigned - other.unsigned) % 2**256)

    def div(self, other: "Int256") -> "Int256":
        if other.unsigned == 0:
            return from_int(0)
        else:
            return from_int((self.unsigned // other.unsigned))

    def sdiv(self, other: "Int256") -> "Int256":
        if other.signed == 0:
            return from_int(0)
        elif self.signed == -2**255 and other.signed == -1:
            return from_signed_int(-2**255)
        else:
            return from_signed_int(sgn(self.signed / other.signed) * int(abs(self.signed / other.signed)))

    def mod(self, other: "Int256") -> "Int256":
        if other.unsigned == 0:
            return from_int(0)
        else:
            return from_int(self.unsigned % other.unsigned)

    def smod(self, other: "Int256") -> "Int256":
        if other.signed == 0:
            return from_int(0)
        else:
            return from_signed_int(sgn(self.signed) * (abs(self.signed) % abs(other.signed)))

    def addmod(self, other: "Int256", modulo: "Int256") -> "Int256":
        if modulo.signed == 0:
            return from_int(0)
        else:
            return from_int((self.unsigned + other.unsigned) % modulo.unsigned)

    def mulmod(self, other: "Int256", modulo: "Int256") -> "Int256":
        if modulo.signed == 0:
            return from_int(0)
        else:
            return from_int((self.unsigned * other.unsigned) % modulo.unsigned)

    def exp(self, exponent: "Int256") -> "Int256":
        return from_int((self.unsigned ** exponent.unsigned) % 2**256)

    def signextend(self, other: "Int256") -> "Int256":
        sign_bit = self._bytes_value[31 - other.unsigned] >> 7
        if sign_bit:
            return Int256(b"\xff" * (31 - other.unsigned) + self._bytes_value[(31 - other.unsigned):32])
        else:
            return Int256(b"\x00" * (31 - other.unsigned) + self._bytes_value[(31 - other.unsigned):32])

    def lt(self, other: "Int256") -> "Int256":
        if self.unsigned < other.unsigned:
            return from_int(1)
        else:
            return from_int(0)

    def gt(self, other: "Int256") -> "Int256":
        if self.unsigned > other.unsigned:
            return from_int(1)
        else:
            return from_int(0)

    def slt(self, other: "Int256") -> "Int256":
        if self.signed < other.signed:
            return from_int(1)
        else:
            return from_int(0)

    def sgt(self, other: "Int256") -> "Int256":
        if self.signed > other.signed:
            return from_int(1)
        else:
            return from_int(0)

    def eq(self, other: "Int256") -> "Int256":
        if self._bytes_value == other._bytes_value:
            return from_int(1)
        else:
            return from_int(0)

    def iszero(self) -> "Int256":
        if self.unsigned == 0:
            return from_int(1)
        else:
            return from_int(0)

    def and_(self, other: "Int256") -> "Int256":
        return from_int(self.unsigned & other.unsigned)

    def or_(self, other: "Int256") -> "Int256":
        return from_int(self.unsigned | other.unsigned)

    def xor(self, other: "Int256") -> "Int256":
        return from_int(self.unsigned ^ other.unsigned)

    def not_(self) -> "Int256":
        return from_signed_int(~self.unsigned)

    def byte(self, index: int) -> "Int256":
        # TODO(brotchie): Handle index >= 32.
        return from_int(self._bytes_value[index])

    def shl(self, shift: int) -> "Int256":
        return from_int((self.unsigned << shift.unsigned) % 2**256)

    def shr(self, shift: int) -> "Int256":
        return from_int(self.unsigned >> shift)

    def sar(self, shift: int) -> "Int256":
        return from_signed_int(self.signed >> shift)


def from_int(value: int) -> Int256:
    return Int256(value.to_bytes(32, "big", signed=False))

def from_signed_int(value: int) -> Int256:
    return Int256(value.to_bytes(32, "big", signed=True))

def sgn(x: int) -> int:
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return 1
