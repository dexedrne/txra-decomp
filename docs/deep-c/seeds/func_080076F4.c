/* Uninstalled ARM frame-local hypothesis. Not byte-identical; not part of the build. */
void func_080076F4(u32 r0) {
    u32 lr;
    u32 r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12;
    u32 frame_2C,frame_30,frame_34,frame_38,frame_3C,frame_40,frame_44,frame_48,frame_4C,frame_50,frame_54,frame_58,frame_5C,frame_60,frame_64;
    frame_2C = r0;
    r5=0x03007770;
    r3 = r0 + (r0 << 3);
    r9 = r3 << 3;
    r2 = r5 + 0x38;
    r3 = r5 + 0x30;
    r10 = *(u32 *)(r2 + r9);
    r12 = r0 + 1;
    r1 = *(u32 *)(r3 + r9);
    r12 += (r12 << 3);
    frame_40 = r1;
    r12 = r12 << 3;
    r8 = *(u32 *)(r2 + r12);
    lr = *(u32 *)(r3 + r12);
    r0 += 2;
    frame_44 = lr;
    r0 += (r0 << 3);
    lr = frame_2C;
    r0 = r0 << 3;
    r1 = *(u32 *)(r3 + r0);
    r7 = *(u32 *)(r2 + r0);
    frame_48 = r1;
    r4=0x083B8698;
    r1 = lr + 3;
    r1 += (r1 << 3);
    r1 = r1 << 3;
    r3 = *(u32 *)(r3 + r1);
    r6 = *(u32 *)(r2 + r1);
    frame_4C = r3;
    lr = r5 + 0x1C;
    r3 = *(u32 *)(lr + r9);
    r3 = *(u32 *)(r4 + r3 << 4);
    frame_30 = r3;
    r2 = *(u32 *)(lr + r12);
    r2 = *(u32 *)(r4 + r2 << 4);
    frame_34 = r2;
    r3 = *(u32 *)(lr + r0);
    r3 = *(u32 *)(r4 + r3 << 4);
    frame_38 = r3;
    r0 = *(u32 *)(lr + r1);
    r2 = r5 + 0x14;
    r3 = *(u32 *)(r2 + r9);
    r0 = *(u32 *)(r4 + r0 << 4);
    frame_3C = r0;
    if (r3 == 0x60) goto L_080077D0;
    r3 = r5 + 0x20;
    r2 = *(u32 *)(r3 + r9);
    if (r2 != 0) goto L_080077E4;
L_080077D0:
    r1 = 0;
    frame_40 = r1;
    r2=0x083334A8;
    r10 = ~0;
    frame_30 = r2;
L_080077E4:
    r3 = frame_2C;
    r12=0x03007770;
    r1 = r3 + 1;
    r3 = r1 + (r1 << 3);
    r0 = r3 << 3;
    r2 = r12 + 0x14;
    r3 = *(u32 *)(r2 + r0);
    frame_54 = r1;
    if (r3 == 0x60) goto L_08007820;
    r3 = r12 + 0x20;
    r2 = *(u32 *)(r3 + r0);
    if (r2 != 0) goto L_08007834;
L_08007820:
    lr = 0;
    frame_44 = lr;
    r1=0x083334A8;
    r8 = ~0;
    frame_34 = r1;
L_08007834:
    r2 = frame_2C;
    r1 = r2 + 2;
    r3 = r1 + (r1 << 3);
    r0 = r3 << 3;
    r3=0x03007770;
    r2 = r3 + 0x14;
    r3 = *(u32 *)(r2 + r0);
    frame_58 = r1;
    if (r3 == 0x60) goto L_08007874;
    r12=0x03007770;
    r3 = r12 + 0x20;
    r2 = *(u32 *)(r3 + r0);
    if (r2 != 0) goto L_08007888;
L_08007874:
    lr = 0;
    frame_48 = lr;
    r1=0x083334A8;
    r7 = ~0;
    frame_38 = r1;
L_08007888:
    r2 = frame_2C;
    r1 = r2 + 3;
    r3 = r1 + (r1 << 3);
    r0 = r3 << 3;
    r3=0x03007770;
    r2 = r3 + 0x14;
    r3 = *(u32 *)(r2 + r0);
    frame_5C = r1;
    if (r3 == 0x60) goto L_080078C8;
    r12=0x03007770;
    r3 = r12 + 0x20;
    r2 = *(u32 *)(r3 + r0);
    if (r2 != 0) goto L_080078DC;
L_080078C8:
    lr = 0;
    frame_4C = lr;
    r1=0x083334A8;
    r6 = ~0;
    frame_3C = r1;
L_080078DC:
    r2=0x03006A98;
    r3 = *(u32 *)0x03006A98 ;
    r4 = 0;
    r5=0x03007410;
    r3 += 1;
    r3 &= 1;
    if (r3 != r4) { r9 = 0xB0; }
    if (r3 == r4) { r9 = r4; }
    r2 = frame_2C;
    r3 = r9 + 1;
    frame_50 = r3;
    r2 = r2 << 3;
    frame_60 = r2;
    do {
        lr = frame_30;
        r2 = frame_50;
        r3 = frame_3C;
        r1 = lr + ((s32)r10 >> 14);
        r1 = *(s8 *)r1;
        r2 = r4 + r2;
        lr = frame_38;
        r0 = r3 + ((s32)r6 >> 14);
        frame_64 = r2;
        r3 = lr + ((s32)r7 >> 14);
        lr = frame_34;
        r0 = *(s8 *)r0;
        r12 = r4 + r9;
        r3 = *(s8 *)r3;
        r2 = lr + ((s32)r8 >> 14);
        r2 = *(s8 *)r2;
        r1 += r0;
        r3 += r2;
        r1 += r3;
        r1 = (s32)r1 >> 2;
        *(u8 *)(r5 + r12) = (u8)r1;
        r1 = frame_40;
        r2 = frame_30;
        r3 = frame_4C;
        r12 = frame_3C;
        lr = frame_48;
        r10 += r1;
        r1 = r2 + ((s32)r10 >> 14);
        r6 += r3;
        r1 = *(s8 *)r1;
        r0 = r12 + ((s32)r6 >> 14);
        r0 = *(s8 *)r0;
        r4 += 2;
        r2 = frame_38;
        r12 = frame_44;
        r7 += lr;
        lr = frame_34;
        r3 = r2 + ((s32)r7 >> 14);
        r8 += r12;
        r2 = lr + ((s32)r8 >> 14);
        r3 = *(s8 *)r3;
        r1 += r0;
        r2 = *(s8 *)r2;
        r8 += r12;
        r12 = frame_64;
        r3 += r2;
        r2 = frame_40;
        r1 += r3;
        r3 = frame_48;
        r1 = (s32)r1 >> 2;
        *(u8 *)(r5 + r12) = (u8)r1;
        r10 += r2;
        lr = frame_4C;
        r7 += r3;
        r6 += lr;
    } while ((s32)r4 <= 0xAF);
    r1 = frame_60;
    r2 = frame_2C;
    r4=0x03007770;
    r3 = r1 + r2;
    r12 = r3 << 3;
    r5 = r4 + 0x3C;
    r3 = *(u32 *)(r5 + r12);
    if (r10 >= r3) {
        r3 = r4 + 0x1C;
        r1 = *(u32 *)(r3 + r12);
        r3=0x083B8698;
        r2 = r3 + 8;
        r3 = *(u32 *)(r2 + r1 << 4);
        if (r3 != 1) { r10 = 0; }
        if (r3 == 1) { r10 = ~0; }
    }
    lr = frame_54;
    r3 = lr + (lr << 3);
    r9 = r3 << 3;
    r2 = *(u32 *)(r5 + r9);
    if (r8 >= r2) {
        r3 = r4 + 0x1C;
        r1 = *(u32 *)(r3 + r9);
        r3=0x083B8698;
        r2 = r3 + 8;
        r3 = *(u32 *)(r2 + r1 << 4);
        if (r3 != 1) { r8 = 0; }
        if (r3 == 1) { r8 = ~0; }
    }
    lr = frame_58;
    r3 = lr + (lr << 3);
    r0 = r3 << 3;
    r2 = *(u32 *)(r5 + r0);
    if (r7 >= r2) {
        r3 = r4 + 0x1C;
        r1 = *(u32 *)(r3 + r0);
        r3=0x083B8698;
        r2 = r3 + 8;
        r3 = *(u32 *)(r2 + r1 << 4);
        if (r3 != 1) { r7 = 0; }
        if (r3 == 1) { r7 = ~0; }
    }
    lr = frame_5C;
    r3 = lr + (lr << 3);
    lr = r3 << 3;
    r2 = *(u32 *)(r5 + lr);
    if (r6 >= r2) {
        r3 = r4 + 0x1C;
        r1 = *(u32 *)(r3 + lr);
        goto L_08007AE4;
L_08007AE4:
        r3=0x083B8698;
        r2 = r3 + 8;
        r3 = *(u32 *)(r2 + r1 << 4);
        if (r3 != 1) { r6 = 0; }
        if (r3 == 1) { r6 = ~0; }
    }
    r1=0x03007770;
    r3 = r1 + 0x38;
    *(u32 *)(r3 + r12) = r10;
    *(u32 *)(r3 + r9) = r8;
    *(u32 *)(r3 + r0) = r7;
    *(u32 *)(r3 + lr) = r6;
    goto L_08007B20;
L_08007B20:

    return;
}
