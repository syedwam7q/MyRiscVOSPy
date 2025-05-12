"""
First-Come, First-Served (FCFS) Scheduler Implementation
Implements a non-preemptive FCFS scheduler
"""

from typing import Optional, List
from .scheduler_base import SchedulerBase, Task, TaskState
from core.simulator import RiscvSimulator

class FCFSScheduler(SchedulerBase):
    """
    First-Come, First-Served (FCFS) scheduler
    
    Schedules tasks in the order they become ready, without preemption
    """
    
    def __init__(self, simulator: RiscvSimulator):
        """
        Initialize the FCFS scheduler
        
        Args:
            simulator: Reference to the RISC-V simulator
        """
        super().__init__(simulator)
        
    def _find_oldest_ready_task(self) -> Optional[Task]:
        """
        Find the task that has been ready for the longest time
        
        Returns:
            The oldest ready task, or None if there are no ready tasks
        """
        ready_tasks = [t for t in self.tasks.values() if t.state == TaskState.READY]
        if not ready_tasks:
            return None
            
        # Sort by last_run_time (older = smaller value)
        return min(ready_tasks, key=lambda t: t.last_run_time)
        
    def schedule(self) -> Optional[Task]:
        """
        Schedule the next task to run
        
        Returns:
            The next task to run, or None if there are no runnable tasks
        """
        # If we have a current task, keep running it (non-preemptive)
        if self.current_task and self.current_task.state == TaskState.RUNNING:
            return self.current_task
            
        # Otherwise, find the oldest ready task
        next_task = self._find_oldest_ready_task()
        
        if next_task:
            self.context_switch(next_task)
        else:
            # No ready tasks, go idle
            if self.current_task:
                self.context_switch(None)
                
        return self.current_task
        
    def _check_preemption(self):
        """
        Check if the current task should be preempted
        
        This is called by the tick method
        """
        # FCFS is non-preemptive, so we don't preempt tasks
        pass
        
    def get_scheduler_type(self) -> str:
        """
        Get the scheduler type
        
        Returns:
            String representation of the scheduler type
        """
        return "First-Come, First-Served (FCFS) Scheduler"