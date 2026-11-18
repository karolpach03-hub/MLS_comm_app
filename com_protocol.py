from enum import IntEnum

START_BYTES:bytes	=b"\xaa\x55"
FRAME_SIZE:int		=11

class OPCODE (IntEnum):
	READ_REQ:int	=0xA0
	READ_RESP:int	=0xA1
	WRITE_REQ:int	=0xA2
	WRITE_ACK:int	=0xA3
	WRITE_NACK:int	=0xA4
	INVALID:int		=0x00
	NOP:int			=0xff

class REGISTER (IntEnum):
	COMMAND:int	=0xA0
	STATUS:int	=0xA1
	FREQ:int	=0xB0
	AMPL:int	=0xB1
	LLIM:int	=0xB2
	ULIM:int	=0xB3
	CENTER:int	=0xB4
	SCREW:int	=0xB5
	INVALID:int	=0x00
	NOP:int		=0xff

class COMMAND (IntEnum):
	ESTOP:int			=0xCAB0
	EESTOP:int			=0xCAB1
	START_OSC:int		=0xCAB2
	STOP_OSC:int		=0xCAB3
	PICK_UP:int			=0xCAB4
	PUT_DOWN:int		=0xCAB5
	START_PROCEDURE:int	=0xCAB6
	STOP_PROCEDURE:int	=0xCAB7
	RESET:int			=0xCAB8
	INVALID:int			=0x0000
	NOP:int				=0xffff

class ERRCODE (IntEnum):
	UNKNOWN:int				=0xCA00
	VAL_OUT_OF_RANGE:int	=0xCA01
	REG_READONLY:int		=0xCA02
	INVALID_CRC:int			=0xCA03
	INVALID:int				=0x0000
	NOP:int					=0xffff

