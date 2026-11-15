#!/usr/bin/env python3
"""Bounded source-shape trials; no exported pseudocode or binary artifacts retained."""
import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'recomp')]
import draft
import measure_candidate as mc
import reloc

DEST = ROOT/'docs/near-misses/decomp-1112c'
WORK = ROOT/'build/decomp-1112c'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean(message):
    return str(message).replace(str(ROOT),'checkout').replace(str(Path.home()),'~')


class Search:
    def __init__(self, source, address, end, profile, tag, check=None):
        self.source = Path(source)
        self.best = self.source.read_text()
        self.a, self.z = int(address, 16), int(end, 16)
        self.profile, self.tag, self.check = profile, tag, check
        self.program = draft.Program()
        self.table = reloc.symbols(self.program)
        self.want = self.program.rom[self.a-draft.BASE:self.z-draft.BASE]
        self.rows, self.seen, self.outputs = [], set(), set()
        self.score = 1 << 30
        WORK.mkdir(parents=True, exist_ok=True)
        DEST.mkdir(parents=True, exist_ok=True)
        self.trial('baseline', self.best)

    def trial(self, name, code):
        identity = sha(code.encode())
        if identity in self.seen:
            return
        self.seen.add(identity)
        row = dict(trial=name, source_sha256=identity)
        try:
            got, frame = mc.diagnostic_compile(code, 'func_%08X' % self.a,
                                               self.a, self.table, self.profile)
            distance = sum(x != y for x, y in zip(self.want, got)) + abs(len(self.want)-len(got))
            row.update(emitted_bytes=len(got), local_frame_bytes=frame,
                       different_bytes=distance, compiled_sha256=sha(got),
                       boundary_rejected=len(got)>len(self.want))
            self.outputs.add(row['compiled_sha256'])
            if len(got) <= len(self.want) and distance < self.score:
                path = WORK/(self.tag+'-trial.c')
                path.write_text(code)
                if self.check:
                    try:
                        receipt = self.check(path)
                    except Exception as exc:
                        row['fixture_rejected'] = clean(exc)[:300]
                        self.rows.append(row)
                        self.save()
                        return
                    row['fixtures_passed'] = receipt
                self.best, self.score = code, distance
                row['retained'] = True
                (WORK/(self.tag+'-best.c')).write_text(code)
                print(self.tag, len(self.rows), name, distance, len(got), frame, flush=True)
        except Exception as exc:
            row['compile_error'] = type(exc).__name__
        self.rows.append(row)
        if len(self.rows) % 20 == 0:
            self.save()

    def save(self):
        with gzip.open(DEST/(self.tag+'-search.json.gz'), 'wt') as f:
            json.dump(dict(profile=self.profile, address='%08X'%self.a,
                           target_end='%08X'%self.z, trials=self.rows), f, separators=(',', ':'))
        (DEST/(self.tag+'-search-summary.json')).write_text(json.dumps(dict(
            source_identities=len(self.seen), measured=sum('compiled_sha256' in r for r in self.rows),
            output_identities=len(self.outputs), compile_failures=sum('compile_error' in r for r in self.rows),
            boundary_rejections=sum(r.get('boundary_rejected',False) for r in self.rows),
            improvements=[{k:v for k,v in r.items() if k!='fixtures_passed'} for r in self.rows if r.get('retained')],
            best_different_bytes=self.score), indent=2)+'\n')


def hud_check(path):
    spec = importlib.util.spec_from_file_location('hud_check', ROOT/'docs/near-misses/hud-owner-1109/check_source.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check(path)


def projected(code, mask):
    # Capture each point before its guard, keeping all calls and transforms ordered.
    rx = re.compile(r'if \((angle|size) > 0\) \{\s*x = g_030055F0\[(1|2)\].field_00;\s*y_projection = g_030055F0\[\2\].field_04;')
    for k,m in reversed(list(enumerate(rx.finditer(code)))):
        guard,point = m[1],int(m[2])
        if mask & (1 << k):
            text = 'x = g_030055F0[%d].field_00;\n y_projection = g_030055F0[%d].field_04;\n if (%s > 0) {'%(point,point,guard)
            code = code[:m.start()]+text+code[m.end():]
    return code


def flash_shape(code, mode):
    if 'HudFlash *flash' in code:
        return code
    a = code.index('    i = 0;\n    do {\n        if (g_03000AD0')
    z = code.index('    {\n        s32 c_projection;', a)
    body = code[a:z]
    body = body.replace('    i = 0;', '    {\n HudFlash *flash = g_03000AD0;\n i = 0;')
    for field, bit in [('active',1), ('x',2), ('y',4), ('size',8)]:
        if mode & bit:
            body = body.replace('g_03000AD0[i].'+field, 'flash->'+field)
    if mode & 16:
        body = body.replace('        if (', '        s32 *flash_size = &g_03000AD0[i].size;\n        if (',1)
        body = body.replace('g_03000AD0[i].size','(*flash_size)')
        body = body.replace('&(*flash_size)', '&g_03000AD0[i].size')
    body = body.replace('    } while (++i <= 7);', '        flash++;\n    } while (++i <= 7);\n }')
    return code[:a]+body+code[z:]


def smoke_shape(code, mode):
    if 'count_cursor' in code:
        return code
    a = code.index('    {\n        s32 c_split_smoke;')
    z = code.index('\ndone:;',a)
    body = code[a:z]
    body = body.replace('        i = 0;', '        s32 *count_cursor = &g_030067F0[0].count;\n s32 *z_cursor = &g_030067F0[0].z;\n i = 0;')
    body = body.replace('            if (g_030067F0[i].count == 0)\n                continue;', '            if (g_030067F0[i].count != 0) {')
    if mode & 1:
        body = body.replace('g_030067F0[i].count','(*count_cursor)')
    if mode & 2:
        body = body.replace('g_030067F0[i].z','(*z_cursor)')
    if mode & 4:
        body = body.replace('            g_030067F0[i].count--;', '            s32 *y_cursor = &g_030067F0[i].y;\n g_030067F0[i].count--;') if not mode & 1 else body.replace('            (*count_cursor)--;', '            s32 *y_cursor = &g_030067F0[i].y;\n (*count_cursor)--;')
        body = body.replace('g_030067F0[i].y','(*y_cursor)').replace('&(*y_cursor)','&g_030067F0[i].y')
    body = body.replace('        } while (++i <= 7);','            }\n count_cursor += 4;\n z_cursor += 4;\n        } while (++i <= 7);')
    return code[:a]+body+code[z:]


def hud():
    s = Search('docs/near-misses/hud-owner-1111/func_0800421C.c','0800421C','08005238','old','hud',hud_check)
    for round_index in range(3):
        start = s.score
        base = s.best
        for mask in range(16):
            s.trial('projected-captures-%d-%d'%(round_index,mask), projected(base,mask))
        base = s.best
        for mode in range(1,32):
            s.trial('flash-cursors-%d-%d'%(round_index,mode), flash_shape(base,mode))
        base = s.best
        for mode in range(1,8):
            s.trial('smoke-cursors-%d-%d'%(round_index,mode), smoke_shape(base,mode))
        base = s.best
        # Decompiler scalar reuse and distinct point-width lifetimes are hypotheses.
        a = base.index('    {\n        s32 c_projection;')
        z = base.index('    {\n        s32 *smoke_y',a)
        for width_role, tag_role, x_role, y_role, scale_role in itertools.product(range(3),repeat=5):
            if round_index and (width_role+tag_role+x_role+y_role+scale_role) % 3 != round_index:
                continue
            region = base[a:z]
            choices = [('size',['size','n','width_projection'][width_role]),
                       ('c_projection',['c_projection','c','t'][tag_role]),
                       ('x',['x','n','point_x_projection'][x_role]),
                       ('y_projection',['y_projection','y','point_y_projection'][y_role]),
                       ('t_projection',['t_projection','t','scale_projection'][scale_role])]
            # Prevent overlapping live roles, rather than trusting a fixture to catch all aliases.
            names = [new for old,new in choices]+['angle']
            if len(set(names)) != len(names):
                continue
            for old,new in choices:
                region = re.sub(r'\b'+old+r'\b',new,region)
            region = re.sub(r'\bs32 (c|t|y);','',region)
            fresh = [n for n in ['width_projection','point_x_projection'] if re.search(r'\b'+n+r'\b',region)]
            region = region.replace('    {','    {\n'+''.join('s32 '+n+';\n' for n in fresh),1)
            s.trial('projection-roles-%d-%d%d%d%d%d'%(round_index,width_role,tag_role,x_role,y_role,scale_role),base[:a]+region+base[z:])
        s.save()
        if s.score == start:
            break
    s.save()


def hud_schedule(code, mask):
    if mask & 1:
        code = code.replace('angle = (g_03002A28 - 5000) & 0x3FFF;', 'angle = g_03002A28;')
        code = code.replace('func_08005CF4(angle, 16, 16, 0, 0);', 'func_08005CF4((angle - 5000) & 0x3FFF, 16, 16, 0, 0);')
    if mask & 2:
        code = code.replace('    c = t - (size * 10 + n * 100);\n','')
        code = code.replace('    func_0801533C((u8 *)1, 0x06014000, 0, 96, 0, 0xA08C, 0xD0,',
                            '    c = t - (size * 10 + n * 100);\n    func_0801533C((u8 *)1, 0x06014000, 0, 96, 0, 0xA08C, 0xD0,')
    if mask & 4:
        code = code.replace('                    y = (car->field_0c * *map_zscale) >> 19;\n','')
        code = code.replace('                    SPRITE(source, 0x100, ((y + 118)',
                            '                    y = (car->field_0c * *map_zscale) >> 19;\n                    SPRITE(source, 0x100, ((y + 118)')
    if mask & 8:
        code = code.replace('                map_zscale = &g_0804F330[map_scale + 0x10000];','')
        code = code.replace('car->field_0c * *map_zscale', 'car->field_0c * g_0804F330[map_scale + 0x10000]')
        code = code.replace('        s32 *map_zscale;','')
    if mask & 16:
        code = code.replace('                source_overlay = g_08306DE0 + ((g_03002330 >> 5) << 12);',
                            '                index_overlay = (u16)g_03002330;')
        code = code.replace('                index_overlay = g_030061E4;',
                            '                source_overlay = g_08306DE0 + (((s32)(s16)index_overlay >> 5) << 12);\n                index_overlay = g_030061E4;')
    if mask & 32:
        code = code.replace('    if (n > 0)\n        angle = n * t / size;\n    else if (n < 0)\n        angle = -n;\n    else\n        angle = 0;',
                            '    if (n <= 0) {\n angle = 0;\n if (n < 0) angle = -n;\n } else angle = n * t / size;')
    return code


def hud_followup():
    src = WORK/'hud-best.c'
    s = Search(src,'0800421C','08005238','old','hud-schedule',hud_check)
    for round_index in range(4):
        start = s.score
        base = s.best
        for mask in range(64):
            s.trial('call-lifetimes-%d-%d'%(round_index,mask),hud_schedule(base,mask))
        base = s.best
        for mask in range(16):
            s.trial('captured-points-%d-%d'%(round_index,mask),projected(base,mask))
        s.save()
        if start == s.score:
            break
    s.save()


def hud_map_roles(code, scale, position, angle):
    a=code.index('    {\n        s32 *map_zscale;') if '    {\n        s32 *map_zscale;' in code else code.index('    {\n\n        {\n            s32 map_scale;')
    z=code.index('    i = 0;\n    do {\n        if (g_03000AD0',a)
    region=code[a:z]
    for old,new in [('map_scale',scale),('map_x',position),('angle',angle)]:
        region=re.sub(r'\b'+old+r'\b',new,region)
    for role in set([scale,position,angle]):
        if role in ('size','t','n','c','x','angle','y'):
            region=re.sub(r'\bs32 '+role+r';','',region)
    if angle=='map_angle':
        region=region.replace('{','{\n s32 map_angle;',1)
    return code[:a]+region+code[z:]


def hud_map():
    s=Search(WORK/'hud-schedule-best.c','0800421C','08005238','old','hud-map',hud_check)
    original=s.best
    for iteration in range(3):
        start=s.score
        base=s.best
        # Operate on this pass's original syntax, keeping the best unrelated phases.
        for scale,position,angle in itertools.product(['map_scale','size','t','n','c'],['map_x','x','t','n','c'],['angle','map_angle','t','n','c']):
            if len({scale,position,angle})!=3:
                continue
            # One map rewrite per baseline; later opening changes are independently combined below.
            s.trial('map-roles-%d-%s-%s-%s'%(iteration,scale,position,angle),hud_map_roles(base,scale,position,angle))
        base=s.best
        for size,source in itertools.product(['overlay_size','size','t','n','c','angle','x','y'],['source_overlay','source']):
            a=base.index('    {\n        s32 overlay_size;')
            z=base.index('    {\n        u32 strip_index;',a)
            region=base[a:z]
            for old,new in [('overlay_size',size),('source_overlay',source)]:
                region=re.sub(r'\b'+old+r'\b',new,region)
            if size!='overlay_size': region=region.replace('s32 '+size+';','')
            if source=='source': region=region.replace('u8 *source;','')
            s.trial('opening-role-%d-%s-%s'%(iteration,size,source),base[:a]+region+base[z:])
        s.save()
        # Further map trials need the same identifiable declarations; record one finite pass.
        break
    s.save()


def hud_refine():
    s=Search(WORK/'hud-map-best.c','0800421C','08005238','old','hud-refine',hud_check)
    base=s.best
    for mask in range(16): s.trial('projected-captures-%d'%mask,projected(base,mask))
    base=s.best
    for mode in range(1,32): s.trial('flash-cursors-%d'%mode,flash_shape(base,mode))
    base=s.best
    for mode in range(1,8): s.trial('smoke-cursors-%d'%mode,smoke_shape(base,mode))
    base=s.best
    for mask in range(64): s.trial('call-lifetimes-%d'%mask,hud_schedule(base,mask))
    s.save()


def stream_check(path):
    import subprocess
    receipt=WORK/'stream-trial-checks.json'
    result=subprocess.run([sys.executable,ROOT/'tools/check_stream_original1112c.py',path.relative_to(ROOT),receipt.relative_to(ROOT),'--cases','240'],capture_output=True,text=True)
    if result.returncode:
        raise ValueError(result.stderr[-300:])
    return json.loads(receipt.read_text())


def stream_shape(code, mask):
    # Preserve the observed repeated row-field lookup through descriptor stores.
    pattern=re.compile(r'settings = (g_080(?:219AC|21520|2158C|215F8|21718)\[[^;]+);(?P<body>\s*RECT\([^;]+;\s*END_FACE\([^;]+;)')
    for m in reversed(list(pattern.finditer(code))):
        family=1 if '219AC' in m[1] else 4 if '21718' in m[1] else 2
        if mask & family:
            body=re.sub(r'\bsettings\[(\d)\]',lambda x:m[1]+'['+x[1]+']',m['body'])
            code=code[:m.start()]+body+code[m.end():]
    if mask & 8:
        a=code.index('    next = center + 1;')
        z=code.index('    first = (ring & 31)',a)
        neighbors=code[a:z]
        code=code[:a]+code[z:]
        code=code.replace('        ring = g_030001B8;',neighbors+'        ring = g_030001B8;')
        code=code.replace('        ring = (g_030001B8 - 29) & 31;',neighbors+'        ring = (g_030001B8 - 29) & 31;')
    if mask & 16:
        code=code.replace('    s32 i, count, next_count, faces;', '    s32 i, count, next_count, faces;\n s32 emitted;')
        code=code.replace('point->active = 1; ++point;', 'point[emitted].active = 1; ++emitted;')
        code=code.replace('(TxraTriple *)point, radius','(TxraTriple *)(point+emitted), radius')
        code=code.replace('    base_angle = ROW(center)->angle;', '    emitted = 0;\n    base_angle = ROW(center)->angle;')
    if mask & 32:
        code=code.replace('face->texture=(t); face->reserved=0; face->kind=(k);',
                          'face->reserved=0; face->kind=(k); face->texture=(t);')
    return code


def stream():
    s=Search(DEST/'stream-baseline.c','08002854','0800418C','old','stream',stream_check)
    base=s.best
    for mask in range(64): s.trial('row-lookups-and-window-%d'%mask,stream_shape(base,mask))
    s.save()


def stream_order(code, mask):
    additions='''
#define P_RAW(radius,heading,elevation) do { \\
    func_08005F48((TxraTriple *)ROW(center), (TxraTriple *)(point+emitted), radius, heading, elevation); \\
} while (0)
#define D_RAW(radius,heading) do { \\
    func_08005DD4((TxraTriple *)ROW(center), (TxraTriple *)(point+emitted), radius, heading); \\
} while (0)
#define MARK_POINT() do { point[emitted].active=1; ++emitted; } while (0)
#define BEGIN_FACE(k,t) do { face->kind=(k); face->reserved=0; face->texture=(t); } while (0)
'''
    code=code.replace('void func_08002854(void)',additions+'\nvoid func_08002854(void)')
    if mask & 1:
        rx=re.compile(r'(RECT\([^;]+;)\s*END_FACE\(1,(g_080(?:219AC|21718)\[[^;]+)\);')
        code=rx.sub(lambda m:'BEGIN_FACE(1,'+m[2]+');\n '+m[1]+'\n ++face;',code)
    if mask & 2:
        code=code.replace('''            P(2560,left_angle,0);
            P(2560,left_angle,g_080219AC[ROW(center)->bank_left][2]);
            INDICES(first+1,ahead+1,ahead,first);''','''            P_RAW(2560,left_angle,0);
            face->index[3]=first; face->index[2]=ahead; MARK_POINT();
            P_RAW(2560,left_angle,g_080219AC[ROW(center)->bank_left][2]);
            face->index[0]=first+1; face->index[1]=ahead+1; MARK_POINT();''')
        code=code.replace('''            P(2560,right_angle,0);
            P(2560,right_angle,g_080219AC[ROW(center)->bank_right][2]);
            INDICES(ahead+next_left+1,first+count+1,first+count,ahead+next_left);''','''            P_RAW(2560,right_angle,0);
            face->index[2]=first+count; face->index[3]=ahead+next_left; MARK_POINT();
            P_RAW(2560,right_angle,g_080219AC[ROW(center)->bank_right][2]);
            face->index[1]=first+count+1; face->index[0]=ahead+next_left+1; MARK_POINT();''')
    if mask & 4:
        a=code.index('    D(960,left_angle);\n    INDICES(following+')
        z=code.index('    bank = ROW(center)->wall_left;',a)
        old=code[a:z]
        # Reuse only our own table expressions from the retained C.
        textures=[]
        for m in re.finditer(r'(RECT\([^;]+;)\s*(END_FACE\(1,[^;]+;)',old): textures.append(m[0])
        assert len(textures)==3
        replacement='''    D_RAW(960,left_angle);
    face->index[3]=road_first; face->index[0]=road_next;
    face[3].index[2]=road_next; face[3].index[3]=road_first; MARK_POINT();
    D_RAW(320,left_angle);
    face->index[2]=road_first+1; face->index[1]=road_next+1;
    '''+textures[0]+'''
    ++faces; face->index[3]=road_first+1; face->index[0]=road_next+1; MARK_POINT();
    D_RAW(320,right_angle);
    face->index[2]=road_first+2; face->index[1]=road_next+2;
    '''+textures[1]+'''
    ++faces; face->index[3]=road_first+2; face->index[0]=road_next+2; MARK_POINT();
    D_RAW(960,right_angle);
    face->index[2]=road_first+3; face->index[1]=road_next+3; MARK_POINT();
    '''+textures[2]+'''
    ++faces; face[1].index[2]=road_first+3; face[1].index[3]=road_next+3;
    count += 4;
'''
        code=code[:a]+replacement+code[z:]
    if mask & 8:
        code=code.replace('''    P(960,left_angle,g_08021718[ROW(center)->wall_left][3]);
    face->index[0] = first+count;
    face->index[1] = following+next_count+4;''','''    P_RAW(960,left_angle,g_08021718[ROW(center)->wall_left][3]);
    face->index[0] = first+count;
    face->index[1] = following+next_count+4; MARK_POINT();''')
        code=code.replace('''    P(960,right_angle,g_08021718[ROW(center)->wall_right][3]);
    INDICES(following+next_count,first+count,road_first+3,road_next+3);''','''    P_RAW(960,right_angle,g_08021718[ROW(center)->wall_right][3]);
    INDICES(following+next_count,first+count,road_first+3,road_next+3); MARK_POINT();''')
    if mask & 16:
        a=code.index('    i = 23;')
        z=code.index('    emitted = 0;',a)
        clear=code[a:z]
        code=code[:a]+'    if (g_03002334==0) {\n'+clear+'    } else {\n'+clear+'    }\n'+code[z:]
    return code


def stream_ordered():
    s=Search(WORK/'stream-best.c','08002854','0800418C','old','stream-order',stream_check)
    base=s.best
    for mask in range(32): s.trial('descriptor-store-order-%d'%mask,stream_order(base,mask))
    s.save()


def stream_lifetime(code, seam, angle, point_form):
    if seam:
        code=stream_order(code,4)
        code=code.replace('    s32 road_first, road_next;','')
        code=code.replace('    road_first = first+count;\n    road_next = following+next_count;','')
        code=code.replace('    INDICES(following+next_count,first+count,road_first+3,road_next+3);',
                          '    face->index[0]=following+next_count; face->index[1]=first+count;')
        code=re.sub(r'\broad_first\b','(first+count)',code)
        code=re.sub(r'\broad_next\b','(following+next_count)',code)
    if angle==1:
        code=code.replace('    s32 base_angle, left_angle, right_angle;','    s32 base_angle;')
        code=code.replace('    left_angle = base_angle + 4096;\n    right_angle = base_angle - 4096;','')
        code=re.sub(r'\bleft_angle\b','(base_angle+4096)',code)
        code=re.sub(r'\bright_angle\b','(base_angle-4096)',code)
    if angle==2:
        code=code.replace('s32 base_angle, left_angle, right_angle;', 'u32 base_angle, left_angle, right_angle;')
    if point_form==1:
        code=code.replace('(point+emitted)', '((u8 *)point+emitted*28)')
    if point_form==2:
        code=code.replace('(point+emitted)', '(&g_02014000[first+emitted])')
    return code


def stream_lifetimes():
    s=Search(WORK/'stream-best.c','08002854','0800418C','old','stream-lifetimes',stream_check)
    base=s.best
    for seam,angle,point_form in itertools.product(range(2),range(3),range(3)):
        s.trial('seam-and-angle-lifetimes-%d-%d-%d'%(seam,angle,point_form),stream_lifetime(base,seam,angle,point_form))
    s.save()


def stream_type_shape(base,mask):
        a=base.index('    for (i=0; i<2; ++i) {')
        z=base.index('\n    }\n}',a)
        region=base[a:z]
        guard=re.compile(r'if \(([^\n]+)\) \{')
        for m in reversed(list(guard.finditer(region))):
            condition=m[1]
            nested=condition.strip() in ['type==11','type==12']
            family=1 if 'type-3' in condition else 8 if 'type-16' in condition else 4 if nested else 2
            if mask & family:
                condition=re.sub(r'\btype\b','ROW(center)->scenery[i]',condition)
                region=region[:m.start(1)]+condition+region[m.end(1):]
        return base[:a]+region+base[z:]


def stream_types():
    s=Search(DEST/'func_08002854.c','08002854','0800418C','old','stream-types',stream_check)
    base=s.best
    for mask in range(16): s.trial('scenery-field-reloads-%d'%mask,stream_type_shape(base,mask))
    s.save()


def stream_phase_shape(code,mask):
    additions='''
#define D_AT(index,radius,heading) do { \\
    func_08005DD4((TxraTriple *)ROW(center), (TxraTriple *)(phase_points+(index)), radius, heading); \\
    phase_points[index].active=1; \\
} while (0)
#define P_AT(index,radius,heading,elevation) do { \\
    func_08005F48((TxraTriple *)ROW(center), (TxraTriple *)(phase_points+(index)), radius, heading, elevation); \\
    phase_points[index].active=1; \\
} while (0)
'''
    code=code.replace('void func_08002854(void)',additions+'\nvoid func_08002854(void)')
    a=code.index('    for (i=0; i<2; ++i) {')
    groups=list(re.finditer(r'^        if \([^\n]+\) \{',code[a:],re.M))
    assert len(groups)==6
    for index,m in reversed(list(enumerate(groups))):
        if not mask & (1 << index):continue
        begin=a+m.start()
        op=code.index('{',begin)
        end=op+1;depth=1
        while depth:
            depth+=(code[end]=='{')-(code[end]=='}');end+=1
        body=code[op+1:end-1]
        calls=list(re.finditer(r'\b(D|P)\(([^;\n]+?)\);',body))
        assert len(calls) in [4,7,8,15]
        for n,call in reversed(list(enumerate(calls))):
            body=body[:call.start()]+call[1]+'_AT('+str(n)+','+call[2]+');'+body[call.end():]
        body='\n StreamPoint *phase_points=point+emitted;'+body+'\n emitted += '+str(len(calls))+';\n'
        code=code[:op+1]+body+code[end-1:]
    return code


def stream_phases():
    s=Search(DEST/'func_08002854.c','08002854','0800418C','old','stream-phases',stream_check)
    base=s.best
    for type_mask,phase_mask in itertools.product([0,2,8,10],range(64)):
        s.trial('scenery-point-bases-%d-%d'%(type_mask,phase_mask),stream_phase_shape(stream_type_shape(base,type_mask),phase_mask))
    s.save()


def arm_check(path):
    import contextlib
    import io
    import tempfile
    spec=importlib.util.spec_from_file_location('arm_original_check',ROOT/'docs/near-misses/arm-16da8-1107/check_semantics.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    previous=sys.argv
    with tempfile.TemporaryDirectory(prefix='arm-1112c-',dir=WORK) as directory:
        module.HERE=Path(directory)
        (module.HERE/'func_08016DA8.c').symlink_to(path)
        sys.argv=['check_semantics.py','--candidate','func_08016DA8.c']
        result=io.StringIO()
        try:
            with contextlib.redirect_stdout(result): module.main()
        finally: sys.argv=previous
    return json.loads(result.getvalue())


def arm_shape(code, mask):
    if mask & 1:
        code=code.replace('            depth[2] = MEM32(direct_c + 24);','            depth[2] = points[ic].depth;')
        code=code.replace('            direct_c = point_address(ic);','')
        code=code.replace('            } else {\n                packet = MEM32(CURRENT);','            } else {\n direct_c = point_address(ic);\n                packet = MEM32(CURRENT);')
    if mask & 2:
        code=code.replace('    u32 depth[4];','')
        code=code.replace('            TrackPoint *points = POINT_ARRAY;','            u32 depth[4];\n            TrackPoint *points = POINT_ARRAY;')
    if mask & 4:
        for name in ['ia','ib','ic','id','part']:
            code=code.replace('    u32 '+name+';','')
        code=code.replace('            TrackPoint *points = POINT_ARRAY;','            u32 ia, ib, ic, id, part;\n            TrackPoint *points = POINT_ARRAY;')
    if mask & 8:
        for letter in 'acb':
            code=code.replace('TrackPoint *p'+letter+' = &points[i'+letter+'];',
                              'TrackPoint *p'+letter+' = (TrackPoint *)((u8 *)points + o'+letter+');')
    if mask & 16:
        for letter in 'acb':
            code=code.replace('MEM32(POINTS + o'+letter+')','p'+letter+'->xyz[0]')
    if mask & 32:
        for letter in 'acb':
            for component in (1,2):
                code=code.replace('p'+letter+'->xyz['+str(component)+']',
                                  'MEM32(POINTS + o'+letter+' + '+str(component*4)+')')
    if mask & 64:
        code=code.replace('    u32 direct_c;','')
        code=code.replace('            TrackPoint *points = POINT_ARRAY;','            u32 direct_c;\n            TrackPoint *points = POINT_ARRAY;')
    return code


def arm(followup=False):
    s=Search(WORK/'arm-best.c' if followup else 'docs/near-misses/arm-16da8-1111/func_08016DA8.c','08016DA8','08017E68','arm','arm-addresses' if followup else 'arm',arm_check)
    base=s.best
    for mask in range(128): s.trial('depth-join-and-point-lifetimes-%d'%mask,arm_shape(base,mask))
    s.save()


def contact_schedule(code, mask, delta, sine, speed):
    if speed:
        code=code.replace('s32 speed = g_03001E60[i].field_28;\n                          s32 other = g_03001E60[j].field_28;',
                          's32 other = g_03001E60[j].field_28;\n s32 speed = g_03001E60[i].field_28;')
    if mask & 1:
        code=code.replace('s1 * x - c1 * z','x * s1 - z * c1')
    if mask & 2:
        code=code.replace('s1 * z + c1 * x','c1 * x + s1 * z')
    if mask & 4:
        code=code.replace('g_083D2280[angle] * xx - c2 * zz','xx * g_083D2280[angle] - zz * c2')
    if mask & 8:
        code=code.replace('g_083D2280[angle] * zz + c2 * xx','c2 * xx + g_083D2280[angle] * zz')
    if delta:
        xdelta='g_03001E60[j].field_04 - g_03001E60[i].field_04'
        zdelta='zpos - g_03001E6C[i][0]'
        if delta==1:
            code=code.replace('xx += '+xdelta+';', 'xx = ('+xdelta+') + xx;')
            code=code.replace('zz += '+zdelta+';', 'zz = ('+zdelta+') + zz;')
        else:
            code=code.replace('                    s32 zz;', '                    s32 zz;\n s32 dx, dz;')
            code=code.replace('xx += '+xdelta+';', 'dx = '+xdelta+';\n xx += dx;')
            code=code.replace('zz += '+zdelta+';', 'dz = '+zdelta+';\n zz += dz;')
    if sine:
        code=code.replace('                    s32 zz;', '                    s32 zz;\n s32 player_sine;')
        if sine==1:
            code=code.replace('                    x = p->field_00;', '                    player_sine = g_083D2280[angle];\n x = p->field_00;')
        else:
            code=code.replace('                    zz += zpos', '                    player_sine = g_083D2280[angle];\n zz += zpos')
            if delta:
                code=code.replace('                    zz = (zpos', '                    player_sine = g_083D2280[angle];\n zz = (zpos')
                code=code.replace('                    dz = zpos', '                    player_sine = g_083D2280[angle];\n dz = zpos')
        a=code.index('                    p->field_00 =')
        z=code.index('                    p++;',a)
        code=code[:a]+code[a:z].replace('g_083D2280[angle]','player_sine')+code[z:]
    return code


def contact_followup():
    s=Search(WORK/'contact-best.c','080181C0','08018854','arm','contact-schedule',contact_check)
    base=s.best
    for mask,delta,sine,speed in itertools.product(range(16),range(3),range(3),range(2)):
        s.trial('coefficient-scheduling-%d-%d-%d-%d'%(mask,delta,sine,speed),contact_schedule(base,mask,delta,sine,speed))
    s.save()


def contact_check(path):
    import contextlib
    import io
    import check_contact1112
    previous = sys.argv
    receipt = WORK/'contact-trial-checks.json'
    try:
        sys.argv = ['check_contact1112.py',str(path.relative_to(ROOT)),str(receipt.relative_to(ROOT))]
        with contextlib.redirect_stdout(io.StringIO()):
            check_contact1112.main()
        return json.loads(receipt.read_text())
    finally:
        sys.argv = previous


def contact_angle(code, mode):
    if not mode:
        return code
    code = code.replace('angle = (-g_03001E60[0].field_20) & 0x3FFF;', 'angle = g_03001E60[0].field_20;')
    if mode == 1:
        code = code.replace('g_083C2280[angle]', 'g_083C2280[(-angle) & 0x3FFF]')
        code = code.replace('g_083D2280[angle]', 'g_083D2280[(-angle) & 0x3FFF]')
    else:
        role = 'a' if mode == 2 else 'inverse_angle'
        code = code.replace('                c2 =', '                '+('s32 inverse_angle;\n' if mode==3 else '')+role+' = (-angle) & 0x3FFF;\n                c2 =')
        code = code.replace('g_083C2280[angle]', 'g_083C2280['+role+']')
        code = code.replace('g_083D2280[angle]', 'g_083D2280['+role+']')
    return code


def contact_roles(code, mask):
    if mask & 1:
        code = code.replace('    do {\n        if (g_03001E60[i].field_00)', '    do {\n TxraRecord *first = &g_03001E60[i];\n        if (g_03001E60[i].field_00)',1)
        code = code.replace('g_03001E60[i].','first->')
    if mask & 2:
        code = code.replace('            do {\n                known = 0;', '            do {\n TxraRecord *second = &g_03001E60[j];\n                known = 0;',1)
        code = code.replace('g_03001E60[j].','second->')
    if mask & 4 and 's32 first_code' not in code:
        code = code.replace('            j = 0;', '            s32 first_code = i * 16;\n j = 0;',1)
        code = code.replace('j + i * 16','j + first_code')
    if mask & 8 and 's32 second_code' not in code:
        code = code.replace('                known = 0;', '                s32 second_code = j * 16;\n known = 0;',1)
        code = code.replace('i + j * 16','i + second_code')
    if mask & 16:
        code = code.replace('                zpos = g_03001E6C[j][0];','                zpos = g_03001E60[j].field_0c;')
        code = code.replace('g_03001E6C[i][0]','g_03001E60[i].field_0c')
    if mask & 32 and 's32 next_i' not in code:
        code = code.replace('    do {\n', '    do {\n s32 next_i = i + 1;\n',1)
        code = code.replace('        i++;','        i = next_i;')
    if mask & 64 and 's32 next_j' not in code:
        code = code.replace('            do {\n','            do {\n s32 next_j = j + 1;\n',1)
        code = code.replace('                j++;','                j = next_j;')
    return code


def contact(followup=False):
    # The checker has its own ROM-free state oracle; it never grants admission.
    s = Search(WORK/'contact-best.c' if followup else 'docs/near-misses/breadth-1112/contact-valid/func_080181C0.c',
               '080181C0','08018854','arm','contact-indices' if followup else 'contact',contact_check)
    for iteration in range(4):
        start = s.score
        base = s.best
        for angle_mode,mask in itertools.product(range(4),range(128) if followup else range(32)):
            s.trial('angle-and-records-%d-%d-%d'%(iteration,angle_mode,mask),
                    contact_roles(contact_angle(base,angle_mode),mask))
        s.save()
        if s.score == start:
            break
    s.save()


if __name__ == '__main__':
    if '--stream-phases' in sys.argv:
        stream_phases()
    elif '--stream-types' in sys.argv:
        stream_types()
    elif '--stream-lifetimes' in sys.argv:
        stream_lifetimes()
    elif '--stream-order' in sys.argv:
        stream_ordered()
    elif '--contact-schedule' in sys.argv:
        contact_followup()
    elif '--arm-addresses' in sys.argv:
        arm(True)
    elif '--arm' in sys.argv:
        arm()
    elif '--stream' in sys.argv:
        stream()
    elif '--hud-refine' in sys.argv:
        hud_refine()
    elif '--hud-map' in sys.argv:
        hud_map()
    elif '--contact-indices' in sys.argv:
        contact(True)
    elif '--contact' in sys.argv:
        contact()
    elif '--schedule' in sys.argv:
        hud_followup()
    else:
        hud()
