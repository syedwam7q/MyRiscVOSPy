"""
Interrupt Controller for RISC-V Simulator
Handles interrupt requests and prioritization
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class Interrupt:
    """Interrupt descriptor"""
    id: int
    priority: int
    handler_address: int
    description: str
    pending: bool = False

class InterruptController:
    """
    Interrupt controller for RISC-V simulator
    
    Handles interrupt requests, prioritization, and dispatching
    """
    
    # Standard RISC-V interrupt IDs
    TIMER_INTERRUPT = 7
    EXTERNAL_INTERRUPT = 11
    SOFTWARE_INTERRUPT = 3
    
    def __init__(self, simulator):
        """
        Initialize the interrupt controller
        
        Args:
            simulator: Reference to the RISC-V simulator
        """
        self.simulator = simulator
        self.interrupts: Dict[int, Interrupt] = {}
        self.enabled = True
        self._register_standard_interrupts()
        
    def _register_standard_interrupts(self):
        """Register standard RISC-V interrupts"""
        self.register_interrupt(
            id=self.TIMER_INTERRUPT,
            priority=10,
            handler_address=0x100,  # Example address
            description="Timer Interrupt"
        )
        
        self.register_interrupt(
            id=self.EXTERNAL_INTERRUPT,
            priority=20,
            handler_address=0x200,  # Example address
            description="External Interrupt"
        )
        
        self.register_interrupt(
            id=self.SOFTWARE_INTERRUPT,
            priority=30,
            handler_address=0x300,  # Example address
            description="Software Interrupt"
        )
        
    def reset(self):
        """Reset the interrupt controller"""
        for interrupt in self.interrupts.values():
            interrupt.pending = False
        self.enabled = True
        
    def register_interrupt(self, id: int, priority: int, 
                          handler_address: int, description: str) -> Interrupt:
        """
        Register a new interrupt
        
        Args:
            id: Interrupt ID
            priority: Interrupt priority (lower value = higher priority)
            handler_address: Address of the interrupt handler
            description: Description of the interrupt
            
        Returns:
            The created Interrupt object
        """
        interrupt = Interrupt(
            id=id,
            priority=priority,
            handler_address=handler_address,
            description=description,
            pending=False
        )
        
        self.interrupts[id] = interrupt
        return interrupt
        
    def trigger_interrupt(self, interrupt_id: int):
        """
        Trigger an interrupt
        
        Args:
            interrupt_id: ID of the interrupt to trigger
            
        Raises:
            ValueError: If the interrupt ID is not registered
        """
        if interrupt_id not in self.interrupts:
            raise ValueError(f"Interrupt ID {interrupt_id} not registered")
            
        self.interrupts[interrupt_id].pending = True
        
    def clear_interrupt(self, interrupt_id: int):
        """
        Clear a pending interrupt
        
        Args:
            interrupt_id: ID of the interrupt to clear
            
        Raises:
            ValueError: If the interrupt ID is not registered
        """
        if interrupt_id not in self.interrupts:
            raise ValueError(f"Interrupt ID {interrupt_id} not registered")
            
        self.interrupts[interrupt_id].pending = False
        
    def has_pending_interrupts(self) -> bool:
        """
        Check if there are any pending interrupts
        
        Returns:
            True if there are pending interrupts, False otherwise
        """
        if not self.enabled:
            return False
            
        return any(interrupt.pending for interrupt in self.interrupts.values())
        
    def get_highest_priority_interrupt(self) -> Optional[Interrupt]:
        """
        Get the highest priority pending interrupt
        
        Returns:
            The highest priority pending interrupt, or None if there are no pending interrupts
        """
        if not self.enabled:
            return None
            
        pending_interrupts = [i for i in self.interrupts.values() if i.pending]
        if not pending_interrupts:
            return None
            
        # Sort by priority (lower value = higher priority)
        return min(pending_interrupts, key=lambda i: i.priority)
        
    def enable(self):
        """Enable the interrupt controller"""
        self.enabled = True
        
    def disable(self):
        """Disable the interrupt controller"""
        self.enabled = False
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of the interrupt controller
        
        Returns:
            Dictionary containing the status of the interrupt controller
        """
        return {
            "enabled": self.enabled,
            "pending": [
                {
                    "id": i.id,
                    "priority": i.priority,
                    "description": i.description
                }
                for i in self.interrupts.values() if i.pending
            ]
        }