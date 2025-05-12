"""
Test module for the disassembler
"""

import unittest
from utils.disassembler import disassemble_instruction

class TestDisassembler(unittest.TestCase):
    """Test cases for the disassembler"""
    
    def test_r_type_instructions(self):
        """Test disassembling R-type instructions"""
        # add x1, x2, x3
        self.assertEqual(disassemble_instruction(0x003100B3), "add ra, sp, gp")
        
        # sub x4, x5, x6
        self.assertEqual(disassemble_instruction(0x40628233), "sub tp, t0, t1")
        
        # and x7, x8, x9
        self.assertEqual(disassemble_instruction(0x009403B3), "and t2, s0/fp, s1")
        
        # or x10, x11, x12
        self.assertEqual(disassemble_instruction(0x00C5E533), "or a0, a1, a2")
        
        # xor x13, x14, x15
        self.assertEqual(disassemble_instruction(0x00F746B3), "xor a3, a4, a5")
        
    def test_i_type_instructions(self):
        """Test disassembling I-type instructions"""
        # addi x1, x2, 10
        self.assertEqual(disassemble_instruction(0x00A10093), "addi ra, sp, 10")
        
        # slti x3, x4, -5
        self.assertEqual(disassemble_instruction(0xFFB22193), "slti gp, tp, -5")
        
        # xori x5, x6, 0xFF
        self.assertEqual(disassemble_instruction(0x0FF34293), "xori t0, t1, 255")
        
        # ori x7, x8, 0x0F
        self.assertEqual(disassemble_instruction(0x00F463B3), "ori t2, s0/fp, 15")
        
        # andi x9, x10, 0xF0
        self.assertEqual(disassemble_instruction(0x0F057493), "andi s1, a0, 240")
        
    def test_load_instructions(self):
        """Test disassembling load instructions"""
        # lw x1, 8(x2)
        self.assertEqual(disassemble_instruction(0x00812083), "lw ra, 8(sp)")
        
        # lh x3, 4(x4)
        self.assertEqual(disassemble_instruction(0x00421183), "lh gp, 4(tp)")
        
        # lb x5, 2(x6)
        self.assertEqual(disassemble_instruction(0x00230283), "lb t0, 2(t1)")
        
        # lbu x7, 1(x8)
        self.assertEqual(disassemble_instruction(0x00144383), "lbu t2, 1(s0/fp)")
        
        # lhu x9, 0(x10)
        self.assertEqual(disassemble_instruction(0x00055483), "lhu s1, 0(a0)")
        
    def test_store_instructions(self):
        """Test disassembling store instructions"""
        # sw x1, 8(x2)
        self.assertEqual(disassemble_instruction(0x00112423), "sw ra, 8(sp)")
        
        # sh x3, 4(x4)
        self.assertEqual(disassemble_instruction(0x00321223), "sh gp, 4(tp)")
        
        # sb x5, 2(x6)
        self.assertEqual(disassemble_instruction(0x00530123), "sb t0, 2(t1)")
        
    def test_branch_instructions(self):
        """Test disassembling branch instructions"""
        # beq x1, x2, 8
        self.assertEqual(disassemble_instruction(0x00208463), "beq ra, sp, 8")
        
        # bne x3, x4, -4
        self.assertEqual(disassemble_instruction(0xFE419EE3), "bne gp, tp, -4")
        
        # blt x5, x6, 16
        self.assertEqual(disassemble_instruction(0x00628863), "blt t0, t1, 16")
        
        # bge x7, x8, -8
        self.assertEqual(disassemble_instruction(0xFE83DCE3), "bge t2, s0/fp, -8")
        
        # bltu x9, x10, 32
        self.assertEqual(disassemble_instruction(0x00A4E063), "bltu s1, a0, 32")
        
        # bgeu x11, x12, -16
        self.assertEqual(disassemble_instruction(0xFEC5F863), "bgeu a1, a2, -16")
        
    def test_jump_instructions(self):
        """Test disassembling jump instructions"""
        # jal x1, 16
        self.assertEqual(disassemble_instruction(0x0100006F), "jal ra, 16")
        
        # jalr x1, x2, 8
        self.assertEqual(disassemble_instruction(0x00810067), "jalr ra, sp, 8")
        
    def test_lui_auipc_instructions(self):
        """Test disassembling LUI and AUIPC instructions"""
        # lui x1, 0x12345
        self.assertEqual(disassemble_instruction(0x123450B7), "lui ra, 0x12345")
        
        # auipc x2, 0x67890
        self.assertEqual(disassemble_instruction(0x67890117), "auipc sp, 0x67890")
        
    def test_system_instructions(self):
        """Test disassembling system instructions"""
        # ecall
        self.assertEqual(disassemble_instruction(0x00000073), "ecall")
        
        # ebreak
        self.assertEqual(disassemble_instruction(0x00100073), "ebreak")
        
if __name__ == '__main__':
    unittest.main()