#pragma once
#include "inttypes.h"

namespace COM
{
    /*
        Frame structure:
        Start [1B] + OPCODE [1B] + OP_ID [1B] + REGISTER [1B] + DATA [4B] + CRC-8 [1B]
    */
    constexpr uint8_t START_BYTE=0xA5;
    enum OPCODE: uint8_t
    {
        READ_REQ    =0x00,
        READ_RESP   =0x01,
        WRITE_REQ   =0x02,
        WRITE_ACK   =0x03,
        WRITE_NACK  =0x04,
        //...
        NOP         =0xff
    };

    enum REGISTER: uint8_t
    {
        COMMAND     =0x00,
        STATUS      =0x01,

        FREQ        =0x10,
        AMPL        =0x11,
        LLIM        =0x12,
        ULIM        =0x13,
        CENTER      =0x14,
        SCREW       =0x15,

        //...
        NOP         =0xff
    };

    enum COMMAND: uint32_t
    {
        ESTOP               =0x0000,
        EESTOP              =0x0001,
        START_OSC           =0x0002,
        STOP_OSC            =0x0003,
        PICK_UP             =0x0004,
        PUT_DOWN            =0x0005,
        START_PROCEDURE     =0x0006,
        STOP_PROCEDURE      =0x0007,
        RESET               =0x0008,
        //...
        NOP                 =0xffff
    };

    enum ERRCODE: uint32_t
    {
        UNKNOWN             =0x0000,
        VAL_OUT_OF_RANGE    =0x0001,
        REG_READONLY        =0x0002,
        INVALID_CRC         =0x0003,
        NOP                 =0xffff
    };
}