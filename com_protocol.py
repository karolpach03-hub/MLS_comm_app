from dataclasses import dataclass

START_BYTE:int	=0xA5

@dataclass(frozen=True)
class OPCODE:
	READ_REQ:int	=0x00
	READ_RESP:int	=0x01
	WRITE_REQ:int	=0x02
	WRITE_ACK:int	=0x03
	WRITE_NACK:int	=0x04
	NOP:int			=0xff

@dataclass(frozen=True)
class REGISTER:
	COMMAND:int	=0x00
	STATUS:int	=0x01
	FREQ:int	=0x10
	AMPL:int	=0x11
	LLIM:int	=0x12
	ULIM:int	=0x13
	CENTER:int	=0x14
	SCREW:int	=0x15
	NOP:int		=0xff

@dataclass(frozen=True)
class COMMAND:
	ESTOP:int			=0x0000
	EESTOP:int			=0x0001
	START_OSC:int		=0x0002
	STOP_OSC:int		=0x0003
	PICK_UP:int			=0x0004
	PUT_DOWN:int		=0x0005
	START_PROCEDURE:int	=0x0006
	STOP_PROCEDURE:int	=0x0007
	RESET:int			=0x0008
	NOP:int				=0xffff

@dataclass(frozen=True)
class ERRCODE:
	UNKNOWN:int				=0x0000
	VAL_OUT_OF_RANGE:int	=0x0001
	REG_READONLY:int		=0x0002
	INVALID_CRC:int			=0x0003
	NOP:int					=0xffff

