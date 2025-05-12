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
                if cycle_count <= 30:
                    # Slower at the beginning to give time to observe
                    time.sleep(1.5)
                elif cycle_count <= 60:
                    time.sleep(1.0)
                elif cycle_count <= 120:
                    # Faster in the middle section
                    time.sleep(0.7)
                else:
                    # Slower again at the end
                    time.sleep(1.0)
            
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