"""
Scheduler Factory
Creates scheduler instances based on the specified type
"""

from typing import Optional
from core.simulator import RiscvSimulator
from .scheduler_base import SchedulerBase
from .priority_scheduler import PriorityScheduler
from .round_robin_scheduler import RoundRobinScheduler
from .fcfs_scheduler import FCFSScheduler

def create_scheduler(scheduler_type: str, simulator: RiscvSimulator, 
                    time_slice: int = 10) -> SchedulerBase:
    """
    Create a scheduler instance based on the specified type
    
    Args:
        scheduler_type: Type of scheduler to create ('priority', 'round-robin', 'fcfs')
        simulator: Reference to the RISC-V simulator
        time_slice: Time slice for round-robin scheduling (in ticks)
        
    Returns:
        Scheduler instance
        
    Raises:
        ValueError: If the scheduler type is not recognized
    """
    if scheduler_type == 'priority':
        return PriorityScheduler(simulator)
    elif scheduler_type == 'round-robin':
        return RoundRobinScheduler(simulator, time_slice)
    elif scheduler_type == 'fcfs':
        return FCFSScheduler(simulator)
    else:
        raise ValueError(f"Unknown scheduler type: {scheduler_type}")