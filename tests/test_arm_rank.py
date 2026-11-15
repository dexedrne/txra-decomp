"""Synthetic ARMv4T instructions; no private ROM is used by these fixtures."""
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'recomp')]
import rank_targets

BASE = 0x08000000
START = BASE + 0x100
HEADER = [0xE1A0C00D, 0xE92DDFF0, 0xE24CB004, 0xE24DD020]
FOOTER = [0xE91B6FF0, 0xE12FFF1E]

def program(body, header=None, footer=None):
    words = (HEADER if header is None else header) + body + (FOOTER if footer is None else footer)
    code = b''.join(w.to_bytes(4, 'little') for w in words)
    return SimpleNamespace(rom=b'\0'*0x100+code,
        by_start={START: {'mode':'arm', 'end':hex(START+len(code))}},
        insns={START:[SimpleNamespace(addr=START+i*4, ir=('fixture',)) for i in range(len(words))]},
        callees={}, callers={}, matched={}, name=lambda _: 'func_08000100')

def rejection(body, **kwargs):
    return rank_targets.rank(program(body, **kwargs), {}, None)[0]['blocked_reason']

class ArmRankTests(unittest.TestCase):
    def test_apcs_leaf_is_not_rejected_for_missing_compiler(self):
        self.assertIsNone(rejection([0xE3A00000]))  # mov r0,#0

    def test_saved_register_can_be_defined_then_used(self):
        self.assertIsNone(rejection([0xE1A04000, 0xE1A00004]))  # mov r4,r0; mov r0,r4

    def test_push_does_not_define_incoming_callee_saved_register(self):
        self.assertIn('live-in', rejection([0xE1A00004]))

    def test_conditional_write_does_not_define_a_register_on_all_paths(self):
        self.assertIn('live-in', rejection([0xE3500000, 0x13A04001, 0xE1A00004]))

    def test_branch_cannot_bypass_definition(self):
        # cmp r0,#0; beq read; mov r4,#1; read: mov r0,r4
        self.assertIn('live-in', rejection([0xE3500000, 0x0A000000, 0xE3A04001, 0xE1A00004]))

    def test_flags_are_not_hidden_arguments(self):
        self.assertIn('flags', rejection([0x02A00001]))  # addeq r0,r0,#1

    def test_processor_state_is_not_ordinary_c(self):
        self.assertIn('processor', rejection([0xE10F0000]))  # mrs r0,cpsr

    def test_calls_remain_manual_review(self):
        self.assertIn('call', rejection([0xEB000000]))

    def test_branch_outside_declared_body_is_rejected(self):
        self.assertIn('outside', rejection([0xEA000100]))

    def test_frame_and_stack_are_not_writable_scratch(self):
        self.assertIn('frame', rejection([0xE3A0B000]))
        self.assertIn('stack', rejection([0xE3A0D000]))

    def test_custom_entry_and_wrong_restore_stay_blocked(self):
        self.assertIn('APCS', rejection([0xE3A00000], header=[]))
        self.assertIn('restore', rejection([0xE3A00000], footer=[0xE91B6FE0,0xE12FFF1E]))

    def test_both_paths_can_define_before_merge(self):
        # cmp; beq second; mov r4,#1; b merge; second: mov r4,#2; merge: mov r0,r4
        self.assertIsNone(rejection([0xE3500000,0x0A000001,0xE3A04001,0xEA000000,0xE3A04002,0xE1A00004]))

    def test_post_armv4_instruction_stays_blocked(self):
        self.assertIn('ARMv4T', rejection([0xE16F0F11]))  # clz r0,r1

    def test_return_slot_and_saved_registers_are_not_local_variables(self):
        self.assertIn('saved frame', rejection([0xE50B0004]))  # str r0,[fp,#-4]
        self.assertIn('saved frame', rejection([0xE58D0020]))  # str r0,[sp,#32]

    def test_instruction_must_fit_inside_declared_extent(self):
        p = program([0xE3A00000])
        p.by_start[START]['end'] = hex(int(p.by_start[START]['end'],16)-1)
        self.assertIn('body', rank_targets.rank(p,{},None)[0]['blocked_reason'])

    def test_carry_is_not_an_incoming_argument(self):
        self.assertIn('flags', rejection([0xE2A00000]))  # adc r0,r0,#0

    def test_matching_footer_must_execute_before_return(self):
        # mov lr,r0; b final_bx (skips the textual restore)
        self.assertIn('restore', rejection([0xE1A0E000,0xEA000000]))

    def test_armv4_descending_array_load_defines_saved_registers(self):
        self.assertIsNone(rejection([0xE8100030,0xE1A00004]))  # ldmda r0,{r4,r5}; mov r0,r4

    def test_user_bank_restore_is_a_processor_contract(self):
        self.assertIsNotNone(rejection([0xE3A00000], footer=[0xE95B6FF0,0xE12FFF1E]))

    def test_restore_base_must_not_write_back_into_restored_frame(self):
        self.assertIsNotNone(rejection([0xE3A00000], footer=[0xE93B6FF0,0xE12FFF1E]))

    def test_allocation_cannot_be_skipped_before_stack_local_store(self):
        header = [0xE1A0C00D,0xE92DDFF0,0xE24CB004,0xEA000000,0xE24DD020]
        self.assertIsNotNone(rejection([0xE58D0000], header=header))

    def test_saved_stack_origin_cannot_be_overwritten_before_frame_setup(self):
        header = [0xE1A0C00D,0xE92DDFF0,0xE1A0C000,0xE24CB004,0xE24DD020]
        self.assertIsNotNone(rejection([0xE3A00000], header=header))

    def test_body_cannot_reenter_the_prologue(self):
        self.assertIsNotNone(rejection([0xE3500000,0x1AFFFFF9]))  # cmp; bne entry

    def test_entry_inside_installed_owner_is_already_covered(self):
        p = program([0xE3A00000])
        size = int(p.by_start[START]['end'], 16) - START
        p.matched = {START-8: {'offset': START-8-BASE, 'size': size+8, 'name': 'func_080000F8'}}
        self.assertEqual(rank_targets.rank(p, {}, None)[0]['blocked_reason'],
                         'covered by installed func_080000F8')
        p.matched[START-8]['size'] = size+4  # owner ends before the entry's last instruction
        self.assertNotIn('covered', rank_targets.rank(p, {}, None)[0]['blocked_reason'] or '')

if __name__ == '__main__':
    unittest.main()
