import struct
from com_protocol import COMMAND, ERRCODE, OPCODE, REGISTER, START_BYTES, FRAME_SIZE

def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return crc


def CRC_validate(frame: bytes) -> bool:
    if len(frame) != FRAME_SIZE:
        return False
    return struct.unpack("<H", frame[9:11])[0] == crc16(frame[2:9])


def pack(transact_id: int, opcode: int, register: int, data: int | float = 0) -> bytes:
    is_int = register in (REGISTER.COMMAND, REGISTER.STATUS)
    fmt = "<BBBI" if is_int else "<BBBf"
    val = int(data) if is_int else float(data)

    payload = struct.pack(fmt, transact_id, opcode, register, val)
    return START_BYTES + payload + struct.pack("<H", crc16(payload))


def unpack(frame: bytes) -> tuple:
    if len(frame) != FRAME_SIZE or frame[:2] != START_BYTES:
        raise ValueError("Invalid frame length or start bytes")
    if not CRC_validate(frame):
        raise ValueError("CRC mismatch")

    payload = frame[2:9]
    transact_id, raw_op, raw_reg = struct.unpack("<BBB", payload[:3])
    opcode = OPCODE(raw_op)
    register = REGISTER(raw_reg)

    if opcode == OPCODE.WRITE_NACK:
        data = ERRCODE(struct.unpack("<I", payload[3:7])[0])
    elif register == REGISTER.COMMAND:
        data = COMMAND(struct.unpack("<I", payload[3:7])[0])
    elif register == REGISTER.STATUS:
        data = struct.unpack("<I", payload[3:7])[0]
    else:
        data = struct.unpack("<f", payload[3:7])[0]

    return transact_id, opcode, register, data

if __name__=="__main__":
    pass
    # packet=pack(1, OPCODE.READ_REQ, REGISTER.FREQ, COMMAND.NOP)
    # print(packet.hex().upper())
    # print(CRC_validate(bytes.fromhex("AA5501A0B000FF7F479E68")))
    