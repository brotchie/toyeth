import enum
import collections
from typing import Dict, DefaultDict, List, Callable
import int256


# Machine State: (g, pc, m, i, s)
#  g - Gas available,
#  pc - Program counter (256 bit)
#  m - memory contents -> series of zeros with size 2**256
#  i - active number of memory contents (counting from index 0)
#  s - stack

BASE256 = 2**256

class MachineState:
    code: bytes
    gas: int = 0
    pc: int = 0
    m: DefaultDict[int, int] = collections.defaultdict(int)
    i: int = 0
    s: List[int256.Int256] = []

    def read_mem_256(self, offset: int) -> int256.Int256:
        return int256.Int256(bytes(self.m[offset + x] for x in range(32)))

    def write_mem_256(self, offset: int, value: int256.Int256) -> None:
        for x, d in enumerate(bytes(value)):
            self.m[offset + x] = d

    def write_mem_8(self, offset: int, value: int256.Int256) -> None:
        self.m[offset] = bytes(value)[31]


class HaltExecution(Exception):
    pass

class InvalidJumpDestination(Exception):
    pass

class Mnemonic(enum.IntEnum):
    STOP = 0x00
    ADD = 0x01
    MUL = 0x02
    SUB = 0x03
    DIV = 0x04
    SDIV = 0x05
    MOD = 0x06
    SMOD = 0x07
    ADDMOD = 0x08
    MULMOD = 0x09
    EXP = 0x0a
    SIGNEXTEND = 0x0b

    LT = 0x10
    GT = 0x11
    SLT = 0x12
    SGT = 0x13
    EQ = 0x14
    ISZERO = 0x15
    AND = 0x16
    OR = 0x17
    XOR = 0x18
    NOT = 0x19
    BYTE = 0x1a
    SHL = 0x1b
    SHR = 0x1c
    SAR = 0x1d

    PUSH1 = 0x60
    PUSH2 = 0x61
    PUSH3 = 0x62
    PUSH4 = 0x63
    PUSH5 = 0x64
    PUSH6 = 0x65
    PUSH7 = 0x66
    PUSH8 = 0x67
    PUSH9 = 0x68
    PUSH10 = 0x69
    PUSH11 = 0x6a
    PUSH12 = 0x6b
    PUSH13 = 0x6c
    PUSH14 = 0x6d
    PUSH15 = 0x6e
    PUSH16 = 0x6f
    PUSH17 = 0x70
    PUSH18 = 0x71
    PUSH19 = 0x72
    PUSH20 = 0x73
    PUSH21 = 0x74
    PUSH22 = 0x75
    PUSH23 = 0x76
    PUSH24 = 0x77
    PUSH25 = 0x78
    PUSH26 = 0x79
    PUSH27 = 0x7a
    PUSH28 = 0x7b
    PUSH29 = 0x7c
    PUSH30 = 0x7d
    PUSH31 = 0x7e
    PUSH32 = 0x7f

    DUP1 = 0x80
    DUP2 = 0x81
    DUP3 = 0x82
    DUP4 = 0x83
    DUP5 = 0x84
    DUP6 = 0x85
    DUP7 = 0x86
    DUP8 = 0x87
    DUP9 = 0x88
    DUP10 = 0x89
    DUP11 = 0x8a
    DUP12 = 0x8b
    DUP13 = 0x8c
    DUP14 = 0x8d
    DUP15 = 0x8e
    DUP16 = 0x8f

    SWAP1 = 0x90
    SWAP2 = 0x91
    SWAP3 = 0x92
    SWAP4 = 0x93
    SWAP5 = 0x94
    SWAP6 = 0x95
    SWAP7 = 0x96
    SWAP8 = 0x97
    SWAP9 = 0x98
    SWAP10 = 0x99
    SWAP11 = 0x9a
    SWAP12 = 0x9b
    SWAP13 = 0x9c
    SWAP14 = 0x9d
    SWAP15 = 0x9e
    SWAP16 = 0x9f

    POP = 0x50
    MLOAD = 0x51
    MSTORE = 0x52
    MSTORE8 = 0x53
    JUMP = 0x56
    JUMPI = 0x57
    PC = 0x58
    MSIZE = 0x59
    GAS = 0x5a
    JUMPDEST = 0x5b


_INSTRUCTION_MAP: Dict[Mnemonic, Callable[[MachineState], None]] = {}

def instruction(m: Mnemonic):
    def wrapper(fn: Callable[[MachineState], None]):
        _INSTRUCTION_MAP[m] = fn
        return fn
    return wrapper

@instruction(Mnemonic.STOP)
def stop(state: MachineState) -> None:
    raise HaltExecution()

@instruction(Mnemonic.ADD)
def add(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.add(b))
    state.pc += 1

@instruction(Mnemonic.MUL)
def mul(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.mul(b))
    state.pc += 1

@instruction(Mnemonic.DIV)
def div(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.div(b))
    state.pc += 1

@instruction(Mnemonic.SDIV)
def sdiv(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.sdiv(b))
    state.pc += 1

@instruction(Mnemonic.MOD)
def mod(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.mod(b))
    state.pc += 1

@instruction(Mnemonic.SMOD)
def smod(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.smod(b))
    state.pc += 1

@instruction(Mnemonic.ADDMOD)
def addmod(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    c = state.s.pop()
    state.s.append(a.addmod(b, c))
    state.pc += 1

@instruction(Mnemonic.MULMOD)
def mulmod(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    c = state.s.pop()
    state.s.append(a.mulmod(b, c))
    state.pc += 1

@instruction(Mnemonic.EXP)
def exp(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.exp(b))
    state.pc += 1

@instruction(Mnemonic.SIGNEXTEND)
def signextend(state: MachineState) -> None:
    size = state.s.pop()
    target = state.s.pop()
    state.s.append(target.signextend(size))
    state.pc += 1

# Comparison and bitwise
@instruction(Mnemonic.LT)
def lt(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.lt(b))
    state.pc += 1

@instruction(Mnemonic.GT)
def gt(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.gt(b))
    state.pc += 1

@instruction(Mnemonic.SLT)
def slt(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.slt(b))
    state.pc += 1

@instruction(Mnemonic.SGT)
def sgt(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.sgt(b))
    state.pc += 1

@instruction(Mnemonic.EQ)
def eq(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.eq(b))
    state.pc += 1

@instruction(Mnemonic.ISZERO)
def iszero(state: MachineState) -> None:
    a = state.s.pop()
    state.s.append(a.iszero())
    state.pc += 1

@instruction(Mnemonic.AND)
def and_(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.and_(b))
    state.pc += 1

@instruction(Mnemonic.OR)
def or_(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.or_(b))
    state.pc += 1

@instruction(Mnemonic.XOR)
def xor(state: MachineState) -> None:
    a = state.s.pop()
    b = state.s.pop()
    state.s.append(a.xor(b))
    state.pc += 1

@instruction(Mnemonic.NOT)
def not_(state: MachineState) -> None:
    a = state.s.pop()
    state.s.append(a.not_())
    state.pc += 1

@instruction(Mnemonic.BYTE)
def byte(state: MachineState) -> None:
    index = state.s.pop().unsigned
    value = state.s.pop()
    state.s.append(value.byte(index))
    state.pc += 1

@instruction(Mnemonic.SHL)
def shl(state: MachineState) -> None:
    shift = state.s.pop()
    value = state.s.pop()
    state.s.append(value.shl(shift))
    state.pc += 1

@instruction(Mnemonic.SHR)
def shl(state: MachineState) -> None:
    shift = state.s.pop()
    value = state.s.pop()
    state.s.append(value.shr(shift))
    state.pc += 1

@instruction(Mnemonic.SAR)
def shl(state: MachineState) -> None:
    shift = state.s.pop()
    value = state.s.pop()
    state.s.append(value.sar(shift))
    state.pc += 1

@instruction(Mnemonic.POP)
def pop(state: MachineState) -> None:
    state.s.pop()
    state.pc += 1

@instruction(Mnemonic.MLOAD)
def mload(state: MachineState) -> None:
    offset = state.s[-1].unsigned
    state.s[-1] = state.read_mem_256(offset)
    state.i = max(state.i, (offset + 32) // 32)
    state.pc += 1

@instruction(Mnemonic.MSTORE)
def mstore(state: MachineState) -> None:
    offset = state.s.pop().unsigned
    value = state.s.pop()
    state.write_mem_256(offset, value)
    state.i = max(state.i, (offset + 32) // 32)
    state.pc += 1

@instruction(Mnemonic.MSTORE8)
def mstore8(state: MachineState) -> None:
    offset = state.s.pop().unsigned
    value = state.s.pop()
    state.write_mem_8(offset, value)
    state.i = max(state.i, (offset + 1) // 32)
    state.pc += 1

@instruction(Mnemonic.JUMP)
def jump(state: MachineState) -> None:
    dest = state.s.pop().unsigned
    if state.code[dest] != Mnemonic.JUMPDEST:
        raise InvalidJumpDestination()
    state.pc = dest

@instruction(Mnemonic.JUMPI)
def jumpi(state: MachineState) -> None:
    dest = state.s.pop().unsigned
    if state.code[dest] != Mnemonic.JUMPDEST:
        raise InvalidJumpDestination()
    cond = state.s.pop()
    if cond != 0:
        state.pc = dest
    else:
        state.pc += 1

@instruction(Mnemonic.PC)
def pc(state: MachineState) -> None:
    state.s.append(int256.from_int(state.pc))
    state.pc += 1

@instruction(Mnemonic.MSIZE)
def msize(state: MachineState) -> None:
    state.s.append(int256.from_int(state.i * 32))
    state.pc += 1

@instruction(Mnemonic.GAS)
def msize(state: MachineState) -> None:
    state.s.append(int256.from_int(state.gas))
    state.pc += 1

@instruction(Mnemonic.JUMPDEST)
def jumpdest(state: MachineState) -> None:
    state.pc += 1

def push_n(n: int) -> Callable[[MachineState], None]:
    def push(state: MachineState) -> None:
        data = (32-n) * b"\x00" + state.code[state.pc + 1:state.pc + 1 + n]
        state.s.append(int256.Int256(data))
        state.pc += 1 + n
    return push

for ii in range(32):
    instruction(0x60 + ii)(push_n(ii + 1))

def dup_n(n: int) -> Callable[[MachineState], None]:
    def dup(state: MachineState) -> None:
        state.s.append(state.s[-n])
        state.pc += 1
    return dup

for ii in range(16):
    instruction(0x80 + ii)(dup_n(ii + 1))

def swap_n(n: int) -> Callable[[MachineState], None]:
    def swap(state: MachineState) -> None:
        x = state.s[-1]
        state.s[-1] = state.s[-(n+1)]
        state.s[-(n+1)] = x
        state.pc += 1
    return swap

for ii in range(16):
    instruction(0x90 + ii)(swap_n(ii + 1))

def compile(asm: str) -> bytes:
    lines = [tuple(line.strip().split(" ")) for line in asm.split("\n")]

    program = []

    for line in lines:
        if not line[0]:
            continue

        if line[0] == "PUSH":
            value = eval(line[1])
            if value == 0:
                encoded_value = b"\x00"
            else:
                encoded_value = value.to_bytes((value.bit_length() + 7) // 8, "big", signed=False)
            program.append(bytes([0x60 + len(encoded_value) - 1]) + encoded_value)
        else:
            m = int(Mnemonic[line[0]])
            program.append(bytes([m]))


    return b"".join(program)

def execute(state: MachineState, m: Mnemonic) -> None:
    _INSTRUCTION_MAP[m](state)

def main():
    state = MachineState()
    state.code = b"\x60\x01\x60\x07\x57\x60\x00\x5b"
    
    state.code = compile("""
        PUSH 0xff
        PUSH 31
        BYTE
    """)

    while state.pc < len(state.code):
        print(f"PC: {state.pc}")
        m = state.code[state.pc]
        execute(state, m)
        print(state.s)

    print(state.m)

if __name__ == "__main__":
    main()
