#ifndef TXRA_TYPES_H
#define TXRA_TYPES_H
/* Provisional layout at g_03001E60; field names record offsets only.
 * Evidence and access widths: docs/MATCH3-LAYOUTS.md. */
typedef struct {
    s16 field_00, field_02;
    s32 field_04, field_08, field_0c;
    u8 unknown_10[16];
    s32 field_20;
    s32 field_24;
    s32 field_28;
    u8 unknown_2c[4];
    s32 field_30;
    s32 field_34;
    s16 field_38;
    s16 field_3a;
    s16 field_3c;
    s16 field_3e;
    s16 field_40;
    s16 field_42;
    u16 field_44;
    u8 unknown_46[2];
    s16 field_48;
    s16 field_4a;
    s16 field_4c;
    s16 field_4e;
    s16 field_50;
    s16 field_52;
    s16 field_54;
    s16 field_56, field_58, field_5a;
    s16 field_5c, field_5e;
    s16 field_60, field_62;
} TxraRecord;
/* Both 08005DD4 and 08005F48 agree on three signed word components. */
typedef struct { s32 field_00, field_04, field_08; } TxraTriple;
/* 0800A5C4/08009F84: 28-byte rows, three initial signed words. */
typedef struct {
    s32 field_00, field_04, field_08;
    u16 field_0c;
    u8 field_0e, field_0f, field_10;
    u8 unknown_11[5];
    u8 field_16;
    u8 unknown_17[5];
} TxraRow28;
/* 0800761C: 20-byte rows; initial three words copied to parallel arrays. */
typedef struct {
    u32 field_00, field_04, field_08;
    u8 unknown_0c[8];
} TxraRow20;
/* 08015DA8 consumes 12-byte transfer entries; zero source terminates. */
typedef struct { u32 field_00, field_04, field_08; } TxraTransfer;
/* Byte record layouts used by the paired slot routines. */
typedef struct { u8 field_00, field_01; u8 unknown_02[14]; } TxraSlot16;
typedef struct { u8 field_00, field_01, field_02; u8 unknown_03[29]; } TxraSlot32;
/* 08013B38/08013C08 walk a 512-byte record after a six-byte header. */
typedef struct { u8 header[6]; u8 payload[506]; } TxraSaveBlock;
/* 080147D0 points the slot tables at +0x30/+0x40/+0x50 into two 72-byte
 * groups of three 24-byte buffers. */
typedef struct { u8 field_00[24], field_18[24], field_30[24]; } TxraLinkBuffers;
/* 08014988 and 080148B0 agree on packet pointer at 28, status bytes,
 * and signed word 14. Offset labels avoid protocol-name assumptions. */
typedef struct {
    u8 field_00,field_01,field_02,field_03;
    u32 field_04;
    u8 field_08,field_09,field_0a,field_0b;
    u8 unknown_0c[8];
    s32 field_14;
    u8 unknown_18[16];
    u8 * volatile field_28;
    u8 *field_2c;
    u8 *field_30[4],*field_40[4],*field_50[4];
    u8 field_60[24], field_78[24];
    TxraLinkBuffers field_90[2];
    u8 unknown_120[48];
} TxraLinkState;
/* 0801084C fills bytes 00/01/08/09 and text pointer 04 before 080154AC. */
typedef struct {
    u8 field_00, field_01, unknown_02[2];
    u8 *field_04;
    u8 field_08, field_09;
} TxraTextRecord;
/* 08005CF4 writes four affine coefficients in every fourth halfword;
 * 08015200 writes three attributes per eight-byte entry, and 08014E8C
 * transfers the 1024-byte shadow to hardware OAM. */
typedef struct { u16 attr0, attr1, attr2; s16 affine_parameter; } TxraOamEntry;
/* 08018A5C selects geometry; 08018AA4/08018B24 consume wait and bit fields. */
typedef struct {
    u32 field_00;
    u16 block_count, wait_control;
    u8 address_bits, unknown_09[3];
} TxraEepromGeometry;
/* 08005F8C initializes eight 72-byte voices; 08006712/08006740 use
 * that stride in the copied sound mixer. Control meanings stay provisional. */
typedef struct { s32 field_00, field_04, field_08, field_0c;
    s32 field_10, field_14, field_18, field_1c;
    s32 field_20, field_24, field_28, field_2c;
    s32 field_30, field_34, field_38, field_3c;
    s32 field_40, field_44;
} TxraSoundVoice;
/* Behavior-backed names; legacy address symbols remain valid aliases. */
extern TxraSaveBlock gSaveStaging;
extern u16 gKeysHeld;
extern u8 gOamShadow[];
extern TxraEepromGeometry *gEepromGeometry;
/* Shared address identities; semantics remain provisional. */
extern TxraRow20 g_083B8378[];
extern TxraRow28 *g_03006874;
extern TxraTriple g_03002E40;
extern TxraLinkState g_03007A30;
extern TxraTextRecord g_03002190;
#endif
