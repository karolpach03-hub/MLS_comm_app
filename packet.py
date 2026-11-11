import struct
from com_protocol import START_BYTE

class Packet:
	def __init__(self,opcode:int, register:int, data:int|float=0):
		self.opcode=opcode
		self.register=register
		if isinstance(data, float):
			self.data=int.from_bytes(struct.pack(">f", data), "big")
		else:
			self.data=data
	
	@staticmethod
	def __crc8(data:bytes)->int:
		crc=0x00
		for byte in data:
			crc^=byte
			for _ in range(8):
				crc=((crc<<1)^0x07)&0xFF if (crc&0x80) else (crc<<1)&0xFF
		return crc

	def pack(self)->bytes:
		payload=struct.pack(
			">BBBI",
			START_BYTE,
			self.opcode,
			self.register,
			self.data
		)
		return payload+bytes([self.__crc8(payload)])