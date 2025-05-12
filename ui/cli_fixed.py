"""
Command Line Interface for the RISC-V Simulator
"""

import cmd
import threading
import time
import os
import sys
from typing import List, Dict, Optional, Any
from core.simulator import RiscvSimulator
from scheduler.scheduler_base import SchedulerBase, TaskState
from scheduler.scheduler_factory import create_scheduler
from ui.visualization import SchedulerVisualizer

class CLI(cmd.Cmd):
    """
    Command Line Interface for the RISC-V Simulator
    """
    
    intro = """
    MyRiscvOSPy - RISC-V Multitasking Scheduler in Python
    Type 'help' or '?' to list commands.
    """
    prompt = "riscv> "
    
    def __init__(self, simulator: RiscvSimulator, scheduler: SchedulerBase):
        """
        Initialize the CLI
        
        Args:
            simulator: Reference to the RISC-V simulator
            scheduler: Reference to the scheduler
        """
        super().__init__()
        self.simulator = simulator
        self.scheduler = scheduler
        self.running = False
        self.simulation_thread = None
        self.example_running = False
        self.example_thread = None
        self.visualization_mode = False
        self.visualizer = None
        
    def do_exit(self, arg):
        """Exit the simulator"""
        if self.running:
            self.do_stop("")
            
        print("Exiting...")
        return True
        
    def do_quit(self, arg):
        """Alias for exit"""
        return self.do_exit(arg)
        
    def do_start(self, arg):
        """Start the simulator"""
        if self.running:
            print("Simulation is already running")
            return
            
        self.running = True
        self.simulation_thread = threading.Thread(target=self._run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        print("Simulation started")
        
    def do_stop(self, arg):
        """Stop the simulation"""
        if not self.running:
            print("Simulation is not running")
            return
            
        self.running = False
        if self.simulation_thread:
            self.simulation_thread.join(timeout=1.0)
            self.simulation_thread = None
            
        # Also stop the example simulation if it's running
        if self.example_running:
            self.example_running = False
            if self.example_thread:
                self.example_thread.join(timeout=1.0)
                self.example_thread = None
                print("Example simulation stopped")
                
                # Restore the original aging mechanism if it was disabled
                if hasattr(self, '_original_apply_aging'):
                    self.scheduler._apply_aging = self._original_apply_aging
                    print("Restored priority aging mechanism for normal operation.")
                
        print("Simulation stopped")
        
    def do_status(self, arg):
        """Show the current status of the simulator"""
        print("Simulator Status:")
        print(f"  Running: {self.running}")
        print(f"  Example Simulation: {self.example_running}")
        print(f"  Visualization Data Collection: {self.visualization_mode}")
        print(f"  Cycle Count: {self.simulator.cycle_count}")
        
        print("\nScheduler Status:")
        stats = self.scheduler.get_scheduler_stats()
        print(f"  Scheduler Type: {self.scheduler.get_scheduler_type()}")
        print(f"  Tick Count: {stats['tick_count']}")
        print(f"  Context Switches: {stats['context_switches']}")
        print(f"  Task Count: {stats['task_count']}")
        
        if stats['running_task']:
            task = self.scheduler.tasks[stats['running_task']]
            print(f"  Running Task: {task.id} ({task.name})")
        else:
            print("  Running Task: None (Idle)")
            
        # Always show task details
        print("\nTask Details:")
        tasks = self.scheduler.get_task_stats()
        
        if not tasks:
            print("  No tasks")
        else:
            print("  ID | Name                 | Priority (Orig) | State      | Run Count")
            print("  ---+----------------------+----------------+------------+----------")
            for task in tasks:
                # Highlight the running task
                if self.scheduler.current_task and self.scheduler.current_task.id == task['id']:
                    print(f"→ {task['id']:2d} | {task['name'][:20]:<20} | {task['priority']:3d} ({task['original_priority']:3d}) | {task['state']:<10} | {task['run_count']:8d}")
                else:
                    print(f"  {task['id']:2d} | {task['name'][:20]:<20} | {task['priority']:3d} ({task['original_priority']:3d}) | {task['state']:<10} | {task['run_count']:8d}")
                    
        if self.visualization_mode:
            print("\nVisualization data collection is enabled.")
            print("Use 'graph' to see the task state graph.")
            
    def do_create(self, arg):
        """Create a new task
        
        Usage: create <name> <priority> <entry_point> [stack_size]
        Example: create MyTask 5 0x1000 1024
        """
        args = arg.split()
        if len(args) < 3:
            print("Usage: create <name> <priority> <entry_point> [stack_size]")
            return
            
        name = args[0]
        
        try:
            priority = int(args[1])
            if priority < 1:
                print("Priority must be at least 1")
                return
        except ValueError:
            print("Priority must be an integer")
            return
            
        try:
            entry_point = int(args[2], 0)  # Base 0 allows for hex input
        except ValueError:
            print("Entry point must be an integer or hex value")
            return
            
        stack_size = 1024
        if len(args) >= 4:
            try:
                stack_size = int(args[3])
                if stack_size < 256:
                    print("Stack size must be at least 256 bytes")
                    return
            except ValueError:
                print("Stack size must be an integer")
                return
                
        task = self.scheduler.create_task(
            name=name,
            priority=priority,
            entry_point=entry_point,
            stack_size=stack_size
        )
        
        print(f"Created task {task.id}: {task.name} (Priority {task.priority})")
        
    def do_terminate(self, arg):
        """Terminate a task
        
        Usage: terminate <task_id>
        Example: terminate 1
        """
        if not arg:
            print("Usage: terminate <task_id>")
            return
            
        try:
            task_id = int(arg)
        except ValueError:
            print("Task ID must be an integer")
            return
            
        try:
            self.scheduler.terminate_task(task_id)
            print(f"Terminated task {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
            
    def do_block(self, arg):
        """Block a task
        
        Usage: block <task_id>
        Example: block 1
        """
        if not arg:
            print("Usage: block <task_id>")
            return
            
        try:
            task_id = int(arg)
        except ValueError:
            print("Task ID must be an integer")
            return
            
        try:
            self.scheduler.block_task(task_id)
            print(f"Blocked task {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
            
    def do_unblock(self, arg):
        """Unblock a task
        
        Usage: unblock <task_id>
        Example: unblock 1
        """
        if not arg:
            print("Usage: unblock <task_id>")
            return
            
        try:
            task_id = int(arg)
        except ValueError:
            print("Task ID must be an integer")
            return
            
        try:
            self.scheduler.unblock_task(task_id)
            print(f"Unblocked task {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
            
    def do_sleep(self, arg):
        """Put a task to sleep for a specified number of ticks
        
        Usage: sleep <task_id> <ticks>
        Example: sleep 1 10
        """
        args = arg.split()
        if len(args) < 2:
            print("Usage: sleep <task_id> <ticks>")
            return
            
        try:
            task_id = int(args[0])
        except ValueError:
            print("Task ID must be an integer")
            return
            
        try:
            ticks = int(args[1])
            if ticks < 1:
                print("Ticks must be at least 1")
                return
        except ValueError:
            print("Ticks must be an integer")
            return
            
        try:
            self.scheduler.sleep_task(task_id, ticks)
            print(f"Put task {task_id} to sleep for {ticks} ticks")
        except ValueError as e:
            print(f"Error: {e}")
            
    def do_tick(self, arg):
        """Manually trigger a scheduler tick
        
        Usage: tick [count]
        Example: tick 5
        """
        count = 1
        if arg:
            try:
                count = int(arg)
                if count < 1:
                    print("Count must be at least 1")
                    return
            except ValueError:
                print("Count must be an integer")
                return
                
        for _ in range(count):
            self.scheduler.tick()
            
        print(f"Triggered {count} scheduler tick(s)")
        print(f"Current tick count: {self.scheduler.tick_count}")
        
    def do_visualize(self, arg):
        """Enable visualization data collection
        
        This will start collecting task state history for visualization
        """
        if self.visualization_mode:
            print("Visualization data collection is already enabled")
            return
            
        self.visualization_mode = True
        if not self.visualizer:
            self.visualizer = SchedulerVisualizer(self.scheduler)
            
        print("Visualization data collection enabled")
        print("Use 'graph' to see the task state graph")
        
    def do_visualize_stop(self, arg):
        """Disable visualization data collection"""
        if not self.visualization_mode:
            print("Visualization data collection is already disabled")
            return
            
        self.visualization_mode = False
        print("Visualization data collection disabled")
        
    def do_graph(self, arg):
        """Show the task state graph
        
        This requires visualization data collection to be enabled
        """
        if not self.visualizer:
            print("Visualization is not initialized")
            print("Use 'visualize' to enable visualization data collection")
            return
            
        if not self.visualization_mode and not self.visualizer.has_data():
            print("No visualization data available")
            print("Use 'visualize' to enable visualization data collection")
            return
            
        print("Generating task state graph...")
        self.visualizer.show_task_states()
        
    def do_reset(self, arg):
        """Reset the simulator and scheduler"""
        if self.running:
            self.do_stop("")
            
        self.simulator.reset()
        
        # Create a new scheduler of the same type
        scheduler_type = "priority"  # Default
        if isinstance(self.scheduler, type):
            scheduler_type = self.scheduler.__class__.__name__.lower()
            if scheduler_type.endswith("scheduler"):
                scheduler_type = scheduler_type[:-9]
                
        self.scheduler = create_scheduler(
            scheduler_type=scheduler_type,
            simulator=self.simulator
        )
        
        self.visualization_mode = False
        self.visualizer = None
        
        print("Simulator and scheduler reset")
        
    def do_example(self, arg):
        """Run an example simulation with many tasks
        
        This will create multiple tasks with different priorities and
        demonstrate how the scheduler handles them over time.
        
        Usage: example [scheduler_type]
        Example: example round-robin
        """
        if self.example_running:
            print("Example simulation is already running")
            return
            
        if self.running:
            self.do_stop("")
            
        # If a scheduler type is specified, create a new scheduler
        if arg:
            scheduler_type = arg.lower()
            if scheduler_type not in ['priority', 'round-robin', 'fcfs']:
                print(f"Unknown scheduler type: {scheduler_type}")
                print("Available types: priority, round-robin, fcfs")
                return
                
            print(f"Creating new {scheduler_type} scheduler...")
            self.scheduler = create_scheduler(
                scheduler_type=scheduler_type,
                simulator=self.simulator,
                time_slice=10 if scheduler_type == 'round-robin' else None
            )
            self.visualizer = SchedulerVisualizer(self.scheduler)
            print(f"Created new {scheduler_type} scheduler")
            
        # Start the simulation
        self.do_start("")
        
        # Don't automatically enable visualization as it can cause the screen to get stuck
        # Instead, inform the user they can enable it manually
        if self.visualization_mode:
            # If visualization was already enabled, disable it to prevent screen issues
            self.do_visualize_stop("")
            print("Disabled visualization mode to prevent screen issues during example simulation.")
            print("You can re-enable it with the 'visualize' command if needed.")
            
        # Disable the aging mechanism by replacing it with a no-op function
        # Store the original function so we can restore it later
        self._original_apply_aging = self.scheduler._apply_aging
        self.scheduler._apply_aging = lambda: None
        print("\nDisabled priority aging mechanism for the example simulation")
        print("This ensures tasks maintain their original priorities")
            
        # Create example tasks
        print("Creating example tasks...")
        
        # Create 30+ tasks with various priorities
        tasks = []
        
        # Create 5 high priority tasks (1-5)
        for i in range(5):
            task = self.scheduler.create_task(
                name=f"HighPriority_{i+1}",
                priority=i+1,
                entry_point=0x1000 + (i * 0x100),
                stack_size=1024
            )
            tasks.append(task)
            print(f"Created task {task.id}: {task.name} (Priority {task.priority})")
        
        # Create 10 medium priority tasks (6-15)
        for i in range(10):
            task = self.scheduler.create_task(
                name=f"MediumPriority_{i+1}",
                priority=6 + i,
                entry_point=0x2000 + (i * 0x100),
                stack_size=1024
            )
            tasks.append(task)
            print(f"Created task {task.id}: {task.name} (Priority {task.priority})")
        
        # Create 10 low priority tasks (16-25)
        for i in range(10):
            task = self.scheduler.create_task(
                name=f"LowPriority_{i+1}",
                priority=16 + i,
                entry_point=0x3000 + (i * 0x100),
                stack_size=1024
            )
            tasks.append(task)
            print(f"Created task {task.id}: {task.name} (Priority {task.priority})")
        
        # Create 5 background tasks (26-30)
        for i in range(5):
            task = self.scheduler.create_task(
                name=f"Background_{i+1}",
                priority=26 + i,
                entry_point=0x4000 + (i * 0x100),
                stack_size=512
            )
            tasks.append(task)
            print(f"Created task {task.id}: {task.name} (Priority {task.priority})")
        
        # Create 2 idle tasks (31-32)
        for i in range(2):
            task = self.scheduler.create_task(
                name=f"Idle_{i+1}",
                priority=31 + i,
                entry_point=0x5000 + (i * 0x100),
                stack_size=512
            )
            tasks.append(task)
            print(f"Created task {task.id}: {task.name} (Priority {task.priority})")
        
        print(f"\nCreated {len(tasks)} tasks with various priorities.")
        print("\nExample simulation is running!")
        print("Tasks will automatically change states to demonstrate scheduling.")
        print("This simulation will run for an extended period to allow observation.")
        print("\nYou can now:")
        print("- Use 'status' to see the current state of tasks")
        print("- Use 'graph' to see the task state graph")
        print("- Use 'stop' to stop the simulation at any time")
        
        # Start the example simulation in a separate thread
        self.example_thread = threading.Thread(target=self._run_example_simulation)
        self.example_thread.daemon = True
        self.example_thread.start()
        
    def _run_example_simulation(self):
        """Run the example simulation in a separate thread"""
        try:
            self.example_running = True
            
            # Get all tasks
            tasks = list(self.scheduler.tasks.values())
            if len(tasks) < 10:
                print("Not enough tasks for example simulation")
                self.example_running = False
                return
                
            # Wait for simulation to stabilize
            time.sleep(1)
            
            # Group tasks by priority for easier management
            high_priority_tasks = tasks[:5]  # First 5 tasks (highest priority)
            medium_priority_tasks = tasks[5:15]  # Next 10 tasks
            low_priority_tasks = tasks[15:25]  # Next 10 tasks
            background_tasks = tasks[25:30]  # Next 5 tasks
            idle_tasks = tasks[30:]  # Last 2 tasks (lowest priority)
            
            print(f"\nStarting example simulation with {len(tasks)} tasks")
            print("This will run for approximately 30 seconds to demonstrate scheduling")
            
            # Provide clear instructions about visualization
            print("\nVisualization tips:")
            print("- Use 'visualize' to enable task state history collection")
            print("- Use 'graph' to see the task state graph")
            print("- Use 'visualize_stop' if the screen gets stuck")
            print("- Use 'status' to see current task states without visualization")
            
            # Cycle through different task states to demonstrate scheduling
            cycle_count = 0
            max_cycles = 30  # Run for just 30 seconds
            
            # Brief introduction before starting
            print("\nStarting simulation - use 'status' to see task states")
            print("The simulation will run for 30 seconds with various task operations")
            
            while self.running and self.example_running and cycle_count < max_cycles:
                cycle_count += 1
                
                # Perform actions every cycle for the short simulation
                # This ensures we see plenty of activity in the 30 seconds
                
                # Use cycle count to determine action type, with more variety
                action_type = cycle_count % 15  # 15 different action types
                
                if action_type == 0:
                    # Block some high priority tasks
                    for i in range(min(2, len(high_priority_tasks))):
                        task = high_priority_tasks[i]
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            self.scheduler.block_task(task.id)
                            print(f"\nBlocked high priority task {task.id} ({task.name})")
                
                elif action_type == 1:
                    # Unblock high priority tasks
                    for task in high_priority_tasks:
                        if task.state == TaskState.BLOCKED:
                            self.scheduler.unblock_task(task.id)
                            print(f"\nUnblocked high priority task {task.id} ({task.name})")
                
                elif action_type == 2:
                    # Put some medium priority tasks to sleep
                    for i in range(min(3, len(medium_priority_tasks))):
                        task = medium_priority_tasks[i]
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            sleep_time = 5 + (i * 3)  # Shorter sleep times
                            self.scheduler.sleep_task(task.id, sleep_time)
                            print(f"\nPut medium priority task {task.id} ({task.name}) to sleep for {sleep_time} ticks")
                
                elif action_type == 3:
                    # Block some medium priority tasks
                    for i in range(3, min(6, len(medium_priority_tasks))):
                        task = medium_priority_tasks[i]
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            self.scheduler.block_task(task.id)
                            print(f"\nBlocked medium priority task {task.id} ({task.name})")
                
                elif action_type == 4:
                    # Terminate some low priority tasks
                    for i in range(min(2, len(low_priority_tasks))):
                        task = low_priority_tasks[i]
                        if task.state != TaskState.TERMINATED:
                            self.scheduler.terminate_task(task.id)
                            print(f"\nTerminated low priority task {task.id} ({task.name})")
                
                elif action_type == 5:
                    # Block some low priority tasks
                    for i in range(2, min(5, len(low_priority_tasks))):
                        task = low_priority_tasks[i]
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            self.scheduler.block_task(task.id)
                            print(f"\nBlocked low priority task {task.id} ({task.name})")
                
                elif action_type == 6:
                    # Unblock some medium priority tasks
                    for task in medium_priority_tasks:
                        if task.state == TaskState.BLOCKED:
                            self.scheduler.unblock_task(task.id)
                            print(f"\nUnblocked medium priority task {task.id} ({task.name})")
                
                elif action_type == 7:
                    # Put some background tasks to sleep
                    for task in background_tasks:
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            sleep_time = 8
                            self.scheduler.sleep_task(task.id, sleep_time)
                            print(f"\nPut background task {task.id} ({task.name}) to sleep for {sleep_time} ticks")
                
                elif action_type == 8:
                    # Create a new high priority task
                    new_task = self.scheduler.create_task(
                        name=f"NewHighPriority_{cycle_count}",
                        priority=1,
                        entry_point=0x6000 + (cycle_count * 0x100),
                        stack_size=1024
                    )
                    high_priority_tasks.append(new_task)
                    print(f"\nCreated new high priority task {new_task.id} ({new_task.name})")
                
                elif action_type == 9:
                    # Unblock some low priority tasks
                    for task in low_priority_tasks:
                        if task.state == TaskState.BLOCKED:
                            self.scheduler.unblock_task(task.id)
                            print(f"\nUnblocked low priority task {task.id} ({task.name})")
                
                elif action_type == 10:
                    # Create a new medium priority task
                    priority = 6 + (cycle_count % 10)
                    new_task = self.scheduler.create_task(
                        name=f"NewMediumTask_{cycle_count}",
                        priority=priority,
                        entry_point=0x7000 + (cycle_count * 0x100),
                        stack_size=1024
                    )
                    medium_priority_tasks.append(new_task)
                    print(f"\nCreated new medium priority task {new_task.id} ({new_task.name}) with priority {priority}")
                
                elif action_type == 11:
                    # Block and unblock tasks in quick succession
                    if high_priority_tasks:
                        task = high_priority_tasks[0]
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            self.scheduler.block_task(task.id)
                            print(f"\nBlocked high priority task {task.id} ({task.name})")
                            # Immediately unblock it
                            self.scheduler.unblock_task(task.id)
                            print(f"Immediately unblocked task {task.id} ({task.name})")
                
                elif action_type == 12:
                    # Put high priority tasks to sleep for a short time
                    for task in high_priority_tasks:
                        if task.state == TaskState.READY or task.state == TaskState.RUNNING:
                            sleep_time = 3
                            self.scheduler.sleep_task(task.id, sleep_time)
                            print(f"\nPut high priority task {task.id} ({task.name}) to sleep for {sleep_time} ticks")
                
                elif action_type == 13:
                    # Create a new low priority task
                    priority = 16 + (cycle_count % 10)
                    new_task = self.scheduler.create_task(
                        name=f"NewLowTask_{cycle_count}",
                        priority=priority,
                        entry_point=0x8000 + (cycle_count * 0x100),
                        stack_size=1024
                    )
                    low_priority_tasks.append(new_task)
                    print(f"\nCreated new low priority task {new_task.id} ({new_task.name}) with priority {priority}")
                
                elif action_type == 14:
                    # Unblock all blocked tasks
                    for task in tasks:
                        if task.state == TaskState.BLOCKED:
                            self.scheduler.unblock_task(task.id)
                            print(f"\nUnblocked task {task.id} ({task.name})")
                
                # Frequent status updates for the short simulation
                if cycle_count % 5 == 0:
                    print(f"\n--- Example simulation progress: cycle {cycle_count}/{max_cycles} ---")
                    
                    # Count tasks in each state
                    ready_count = sum(1 for t in tasks if t.state == TaskState.READY)
                    running_count = sum(1 for t in tasks if t.state == TaskState.RUNNING)
                    blocked_count = sum(1 for t in tasks if t.state == TaskState.BLOCKED)
                    sleeping_count = sum(1 for t in tasks if t.state == TaskState.SLEEPING)
                    terminated_count = sum(1 for t in tasks if t.state == TaskState.TERMINATED)
                    
                    print(f"Tasks: {len(tasks)} total, {ready_count} ready, {running_count} running, " +
                          f"{blocked_count} blocked, {sleeping_count} sleeping, {terminated_count} terminated")
                    print("Use 'status' to see detailed task states")
                    
                    # Add reminder about visualization options
                    if self.visualization_mode:
                        print("Visualization is ON - use 'graph' to see task transitions")
                        print("If screen gets stuck, use 'visualize_stop' to disable visualization")
                    else:
                        print("Visualization is OFF - use 'visualize' to enable if desired")
                    
                    # Reset task priorities to their original values
                    # This prevents all tasks from eventually reaching priority 1 due to aging
                    reset_count = 0
                    for task in tasks:
                        if task.priority != task.original_priority:
                            task.priority = task.original_priority
                            reset_count += 1
                            
                    if reset_count > 0:
                        print(f"Reset priorities for {reset_count} tasks to demonstrate priority scheduling")
                
                # Variable wait time between actions
                time.sleep(1.0)  # Use a consistent 1 second delay for the short simulation
            
            # Count tasks in each state for final summary
            ready_count = sum(1 for t in tasks if t.state == TaskState.READY)
            running_count = sum(1 for t in tasks if t.state == TaskState.RUNNING)
            blocked_count = sum(1 for t in tasks if t.state == TaskState.BLOCKED)
            sleeping_count = sum(1 for t in tasks if t.state == TaskState.SLEEPING)
            terminated_count = sum(1 for t in tasks if t.state == TaskState.TERMINATED)
            
            print("\n=== Example simulation completed ===")
            print(f"Final task count: {len(tasks)} total tasks")
            print(f"Task states: {ready_count} ready, {running_count} running, " +
                  f"{blocked_count} blocked, {sleeping_count} sleeping, {terminated_count} terminated")
            
            # Disable visualization if it was enabled to prevent screen issues
            if self.visualization_mode:
                self.do_visualize_stop("")
                print("\nVisualization mode has been automatically disabled to prevent screen issues.")
                print("You can re-enable it with the 'visualize' command if needed.")
            
            # Restore the original aging mechanism
            if hasattr(self, '_original_apply_aging'):
                self.scheduler._apply_aging = self._original_apply_aging
                print("Restored priority aging mechanism for normal operation.")
            
            print("\nYou can continue to interact with the simulator:")
            print("- Use 'status' to see the detailed state of all tasks")
            print("- Use 'visualize' to enable task state history collection")
            print("- Use 'graph' to see the task state transition graph")
            print("- Try other commands like 'block', 'unblock', 'sleep', etc.")
            print("- Run 'example' again with a different scheduler type (priority, round-robin, fcfs)")
            
            self.example_running = False
            
        except Exception as e:
            print(f"\nExample simulation error: {e}")
            self.example_running = False
            
    def _run_simulation(self):
        """Run the simulation in a separate thread"""
        try:
            while self.running:
                # Perform a scheduler tick
                self.scheduler.tick()
                
                # If visualization is enabled, update the visualizer
                if self.visualization_mode and self.visualizer:
                    self.visualizer.update()
                    
                # Sleep to control simulation speed
                time.sleep(0.1)
                
        except Exception as e:
            print(f"\nSimulation error: {e}")
            self.running = False
            
    def start(self):
        """Start the CLI"""
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            print("\nExiting...")
            if self.running:
                self.do_stop("")