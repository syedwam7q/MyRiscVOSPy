"""
Visualization module for RISC-V simulator
Provides visualization utilities for the simulator
"""

from typing import Dict, List, Any
import time
import os
from scheduler.scheduler_base import SchedulerBase, TaskState

class ConsoleVisualizer:
    """
    Console-based visualizer for the scheduler
    
    Displays task states and scheduler information in the console
    """
    
    def __init__(self, scheduler: SchedulerBase):
        """
        Initialize the console visualizer
        
        Args:
            scheduler: Reference to the scheduler
        """
        self.scheduler = scheduler
        self.last_update = 0
        self.update_interval = 0.5  # Update every 0.5 seconds
        
    def update(self):
        """Update the visualization"""
        current_time = time.time()
        if current_time - self.last_update < self.update_interval:
            return
            
        self.last_update = current_time
        self._clear_screen()
        self._draw_header()
        self._draw_tasks()
        self._draw_stats()
        
    def _clear_screen(self):
        """Clear the console screen"""
        # Instead of clearing the screen, just print a separator
        print("\n" + "=" * 80)
        
    def _draw_header(self):
        """Draw the header"""
        print("=" * 80)
        print(f"RISC-V Multitasking Scheduler - {self.scheduler.get_scheduler_type()}")
        print("=" * 80)
        
    def _draw_tasks(self):
        """Draw the task list"""
        tasks = self.scheduler.get_task_stats()
        
        if not tasks:
            print("No tasks")
            return
            
        print("Tasks:")
        print("  ID | Name                 | Priority | State      | Run Count")
        print("  ---+----------------------+----------+------------+----------")
        for task in tasks:
            # Highlight the running task
            if self.scheduler.current_task and self.scheduler.current_task.id == task['id']:
                print(f"→ {task['id']:2d} | {task['name'][:20]:<20} | {task['priority']:8d} | {task['state']:<10} | {task['run_count']:8d}")
            else:
                print(f"  {task['id']:2d} | {task['name'][:20]:<20} | {task['priority']:8d} | {task['state']:<10} | {task['run_count']:8d}")
                
    def _draw_stats(self):
        """Draw scheduler statistics"""
        stats = self.scheduler.get_scheduler_stats()
        
        print("\nScheduler Statistics:")
        print(f"  Tick Count: {stats['tick_count']}")
        print(f"  Context Switches: {stats['context_switches']}")
        print(f"  Task Count: {stats['task_count']}")
        
        if stats['running_task']:
            task = self.scheduler.tasks[stats['running_task']]
            print(f"  Running Task: {task.id} ({task.name})")
        else:
            print("  Running Task: None (Idle)")
            
        print("\nVisualization active - continue using commands")
        
class TaskStateGraph:
    """
    Task state graph generator
    
    Generates a textual graph of task states over time
    """
    
    def __init__(self, scheduler: SchedulerBase, max_history: int = 100):
        """
        Initialize the task state graph
        
        Args:
            scheduler: Reference to the scheduler
            max_history: Maximum number of history points to keep
        """
        self.scheduler = scheduler
        self.max_history = max_history
        self.history = []
        self.last_update = 0
        self.update_interval = 0.1  # Update every 0.1 seconds
        
    def update(self):
        """Update the task state history"""
        current_time = time.time()
        if current_time - self.last_update < self.update_interval:
            return
            
        self.last_update = current_time
        
        # Record the current state
        state = {
            'tick': self.scheduler.tick_count,
            'tasks': {}
        }
        
        for task_id, task in self.scheduler.tasks.items():
            state['tasks'][task_id] = {
                'state': task.state.name,
                'priority': task.priority
            }
            
        self.history.append(state)
        
        # Trim history if needed
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            
    def draw(self, width: int = 80):
        """
        Draw the task state graph
        
        Args:
            width: Width of the graph in characters
        """
        if not self.history:
            print("No history data")
            return
            
        # Get all task IDs
        task_ids = set()
        for state in self.history:
            task_ids.update(state['tasks'].keys())
            
        task_ids = sorted(task_ids)
        
        # Draw the graph
        print("  " + "-" * width)
        
        for task_id in task_ids:
            line = f"  Task {task_id}: "
            
            # Calculate how many history points to show
            points_to_show = min(len(self.history), width - len(line))
            start_idx = max(0, len(self.history) - points_to_show)
            
            for i in range(start_idx, len(self.history)):
                state = self.history[i]
                if task_id in state['tasks']:
                    task_state = state['tasks'][task_id]['state']
                    if task_state == 'RUNNING':
                        line += 'R'
                    elif task_state == 'READY':
                        line += '.'
                    elif task_state == 'BLOCKED':
                        line += 'B'
                    elif task_state == 'SLEEPING':
                        line += 'S'
                    elif task_state == 'TERMINATED':
                        line += 'T'
                else:
                    line += ' '
                    
            print(line)
            
        print("  " + "-" * width)
        print("  Legend: R=Running, .=Ready, B=Blocked, S=Sleeping, T=Terminated")
        
class SchedulerVisualizer:
    """
    Combined visualizer for the scheduler
    
    Combines multiple visualization components
    """
    
    def __init__(self, scheduler: SchedulerBase):
        """
        Initialize the scheduler visualizer
        
        Args:
            scheduler: Reference to the scheduler
        """
        self.scheduler = scheduler
        self.console_visualizer = ConsoleVisualizer(scheduler)
        self.task_state_graph = TaskStateGraph(scheduler)
        
    def update(self):
        """Update all visualizations"""
        self.console_visualizer.update()
        self.task_state_graph.update()
        
    def draw(self):
        """Draw all visualizations"""
        self.console_visualizer.update()
        print("\n")
        self.task_state_graph.draw()
        
    def show_task_states(self):
        """Show task states (alias for draw)"""
        self.draw()
        
    def has_data(self):
        """Check if there is visualization data available"""
        return len(self.task_state_graph.history) > 0