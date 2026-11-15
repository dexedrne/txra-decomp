"""Structural classifiers use synthetic arrays; never serialize private assets."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path('tools').resolve()))
import structures as s
import struct
import unittest


def container(body):
    return b'NSP8'+struct.pack('<H',len(body)+8)+bytes(6)+body


class StructureTests(unittest.TestCase):
    def test_reverse_literal_exact_extent(self):
        data=container(b'abcd'+bytes([4]))
        decoded,size=s.reverse_decode(data,0,4)
        self.assertEqual(decoded,b'abcd')
        self.assertEqual(size,len(data))
        self.assertEqual(s.reverse_decode(container(b'a'+bytes([1])),0,1)[0],b'a')
    def test_reverse_repeat_and_both_copy_directions(self):
        # Commands consumed right to left: literal abcd at destination 8..11,
        # forward copy 8..11 into 7..4, backward copy 8..11 into 3..0.
        data=container(bytes([8,0,0x84,8,0,0xc4])+b'abcd'+bytes([4]))
        self.assertEqual(s.reverse_decode(data,0,12)[0],b'abcddcbaabcd')
        self.assertEqual(s.reverse_decode(container(bytes([77,0x48])),0,8)[0],b'M'*8)
    def test_reverse_rejects_uninitialized_and_bounds(self):
        cases=[(container(bytes([0,0,0x84])),4),
               (container(b'a'+bytes([2])),2),
               (container(bytes([77,0x48])),7),
               (container(bytes([0])),8),
               (container(b'abcd'+bytes([4])),5)]
        for data,length in cases:
            with self.subTest(length=length,data_size=len(data)):
                with self.assertRaises(ValueError):s.reverse_decode(data,0,length)
        with self.assertRaises(ValueError):s.reverse_decode(b'bad!',0,4)
    def test_bios_decoders_emit_exact_output(self):
        self.assertEqual(s.bios_decode(bytes([0x10,6,0,0,0x10,65,66,67,0,2]),0,10,'bios-lz77'),b'ABCABC')
        self.assertEqual(s.bios_decode(bytes([0x30,6,0,0,0x83,77]),0,6,'bios-rle'),b'M'*6)
        data=bytes([0x28,4,0,0,1,0xc0,65,66])+struct.pack('<I',0x50000000)
        self.assertEqual(s.bios_decode(data,0,12,'bios-huffman8'),b'ABAB')
        data=bytes([0x24,2,0,0,1,0xc0,1,2])+struct.pack('<I',0x50000000)
        self.assertEqual(s.bios_decode(data,0,12,'bios-huffman4'),bytes([0x21,0x21]))
        for fmt in ('bios-lz77','bios-rle'):
            with self.assertRaises(ValueError):s.bios_decode(bytes([0,8,0,0]),0,4,fmt)
    def test_raster_banks_require_three_distinct_bounded_sources(self):
        rom=bytearray(0x60000)
        struct.pack_into('<I',rom,0x18b0,s.BASE+0x20000)
        struct.pack_into('<3I',rom,0x20000,s.BASE+0x30000,s.BASE+0x40000,s.BASE+0x50000)
        self.assertEqual([b['size'] for b in s.raster_banks(rom)],[65536]*3)
        struct.pack_into('<I',rom,0x20008,s.BASE+0x60004)
        self.assertEqual(s.raster_banks(rom),[])
    def test_palette_requires_reference_alignment_and_all_15bit_words(self):
        rom=bytearray(2048)
        struct.pack_into('<I',rom,0xc0,s.BASE+1024)
        blocks=[{'offset':512,'size':509}]
        self.assertEqual(list(s.attached_palettes(rom,blocks))[0]['offset'],1024)
        struct.pack_into('<H',rom,1024+510,0x8000)
        self.assertEqual(list(s.attached_palettes(rom,blocks)),[])
        struct.pack_into('<H',rom,1024+510,0)
        struct.pack_into('<I',rom,0xc0,0)
        self.assertEqual(list(s.attached_palettes(rom,blocks)),[])
    def test_course_array_uses_literal_count_not_next_pointer(self):
        rom=bytearray(0x24000)
        struct.pack_into('<I',rom,0x7ce0,s.BASE+0x20000)
        struct.pack_into('<I',rom,0x7ce8,100)
        blocks=list(s.course_records(rom))
        self.assertEqual([(b['offset'],b['size'],b['count']) for b in blocks],[(0x20000,2800,100)])
        struct.pack_into('<I',rom,0x7ce8,8193)
        self.assertEqual(list(s.course_records(rom)),[])
    def test_reciprocal_requires_complete_symmetric_bounded_shape(self):
        rom=bytearray(0xa0000)
        struct.pack_into('<I',rom,0x164cc,s.BASE+0x20000)
        values=[0]+[-round(524288/i) for i in range(65535,0,-1)]+[524288]+[round(524288/i) for i in range(1,65536)]
        struct.pack_into('<131072i',rom,0x20000,*values)
        self.assertEqual(s.reciprocal_table(rom)[0]['size'],0x80000)
        struct.pack_into('<i',rom,0x20000+100*4,999999)
        self.assertEqual(s.reciprocal_table(rom),[])
    def test_raster_reciprocal_requires_every_entry_and_exact_end(self):
        rom=bytearray(0x4000)
        start=0x2000
        struct.pack_into('<I',rom,0x5d0,s.BASE+start)
        values=[65535]+[(32768+i//2)//i for i in range(1,1025)]+[0]
        struct.pack_into('<1026H',rom,start,*values)
        block=s.raster_reciprocal_table(rom)[0]
        self.assertEqual((block['offset'],block['size'],block['stride'],block['count']),(start,2050,2,1025))
        for index in (0,1,511,1024):
            damaged=bytearray(rom)
            struct.pack_into('<H',damaged,start+index*2,values[index]^1)
            self.assertEqual(s.raster_reciprocal_table(damaged),[])
        struct.pack_into('<H',rom,start+2050,(32768+1025//2)//1025)
        self.assertEqual(s.raster_reciprocal_table(rom),[])
    def test_raster_reciprocal_rejects_missing_pointer_and_truncation(self):
        self.assertEqual(s.raster_reciprocal_table(bytes(1024)),[])
        rom=bytearray(0x4000)
        for pointer in (0,s.BASE+0x2001,s.BASE+0x3f00):
            struct.pack_into('<I',rom,0x5d0,pointer)
            self.assertEqual(s.raster_reciprocal_table(rom),[])

if __name__=='__main__':unittest.main()
