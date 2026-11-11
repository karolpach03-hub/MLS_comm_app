from com_protocol import OPCODE, REGISTER, START_BYTE, ERRCODE
import threading
from packet import Packet
from queue import Queue

class MLS_COM:
	def __init__(self, timeout=3.0):
		self.__mutex=threading.Lock()
		self.__timeout=timeout
		self.__rx_queue=Queue()

	def __transceiver(self, opcode:int, register:int, data:int|float=None)->Packet:
		with self.__mutex:
			rx_resp=Packet()
			tx_packet=Packet(opcode, register, data)
			self.__tx(tx_packet.pack())

			#wait here for response

			return rx_resp

	def __tx(self, data:bytes):
		pass

	def connect(self):
		#connection (including port etc) will be here
		pass

	def disconnect(self):
		pass

	def wake(self):
		pass

	def put_to_sleep(self):
		pass

	#---SETTERS---

	def __setter_resp_handler(resp:Packet):
		if resp.opcode==OPCODE.WRITE_ACK:
			return #successfull write
		
		if resp.opcode==OPCODE.WRITE_NACK:
			err_code=resp.data
			if err_code==ERRCODE.VAL_OUT_OF_RANGE:
				raise ValueError("Value out of range")
			elif err_code==ERRCODE.REG_READONLY:
				raise ValueError("Register readonly")
			elif err_code==ERRCODE.INVALID_CRC:
				raise ValueError("Invalid CRC")
			else:
				raise RuntimeError()
	
	def set_frequency(self, value:float=1.0)->None:
		'''Sets the frequency of the movement. Blocks until MLS ACKs the write. Raises exception on NACK.'''
		resp=self.__transceiver(OPCODE.WRITE_REQ, REGISTER.FREQ, data=value)
		self.__setter_resp_handler(resp)

	# def set_amplitude(self, value=1.0):
	# 	pass

	# def set_center(self, value=10.0):
	# 	pass

	# def set_upper_limit(self, value:float=None):
	# 	pass

	# def set_lower_limit(self, value:float=None):
	# 	pass

	'''GETTERS'''
	#...





if __name__=="__main__":
	# packet=Packet(opcode=OPCODE.WRITE, register=REGISTER.FREQ, data=0.7231)
	# print(packet.pack().hex().upper())
	MLS_COM.set_frequency
	pass