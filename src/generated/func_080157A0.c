/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
u8 func_080157A0(u8 value)
{
    u8 offset;
    if((offset=value-65)<=25) value=offset+1;
    else if((offset=value-97)<=25) value=offset+1;
    else if((offset=value-48)<=9) value=offset+32;
    else {
        switch(value) {
        case 32: value=0;break;
        case 63: value=27;break;
        case 33: value=28;break;
        case 39: value=29;break;
        case 45: value=30;break;
        case 46: value=31;break;
        case 44: value=42;break;
        case 58: case 61: value=43;break;
        case 37: value=46;break;
        case 36: value=90;break;
        case 38: value=47;break;
        case 35: value=95;break;
        case 153: value=81;break;
        case 174: value=82;break;
        case 161: value=44;break;
        case 191: value=45;break;
        case 192: value=48;break;
        case 193: value=49;break;
        case 194: value=50;break;
        case 195: value=51;break;
        case 196: value=52;break;
        case 199: value=53;break;
        case 200: value=54;break;
        case 201: value=55;break;
        case 202: value=56;break;
        case 203: value=57;break;
        case 204: value=58;break;
        case 205: value=59;break;
        case 206: value=60;break;
        case 207: value=61;break;
        case 209: value=62;break;
        case 210: value=63;break;
        case 211: value=64;break;
        case 212: value=65;break;
        case 213: value=66;break;
        case 214: value=67;break;
        case 217: value=68;break;
        case 218: value=69;break;
        case 219: value=70;break;
        case 220: value=71;break;
        case 223: value=72;break;
        case 251: value=75;break;
        case 252: value=76;break;
        case 253: value=77;break;
        case 254: value=78;break;
        case 255: value=79;break;
        }
    }
    return value;
}
