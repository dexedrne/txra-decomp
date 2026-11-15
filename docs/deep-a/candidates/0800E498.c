/* Unmatched diagnostic source; not installed or accepted as behavior-correct. */
extern s16 g_03005F60;
extern u32 g_03002328,g_030014B4,g_030001C0,g_03002180;
extern s32 g_03002320[];
extern TxraRecord g_03001E60[];
extern u8 g_03000B79;
extern s16 g_080200E4[][16];
extern u8 g_03000B60[][32];
extern u32 g_03000B58,g_03000AC8,g_03005FD4;
extern s32 func_0800EC70(s32,s32),func_0800ECCC(s32,s32);
extern void func_08012600(s32),func_08014250(s32,s32);
#define DEEP_RESET() {g_030001C0=0;g_03002180=0;}
#define DEEP_RANGE(first,last,copy,column) \
    if(!g_030014B4) { \
        g_03001E60[7].field_02--; \
        if(g_03001E60[7].field_02<(first))g_03001E60[7].field_02=(last); \
        if(copy)g_03001E60[0].field_02=g_03001E60[7].field_02; \
        func_08014250(g_080200E4[g_03001E60[copy?0:7].field_02-16][column],g_080200E4[g_03001E60[copy?0:7].field_02-16][0]); \
        DEEP_RESET(); \
    } \
    if(g_030014B4==2) { \
        g_03001E60[7].field_02++; \
        if(g_03001E60[7].field_02>(last))g_03001E60[7].field_02=(first); \
        if(copy)g_03001E60[0].field_02=g_03001E60[7].field_02; \
        func_08014250(g_080200E4[g_03001E60[copy?0:7].field_02-16][column],g_080200E4[g_03001E60[copy?0:7].field_02-16][0]); \
        DEEP_RESET(); \
    }
#define DEEP_SELECT(mode,slot) \
    if(!g_030014B4) { \
        u8 *record; \
        slot=func_0800EC70(mode,slot);record=g_03000B60[slot]; \
        g_03001E60[7].field_02=record[2]; \
        func_08014250(g_080200E4[record[2]-16][record[25]+2],g_080200E4[record[2]-16][0]); \
        func_08012600(key); DEEP_RESET(); \
    } \
    if(g_030014B4==2) { \
        u8 *record; \
        slot=func_0800ECCC(mode,slot);record=g_03000B60[slot]; \
        g_03001E60[7].field_02=record[2]; \
        func_08014250(g_080200E4[record[2]-16][record[25]+2],g_080200E4[record[2]-16][0]); \
        func_08012600(key); DEEP_RESET(); \
    }
void func_0800E498(u32 key)
{
    if(g_03005F60) {
        g_03005F60++;
        if(g_03005F60>31){g_03005F60=0;g_03002328=1000;}
        if(g_03005F60<=15)g_03002320[2]=(g_03005F60<<8)+1000;
        else g_03002320[2]=((31-g_03005F60)<<8)+1000;
        if((u16)g_03005F60==16)switch(key) {
        case 46:
            DEEP_RANGE(16,21,1,g_03000B79+2);break;
        case 47:
            DEEP_RANGE(22,26,1,g_03000B79+2);break;
        case 48:
            DEEP_RANGE(27,31,1,g_03000B79+2);break;
        case 36:
            DEEP_RANGE(16,21,0,2);break;
        case 37:
            DEEP_RANGE(22,26,0,2);break;
        case 38:
            DEEP_RANGE(27,31,0,2);break;
        case 39: case 42: case 75: case 101: case 127:
            DEEP_SELECT(0,g_03000B58);break;
        case 40: case 43: case 76: case 102: case 128:
            DEEP_SELECT(1,g_03000AC8);break;
        case 41: case 44: case 77: case 103: case 129:
            DEEP_SELECT(2,g_03005FD4);break;
        }
    }
}
