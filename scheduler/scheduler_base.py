"""
Base Scheduler Implementation
Defines the base class for all scheduler implementations
"""

from typing import Dict, List, Optional, Any
from enum import Enum, auto
import time
from core.simulator import RiscvSimulator

class TaskState(Enum):
    """Task states"""
    READY = auto()      # Ready to run
    RUNNING = auto()    # Currently running
    BLOCKED = auto()    # Blocked, waiting for an event
    SLEEPING = auto()   # Sleeping for a specified time
    TERMINATED = auto() # Terminated

class Task:
    """
    Task representation for the scheduler
    """
    
    def __init__(self, id: int, name: str, priority: int, 
                entry_point: int, stack_size: int = 1024):
        """
        Initialize a task
        
        Args:
            id: Task ID
            name: Task name
            priority: Task priority (lower value = higher priority)
            entry_point: Entry point address in memory
            stack_size: Stack size in bytes
        """
        self.id = id
        self.name = name
        self.priority = priority
        self.original_priority = priority  # For aging mechanism
        self.entry_point = entry_point
        self.stack_size = stack_size
        self.stack_pointer = 0  # Will be set by the scheduler
        self.state = TaskState.READY
        self.context = None  # Will be set when task is first run or context-switched
        self.wake_time = 0  # For sleeping tasks
        self.creation_time = time.time()
        self.total_runtime = 0  # Total time spent running
        self.last_run_time = 0  # Last time the task was run
        self.run_count = 0  # Number of times the task has been run
        
    def __repr__(self) -> str:
        """String representation of the task"""
        return f"Task(id={self.id}, name='{self.name}', priority={self.priority}, state={self.state.name})"

class SchedulerBase:
    """
    Base class for all scheduler implementations
    """
    
    def __init__(self, simulator: RiscvSimulator):
        """
        Initialize the scheduler
        
        Args:
            simulator: Reference to the RISC-V simulator
        """
        self.simulator = simulator
        self.tasks: Dict[int, Task] = {}
        self.current_task: Optional[Task] = None
        self.next_task_id = 1
        self.tick_count = 0
        self.context_switches = 0
        self.preemptions = 0
        self.verbose = False  # Verbose mode flag
        
    def create_task(self, name: str, priority: int, 
                   entry_point: int, stack_size: int = 1024) -> Task:
        """
        Create a new task
        
        Args:
            name: Task name
            priority: Task priority (lower value = higher priority)
            entry_point: Entry point address in memory
            stack_size: Stack size in bytes
            
        Returns:
            The created Task object
        """
        task_id = self.next_task_id
        self.next_task_id += 1
        
        task = Task(
            id=task_id,
            name=name,
            priority=priority,
            entry_point=entry_point,
            stack_size=stack_size
        )
        
        # Allocate stack space (simplified for simulation)
        # In a real OS, this would involve memory allocation
        task.stack_pointer = 0x80000000 - (task_id * stack_size)
        
        self.tasks[task_id] = task
        return task
        
    def terminate_task(self, task_id: int):
        """
        Terminate a task
        
        Args:
            task_id: ID of the task to terminate
            
        Raises:
            ValueError: If the task ID is not found
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task ID {task_id} not found")
            
        task = self.tasks[task_id]
        task.state = TaskState.TERMINATED
        
        # If terminating the current task, force a context switch
        if self.current_task and self.current_task.id == task_id:
            self.current_task = None
            self.schedule()
            
    def block_task(self, task_id: int):
        """
        Block a task
        
        Args:
            task_id: ID of the task to block
            
        Raises:
            ValueError: If the task ID is not found
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task ID {task_id} not found")
            
        task = self.tasks[task_id]
        task.state = TaskState.BLOCKED
        
        # If blocking the current task, force a context switch
        if self.current_task and self.current_task.id == task_id:
            self.current_task = None
            self.schedule()
            
    def unblock_task(self, task_id: int):
        """
        Unblock a task
        
        Args:
            task_id: ID of the task to unblock
            
        Raises:
            ValueError: If the task ID is not found
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task ID {task_id} not found")
            
        task = self.tasks[task_id]
        if task.state == TaskState.BLOCKED:
            task.state = TaskState.READY
            
    def sleep_task(self, task_id: int, ticks: int):
        """
        Put a task to sleep for a specified number of ticks
        
        Args:
            task_id: ID of the task to sleep
            ticks: Number of ticks to sleep
            
        Raises:
            ValueError: If the task ID is not found
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task ID {task_id} not found")
            
        task = self.tasks[task_id]
        task.state = TaskState.SLEEPING
        task.wake_time = self.tick_count + ticks
        
        # If sleeping the current task, force a context switch
        if self.current_task and self.current_task.id == task_id:
            self.current_task = None
            self.schedule()
            
    def tick(self):
        """
        Process a scheduler tick
        
        This is called periodically by the system timer
        """
        self.tick_count += 1
        
        # Wake up sleeping tasks
        for task in self.tasks.values():
            if task.state == TaskState.SLEEPING and task.wake_time <= self.tick_count:
                task.state = TaskState.READY
                
        # Apply aging mechanism
        self._apply_aging()
        
        # Check if we need to preempt the current task
        self._check_preemption()
        
    def _apply_aging(self):
        """
        Apply aging mechanism to prevent starvation
        
        Increases the priority of tasks that have been waiting for a long time
        """
        # This is a simple implementation - real systems would be more sophisticated
        for task in self.tasks.values():
            if task.state == TaskState.READY:
                # Increase priority (decrease priority value) for waiting tasks
                # but don't exceed the original priority
                if task.priority > 1:  # Don't go below 1
                    # The longer a task waits, the more its priority increases
                    wait_time = self.tick_count - task.last_run_time
                    if wait_time > 100:  # Threshold for aging
                        task.priority = max(task.priority - 1, 1)
                        
    def _check_preemption(self):
        """
        Check if the current task should be preempted
        
        This is called by the tick method
        """
        # Base implementation does nothing - subclasses will override
        pass
        
    def schedule(self) -> Optional[Task]:
        """
        Schedule the next task to run
        
        Returns:
            The next task to run, or None if there are no runnable tasks
        """
        # Base implementation does nothing - subclasses will override
        return None
        
    def context_switch(self, new_task: Optional[Task]):
        """
        Perform a context switch to a new task
        
        Args:
            new_task: The task to switch to, or None to idle
        """
        # Verbose logging for context switch
        if self.verbose:
            from_task = f"Task {self.current_task.id} ({self.current_task.name})" if self.current_task else "None"
            to_task = f"Task {new_task.id} ({new_task.name})" if new_task else "None"
            print(f"[VERBOSE] Context switch: {from_task} -> {to_task}")
        
        if self.current_task:
            # Save current task context
            if self.current_task.state == TaskState.RUNNING:
                old_state = self.current_task.state
                self.current_task.state = TaskState.READY
                
                if self.verbose:
                    print(f"[VERBOSE] Task {self.current_task.id} ({self.current_task.name}) state change: {old_state.name} -> {self.current_task.state.name}")
                
            self.current_task.context = self.simulator.registers.save_context()
            self.current_task.last_run_time = self.tick_count
            
            if self.verbose:
                print(f"[VERBOSE] Saved context for Task {self.current_task.id} ({self.current_task.name})")
                print(f"[VERBOSE] PC: 0x{self.current_task.context.pc:08x}, SP: 0x{self.current_task.context.registers[2]:08x}")
            
        # Switch to new task
        self.current_task = new_task
        
        if new_task:
            # Restore new task context or initialize if first run
            if new_task.context:
                self.simulator.registers.restore_context(new_task.context)
                
                if self.verbose:
                    print(f"[VERBOSE] Restored context for Task {new_task.id} ({new_task.name})")
                    print(f"[VERBOSE] PC: 0x{new_task.context.pc:08x}, SP: 0x{new_task.context.registers[2]:08x}")
            else:
                # First time running this task
                self.simulator.registers.reset()
                self.simulator.registers.set_pc(new_task.entry_point)
                # Set stack pointer (x2 in RISC-V)
                self.simulator.registers.write(2, new_task.stack_pointer)
                
                if self.verbose:
                    print(f"[VERBOSE] Initialized new Task {new_task.id} ({new_task.name})")
                    print(f"[VERBOSE] Entry point: 0x{new_task.entry_point:08x}, SP: 0x{new_task.stack_pointer:08x}")
                
            old_state = new_task.state
            new_task.state = TaskState.RUNNING
            new_task.run_count += 1
            
            if self.verbose:
                print(f"[VERBOSE] Task {new_task.id} ({new_task.name}) state change: {old_state.name} -> {new_task.state.name}")
                print(f"[VERBOSE] Run count: {new_task.run_count}")
            
        self.context_switches += 1
        
        if self.verbose:
            print(f"[VERBOSE] Total context switches: {self.context_switches}")
        
    def get_task_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all tasks
        
        Returns:
            List of dictionaries containing task statistics
        """
        return [
            {
                "id": task.id,
                "name": task.name,
                "priority": task.priority,
                "original_priority": task.original_priority,
                "state": task.state.name,
                "run_count": task.run_count,
                "total_runtime": task.total_runtime,
                "creation_time": task.creation_time
            }
            for task in self.tasks.values()
        ]
        
    def get_scheduler_stats(self) -> Dict[str, Any]:
        """
        Get statistics for the scheduler
        
        Returns:
            Dictionary containing scheduler statistics
        """
        return {
            "tick_count": self.tick_count,
            "context_switches": self.context_switches,
            "task_count": len(self.tasks),
            "running_task": self.current_task.id if self.current_task else None
        }