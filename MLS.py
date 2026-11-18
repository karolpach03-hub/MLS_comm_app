import threading
from serial import Serial as SM, SerialException
from serial.tools import list_ports
import packet
from com_protocol import COMMAND, OPCODE, REGISTER, START_BYTES


class DeviceError(Exception):
    pass


class MLS:
    def __init__(self, timeout: float = 0.5, baudrate: int = 115200):
        self.__timeout = timeout
        self.__baudrate = baudrate
        self.__serial: SM | None = None

        self.__tx_lock = threading.Lock()
        self.__pending_lock = threading.Lock()
        self.__pending: dict[int, dict] = {}
        self.__next_id = 1
        self.__running = False
        self.__rx_thread: threading.Thread | None = None

    @staticmethod
    def list_ports() -> list[str]:
        return [p.device for p in list_ports.comports()]

    @property
    def is_open(self) -> bool:
        return self.__serial is not None and self.__serial.is_open

    def open_port(self, port: str, baudrate: int | None = None):
        if self.is_open:
            self.close_port()

        if baudrate is not None:
            self.__baudrate = baudrate

        self.__serial = SM(port, baudrate=self.__baudrate, timeout=0.05)
        self.__serial.reset_input_buffer()
        self.__serial.reset_output_buffer()

        self.__running = True
        self.__rx_thread = threading.Thread(target=self.__rx_loop, daemon=True)
        self.__rx_thread.start()

    def close_port(self):
        self.__running = False
        if self.__serial is not None:
            try:
                self.__serial.cancel_read()
            except Exception:
                pass
        if self.__rx_thread is not None and self.__rx_thread.is_alive():
            self.__rx_thread.join(timeout=0.2)
        if self.__serial is not None and self.__serial.is_open:
            self.__serial.close()
        self.__serial = None
        self.__rx_thread = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close_port()

    def __alloc_id(self) -> int:
        tid = self.__next_id
        self.__next_id = 1 if self.__next_id >= 255 else self.__next_id + 1
        return tid

    def __rx_loop(self):
        buf = bytearray()
        while self.__running and self.__serial is not None:
            try:
                chunk = self.__serial.read(1)
                if chunk:
                    if self.__serial.in_waiting:
                        chunk += self.__serial.read(self.__serial.in_waiting)
                    buf.extend(chunk)
            except SerialException:
                break

            while len(buf) >= packet.FRAME_SIZE:
                idx = buf.find(START_BYTES)
                if idx == -1:
                    del buf[:-1]
                    break
                if idx > 0:
                    del buf[:idx]
                if len(buf) < packet.FRAME_SIZE:
                    break

                candidate = bytes(buf[:packet.FRAME_SIZE])
                try:
                    tid, opcode, register, data = packet.unpack(candidate)
                except ValueError:
                    del buf[:1]
                    continue

                del buf[:packet.FRAME_SIZE]
                with self.__pending_lock:
                    slot = self.__pending.get(tid)
                    if slot is not None:
                        slot["response"] = (opcode, register, data)
                        slot["event"].set()

    def __transact(self, opcode: OPCODE, register: REGISTER, data: int | float = 0):
        if not self.is_open:
            raise ConnectionError("Serial port is not open")

        with self.__pending_lock:
            tid = self.__alloc_id()
            slot = {"event": threading.Event(), "response": None}
            self.__pending[tid] = slot

        frame = packet.assemble(tid, opcode, register, data)
        try:
            with self.__tx_lock:
                self.__serial.write(frame)

            if not slot["event"].wait(self.__timeout):
                raise TimeoutError(f"No response for {register.name} (ID {tid})")

            resp_op, _, resp_data = slot["response"]
            if resp_op == OPCODE.WRITE_NACK:
                raise DeviceError(f"{register.name} rejected: {resp_data.name}")
            return resp_data
        finally:
            with self.__pending_lock:
                self.__pending.pop(tid, None)

    def __read_reg(self, register: REGISTER):
        return self.__transact(OPCODE.READ_REQ, register)

    def __write_reg(self, register: REGISTER, value: int | float):
        return self.__transact(OPCODE.WRITE_REQ, register, value)

    def __send_cmd(self, command: COMMAND):
        return self.__transact(OPCODE.WRITE_REQ, REGISTER.COMMAND, command)

    def set_frequency(self, freq: float) -> float:
        return self.__write_reg(REGISTER.FREQ, freq)

    def get_frequency(self) -> float:
        return self.__read_reg(REGISTER.FREQ)


if __name__ == "__main__":
    #print("Available ports:", MLS.list_ports())
    pass