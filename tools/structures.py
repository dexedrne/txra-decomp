"""Cartridge-specific structural proofs. Returns metadata; decoded bytes stay local."""
import struct
BASE = 0x08000000


def reverse_decode(rom, offset, output_size):
    """Decode the byte commands at 0801251C, with checked initialized copies.

    The caller supplies the destination size, just as guest r2 does. The first
    four bytes identify this container; +4 is the last-command displacement
    minus three. The six prefix bytes after that field are not commands.
    """
    if output_size <= 0 or output_size > 0x40000 or offset < 0 or offset+12 > len(rom):
        raise ValueError('invalid reverse block bounds')
    if rom[offset:offset+4] != b'NSP8':
        raise ValueError('unknown reverse container')
    end = offset+struct.unpack_from('<H', rom, offset+4)[0]+4
    if not offset+12 < end <= len(rom):
        raise ValueError('invalid encoded extent')
    source, dest = end-1, output_size-1
    output = bytearray(output_size)
    initialized = bytearray(output_size)
    def take():
        nonlocal source
        if source < offset+12: raise ValueError('truncated command')
        value = rom[source]; source -= 1
        return value
    first=True
    while first or dest > 0:  # do/while, signed comparison at 080125F0
        first=False
        token = take(); kind, count = token >> 6, token & 63
        if not count or count > dest+1: raise ValueError('empty/overrun command')
        if kind in (2, 3):
            high, low = take(), take(); index = high*256+low
            indices = range(index, index+count) if kind == 3 else range(index+count-1, index-1, -1)
            for index in indices:
                if not 0 <= index < output_size or not initialized[index]:
                    raise ValueError('copy from uninitialized output')
                output[dest] = output[index]; initialized[dest] = 1; dest -= 1
        elif kind == 1:
            value = take()
            for _ in range(count):
                output[dest] = value; initialized[dest] = 1; dest -= 1
        else:
            for _ in range(count):
                output[dest] = take(); initialized[dest] = 1; dest -= 1
    if dest != -1 or source != offset+11:
        raise ValueError('incomplete output or trailing commands')
    return bytes(output), end-offset


def course_records(rom):
    """Six literal-selected arrays; count is installed beside the base pointer."""
    for pointer_slot, count_slot in ((0x7ce0,0x7ce8),(0x7d08,0x7d10),
                                   (0x7d30,0x7d38),(0x7d58,0x7d60),
                                   (0x7d78,0x7d80),(0x815c,0x8164)):
        if count_slot+4 > len(rom): continue
        start = struct.unpack_from('<I',rom,pointer_slot)[0]-BASE
        count = struct.unpack_from('<I',rom,count_slot)[0]
        if 0x20000 <= start < len(rom) and 32 <= count <= 8192 and start+count*28 <= len(rom):
            yield dict(offset=start,size=count*28,type='table',format='course-records-stride28',
                       stride=28,count=count,
                       evidence=f'Literal {BASE+pointer_slot:08X} selects base; {BASE+count_slot:08X} supplies wrap count; 08007E94-08007EA2 and 080029F0-08002A00 index 28-byte records.')


def reverse_blocks(rom):
    """Only referenced containers with independently supplied output sizes."""
    candidates = {}
    # Car selection IDs 16..31 select sixteen source literals at 080085E0;
    # 08008662-0800866C supplies r2=65536 to the byte decoder.
    for slot in range(0x8680,0x86c0,4):
        if slot+4 <= len(rom):
            candidates[struct.unpack_from('<I',rom,slot)[0]-BASE] = (65536,slot,'08008662-0800866C')
    # Screen callers all supply 0x9600; the larger panel supplies a literal size.
    for slot, size, caller in ((0xd74c,62880,'0800D674-0800D67C'),
          (0xd758,38400,'0800D680-0800D68A'),(0xd760,38400,'0800D69A-0800D6A0'),
          (0xf198,38400,'0800F17C-0800F18C'),(0xf1f4,38400,'0800F1CC-0800F1D4'),(0xf270,38400,'0800F226-0800F230'),
          (0x12c6c,38400,'08012B7C-08012B84'),(0x12e64,38400,'08012DC8-08012DD2'),
          (0x13068,38400,'08012FC8-08012FD2'),(0x13460,38400,'0801321C-08013222'),
          (0x13908,38400,'0801389A-080138A6')):
        if slot+4 <= len(rom): candidates[struct.unpack_from('<I',rom,slot)[0]-BASE] = (size,slot,caller)
    for offset,(size,slot,caller) in sorted(candidates.items()):
        try: decoded, encoded = reverse_decode(rom,offset,size)
        except ValueError: continue
        yield dict(offset=offset,size=encoded,type='compressed',format='custom-reverse-byte-lz-rle',
                   decompressed_size=len(decoded),pointer_slot=slot,
                   evidence=f'Caller {caller}, source literal {BASE+slot:08X}; complete checked decode of 0801251C commands; every copy reads initialized output, exact source/output end.')


def structures(rom):
    blocks=list(reverse_blocks(rom))
    return list(course_records(rom))+blocks+reciprocal_table(rom)+raster_reciprocal_table(rom)+list(attached_palettes(rom,blocks))+raster_banks(rom)


def raster_reciprocal_table(rom):
    """Prove the complete halfword edge-slope table, excluding its aligner.

    The shared rasterizer literal supplies the base. Every nonzero entry must
    match the rounded Q15 reciprocal, with the zero-index saturation sentinel.
    Refuse a matching prefix of a longer sequence: the next halfword must break
    the formula. This is a data-format proof, not function-discovery evidence.
    """
    if len(rom) < 0x5d4: return []
    start=struct.unpack_from('<I',rom,0x5d0)[0]-BASE
    count=1025
    if start<0xc0 or start%2 or start+(count+1)*2>len(rom): return []
    values=struct.unpack_from('<1026H',rom,start)
    if values[0]!=65535: return []
    for index in range(1,count):
        if values[index]!=(32768+index//2)//index: return []
    if values[count]==(32768+count//2)//count: return []
    return [dict(offset=start,size=count*2,type='table',format='unsigned-q15-raster-reciprocal',
                 stride=2,count=count,
                 evidence='080003BC-080003C4 loads the shared table and reads a halfword at twice the edge-height index; the sibling rasterizers share the base. All 1024 positive-index entries exactly equal the nearest integer to 32768/index; the zero sentinel and first nonmatching following halfword are checked. The following alignment halfword is excluded.')]


def reciprocal_table(rom):
    """Prove the signed Q19 projection lookup, including its complete shape."""
    if len(rom) < 0x164d0: return []
    start = struct.unpack_from('<I',rom,0x164cc)[0]-BASE
    count = 0x20000
    if start < 0x20000 or start+count*4 > len(rom): return []
    values = struct.unpack_from('<'+str(count)+'i',rom,start)
    middle = 0x10000
    if values[0] != 0 or values[middle] != 0x80000: return []
    for i in range(1,middle):
        value = values[middle+i]
        if value <= 0 or abs(value*i-0x80000) > i or values[middle-i] != -value:
            return []
        if i>1 and value>values[middle+i-1]: return []
    return [dict(offset=start,size=count*4,type='table',format='signed-q19-reciprocal-lookup',
                 stride=4,count=count,
                 evidence='08016452-0801645E and 080167F4-080167FC index signed depth/2 + 65536, read a word, multiply projected coordinates; all 65535 nonzero pairs are antisymmetric, positive half monotone, each within one integer unit of 524288/index; boundary and zero sentinels checked.')]


def bios_decode(rom, offset, encoded_size, fmt):
    """Decode a previously validated BIOS stream, retaining no payload on disk."""
    limit=offset+encoded_size
    total=int.from_bytes(rom[offset+1:offset+4],'little')
    output=bytearray();p=offset+4
    def take():
        nonlocal p
        if p>=limit:raise ValueError('truncated BIOS source')
        value=rom[p];p+=1;return value
    if fmt=='bios-lz77':
        while len(output)<total:
            flags=take()
            for bit in range(7,-1,-1):
                if len(output)==total:break
                if flags & (1<<bit):
                    a,b=take(),take();count=(a>>4)+3;back=((a&15)<<8|b)+1
                    if back>len(output) or len(output)+count>total:raise ValueError('invalid LZ copy')
                    for _ in range(count):output.append(output[-back])
                else:output.append(take())
    elif fmt=='bios-rle':
        while len(output)<total:
            control=take();count=(control&127)+(3 if control&128 else 1)
            if len(output)+count>total:raise ValueError('RLE overrun')
            if control&128:output.extend(bytes([take()])*count)
            else:output.extend(take() for _ in range(count))
    elif fmt in ('bios-huffman4','bios-huffman8'):
        tree_start=p;tree_end=tree_start+(take()+1)*2;root=tree_start+1
        if tree_end>limit:raise ValueError('truncated tree')
        p=tree_end;node=root;bits=word=0;symbols=[]
        wanted=total*(2 if fmt.endswith('4') else 1)
        while len(symbols)<wanted:
            if not bits:
                word=sum(take()<<(8*i) for i in range(4));bits=32
            bits-=1;side=word>>bits&1;value=rom[node]
            child=(node&~1)+((value&63)+1)*2+side
            if not root<=child<tree_end:raise ValueError('tree edge out of bounds')
            if value&(0x40 if side else 0x80):
                symbols.append(rom[child]);node=root
            else:node=child
        if fmt.endswith('4'):
            if any(v>15 for v in symbols):raise ValueError('invalid nibble')
            output.extend(symbols[i]|symbols[i+1]<<4 for i in range(0,len(symbols),2))
        else:output.extend(symbols)
    else:raise ValueError('unknown BIOS format')
    if len(output)!=total or p!=limit:raise ValueError('BIOS source/output extent mismatch')
    return bytes(output)


def attached_palettes(rom, blocks):
    """Referenced 256-color arrays immediately following decoded containers."""
    references={}
    for slot in range(0xc0,len(rom)-3,4):
        target=struct.unpack_from('<I',rom,slot)[0]-BASE
        if 0<=target<len(rom):references.setdefault(target,slot)
    for block in blocks:
        start=(block['offset']+block['size']+3)&~3
        if start not in references or start+512>len(rom):continue
        colors=struct.unpack_from('<256H',rom,start)
        if any(color&0x8000 for color in colors):continue
        yield dict(offset=start,size=512,type='graphics',format='attached-palette-bgr555-256',
                   count=256,stride=2,pointer_slot=references[start],
                   evidence=f'Aligned trailer of checked indexed-byte container at {BASE+block["offset"]:08X}; independent ROM reference at {BASE+references[start]:08X}; all 256 halfwords satisfy 15-bit color bounds. Palette source references include the screen DMA setup at 0800F190 and per-car selection table at 08020DA8.')


def raster_banks(rom):
    """Contiguous full texture banks selected by the software rasterizer."""
    if len(rom)<0x18b4:return []
    table=struct.unpack_from('<I',rom,0x18b0)[0]-BASE
    if not 0x20000<=table<len(rom)-80:return []
    targets=struct.unpack_from('<20I',rom,table)
    if any(target and not BASE+0x20000<=target<BASE+len(rom) for target in targets):return []
    # Small standalone sources (e.g. the shadow) have restricted UVs; do not
    # extrapolate them to 64 KiB merely from the rasterizer's address space.
    banks=sorted({target for target in targets if target and (target-targets[0])%65536==0})
    if len(banks)<3 or banks[-1]-banks[0]!=(len(banks)-1)*65536:return []
    if banks[-1]-BASE+65536>len(rom):return []
    return [dict(offset=target-BASE,size=65536,type='graphics',format='software-raster-index8-bank',
                 width=256,height=256,stride=256,pointer_slot=table+targets.index(target)*4,
                 evidence=f'ROM source pointer {BASE+table+targets.index(target)*4:08X}, rasterizer table literal 080018B0; {len(banks)} ROM targets form consecutive 65536-byte banks. 08001840-08001860 extracts two unsigned 8-bit coordinates, reads source[y*256+x] as bytes and packs two pixels to the framebuffer. Small isolated sources are excluded; this does not imply tile ordering.') for target in banks]
