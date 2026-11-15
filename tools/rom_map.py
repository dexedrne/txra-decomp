#!/usr/bin/env python3
"""Evidence-based metadata map. Never emits ROM bytes or decoded content."""
import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path

from structures import structures, bios_decode

BASE = 0x08000000

# A range's format selects its evidence line; more specific structural proofs
# include source sites and exact extents in structures.json.
FORMAT_EVIDENCE = {
    'unclassified':'No validated extent or format; deliberately unknown.',
    'observed-rom-read':'Exact ROM-byte read union in fingerprint-checked guest coverage; no neighboring extent inferred.',
    'cartridge-header':'Fixed cartridge header offsets, checksum and reset branch.',
    'arm':'Recursive ARMv4T instruction descent, with observed-PC confirmation where executed.',
    'thumb':'Recursive ARMv4T instruction descent, with observed-PC confirmation where executed.',
    'literal-pool-or-switch':'PC-relative load resolution or bounded recovered switch table in the disassembly inventory.',
    'rom-pointer-array':'At least three adjacent aligned words each address this ROM; this classifies slots, not targets.',
    'ascii-null-terminated':'ROM-referenced printable ASCII run of at least eight bytes, terminated by zero; contents never serialized.',
    'ff':'At least 64 consecutive FF bytes; constant fill, not a claim of unused padding.',
    'terminal-zero':'At least 64 consecutive zero bytes at the image end.',
    'palette-bgr555':'Exact ROM-to-palette hardware transfer source.',
    'oam-attributes':'Exact ROM-to-OAM hardware transfer source.',
    'vram-transfer-format-unresolved':'Exact ROM-to-VRAM transfer; tile order, bit depth and map interpretation unresolved.',
    'cpuset-source':'Exact BIOS copy source extent, with fill/rounding accounted for.',
    'dma-source':'Exact aligned DMA source extent recorded by guest hardware logging.',
    'custom-sample-descriptor16':'Mixer 08007780 indexes 16-byte records; 0800733C reads declared sample length.',
    'custom-sample-descriptor20':'Refill routine 080062C0 consumes 20-byte records and 176-sample periods or pitched source limit.',
    'signed-pcm8-declared-extent':'Complete in-ROM source extent declared by a validated custom mixer descriptor.',
    'pcm8-wave-header-and-samples':'Validated sample header reached through a bounded tone entry.',
    'tone-entry-candidate':'Bounded tone parameters and valid referenced PCM header; candidate semantics retained.',
    'song-header-track-pointer-table':'Bounded track count, ROM voice pointer and track pointers, with a validated sample header.',
    'alignment-halfword':'Unreached two-byte gap inside the program enclosure, after code or a pool and before a word-aligned pool or instruction span; zero or Thumb no-operation aligner.',
    'code-entry-pointer-array':'Run of at least three adjacent aligned words, each addressing a distinct mapped function entry (ROM or unique copied-RAM alias); only previously unknown slots are labelled.',
}
PROGRAM_END = 0x18EC4  # end of the IRQ callback table; the program enclosure is fully mapped before it
for name in ('bios-lz77','bios-rle','bios-huffman4','bios-huffman8'):
    FORMAT_EVIDENCE[name]='Referenced BIOS container; complete checked decode, exact consumed source and output sizes.'
for name in ('course-records-stride28','custom-reverse-byte-lz-rle','signed-q19-reciprocal-lookup','unsigned-q15-raster-reciprocal',
             'attached-palette-bgr555-256','software-raster-index8-bank'):
    FORMAT_EVIDENCE[name]='Range-specific consumer sites, dimensions/counts and validation in docs/map/structures.json.'


def compressed_size(rom, offset):
    """Validate a complete BIOS LZ/RLE/Huffman stream; return encoded size/format.

    Length is the consumed source extent, NOT the uncompressed header length.
    Bounds, backward references, tree edges and output limits are checked.
    """
    try:
        kind = rom[offset]
        total = int.from_bytes(rom[offset+1:offset+4], 'little')
        if offset+4 > len(rom) or not 1 <= total <= 0x400000:
            return None
        p, produced = offset+4, 0
        def byte():
            nonlocal p
            v = rom[p]
            p += 1
            return v
        if kind == 0x10:
            while produced < total:
                flags = byte()
                for bit in range(7, -1, -1):
                    if produced >= total:
                        break
                    if flags & (1 << bit):
                        a, b = byte(), byte()
                        length, back = (a >> 4)+3, ((a & 15) << 8 | b)+1
                        if back > produced or produced+length > total:
                            return None
                        produced += length
                    else:
                        byte()
                        produced += 1
            fmt = 'bios-lz77'
        elif kind == 0x30:
            while produced < total:
                control = byte()
                length = (control & 127) + (3 if control & 128 else 1)
                if produced+length > total:
                    return None
                for _ in range(1 if control & 128 else length):
                    byte()
                produced += length
            fmt = 'bios-rle'
        elif kind in (0x24, 0x28):
            tree_size = (byte()+1)*2
            tree_start, tree_end = p-1, p-1+tree_size
            if tree_end > len(rom):
                return None
            node, p, word, bits = tree_start+1, tree_end, 0, 0
            symbols, wanted = 0, total*(2 if kind == 0x24 else 1)
            while symbols < wanted:
                if not bits:
                    if p+4 > len(rom):
                        return None
                    word = struct.unpack_from('<I', rom, p)[0]
                    p += 4
                    bits = 32
                bits -= 1
                side = (word >> bits) & 1
                value = rom[node]
                child = (node & ~1) + ((value & 63)+1)*2 + side
                if not tree_start+1 <= child < tree_end:
                    return None
                if value & (0x40 if side else 0x80):
                    if kind == 0x24 and rom[child] > 15:
                        return None
                    symbols += 1
                    node = tree_start+1
                else:
                    node = child
            fmt = 'bios-huffman4' if kind == 0x24 else 'bios-huffman8'
        else:
            return None
        return p-offset, fmt
    except (IndexError, struct.error):
        return None


def pcm_size(rom, offset):
    if offset < 0 or offset+16 > len(rom) or offset & 3:
        return None
    kind, status, frequency, loop, size = struct.unpack_from('<HHIII', rom, offset)
    if kind != 0 or status not in (0, 0x4000) or not 1024 <= frequency <= 96000*1024:
        return None
    if not 16 <= size <= 0x200000 or offset+16+size > len(rom) or loop > size:
        return None
    return 16+size


def fill_runs(rom, minimum=64):
    """Only FF runs and terminal zero padding; interior zero data is not fill."""
    p = 0
    while p < len(rom):
        if rom[p] != 255:
            p += 1
            continue
        end = p+1
        while end < len(rom) and rom[end] == 255:
            end += 1
        if end-p >= minimum:
            yield p, end-p, 'ff'
        p = end
    end = len(rom)
    while end and rom[end-1] == 0:
        end -= 1
    if len(rom)-end >= minimum:
        yield end, len(rom)-end, 'terminal-zero'


def entry_pointer_values(functions, base=BASE):
    """Word values that address a mapped entry: ROM Thumb (odd), ROM ARM, and copied-RAM aliases."""
    values = {}
    for f in functions or []:
        start = int(f['start'], 16)
        thumb = f['mode'] == 'thumb'
        values[start | 1 if thumb else start] = start
        for alias in f.get('runtime_aliases', []):
            a = int(alias['start'], 16)
            values[a | 1 if thumb else a] = start
    return values


def refine_unknown_mask(rom, mask, unknown_tag, tag_for, splits, functions, base=BASE):
    """Two reviewed rules for bytes the overlay leaves unknown. Only unknown bytes change."""
    starts = {int(r['start'], 16)-base for r in splits if r['kind'] in ('literal', 'arm', 'thumb')}
    for p in range(0, min(PROGRAM_END, len(rom))-1, 2):
        if (mask[p] == unknown_tag and mask[p+1] == unknown_tag and (p+2) % 4 == 0 and p
                and mask[p-1] != unknown_tag and p+2 in starts and rom[p:p+2] in (b'\0\0', b'\xc0\x46')):
            mask[p] = mask[p+1] = tag_for('fill', 'alignment-halfword')
    values = entry_pointer_values(functions, base)
    run = []
    def flush():
        if len(run) >= 3 and len({values[v] for _, v in run}) >= 3:
            tag = tag_for('table', 'code-entry-pointer-array')
            for q, _ in run:
                for i in range(q, q+4):
                    if mask[i] == unknown_tag:
                        mask[i] = tag
    for p in range(0, len(rom)-3, 4):
        v = struct.unpack_from('<I', rom, p)[0]
        if v in values:
            run.append((p, v))
        else:
            flush(); run = []
    flush()


def spans_from_mask(mask, labels):
    spans = []
    start = 0
    for end in range(1, len(mask)+1):
        if end == len(mask) or mask[end] != mask[start]:
            kind, fmt = labels[mask[start]]
            spans.append(dict(offset=start, size=end-start, type=kind, format=fmt))
            start = end
    return spans


def refine_spans(rom, spans, splits, functions, base=BASE):
    """Apply refine_unknown_mask to an existing partition (used when coverage captures are private)."""
    labels = []; ids = {}
    def tag_for(kind, fmt):
        if (kind, fmt) not in ids:
            ids[(kind, fmt)] = len(labels); labels.append((kind, fmt))
        return ids[(kind, fmt)]
    unknown = tag_for('unknown', 'unclassified')
    mask = bytearray(len(rom))
    for s in spans:
        mask[s['offset']:s['offset']+s['size']] = bytes([tag_for(s['type'], s.get('format', 'unclassified'))])*s['size']
    refine_unknown_mask(rom, mask, unknown, tag_for, splits, functions, base)
    return spans_from_mask(mask, labels)


def classify(rom, cfg, splits, traces, functions=None):
    """Priority overlay; each ROM byte appears in exactly one output span."""
    labels = [('unknown', 'unclassified')]
    ids = {labels[0]: 0}
    mask = bytearray(len(rom))
    def add(start, size, kind, fmt, overwrite=True):
        if start < 0 or size <= 0 or start+size > len(rom):
            raise ValueError('out-of-ROM block')
        key = (kind, fmt)
        if key not in ids:
            ids[key] = len(labels)
            labels.append(key)
        tag = ids[key]
        if overwrite:
            mask[start:start+size] = bytes([tag])*size
        else:
            for i in range(start, start+size):
                if not mask[i]: mask[i] = tag
    references = set()
    pointer_words = []
    for p in range(0xc0, len(rom)-3, 4):
        v = struct.unpack_from('<I', rom, p)[0]
        if BASE <= v < BASE+len(rom):
            references.add(v-BASE)
            pointer_words.append(p)
    for start, size, fmt in fill_runs(rom):
        add(start, size, 'fill', fmt)
    # Exact observed read bytes: these do not imply the extent of an asset.
    for trace in traces:
        if trace.get('overflow'):
            raise ValueError('coverage overflow')
        for start, size in trace['reads']:
            add(start, size, 'data', 'observed-rom-read')
        for kind, pc, src, dst, size in trace['transfers']:
            if 8 <= src >> 24 <= 12:
                off = src & 0x3fffff
                references.add(off)
                if off+size <= len(rom):
                    fmt = ('palette-bgr555' if dst >> 24 == 5 else
                           'oam-attributes' if dst >> 24 == 7 else
                           'vram-transfer-format-unresolved' if dst >> 24 == 6 else
                           'cpuset-source' if kind in (11, 12) else 'dma-source')
                    add(off, size, 'graphics' if dst >> 24 in (5, 6, 7) else 'data', fmt)
    # Pointer runs are tables, not an assertion about the pointed-to contents.
    group = []
    for p in pointer_words+[len(rom)+4]:
        if group and p != group[-1]+4:
            if len(group) >= 3:
                add(group[0], len(group)*4, 'table', 'rom-pointer-array')
            group = []
        group.append(p)
    for p in sorted(references):
        if p & 3 == 0:
            found = compressed_size(rom, p)
            if found:
                size, fmt = found
                bios_decode(rom, p, size, fmt)
                add(p, size, 'compressed', fmt)
    # This cartridge uses custom audio descriptors, established from the mixer:
    # 07780 indexes 16-byte records; 0733C reads byte length at +4, subtracts
    # four guard bytes, and shifts by 14 for the signed PCM mixer at 07924.
    # 062C0 uses 20-byte records; +4 counts 176-sample refill periods.
    for literal, stride in ((0x7ad4, 16), (0x62dc, 20)):
        if len(rom) < literal+4: continue
        table = struct.unpack_from('<I', rom, literal)[0]-BASE
        if not 0 <= table < len(rom): continue
        for i in range(256):
            entry = table+i*stride
            if entry+stride > len(rom): break
            ptr, length = struct.unpack_from('<II', rom, entry)
            if not BASE <= ptr < BASE+len(rom) or not 4 <= length <= len(rom): break
            if stride == 20:
                limit = struct.unpack_from('<I', rom, entry+16)[0]
                length = (limit+15)//16 if limit else length*176
            if not 1 <= length <= len(rom) or ptr-BASE+length > len(rom): break
            add(entry, stride, 'audio', 'custom-sample-descriptor'+str(stride))
            add(ptr-BASE, length, 'audio', 'signed-pcm8-declared-extent')
    # Sample headers are accepted only through valid 12-byte tone entries.
    sample_headers = set()
    for p in range(0xc0, len(rom)-11, 4):
        tone, key, length, pan, wave = struct.unpack_from('<BBBBI', rom, p)
        if tone not in (0, 8) or key > 127 or pan > 255 or not BASE <= wave < BASE+len(rom):
            continue
        sample = wave-BASE
        size = pcm_size(rom, sample)
        if size:
            sample_headers.add(sample)
            add(sample, size, 'audio', 'pcm8-wave-header-and-samples')
            add(p, 12, 'audio', 'tone-entry-candidate')
    # Song headers: all track pointers and voice pointer must be in ROM.
    for p in sorted(references):
        if p & 3 or p+12 > len(rom): continue
        tracks, blocks = rom[p], rom[p+1]
        if not 1 <= tracks <= 16 or blocks or p+8+tracks*4 > len(rom): continue
        voice = struct.unpack_from('<I', rom, p+4)[0]
        if not BASE <= voice < BASE+len(rom)-12: continue
        voice_wave = struct.unpack_from('<I', rom, voice-BASE+4)[0]-BASE
        if voice_wave not in sample_headers: continue
        pointers = struct.unpack_from('<'+'I'*tracks, rom, p+8)
        if all(BASE <= v < BASE+len(rom) for v in pointers):
            add(p, 8+tracks*4, 'audio', 'song-header-track-pointer-table')
    for p in sorted(references):
        end = p
        while end < min(len(rom), p+512) and 32 <= rom[end] < 127:
            end += 1
        if end-p >= 8 and end < len(rom) and rom[end] == 0:
            add(p, end-p+1, 'text', 'ascii-null-terminated')
    for block in structures(rom):
        add(block['offset'], block['size'], block['type'], block['format'])
    # Header, literal pools, switches and instruction spans override heuristics.
    add(4, 188, 'data', 'cartridge-header')
    for r in splits:
        start, end = int(r['start'], 16)-BASE, int(r['end'], 16)-BASE
        if r['kind'] == 'literal': add(start, end-start, 'table', 'literal-pool-or-switch')
        elif r['kind'] in ('arm', 'thumb'): add(start, end-start, 'code', r['kind'])
    # Executed ROM PCs (and established copied aliases) are conclusive code.
    for trace in traces:
        for pc, thumb in trace['pcs']:
            off = pc-BASE
            if not 0 <= off < len(rom):
                copies = [c for c in cfg['copies'] if c['run'] <= pc < c['run']+c['size']]
                if not copies: continue
                # Overlapping aliases must match the actually installed bytes;
                # static copy ranges alone cannot distinguish modifications.
                if len(copies) != 1: continue
                off = copies[0]['load']-BASE+pc-copies[0]['run']
            add(off, 2 if thumb else 4, 'code', 'thumb' if thumb else 'arm')
    def tag_for(kind, fmt):
        key = (kind, fmt)
        if key not in ids:
            ids[key] = len(labels)
            labels.append(key)
        return ids[key]
    if functions is not None:
        refine_unknown_mask(rom, mask, 0, tag_for, splits, functions)
    return spans_from_mask(mask, labels)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('coverage', nargs='*')
    parser.add_argument('--refine-diff', type=Path,
                        help='apply only the reviewed unknown-byte rules to the current partition; write a span diff')
    args = parser.parse_args()
    cfgpath = Path('tools/rom.cfg')
    cfg = json.loads(cfgpath.read_text())
    rom = Path('baserom.gba').read_bytes()
    if len(rom) != cfg['size'] or hashlib.sha1(rom).hexdigest() != cfg['sha1']:
        raise ValueError('wrong private ROM')
    fpath = Path('docs/map/functions.json')
    functions = json.loads(fpath.read_text())['functions'] if fpath.exists() else None
    splits = json.loads(Path('docs/map/splits.json').read_text())['regions']
    if args.refine_diff:
        if functions is None:
            raise SystemExit('docs/map/functions.json is required for --refine-diff')
        old = cfg['mapping']
        new = refine_spans(rom, old, splits, functions)
        key = lambda b: (b['offset'], b['size'], b['type'], b.get('format'))
        removed = sorted(set(map(key, old)) - set(map(key, new)))
        added = sorted(set(map(key, new)) - set(map(key, old)))
        diff = {'removed': [dict(zip(('offset', 'size', 'type', 'format'), r)) for r in removed],
                'added': [dict(zip(('offset', 'size', 'type', 'format'), a)) for a in added]}
        args.refine_diff.write_text(json.dumps(diff, indent=1)+'\n')
        moved = {}
        for a in diff['added']:
            moved[a['type']+':'+a['format']] = moved.get(a['type']+':'+a['format'], 0)+a['size']
        print(json.dumps({'removed': len(removed), 'added': len(added), 'bytes_by_new_label': moved}))
        return
    traces = [json.loads(Path(p).read_text()) for p in args.coverage]
    crc=f'{zlib.crc32(rom):08x}'
    for trace in traces:
        if trace.get('rom_crc32') != crc:
            raise ValueError('coverage fingerprint does not match the private ROM')
    cfg['mapping'] = classify(rom, cfg, splits, traces, functions)
    Path('docs/map/structures.json').write_text(json.dumps({'blocks':structures(rom)},indent=2)+'\n')
    sources=set()
    for trace in traces:
        for source, target in trace['branches']:
            pc=source&~1
            if not BASE <= pc < BASE+len(rom):
                copies=[c for c in cfg['copies'] if c['run'] <= pc < c['run']+c['size']]
                if len(copies)!=1: continue
                pc=copies[0]['load']+pc-copies[0]['run']
            sources.add(f'0x{pc:08X}')
    indirect=json.loads(Path('docs/map/indirect.json').read_text())
    sites={r['source'] for r in indirect['transfers']+indirect.get('veneer_calls',[])}
    cfg['indirect_sources_observed']=sorted(sources & sites)
    cfg['format_evidence']={b['format']:FORMAT_EVIDENCE[b['format']] for b in cfg['mapping']}
    mapping=cfg.pop('mapping')
    # One metadata block per line keeps the exact read partition reviewable.
    header=json.dumps(cfg,indent=2)
    cfgpath.write_text(header[:-2]+',\n  "mapping": [\n'+
                      ',\n'.join('    '+json.dumps(block,separators=(',',':')) for block in mapping)+
                      '\n  ]\n}\n')
    counts = {}
    for span in mapping:
        counts[span['type']] = counts.get(span['type'], 0)+span['size']
    summary={'complete':False,'rom_sha1':cfg['sha1'],'method':'Full-ROM pointer candidates and recursive ARMv4T descent; unique executed PC/read/transfer sets; validated typed structures.',
             'sessions':[], 'classified_bytes':counts}
    all_pcs=set();all_branches=set();reads=bytearray(len(rom))
    for path,trace in zip(args.coverage,traces):
        all_pcs.update(tuple(pc) for pc in trace['pcs'])
        all_branches.update(tuple(edge) for edge in trace['branches'])
        for start,size in trace['reads']:reads[start:start+size]=b'\1'*size
        statpath=Path(str(path).replace('-coverage.json','.json'))
        stats=json.loads(statpath.read_text()) if statpath.exists() else {}
        summary['sessions'].append({'name':Path(path).stem.removesuffix('-coverage'),
                                    'unique_pcs':len(trace['pcs']),'unique_branch_edges':len(trace['branches']),
                                    'unique_transfers':len(trace['transfers']),'semantic_entries':len(trace.get('entries',[])),**stats})
    summary.update(unique_executed_pcs=len(all_pcs),unique_branch_edges=len(all_branches),rom_read_bytes=sum(reads))
    Path('docs/map/coverage.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(counts))

if __name__ == '__main__': main()
