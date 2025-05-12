"""
RISC-V Registers Module
Implements the register file for a RISC-V processor
"""

from typing import Dict, List, Any

class Registers:
    """
    RISC-V register file implementation
    
    RISC-V has 32 general-purpose registers (x0-x31) and special registers like PC
    """
    
    # Register names for RISC-V
    REGISTER_NAMES = [
        "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
        "s0/fp", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
        "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
        "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"
    ]
    
    def __init__(self):
        """Initialize the register file"""
        # General purpose registers (x0-x31)
        self.registers = [0] * 32
        
        # Program counter
        self.pc = 0
        
        # Saved context for interrupts/context switching
        self.saved_context = None
        
    def reset(self):
        """Reset all registers to 0"""
        self.registers = [0] * 32
        self.pc = 0
        self.saved_context = None
        
    def read(self, reg_num: int) -> int:
        """
        Read a value from a register
        
        Args:
            reg_num: Register number (0-31)
            
        Returns:
            Value in the register
            
        Note:
            x0 is hardwired to 0 in RISC-V
        """
        if reg_num < 0 or reg_num > 31:
            raise ValueError(f"Invalid register number: {reg_num}")
            
        # x0 is hardwired to 0 in RISC-V
        if reg_num == 0:
            return 0
            
        return self.registers[reg_num]
        
    def write(self, reg_num: int, value: int):
        """
        Write a value to a register
        
        Args:
            reg_num: Register number (0-31)
            value: Value to write
            
        Note:
            Writing to x0 has no effect (it's hardwired to 0)
        """
        if reg_num < 0 or reg_num > 31:
            raise ValueError(f"Invalid register number: {reg_num}")
            
        # x0 is hardwired to 0 in RISC-V, writes have no effect
        if reg_num == 0:
            return
            
        self.registers[reg_num] = value & 0xFFFFFFFF  # 32-bit value
        
    def get_pc(self) -> int:
        """
        Get the program counter value
        
        Returns:
            Current PC value
        """
        return self.pc
        
    def set_pc(self, value: int):
        """
        Set the program counter value
        
        Args:
            value: New PC value
        """
        self.pc = value & 0xFFFFFFFF  # 32-bit value
        
    def get_all(self) -> Dict[str, int]:
        """
        Get all register values
        
        Returns:
            Dictionary mapping register names to values
        """
        result = {f"x{i}": self.registers[i] for i in range(32)}
        result.update({
            "pc": self.pc,
            "names": {f"x{i}": self.REGISTER_NAMES[i] for i in range(32)}
        })
        return result
        
    def save_context(self) -> Dict[str, Any]:
        """
        Save the current register context (for interrupts/context switching)
        
        Returns:
            Saved context dictionary
        """
        context = {
            "registers": self.registers.copy(),
            "pc": self.pc
        }
        self.saved_context = context
        return context
        
    def restore_context(self, context: Dict[str, Any] = None):
        """
        Restore a previously saved context
        
        Args:
            context: Context to restore (uses saved_context if None)
        """
        if context is None:
            if self.saved_context is None:
                raise ValueError("No context to restore")
            context = self.saved_context
            
        self.registers = context["registers"].copy()
        self.pc = context["pc"]