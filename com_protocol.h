#pragma once
#include "inttypes.h"

namespace COM
{
    /*
        Frame structure:
        Start [2B] + TRANSACT_ID [1B] + OPCODE [1B] + REGISTER [1B] + DATA [4B] + CRC-16 [2B] (payload only)
    */
    constexpr uint8_t START_BYTES[]={0xAA, 0x55};
    constexpr uint8_t FRAME_SIZE=11;
    enum class OPCODE: uint8_t
    {
        READ_REQ    =0xA0,
        READ_RESP   =0xA1,
        WRITE_REQ   =0xA2,
        WRITE_ACK   =0xA3,
        WRITE_NACK  =0xA4,
        //...
        INVALID     =0x00,
        NOP         =0xff
    };

    enum class  REGISTER: uint8_t
    {
        COMMAND     =0xA0,
        STATUS      =0xA1,

        FREQ        =0xB0,
        AMPL        =0xB1,
        LLIM        =0xB2,
        ULIM        =0xB3,
        CENTER      =0xB4,
        SCREW       =0xB5,

        //...
        INVALID     =0x00,
        NOP         =0xff
    };

    enum class  COMMAND: uint32_t
    {
        ESTOP               =0xCAB0,
        EESTOP              =0xCAB1,
        START_OSC           =0xCAB2,
        STOP_OSC            =0xCAB3,
        PICK_UP             =0xCAB4,
        PUT_DOWN            =0xCAB5,
        START_PROCEDURE     =0xCAB6,
        STOP_PROCEDURE      =0xCAB7,
        RESET               =0xCAB8,
        //...
        INVALID             =0x0000,
        NOP                 =0xffff
    };

    enum class  ERRCODE: uint32_t
    {
        UNKNOWN             =0xCA00,
        VAL_OUT_OF_RANGE    =0xCA01,
        REG_READONLY        =0xCA02,
        INVALID_CRC         =0xCA03,
        //...
        INVALID             =0x0000,
        NOP                 =0xffff
    };
}