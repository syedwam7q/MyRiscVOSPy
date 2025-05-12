"""
RISC-V Simulator Core
Simulates a RISC-V processor with registers, memory, and execution capabilities
"""

import time
from typing import Dict, List, Optional, Callable
from .registers import Registers
from .memory import Memory
from .interrupts import InterruptController

class RiscvSimulator:
    """
    Simulates a RISC-V processor with registers, memory, and execution capabilities
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize the RISC-V simulator
        
        Args:
            debug: Enable debug mode
        """
        self.registers = Registers()
        self.memory = Memory(size=1024 * 1024)  # 1MB memory
        self.interrupt_controller = InterruptController(self)
        self.debug = debug
        self.verbose = False  # Verbose mode flag
        self.running = False
        self.cycle_count = 0
        self.instruction_handlers: Dict[int, Callable] = {}
        self._register_instruction_handlers()
        
    def _register_instruction_handlers(self):
        """Register handlers for different instruction types"""
        # This would map RISC-V opcodes to handler functions
        # For simulation purposes, we'll implement a simplified set
        pass
        
    def reset(self):
        """Reset the simulator state"""
        self.registers.reset()
        self.memory.reset()
        self.interrupt_controller.reset()
        self.cycle_count = 0
        self.running = False
        
    def load_program(self, program: List[int], address: int = 0):
        """
        Load a program into memory
        
        Args:
            program: List of instructions (as integers)
            address: Starting address in memory
        """
        for i, instruction in enumerate(program):
            self.memory.write_word(address + (i * 4), instruction)
        
        # Set program counter to the start address
        self.registers.set_pc(address)
        
    def step(self) -> bool:
        """
        Execute a single instruction
        
        Returns:
            True if execution should continue, False otherwise
        """
        if not self.running:
            return False
            
        # Check for pending interrupts
        if self.interrupt_controller.has_pending_interrupts():
            self._handle_interrupt()
            
        # Fetch instruction
        pc = self.registers.get_pc()
        instruction = self.memory.read_word(pc)
        
        if instruction == 0:  # Null instruction, end of program
            self.running = False
            return False
            
        # Decode and execute instruction
        self._execute_instruction(instruction)
        
        # Increment cycle count
        self.cycle_count += 1
        
        # Update program counter (if not already modified by the instruction)
        if pc == self.registers.get_pc():
            self.registers.set_pc(pc + 4)
            
        return True
        
    def _execute_instruction(self, instruction: int):
        """
        Execute a single instruction
        
        Args:
            instruction: The instruction to execute
        """
        # Extract opcode (lowest 7 bits in RISC-V)
        opcode = instruction & 0x7F
        
        # Verbose logging
        if self.verbose:
            pc = self.registers.get_pc()
            print(f"[VERBOSE] Executing instruction at 0x{pc:08x}: 0x{instruction:08x}")
            print(f"[VERBOSE] Opcode: 0x{opcode:02x}")
            
            # Try to disassemble the instruction if possible
            try:
                from utils.disassembler import disassemble_instruction
                disasm = disassemble_instruction(instruction, pc)
                print(f"[VERBOSE] Disassembly: {disasm}")
            except:
                pass
        
        # Find and call the appropriate handler
        handler = self.instruction_handlers.get(opcode)
        if handler:
            if self.verbose:
                print(f"[VERBOSE] Found handler for opcode 0x{opcode:02x}")
                
                # Save registers before execution for comparison
                regs_before = self.registers.save_context()
                
            # Execute the instruction
            handler(instruction)
            
            if self.verbose:
                # Compare registers after execution
                regs_after = self.registers.save_context()
                
                # Check which registers changed
                changed_regs = []
                for i in range(32):
                    if regs_before.registers[i] != regs_after.registers[i]:
                        reg_name = f"x{i}"
                        if i == 0: reg_name = "zero"
                        elif i == 1: reg_name = "ra"
                        elif i == 2: reg_name = "sp"
                        elif i == 3: reg_name = "gp"
                        elif i == 4: reg_name = "tp"
                        elif i == 5: reg_name = "t0"
                        elif i == 6: reg_name = "t1"
                        elif i == 7: reg_name = "t2"
                        
                        changed_regs.append(f"{reg_name}(x{i}): 0x{regs_before.registers[i]:08x} -> 0x{regs_after.registers[i]:08x}")
                
                if changed_regs:
                    print(f"[VERBOSE] Register changes:")
                    for change in changed_regs:
                        print(f"[VERBOSE]   {change}")
                
                # Check if PC changed
                if regs_before.pc != regs_after.pc:
                    print(f"[VERBOSE] PC changed: 0x{regs_before.pc:08x} -> 0x{regs_after.pc:08x}")
        else:
            if self.debug:
                print(f"Unknown instruction: 0x{instruction:08x}")
                
    def _handle_interrupt(self):
        """Handle a pending interrupt"""
        interrupt = self.interrupt_controller.get_highest_priority_interrupt()
        if interrupt:
            # Save current context
            self.registers.save_context()
            
            # Jump to interrupt handler
            self.registers.set_pc(interrupt.handler_address)
            
    def run(self, max_cycles: Optional[int] = None):
        """
        Run the simulator until completion or max_cycles is reached
        
        Args:
            max_cycles: Maximum number of cycles to execute (None for unlimited)
        """
        self.running = True
        cycle = 0
        
        while self.running:
            if max_cycles is not None and cycle >= max_cycles:
                break
                
            if not self.step():
                break
                
            cycle += 1
            
            # Small delay to prevent CPU hogging in simulation
            time.sleep(0.001)
            
    def trigger_interrupt(self, interrupt_id: int):
        """
        Trigger an interrupt
        
        Args:
            interrupt_id: ID of the interrupt to trigger
        """
        self.interrupt_controller.trigger_interrupt(interrupt_id)
        
    def get_state(self) -> Dict:
        """
        Get the current state of the simulator
        
        Returns:
            Dictionary containing the current state
        """
        return {
            'registers': self.registers.get_all(),
            'pc': self.registers.get_pc(),
            'cycle_count': self.cycle_count,
            'running': self.running
        }