"""
Sample Tasks for RISC-V Simulator
Provides sample tasks for testing the scheduler
"""

from typing import List
from core.simulator import RiscvSimulator
from scheduler.scheduler_base import SchedulerBase

def create_sample_tasks(scheduler: SchedulerBase, count: int = 5) -> List[int]:
    """
    Create sample tasks for testing
    
    Args:
        scheduler: Reference to the scheduler
        count: Number of tasks to create
        
    Returns:
        List of task IDs
    """
    task_ids = []
    
    # Create a simple task that increments a counter
    counter_task = scheduler.create_task(
        name="Counter",
        priority=5,
        entry_point=0x1000,
        stack_size=1024
    )
    task_ids.append(counter_task.id)
    
    # Create a task that performs a computation
    compute_task = scheduler.create_task(
        name="Compute",
        priority=10,
        entry_point=0x2000,
        stack_size=1024
    )
    task_ids.append(compute_task.id)
    
    # Create a task that simulates I/O operations
    io_task = scheduler.create_task(
        name="IO",
        priority=3,
        entry_point=0x3000,
        stack_size=1024
    )
    task_ids.append(io_task.id)
    
    # Create additional tasks if needed
    for i in range(count - 3):
        if i % 3 == 0:
            # High priority task
            task = scheduler.create_task(
                name=f"HighPriority{i}",
                priority=2,
                entry_point=0x4000 + (i * 0x1000),
                stack_size=1024
            )
        elif i % 3 == 1:
            # Medium priority task
            task = scheduler.create_task(
                name=f"MediumPriority{i}",
                priority=7,
                entry_point=0x4000 + (i * 0x1000),
                stack_size=1024
            )
        else:
            # Low priority task
            task = scheduler.create_task(
                name=f"LowPriority{i}",
                priority=15,
                entry_point=0x4000 + (i * 0x1000),
                stack_size=1024
            )
            
        task_ids.append(task.id)
        
    return task_ids

def load_sample_programs(simulator: RiscvSimulator):
    """
    Load sample programs into memory
    
    Args:
        simulator: Reference to the simulator
    """
    # Counter program
    # Simple program that increments a counter in a loop
    counter_program = [
        0x00100093,  # addi x1, x0, 1      # x1 = 1 (increment value)
        0x00000113,  # addi x2, x0, 0      # x2 = 0 (counter)
        0x00110133,  # add x2, x2, x1      # x2 = x2 + x1 (increment counter)
        0xFF9FF06F,  # jal x0, -8          # Jump back to the add instruction
    ]
    simulator.load_program(counter_program, 0x1000)
    
    # Compute program
    # Program that performs a simple computation (Fibonacci)
    compute_program = [
        0x00100093,  # addi x1, x0, 1      # x1 = 1 (first Fibonacci number)
        0x00100113,  # addi x2, x0, 1      # x2 = 1 (second Fibonacci number)
        0x00000193,  # addi x3, x0, 0      # x3 = 0 (temporary storage)
        0x00208193,  # addi x3, x1, 2      # x3 = x1 + 2 (simulate computation)
        0x002081B3,  # add x3, x1, x2      # x3 = x1 + x2 (next Fibonacci number)
        0x00010093,  # addi x1, x2, 0      # x1 = x2
        0x00018113,  # addi x2, x3, 0      # x2 = x3
        0xFF5FF06F,  # jal x0, -12         # Jump back to the computation
    ]
    simulator.load_program(compute_program, 0x2000)
    
    # I/O program
    # Program that simulates I/O operations (reading and writing)
    io_program = [
        0x00100093,  # addi x1, x0, 1      # x1 = 1 (data to write)
        0x00200113,  # addi x2, x0, 2      # x2 = 2 (I/O address)
        0x00112023,  # sw x1, 0(x2)        # Store x1 to address in x2 (write)
        0x00012183,  # lw x3, 0(x2)        # Load from address in x2 to x3 (read)
        0xFF9FF06F,  # jal x0, -8          # Jump back to the store instruction
    ]
    simulator.load_program(io_program, 0x3000)
    
    # Generic program for additional tasks
    # Simple program that performs some computation and jumps back
    generic_program = [
        0x00100093,  # addi x1, x0, 1      # x1 = 1
        0x00200113,  # addi x2, x0, 2      # x2 = 2
        0x00300193,  # addi x3, x0, 3      # x3 = 3
        0x00400213,  # addi x4, x0, 4      # x4 = 4
        0x00208233,  # add x4, x1, x2      # x4 = x1 + x2
        0x00418233,  # add x4, x3, x4      # x4 = x3 + x4
        0xFF5FF06F,  # jal x0, -12         # Jump back to the computation
    ]
    
    # Load the generic program at different addresses for additional tasks
    for i in range(10):
        simulator.load_program(generic_program, 0x4000 + (i * 0x1000))