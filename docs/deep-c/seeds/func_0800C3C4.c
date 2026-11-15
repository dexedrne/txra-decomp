/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
extern s32 func_08014614(s32,s32);
extern void func_0801604C(u32,u32);
extern u8 g_03001E60[];
void func_0800C3C4(u32 r0) {
    u32 r1, r2, r3, r4, r5, r6, r7, r8, r9, r10;
    u32 sp00; /* stack slots */
    sp00 = r0;
    r5 = (u32)g_03001E60;
    r0 = 0x64;
    r1 = sp00;
    r6 = r1;
    r6 *= r0;
    r2 = r6 + r5;
    r1 = r2;
    r1 += 0x40;
    r3 = *(u16 *)r1;
    r4 = 0;
    r0 = *(s16 *)(r1 + r4);
    if ((s32)r0 > 0) {
        r0 = r3 - 1;
        *(u16 *)r1 = (u16)r0;
    }
    r0 = r5;
    r0 += 0x30;
    r0 = r6 + r0;
    r4 = *(u32 *)r0;
    r1 = r2;
    r1 += 0x44;
    r0 = 0x20;
    r1 = *(u16 *)r1;
    r0 &= r1;
    if (r0 == 0) goto L_0800C48A;
    r0 = r2;
    r0 += 0x56;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    if ((s32)r4 > (s32)r0) {
        r3 = 0xFFFFFEA2;
        r4 = r0 + r3;
    }
    if ((s32)r4 > 0) {
        r4 -= 0xFA;
    }
    r0 = r2;
    r0 += 0x54;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    r4 -= r0;
    r1 = r2;
    r1 += 0x58;
    r2 = 0;
    r0 = *(s16 *)(r1 + r2);
    if ((s32)r4 >= (s32)-(r0)) goto L_0800C48A;
    r0 = r5;
    r0 += 0x28;
    r3 = r6 + r0;
    r2 = *(u32 *)r3;
    r0 = 0x780;
    if ((s32)r2 <= (s32)r0) goto L_0800C48A;
    r0 = r2;
    r0 -= 0x40;
    *(u32 *)r3 = r0;
    r3 = 0;
    r0 = *(s16 *)(r1 + r3);
    r4 = -r0;
    r0 = sp00;
    if (r0 != 0) goto L_0800C48A;
    r6 = r5;
    r6 += 0x40;
    r1 = 0;
    r0 = *(s16 *)(r6 + r1);
    if (r0 != 0) goto L_0800C48A;
    r0 = 0xE;
    r1 = 1;
    func_0801604C(r0, r1);
    r0 = 0x40;
    *(u16 *)r6 = (u16)r0;
    r2 = 0x3C;
    r0 = *(s16 *)(r5 + r2);
    if (r0 != 0) goto L_0800C48A;
    r0 = 0x10;
    *(u16 *)(r5 + 0x3C) = (u16)r0;
    r1 = *(u32 *)(r5 + 0x20);
    r3 = 0xFFFFF000;
    r0 = r1 + r3;
    r3 = 0x3FFF;
    r2 = r3;
    r0 &= r2;
    *(u16 *)(r5 + 0x3A) = (u16)r0;
    r1 &= r2;
    *(u16 *)(r5 + 0x3E) = (u16)r1;
L_0800C48A:
    r5 = (u32)g_03001E60;
    r0 = 0x64;
    r1 = sp00;
    r6 = r1;
    r6 *= r0;
    r3 = r6 + r5;
    r1 = r3;
    r1 += 0x44;
    r7 = 0x10;
    r0 = r7;
    r1 = *(u16 *)r1;
    r0 &= r1;
    if (r0 == 0) goto L_0800C52A;
    r0 = r3;
    r0 += 0x56;
    r1 = 0;
    r2 = *(s16 *)(r0 + r1);
    if ((s32)r4 < (s32)-(r2)) {
        r0 = 0x15E;
        r4 = r0 - r2;
    }
    if ((s32)r4 < 0) {
        r4 += 0xFA;
    }
    r0 = r3;
    r0 += 0x54;
    r2 = 0;
    r0 = *(s16 *)(r0 + r2);
    r4 += r0;
    r1 = r3;
    r1 += 0x58;
    r3 = 0;
    r0 = *(s16 *)(r1 + r3);
    if ((s32)r4 <= (s32)r0) goto L_0800C52A;
    r0 = r5;
    r0 += 0x28;
    r3 = r6 + r0;
    r2 = *(u32 *)r3;
    r0 = 0x780;
    if ((s32)r2 <= (s32)r0) goto L_0800C52A;
    r0 = r2;
    r0 -= 0x40;
    *(u32 *)r3 = r0;
    r0 = 0;
    r4 = *(s16 *)(r1 + r0);
    r1 = sp00;
    if (r1 != 0) goto L_0800C52A;
    r6 = r5;
    r6 += 0x40;
    r2 = 0;
    r0 = *(s16 *)(r6 + r2);
    if (r0 != 0) goto L_0800C52A;
    r0 = 0xE;
    r1 = 1;
    func_0801604C(r0, r1);
    r0 = 0x40;
    *(u16 *)r6 = (u16)r0;
    r3 = 0x3C;
    r0 = *(s16 *)(r5 + r3);
    if (r0 != 0) goto L_0800C52A;
    *(u16 *)(r5 + 0x3C) = (u16)r7;
    r0 = *(u32 *)(r5 + 0x20);
    r2 = 0x1000;
    r1 = r0 + r2;
    r3 = 0x3FFF;
    r2 = r3;
    r1 &= r2;
    *(u16 *)(r5 + 0x3A) = (u16)r1;
    r0 &= r2;
    *(u16 *)(r5 + 0x3E) = (u16)r0;
L_0800C52A:
    r1 = (u32)g_03001E60;
    r0 = 0x64;
    r2 = sp00;
    r0 *= r2;
    r3 = r0 + r1;
    r0 = r3;
    r0 += 0x44;
    r2 = *(u16 *)r0;
    r0 = 0x20;
    r0 &= r2;
    r5 = r1;
    if (r0 != 0) goto L_0800C56A;
    r0 = 0x10;
    r0 &= r2;
    if (r0 != 0) goto L_0800C56A;
    r0 = r3;
    r0 += 0x56;
    r3 = 0;
    r0 = *(s16 *)(r0 + r3);
    r1 = -r0;
    if ((s32)r4 < (s32)r1) {
        r4 = r1;
    }
    if ((s32)r4 > (s32)r0) {
        r4 = r0;
    }
    r3 = (s32)r4 >> 2;
    if (r4 == 0) goto L_0800C56A;
    r4 -= r3;
L_0800C56A:
    r8 = r5;
    r0 = 0x64;
    r1 = sp00;
    r5 = r1;
    r5 *= r0;
    r0 = r8;
    r0 += 0x30;
    r0 = r5 + r0;
    *(u32 *)r0 = r4;
    r2 = r8;
    r7 = r5 + r2;
    r0 = r7;
    r0 += 0x56;
    r3 = 0;
    r0 = *(s16 *)(r0 + r3);
    r1 = -r0;
    if ((s32)r4 < (s32)r1) {
        r4 = r1;
    }
    if ((s32)r4 > (s32)r0) {
        r4 = r0;
    }
    r0 = r8;
    r0 += 0x28;
    r0 += r5;
    r10 = r0;
    r0 = *(u32 *)r0;
    r3 = r8;
    r3 += 0x20;
    if ((s32)r0 < 0) {
        r4 = -r4;
        r4 = (s32)r4 >> 1;
        r2 = r5 + r3;
        r1 = (s32)r4 >> 3;
        r0 = *(u32 *)r2;
        r0 -= r1;
        r1 = 0x3FFF;
        r0 &= r1;
        *(u32 *)r2 = r0;
    }
    r1 = r10;
    r0 = *(u32 *)r1;
    if ((s32)r0 > 0) {
        r4 = (s32)r4 >> 1;
        r2 = r5 + r3;
        r1 = (s32)r4 >> 3;
        r0 = *(u32 *)r2;
        r0 -= r1;
        r1 = 0x3FFF;
        r0 &= r1;
        *(u32 *)r2 = r0;
    }
    r6 = r5 + r3;
    r0 = *(u32 *)r6;
    r3 = 0x38;
    r2 = *(s16 *)(r7 + r3);
    r1 = 0x03006874 /* IWRAM */;
    r9 = r1;
    r3 = *(u32 *)0x03006874 /* IWRAM */;
    r1 = r2 << 3;
    r1 -= r2;
    r1 <<= 2;
    r1 += r3;
    r1 = *(u16 *)(r1 + 0xC);
    r2 = 0x1000;
    r1 += r2;
    r3 = 0x3FFF;
    r1 &= r3;
    r0 = func_08014614(r0, r1);
    r3 = r0;
    r0 = 0x1FFF;
    if ((s32)r3 > (s32)r0) {
        r1 = 0xFFFFE000;
        r3 += r1;
    }
    r0 = 0xFFFFF1F0;
    if ((s32)r3 < (s32)r0) {
        r2 = 0x38;
        r1 = *(s16 *)(r7 + r2);
        r0 = r9;
        r2 = *(u32 *)r0;
        r0 = r1 << 3;
        r0 -= r1;
        r0 <<= 2;
        r0 += r2;
        r0 = *(u16 *)(r0 + 0xC);
        r1 = 0x1E0E;
        r0 += r1;
        *(u32 *)r6 = r0;
    }
    r0 = 0xE10;
    if ((s32)r3 > (s32)r0) {
        r2 = 0x38;
        r1 = *(s16 *)(r7 + r2);
        r3 = r9;
        r2 = *(u32 *)r3;
        r0 = r1 << 3;
        r0 -= r1;
        r0 <<= 2;
        r0 += r2;
        r0 = *(u16 *)(r0 + 0xC);
        r1 = 0x1F2;
        r0 += r1;
        *(u32 *)r6 = r0;
    }
    r1 = *(u32 *)r6;
    r2 = 0x3FFF;
    r1 &= r2;
    *(u32 *)r6 = r1;
    r6 = r8;
    r6 += 0x34;
    r5 += r6;
    r0 = *(u32 *)r5;
    r0 = (s32)r0 >> 3;
    r0 = func_08014614(r0, r1);
    r3 = r0;
    r0 = 0x1FFF;
    if ((s32)r3 > (s32)r0) {
        r1 = 0xFFFFC000;
        r3 += r1;
    }
    r3 <<= 3;
    r0 = *(u32 *)r5;
    r0 += r3;
    r1 = 0x1FFFF;
    r0 &= r1;
    *(u32 *)r5 = r0;
    r3 = 0;
    r2 = 0x190;
    if ((s32)r4 > (s32)r2) {
        r3 = 0xFFFFFE70;
        r0 = r4 + r3;
        r0 = (s32)r0 >> 1;
        r3 = r10;
        r1 = *(u32 *)r3;
        r0 *= r1;
        r3 = (s32)r0 >> 14;
    }
    r0 = 0xFFFFFE70;
    if ((s32)r4 < (s32)r0) {
        r0 = r4 + r2;
        r0 = (s32)r0 >> 1;
        r4 = r10;
        r1 = *(u32 *)r4;
        r0 *= r1;
        r3 = (s32)r0 >> 14;
    }
    r0 = 0x64;
    r1 = sp00;
    r2 = r1;
    r2 *= r0;
    r4 = r8;
    r0 = r2 + r4;
    r1 = r0;
    r1 += 0x4E;
    r4 = 0;
    r0 = *(s16 *)(r1 + r4);
    if ((s32)r3 > (s32)r0) {
        r0 = *(u16 *)r1;
        r0 += 1;
        *(u16 *)r1 = (u16)r0;
    }
    r4 = 0;
    r0 = *(s16 *)(r1 + r4);
    if ((s32)r3 < (s32)r0) {
        r0 = *(u16 *)r1;
        r0 -= 1;
        *(u16 *)r1 = (u16)r0;
    }
    r0 = 0x030021D4 /* IWRAM */;
    r1 = *(u32 *)0x030021D4 /* IWRAM */;
    r3 = r0;
    if (r1 == 1) goto L_0800C6D4;
    goto L_0800C7FE;
L_0800C6D4:
    r0 = 0x030021CC /* IWRAM */;
    r1 = 0;
    r0 = *(s16 *)(r0 + r1);
    if (r0 == 0) goto L_0800C6E0;
    goto L_0800C7FE;
L_0800C6E0:
    r0 = r2 + r6;
    r1 = *(u32 *)r0;
    r1 = (s32)r1 >> 3;
    r0 = 0x2000;
    r0 -= r1;
    r2 = 0x3FFF;
    r0 &= r2;
    r4 = 0x03002E40 /* IWRAM */;
    r1 = *(u32 *)0x03002E44 /* IWRAM */;
    r0 = func_08014614(r0, r1);
    r3 = r0;
    r0 = 0x3FFF;
    r3 &= r0;
    r1 = 0x1FFF;
    if ((s32)r3 > (s32)r1) {
        r0 = 0xFFFFC000;
        r3 += r0;
    }
    r0 = r3 + 4;
    if (r0 <= 8) goto L_0800C766;
    r3 = (s32)r3 >> 2;
    r0 = 0x3C;
    r0 = -r0;
    if ((s32)r3 < (s32)r0) {
        r3 = r0;
    }
    goto L_0800C75C;
L_0800C75C:
    if ((s32)r3 > 0x3C) {
        r3 = 0x3C;
    }
    r0 = *(u32 *)(r4 + 4);
    r0 -= r3;
    goto L_0800C778;
L_0800C766:
    if ((s32)r3 < 0) {
        r0 = *(u32 *)(r4 + 4);
        r0 += 1;
        *(u32 *)(r4 + 4) = r0;
    }
    if ((s32)r3 <= 0) goto L_0800C77A;
    r0 = *(u32 *)(r4 + 4);
    r0 -= 1;
L_0800C778:
    *(u32 *)(r4 + 4) = r0;
L_0800C77A:
    r6 = 0x03002E40 /* IWRAM */;
    r1 = *(u32 *)0x03002E44 /* IWRAM */;
    r0 = 0x1000;
    r0 -= r1;
    r7 = 0x3FFF;
    r0 &= r7;
    r2 = (u32)g_03001E60;
    r1 = 0x64;
    r3 = sp00;
    r1 *= r3;
    r4 = r1 + r2;
    r2 = 0x38;
    r1 = *(s16 *)(r4 + r2);
    r5 = 0x03006874 /* IWRAM */;
    r3 = *(u32 *)0x03006874 /* IWRAM */;
    r2 = r1 << 3;
    r2 -= r1;
    r2 <<= 2;
    r2 += r3;
    r1 = r7;
    r2 = *(u16 *)(r2 + 0xC);
    r1 &= r2;
    r0 = func_08014614(r0, r1);
    r3 = r0;
    r0 = 0x1FFF;
    if ((s32)r3 > (s32)r0) {
        r0 = 0xFFFFC000;
        r3 += r0;
    }
    r0 = 0xFFFFFD00;
    if ((s32)r3 < (s32)r0) {
        r2 = 0x38;
        r1 = *(s16 *)(r4 + r2);
        r2 = *(u32 *)r5;
        r0 = r1 << 3;
        r0 -= r1;
        r0 <<= 2;
        r0 += r2;
        r1 = 0xD00;
        r0 = *(u16 *)(r0 + 0xC);
        r1 -= r0;
        *(u32 *)(r6 + 4) = r1;
    }
    r0 = 0x300;
    if ((s32)r3 > (s32)r0) {
        r3 = 0x38;
        r1 = *(s16 *)(r4 + r3);
        r2 = *(u32 *)r5;
        r0 = r1 << 3;
        r0 -= r1;
        r0 <<= 2;
        r0 += r2;
        r1 = 0x1300;
        r0 = *(u16 *)(r0 + 0xC);
        r1 -= r0;
        *(u32 *)(r6 + 4) = r1;
    }
    r0 = *(u32 *)(r6 + 4);
    r0 &= r7;
    *(u32 *)(r6 + 4) = r0;
    r3 = 0x030021D4 /* IWRAM */;
L_0800C7FE:
    r0 = *(u32 *)r3;
    if (r0 == 0) {
        r2 = 0x03002E40 /* IWRAM */;
        r1 = (u32)g_03001E60;
        r0 = 0x64;
        r4 = sp00;
        r0 *= r4;
        r1 += 0x20;
        r0 += r1;
        r1 = *(u32 *)r0;
        r0 = 0x2000;
        r0 -= r1;
        r1 = 0x3FFF;
        r0 &= r1;
        *(u32 *)0x03002E44 /* IWRAM */ = r0;
    }
    return;
}
