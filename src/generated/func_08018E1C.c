/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
void *func_08018E1C(void *dst0, const void *src0, u32 len0)
{
 char *dst=dst0;
 const char *src=src0;
 long *aligned_dst;
 const long *aligned_src;
 int len=len0;
 if (!(len < (sizeof(long)<<2)) && !(((long)src & (sizeof(long)-1)) | ((long)dst & (sizeof(long)-1)))) {
  aligned_dst=(long *)dst; aligned_src=(const long *)src;
  while (len >= (sizeof(long)<<2)) {
   *aligned_dst++=*aligned_src++;
   *aligned_dst++=*aligned_src++;
   *aligned_dst++=*aligned_src++;
   *aligned_dst++=*aligned_src++;
   len-=sizeof(long)<<2;
  }
  while (len >= sizeof(long)) { *aligned_dst++=*aligned_src++;len-=sizeof(long); }
  dst=(char *)aligned_dst;src=(const char *)aligned_src;
 }
 while(len--) *dst++=*src++;
 return dst0;
}
