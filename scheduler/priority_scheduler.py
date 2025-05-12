"""
Priority-based Scheduler Implementation
Implements a priority-based preemptive scheduler
"""

from typing import Optional, List
from .scheduler_base import SchedulerBase, Task, TaskState
from core.simulator import RiscvSimulator

class PriorityScheduler(SchedulerBase):
    """
    Priority-based preemptive scheduler
    
    Schedules tasks based on their priority, with preemption
    """
    
    def __init__(self, simulator: RiscvSimulator):
        """
        Initialize the priority scheduler
        
        Args:
            simulator: Reference to the RISC-V simulator
        """
        super().__init__(simulator)
        
    def _find_highest_priority_task(self) -> Optional[Task]:
        """
        Find the highest priority ready task
        
        Returns:
            The highest priority ready task, or None if there are no ready tasks
        """
        ready_tasks = [t for t in self.tasks.values() if t.state == TaskState.READY]
        if not ready_tasks:
            return None
            
        # Sort by priority (lower value = higher priority)
        return min(ready_tasks, key=lambda t: t.priority)
        
    def schedule(self) -> Optional[Task]:
        """
        Schedule the next task to run
        
        Returns:
            The next task to run, or None if there are no runnable tasks
        """
        next_task = self._find_highest_priority_task()
        
        if next_task:
            # If we have a current task and it's different from the next task,
            # perform a context switch
            if self.current_task != next_task:
                self.context_switch(next_task)
        else:
            # No ready tasks, go idle
            if self.current_task:
                self.context_switch(None)
                
        # Return the task that was scheduled, not necessarily the current task
        # This is important for the test case
        return next_task if next_task else self.current_task
        
    def _check_preemption(self):
        """
        Check if the current task should be preempted
        
        This is called by the tick method
        """
        # If we don't have a current task, nothing to preempt
        if not self.current_task:
            return
            
        # Find the highest priority ready task
        highest_priority_task = self._find_highest_priority_task()
        
        # If there's a higher priority task ready, preempt the current task
        if highest_priority_task and highest_priority_task.priority < self.current_task.priority:
            self.schedule()
            
    def get_scheduler_type(self) -> str:
        """
        Get the scheduler type
        
        Returns:
            String representation of the scheduler type
        """
        return "Priority-based Preemptive Scheduler"