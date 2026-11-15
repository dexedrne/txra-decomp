/* Uninstalled ARM frame-local hypothesis. Not byte-identical; not part of the build. */
void func_080181C0(void) {
    u32 lr;
    u32 r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r14;
    u32 frame_2C,frame_30,frame_34,frame_38,frame_3C,frame_40,frame_44,frame_48,frame_4C,frame_50,frame_54,frame_58,frame_5C,frame_60,frame_64,frame_68,frame_6C,frame_70;
    r0 = 0;
    r2=0x03001E60;
    frame_44 = r0;
    frame_40 = r0;
    frame_30 = r0;
    r3 = *(u32 *)0x03001E80 ;
    r3 = -r3;
    r3 = r3 << 18;
    r3 = r3 >> 18;
    frame_34 = r3;
    do {
        r1 = frame_30;
        r4=0x03001E60;
        lr = frame_30;
        r3 = r1 << 2;
        r2 = r3 + r1;
        r2 += (r2 << 2);
        r2 = r2 << 2;
        r1 = *(s16 *)(r4 + r2);
        frame_6C = r3;
        lr += 1;
        frame_64 = lr;
        if (r1 != 0) {
            r1 = frame_30;
            r0 = 0;
            frame_2C = r0;
            r1 = r1 << 4;
            frame_4C = r1;
            do {
                r2 = 0;
                frame_48 = r2;
                r3 = frame_2C;
                r4=0x03005F90;
                lr = frame_30;
                r2 = r3 << 4;
                r1 = *(u32 *)0x03005F90 ;
                r3 = lr + r2;
                frame_70 = r2;
                if (r1 == r3) goto L_08018280;
                r0 = frame_2C;
                r2 = frame_4C;
                r3 = r0 + r2;
                if (r1 != r3) goto L_08018288;
L_08018280:
                r3 = 1;
                frame_48 = r3;
L_08018288:
                r4=0x03005F90;
                lr = frame_30;
                r0 = frame_70;
                r2 = *(u32 *)0x03005F94 ;
                r3 = lr + r0;
                if (r2 == r3) goto L_080182B8;
                r1 = frame_2C;
                r4 = frame_4C;
                r3 = r1 + r4;
                if (r2 != r3) goto L_080182C0;
L_080182B8:
                lr = 1;
                frame_48 = lr;
L_080182C0:
                r0=0x03005F90;
                r1 = frame_30;
                r4 = frame_70;
                r2 = *(u32 *)0x03005F98 ;
                r3 = r1 + r4;
                if (r2 == r3) goto L_080182F0;
                lr = frame_2C;
                r0 = frame_4C;
                r3 = lr + r0;
                if (r2 != r3) goto L_080182F8;
L_080182F0:
                r1 = 1;
                frame_48 = r1;
L_080182F8:
                r3=0x03005F90;
                r4 = frame_30;
                lr = frame_70;
                r2 = *(u32 *)0x03005F9C ;
                r3 = r4 + lr;
                if (r2 == r3) goto L_08018328;
                r0 = frame_2C;
                r1 = frame_4C;
                r3 = r0 + r1;
                if (r2 != r3) goto L_08018330;
L_08018328:
                r2 = 1;
                frame_48 = r2;
L_08018330:
                r4=0x080202E4;
                lr = frame_6C;
                r0 = frame_40;
                r1 = frame_2C;
                r3 = *(u32 *)(r4 + lr);
                r1 += 1;
                frame_60 = r1;
                if ((r0 & r3) != 0) goto L_080187E8;
                r3 = frame_2C;
                r2 = r3 << 2;
                r3 = *(u32 *)(r4 + r2);
                frame_68 = r2;
                r12 = r0 & r3;
                if (r12 != 0) goto L_080187E8;
                r4 = frame_2C;
                r14=0x03001E60;
                r1 = frame_30;
                r3 = r2 + r4;
                r3 += (r3 << 2);
                r0 = r3 << 2;
                r2 = *(s16 *)(lr + r0);
                if (r4 == r1) goto L_080187E8;
                r2=0x030057A0;
                r1 = ~0x3F;
                *(u32 *)0x030057A0  = r1;
                r3 = ~0xBF;
                *(u32 *)0x030057A8  = r3;
                r4=0x030057A0;
                r2 = 0x40;
                *(u32 *)0x030057AC  = r2;
                *(u32 *)0x030057B4  = r3;
                *(u32 *)0x030057B8  = r1;
                *(u32 *)0x030057C4  = r2;
                *(u32 *)0x030057D0  = r1;
                *(u32 *)0x030057D8  = r12;
                *(u32 *)0x030057DC  = r2;
                *(u32 *)0x030057E4  = r12;
                r3 += 0x180;
                *(u32 *)0x030057C0  = r3;
                *(u32 *)0x030057CC  = r3;
                r1 = lr + 0x20;
                r14=0x03001E6C;
                r2=0x03001E60;
                frame_54 = r0;
                r6 = r4;
                r4=0x08020B04;
                lr = *(u32 *)(lr + r0);
                frame_5C = lr;
                r3 = r0 + r2;
                r2 = *(s16 *)(r3 + 2);
                r14=0x08020B08;
                r2 = r2 << 3;
                r4 = *(u32 *)(r4 + r2);
                r3 = *(u32 *)(r1 + r0);
                frame_38 = r4;
                r0=0x083D2280;
                r1 = frame_6C;
                r2 = *(u32 *)(lr + r2);
                r3 = r3 << 18;
                frame_3C = r2;
                r3 = r3 >> 18;
                r2 = frame_30;
                r3 = r3 << 2;
                r0 = *(u32 *)(r0 + r3);
                r1 += r2;
                r2=0x083C2280;
                frame_50 = r0;
                frame_58 = r1;
                r10 = *(u32 *)(r2 + r3);
                r3 = frame_34;
                r7 = 5;
                r9 = r3 << 2;
                r8 = *(u32 *)(r2 + r9);
                do {
                    r0 = *(u32 *)r6;
                    r4 = frame_50;
                    r4 = r0 * r4;
                    r3 = *(u32 *)(r6 + 8);
                    r2 = frame_50;
                    r2 = r3 * r2;
                    r12 = r10 * r3;

                    lr = frame_58;
                    r0=0x03001E64;
                    r2 = frame_54;
                    r1 = lr + (lr << 2);
                    lr = *(u32 *)(r0 + r2);
                    r1 = r1 << 2;
                    r3 = *(u32 *)(r0 + r1);
                    lr -= r3;
                    r3=0x083D2280;
                    r4 -= r12;
                    r2 = *(u32 *)(r3 + r9);
                    lr += ((s32)r4 >> 12);
                    r12 = r2 * lr;
                    r4=0x03001E6C;
                    r0 = frame_5C;
                    r3 = *(u32 *)(r4 + r1);
                    r3 = r0 - r3;
                    r3 += ((s32)r5 >> 12);
                    r1 = r2 * r3;
                    r0 = r8 * r3;

                    r12 -= r0;
                    r12 = (s32)r12 >> 12;
                    *(u32 *)r6 = r12;
                    r2 = (s32)r2 >> 12;
                    *(u32 *)(r6 + 8) = r2;
                    r7 -= 1;
                    r6 += 0xC;
                } while ((s32)r7 >= 0);
                r1 = frame_38;
                r0 = frame_6C;
                r2 = frame_30;
                r4 = frame_68;
                r7 = 0;
                lr = frame_2C;
                r12 = -r1;
                r1 = r0 + r2;
                r3 = r4 + lr;
                r3 += (r3 << 2);
                r2=0x03001E60;
                r6 = r3 << 2;
                r10 = r2 + 0x20;
L_08018528:
                r3 = r7 + (r7 << 1);
                r8 = r3 << 2;
                r3=0x030057A0;
                lr = *(u32 *)(r3 + r8);
                if ((s32)lr <= (s32)r12) goto L_080187DC;
                r4 = frame_38;
                if ((s32)lr >= (s32)r4) goto L_080187DC;
                r4 = frame_3C;
                r3 += 8;
                r3 = *(u32 *)(r3 + r8);
                r2 = -r4;
                if ((s32)r3 <= (s32)r2) goto L_080187DC;
                if ((s32)r3 >= (s32)r4) goto L_080187DC;
                r2 = frame_48;
                if (r2 != 0) goto L_080187AC;
                r1 += (r1 << 2);
                r4=0x03001E88;
                r1 = r1 << 2;
                r2=0x03001E60;
                r9 = 0x3C;
                r3 = *(u16 *)(r4 + r6);
                r0 = r1 + r2;
                r3 += 0x230;
                *(u16 *)(r0 + r9) = (u16)r3;
                r3=0x03001E60;
                r2 = *(u16 *)(r4 + r1);
                r12 = r6 + r3;
                r2 += 0x230;
                *(u16 *)(r12 + r9) = (u16)r2;
                goto L_080185E0;
L_080185E0:
                r4 = *(u16 *)(r10 + r1);
                r7 = 0x3E;
                *(u16 *)(r0 + r7) = (u16)r4;
                r2 = *(u16 *)(r10 + r6);
                *(u16 *)(r12 + r7) = (u16)r2;
                r5 = ~0xC000;
                r2 = *(u16 *)(r10 + r6);
                r4 = 0x3A;
                r2 &= r5;
                *(u16 *)(r0 + r4) = (u16)r2;
                r3 = *(u16 *)(r10 + r1);
                r3 &= r5;
                *(u16 *)(r12 + r4) = (u16)r3;
                if ((s32)lr > 0x20) {
                    r3 = *(u16 *)(r0 + 0x3A);
                    r2 = *(u16 *)(r0 + 0x3E);
                    r3 -= 0x100;
                    r3 &= r5;
                    r2 -= 0x100;
                    *(u16 *)(r0 + 0x3A) = (u16)r3;
                    r2 &= r5;
                    *(u16 *)(r0 + 0x3E) = (u16)r2;
                    r3 = *(u16 *)(r12 + 0x3A);
                    r2 = *(u16 *)(r12 + 0x3E);
                    r3 += 0x100;
                    r3 &= r5;
                    r2 += 0x100;
                    *(u16 *)(r12 + 0x3A) = (u16)r3;
                    r2 &= r5;
                    *(u16 *)(r12 + 0x3E) = (u16)r2;
                }
                r14=0x030057A0;
                r3 = *(u32 *)(lr + r8);
                if ((s32)r3 < (s32)-(0x20)) {
                    r3 = *(u16 *)(r0 + r4);
                    r2 = *(u16 *)(r0 + r7);
                    r3 += 0x100;
                    r3 &= r5;
                    r2 += 0x100;
                    *(u16 *)(r0 + r4) = (u16)r3;
                    r2 &= r5;
                    *(u16 *)(r0 + r7) = (u16)r2;
                    r3 = *(u16 *)(r12 + r4);
                    r2 = *(u16 *)(r12 + r7);
                    r3 -= 0x100;
                    r3 &= r5;
                    r2 -= 0x100;
                    *(u16 *)(r12 + r4) = (u16)r3;
                    r2 &= r5;
                    *(u16 *)(r12 + r7) = (u16)r2;
                }
                r3 = *(s16 *)(r0 + r9);
                if ((s32)r3 < 0) {
                    r1 = frame_30;
                    if (r1 != 0) { r3 = r3 << 2; }
                    if (r1 != 0) { *(u16 *)(r0 + r9) = (u16)r3; }
                }
                r3=0x03001E60;
                r1 = 0x3C;
                r2 = r6 + r3;
                r3 = *(s16 *)(r2 + r1);
                if ((s32)r3 < 0) {
                    r4 = frame_2C;
                    if (r4 != 0) { r3 = r3 << 2; }
                    if (r4 != 0) { *(u16 *)(r2 + r1) = (u16)r3; }
                }
                lr = frame_6C;
                r0 = frame_30;
                r3=0x03001E88;
                r4=0x03001E88;
                r1 = lr + r0;
                r1 += (r1 << 2);
                r1 = r1 << 2;
                r2 = *(u32 *)(r3 + r1);
                r0 = *(u32 *)(r3 + r6);
                r2 = (s32)r2 >> 1;
                *(u32 *)(r3 + r6) = r2;
                r3=0x030021CC;
                r2 = *(s16 *)0x030021CC ;
                r0 = (s32)r0 >> 1;
                *(u32 *)(r4 + r1) = r0;
                if (r2 == 0) {
                    lr = frame_30;
                    r0 = frame_2C;
                    r1 = frame_44;
                    if (lr == 0) { r1 = 1; }
                    frame_44 = r1;
                }
                r2=0x080202E4;
                r4 = frame_6C;
                r0 = frame_40;
                r3 = *(u32 *)(r2 + r4);
                lr = frame_48;
                r0 |= r3;
                frame_40 = r0;
                if (lr != 0) goto L_080187E8;
                r1 = frame_30;
                r3 = frame_70;
                r7 = lr;
                r0=0x03005F90;
                r2 = r1 + r3;
                do {
                    r1 = r7 << 2;
                    r3 = *(u32 *)(r0 + r1);
                    if (r3 == 0) { r4=0x03005F90; }
                    if (r3 == 0) { *(u32 *)(r4 + r1) = r2; }
                    r7 += 1;
                } while ((s32)r7 <= 3);
                goto L_080187E8;
L_080187AC:
                r14=0x080202E4;
                r3 = *(u32 *)(lr + r0);
                r0 = frame_40;
                r0 |= r3;
                frame_40 = r0;
                goto L_080187E8;
L_080187DC:
                r7 += 1;
                if ((s32)r7 <= 5) goto L_08018528;
L_080187E8:
                r1 = frame_60;
                frame_2C = r1;
            } while ((s32)r1 <= 7);
        }
        r2 = frame_64;
        frame_30 = r2;
    } while ((s32)r2 <= 7);
    r3 = frame_40;
    if (r3 == 0) {
        r1 = r3;
        r4 = 3;
        frame_2C = r4;
        r3 = 0xC;
        r2=0x03005F90;
        do {
            *(u32 *)(r3 + r2) = r1;
            lr = frame_2C;
            lr -= 1;
            frame_2C = lr;
            r3 -= 4;
        } while ((s32)lr >= 0);
    }
    r0 = frame_44;
    goto L_0801884C;
L_0801884C:

    return;
}
