extern void func_080144F4(void),func_08014518(void),func_08014420(void *,void *,u32);
extern u32 func_08005E84(void);
extern u8 g_03000DE8[],g_03005F64[],g_030014A4[],g_030001E0[],g_03005FA0[],g_03000B60[],g_03005680[],g_03001E60[];
extern u32 g_030021D4,g_03000DE4,g_03006870;
u32 func_08013B38(void) {
 u32 result; u8 *p,*q; TxraSaveBlock *block; TxraRecord *record; s32 i; u32 v;
 func_080144F4(); result=func_08005E84();
 if(result==0) {
 { u32 address=(u32)&gSaveStaging; address+=6;p=(u8 *)address; }
 func_08014420(p,g_03000DE8,8);p+=8;
 func_08014420(p,g_03005F64,2);p+=2;
 func_08014420(p,g_030014A4,4);p+=4;
 func_08014420(p,g_030001E0,12);p+=12;
 func_08014420(p,g_03005FA0,30);p+=30;
 func_08014420(p,g_03000B60,128);p+=128;
 q=g_03005680;
 for(i=127;i>=0;i--) {*q=*p++; q+=2;}
 record=(TxraRecord *)g_03001E60; v=*p; record->field_02=v; p++; *(u16 *)((u8 *)record+702)=v;
 g_030021D4=*p++;g_03000DE4=*p;g_03006870=p[1];
 }
 func_08014518();return result;
}
