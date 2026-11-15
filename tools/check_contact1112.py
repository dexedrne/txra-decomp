#!/usr/bin/env python3
"""Compare an uninstalled contact hypothesis with prior C on synthetic state.

This is not execution of original instructions and cannot admit a replacement.
The negative control narrows a signed sine coefficient and must be detected.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'recomp'))
import draft

BASELINE = Path('docs/near-misses/hand-20261104b/func_080181C0.c')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def adjusted(code, name):
    for alias in ('g_03001E64', 'g_03001E6C'):
        code = code.replace('extern s32 '+alias+'[][25];', '')
    return code.replace('func_080181C0', name)


HARNESS = r'''
#include <stdio.h>
#include <string.h>
#include <stddef.h>
TxraRecord g_03001E60[8];
TxraTriple g_030057A0[6];
s32 g_03005F90[4], g_080202E4[8], g_08020B04[8], g_08020B08[8];
s32 g_083D2280[16384], g_083C2280[16384];
s16 g_030021CC;
#define g_03001E64 (*(s32 (*)[8][25])((u8 *)g_03001E60+4))
#define g_03001E6C (*(s32 (*)[8][25])((u8 *)g_03001E60+12))
_Static_assert(sizeof(TxraRecord)==100, "record stride");
_Static_assert(offsetof(TxraRecord, field_04)==4, "x alias");
_Static_assert(offsetof(TxraRecord, field_0c)==12, "z alias");
'''

DRIVER = r'''
typedef struct {
    TxraRecord cars[8];
    TxraTriple points[6];
    s32 known[4];
    s16 flag;
} State;
static u32 seed=1112;
static u32 random_word(void) { seed=seed*1664525U+1013904223U; return seed; }
static void store(State *s) {
    memcpy(s->cars,g_03001E60,sizeof(s->cars));
    memcpy(s->points,g_030057A0,sizeof(s->points));
    memcpy(s->known,g_03005F90,sizeof(s->known));
    s->flag=g_030021CC;
}
static void restore(const State *s) {
    memcpy(g_03001E60,s->cars,sizeof(s->cars));
    memcpy(g_030057A0,s->points,sizeof(s->points));
    memcpy(g_03005F90,s->known,sizeof(s->known));
    g_030021CC=s->flag;
}
static int same(const State *a,const State *b) {
    return memcmp(a->cars,b->cars,sizeof(a->cars))==0
        && memcmp(a->points,b->points,sizeof(a->points))==0
        && memcmp(a->known,b->known,sizeof(a->known))==0 && a->flag==b->flag;
}
int main(void) {
    unsigned case_id, i, bad_differences=0, changed=0;
    State initial, reference, actual, negative;
    s32 expected, got, bad;
    for(i=0;i<8;i++) { g_080202E4[i]=1<<i; g_08020B04[i]=64+(i%4)*32; g_08020B08[i]=96+(i%4)*48; }
    /* A bounded signed triangular wave is synthetic, not a cartridge lookup. */
    for(i=0;i<16384;i++) {
        s32 p=(s32)(i&8191);
        s32 s=p<4096?p:8192-p;
        if(i&8192) s=-s;
        g_083D2280[i]=s;
    }
    for(i=0;i<16384;i++) g_083C2280[i]=g_083D2280[(i+4096)&16383];
    for(case_id=0;case_id<768;case_id++) {
        memset(g_03001E60,0,sizeof(g_03001E60));
        memset(g_030057A0,0,sizeof(g_030057A0));
        for(i=0;i<8;i++) {
            TxraRecord *p=&g_03001E60[i];
            p->field_00=(case_id%8==0)?0:(case_id%8==1?i==0:(random_word()&3)!=0);
            p->field_02=random_word()%4;
            p->field_04=(case_id%3==0)?(s32)i*12:(s32)(random_word()%3001)-1500;
            p->field_0c=(case_id%3==0)?(s32)i*8:(s32)(random_word()%3001)-1500;
            p->field_20=(s32)(random_word()%65536)-32768;
            p->field_28=random_word()%1000;
            p->field_3a=(s16)random_word(); p->field_3e=(s16)random_word();
        }
        for(i=0;i<4;i++) g_03005F90[i]=(case_id&1)?random_word()%128:0;
        g_030021CC=case_id%2;
        store(&initial);
        expected=reference_contact(); store(&reference);
        if(!same(&initial,&reference)) changed++;
        restore(&initial); got=candidate_contact(); store(&actual);
        if(expected!=got || !same(&reference,&actual)) {
            printf("candidate mismatch in case %u\n",case_id); return 1;
        }
        restore(&initial); bad=narrowed_contact(); store(&negative);
        if(expected!=bad || !same(&reference,&negative)) bad_differences++;
    }
    if(!bad_differences || !changed) return 2;
    printf("{\"cases\":768,\"passed\":768,\"state_changing_cases\":%u,\"rejected_narrowing_control_cases\":%u}\n",changed,bad_differences);
    return 0;
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('receipt', type=Path)
    args = parser.parse_args()
    baseline, candidate = BASELINE.read_text(), args.candidate.read_text()
    # The baseline groups declarations, so narrow just this coefficient without
    # changing the other signed coefficients sharing its declaration.
    bad = baseline.replace('s32 s1, c1, c2, k, model, a;', 'u16 s1; s32 c1, c2, k, model, a;')
    assert bad != baseline
    source = draft.TYPEDEFS+'\n#include "types.h"\n'+HARNESS
    source += adjusted(baseline, 'reference_contact')
    source += adjusted(candidate, 'candidate_contact')
    source += adjusted(bad, 'narrowed_contact')+DRIVER
    with tempfile.TemporaryDirectory(prefix='contact-fixture-', dir='build') as td:
        root = Path(td)
        (root/'check.c').write_text(source)
        command = ['cc', '-std=c11', '-O1', '-fwrapv', '-fno-strict-aliasing', '-Isrc', str(root/'check.c'), '-o', str(root/'check')]
        subprocess.run(command, check=True, capture_output=True, text=True)
        result = subprocess.run([str(root/'check')], check=True, capture_output=True, text=True, timeout=30)
    r = json.loads(result.stdout)
    r.update(candidate=str(args.candidate), candidate_sha256=digest(candidate.encode()), baseline=str(BASELINE),
             baseline_sha256=digest(baseline.encode()), harness_sha256=digest(source.encode()),
             original_instructions_executed=False, installation_authority=False,
             limitations='Prior-C equivalence on synthetic bounded state only; not a proof of original semantics or arbitrary malformed inputs.')
    args.receipt.write_text(json.dumps(r, indent=2)+'\n')
    print(json.dumps(r))


if __name__ == '__main__':
    main()
