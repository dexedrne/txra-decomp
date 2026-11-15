/* Byte-verified C; address name retained pending semantic review.
 * Menu sprite builder (deep-a draft finished in slice j3): header bars,
 * one tile per menu item chosen from the setup bytes, then the cursor and
 * two preview sprites. The column table is a two-dimensional array, so
 * item[i] and columns[count][i] share the i * 2 induction variable that
 * loop.c strength-reduces (the original's stack slot); slide + 120 is used
 * inline after the loop, where PRE places it before the loop like the
 * original; the cursor source goes through the source variable. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct {u16 kind,count,item[20];} TxraMenu44;
extern TxraMenu44 g_08175B04[];
extern u16 g_080213A4[][5];
extern u8 g_03000B60[];
extern u8 g_082AD1CC[],g_082ACFCC[],g_08294FCC[],g_082A03CC[],g_082BB5CC[],g_082BF5CC[],g_082F9EE0[];
extern s32 g_03001B20,g_03005FCC,g_030061E4,g_030014B4,g_030014B8,g_03005F40,g_03000AC4;
extern s16 g_03001B10,g_03001E50,g_030001E0[];
extern s32 func_08005C7C(void);
extern void func_0801533C(u32,u32,u32,u32,u32,u32,u32,u32,u32);
#define MENU_SPRITE(source,size,attr0,attr1) \
    func_0801533C((u32)(source),0x06014000+(g_030061E4<<5),size,96,2,attr0,attr1,(g_030061E4+512)|1024,0)
#define MENU_OPTION(slot,flags,current,normal,owned,selected) \
    if(i==(slot)){tile=normal;if(g_03000B60[flags]&(1<<(slot)))tile=owned;if(g_03000B60[current]==(slot)+1)tile=selected;}
void func_08005238(s32 key)
{
    u32 kind=g_08175B04[key].kind;
    u8 *source;
    s32 slide,i,tile,x,available;
    if(kind-1<=1) {
        source=g_082AD1CC;
        if(g_03001B20&128)source+=256;
        MENU_SPRITE(source,256,0x2004,0x401d);g_030061E4+=16;
        if(kind==2) {
            source=g_082ACFCC;
            if(g_03001B20&256)source+=256;
            MENU_SPRITE(source,256,0x2004,0x4008);g_030061E4+=16;
        }
    }
    if(g_03001B20)slide=g_03001B20&63;else slide=g_03005FCC;
    for(i=0;i<g_08175B04[key].count;i++) {
        tile=g_08175B04[key].item[i];
        if(key==26 || key==65 || key==91 || key==117) {
            MENU_OPTION(0,3,14,50,69,20);
            MENU_OPTION(1,3,14,53,71,21);
            MENU_OPTION(2,3,14,54,72,22);
        }
        if(key==27 || key==66 || key==92 || key==118) {
            MENU_OPTION(0,4,15,50,69,20);
            MENU_OPTION(1,4,15,53,71,21);
            MENU_OPTION(2,4,15,54,72,22);
        }
        if(key==22 || key==61 || key==87 || key==113) {
            MENU_OPTION(0,5,16,50,69,20);
            MENU_OPTION(1,5,16,53,71,21);
            MENU_OPTION(2,5,16,54,72,22);
        }
        if(key==23 || key==62 || key==88 || key==114) {
            MENU_OPTION(0,6,17,50,69,20);
            MENU_OPTION(1,6,17,53,71,21);
            MENU_OPTION(2,6,17,54,72,22);
        }
        if(key==24 || key==63 || key==89 || key==115) {
            MENU_OPTION(0,7,18,50,69,20);
            MENU_OPTION(1,7,18,53,71,21);
            MENU_OPTION(2,7,18,54,72,22);
        }
        if(key==25 || key==64 || key==90 || key==116) {
            MENU_OPTION(0,8,19,50,69,20);
            MENU_OPTION(1,8,19,53,71,21);
            MENU_OPTION(2,8,19,54,72,22);
            MENU_OPTION(3,8,19,55,73,23);
            MENU_OPTION(4,8,19,32,74,24);
        }
        if(key==30 || key==69 || key==95 || key==121) {
            MENU_OPTION(0,10,21,50,69,20);
            MENU_OPTION(1,10,21,53,71,21);
            MENU_OPTION(2,10,21,54,72,22);
            MENU_OPTION(3,10,21,55,73,23);
            MENU_OPTION(4,10,21,32,74,24);
        }
        if(key==31 || key==70 || key==96 || key==122) {
            MENU_OPTION(0,11,22,50,69,20);
            MENU_OPTION(1,11,22,53,71,21);
            MENU_OPTION(2,11,22,54,72,22);
            MENU_OPTION(3,11,22,55,73,23);
            MENU_OPTION(4,11,22,32,74,24);
        }
        if(key==32 || key==71 || key==97 || key==123) {
            MENU_OPTION(0,12,23,50,69,20);
            MENU_OPTION(1,12,23,53,71,21);
            MENU_OPTION(2,12,23,54,72,22);
            MENU_OPTION(3,12,23,55,73,23);
            MENU_OPTION(4,12,23,32,74,24);
        }
        if(key==33 || key==72 || key==98 || key==124) {
            MENU_OPTION(0,13,24,50,69,20);
            MENU_OPTION(1,13,24,53,71,21);
            MENU_OPTION(2,13,24,54,72,22);
            MENU_OPTION(3,13,24,55,73,23);
            MENU_OPTION(4,13,24,32,74,24);
        }
        if(key==14 || key==57 || key==83 || key==109) {
            MENU_OPTION(0,9,20,50,69,20);
            MENU_OPTION(1,9,20,53,71,21);
            MENU_OPTION(2,9,20,54,72,22);
        }
        if(key==17) {
            available=func_08005C7C();
            if(i==0){tile=38;if(available>3)tile=76;}
            if(i==1){tile=39;if(available>3)tile=77;}
            if(i==2){tile=40;if(available>3)tile=78;}
        }
        if(key==18) {
            available=func_08005C7C();
            if(i==0){tile=38;if(available<=1 || g_030014B8<=0)tile=76;}
            if(i==1){tile=39;if(available<=1 || g_03005F40<=0)tile=77;}
            if(i==2){tile=40;if(available<=1 || g_03000AC4<=0)tile=78;}
        }
        if(key==19 || key==60 || key==86 || key==112) {
            available=func_08005C7C();
            if(i==0){tile=38;if(available<=1 || g_030014B8<=0)tile=76;}
            if(i==1){tile=39;if(available<=1 || g_03005F40<=0)tile=77;}
            if(i==2){tile=40;if(available<=1 || g_03000AC4<=0)tile=78;}
        }
        x=g_080213A4[g_08175B04[key].count][i];
        source=g_08294FCC+(tile<<10);
        MENU_SPRITE(source,1024,((slide+110)&255)|0x2000,(x&511)|0x8000);g_030061E4+=32;
    }
    { u16 *row=(u16 *)g_080213A4; s32 s=g_030014B4; x=row[g_08175B04[key].count*5+s]; }
    source=g_082A03CC;
    MENU_SPRITE(source,1024,((slide+120)&255)|0x2000,((x+1)&511)|0x8000);g_030061E4+=32;
    if(key==11) {
        if(g_03001B10<=95)source=g_082BB5CC+((s16)(g_03001B10/6)<<10);
        else source=g_082BF5CC+((g_03001B10-96)<<10);
        if(!g_03005FCC && !g_03001B20){MENU_SPRITE(source,1024,0x2020,0x8068);g_030061E4+=32;}
    }
    if(key==7 || key==52 || key==78 || key==104) {
        source=g_082F9EE0+(g_03001E50<<12);
        if(!g_030001E0[g_03001E50])source=g_082F9EE0+0x7000;
        if(!g_03005FCC && !g_03001B20){MENU_SPRITE(source,4096,0x2024,0xc080);g_030061E4+=128;}
    }
}
