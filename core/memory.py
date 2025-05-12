"""
Memory Module for RISC-V Simulator
Implements a simple memory model for the RISC-V simulator
"""

from typing import List, Optional

class Memory:
    """
    Simple memory implementation for RISC-V simulator
    """
    
    def __init__(self, size: int = 1024 * 1024):
        """
        Initialize memory with specified size
        
        Args:
            size: Memory size in bytes (default: 1MB)
        """
        self.size = size
        self.memory = bytearray(size)
        self.verbose = False  # Verbose mode flag
        
    def reset(self):
        """Reset memory to all zeros"""
        self.memory = bytearray(self.size)
        
    def _check_address(self, address: int):
        """
        Check if address is valid
        
        Args:
            address: Memory address to check
            
        Raises:
            ValueError: If address is out of bounds
        """
        if address < 0 or address >= self.size:
            raise ValueError(f"Memory address out of bounds: 0x{address:08x}")
            
    def read_byte(self, address: int) -> int:
        """
        Read a byte from memory
        
        Args:
            address: Memory address to read from
            
        Returns:
            Byte value at the specified address
        """
        self._check_address(address)
        value = self.memory[address]
        
        if self.verbose:
            print(f"[VERBOSE] Memory read: byte at 0x{address:08x} = 0x{value:02x}")
            
        return value
        
    def write_byte(self, address: int, value: int):
        """
        Write a byte to memory
        
        Args:
            address: Memory address to write to
            value: Byte value to write
        """
        self._check_address(address)
        old_value = self.memory[address] if self.verbose else None
        
        # Mask to ensure only a byte is written
        value_to_write = value & 0xFF
        self.memory[address] = value_to_write
        
        if self.verbose:
            print(f"[VERBOSE] Memory write: byte at 0x{address:08x} = 0x{value_to_write:02x} (was 0x{old_value:02x})")
        
    def read_half(self, address: int) -> int:
        """
        Read a halfword (2 bytes) from memory
        
        Args:
            address: Memory address to read from
            
        Returns:
            Halfword value at the specified address
        """
        self._check_address(address)
        self._check_address(address + 1)
        
        # Little-endian
        return (self.memory[address] | 
                (self.memory[address + 1] << 8))
                
    def write_half(self, address: int, value: int):
        """
        Write a halfword (2 bytes) to memory
        
        Args:
            address: Memory address to write to
            value: Halfword value to write
        """
        self._check_address(address)
        self._check_address(address + 1)
        
        # Little-endian
        self.memory[address] = value & 0xFF
        self.memory[address + 1] = (value >> 8) & 0xFF
        
    def read_word(self, address: int) -> int:
        """
        Read a word (4 bytes) from memory
        
        Args:
            address: Memory address to read from
            
        Returns:
            Word value at the specified address
        """
        self._check_address(address)
        self._check_address(address + 3)
        
        # Little-endian
        return (self.memory[address] | 
                (self.memory[address + 1] << 8) |
                (self.memory[address + 2] << 16) |
                (self.memory[address + 3] << 24))
                
    def write_word(self, address: int, value: int):
        """
        Write a word (4 bytes) to memory
        
        Args:
            address: Memory address to write to
            value: Word value to write
        """
        self._check_address(address)
        self._check_address(address + 3)
        
        # Little-endian
        self.memory[address] = value & 0xFF
        self.memory[address + 1] = (value >> 8) & 0xFF
        self.memory[address + 2] = (value >> 16) & 0xFF
        self.memory[address + 3] = (value >> 24) & 0xFF
        
    def read_block(self, address: int, size: int) -> bytearray:
        """
        Read a block of memory
        
        Args:
            address: Starting memory address
            size: Number of bytes to read
            
        Returns:
            Bytearray containing the memory block
        """
        self._check_address(address)
        self._check_address(address + size - 1)
        
        return self.memory[address:address + size]
        
    def write_block(self, address: int, data: bytearray):
        """
        Write a block of memory
        
        Args:
            address: Starting memory address
            data: Bytearray containing the data to write
        """
        self._check_address(address)
        self._check_address(address + len(data) - 1)
        
        self.memory[address:address + len(data)] = data
        
    def dump(self, start_address: int, size: int) -> str:
        """
        Dump memory contents as a formatted string
        
        Args:
            start_address: Starting memory address
            size: Number of bytes to dump
            
        Returns:
            Formatted string representation of memory contents
        """
        self._check_address(start_address)
        self._check_address(start_address + size - 1)
        
        result = []
        for i in range(0, size, 16):
            addr = start_address + i
            bytes_to_read = min(16, size - i)
            
            # Address
            line = f"0x{addr:08x}: "
            
            # Hex values
            hex_values = []
            for j in range(bytes_to_read):
                hex_values.append(f"{self.memory[addr + j]:02x}")
            line += " ".join(hex_values)
            
            # Padding for alignment
            line += "   " * (16 - bytes_to_read)
            
            # ASCII representation
            line += "  |"
            for j in range(bytes_to_read):
                byte = self.memory[addr + j]
                if 32 <= byte <= 126:  # Printable ASCII
                    line += chr(byte)
                else:
                    line += "."
            line += "|"
            
            result.append(line)
            
        return "\n".join(result)