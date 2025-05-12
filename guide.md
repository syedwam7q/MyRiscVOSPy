# PMARS Demonstration Commands Guide

This guide provides a comprehensive set of commands to demonstrate the Python Multitasking Architecture for RISC-V Systems (PMARS) project for your Advanced Computer Architecture presentation.

## Table of Contents

1. Initial Setup and Basic Overview
2. Using Preset Task Configurations and Scheduler Selection
3. Task State Transitions Demonstration
4. Memory and Register Examination
5. Aging Mechanism Demonstration
6. Comprehensive Presentation Demonstration
7. Example Simulation
8. Demonstration Script for Presentation Flow
9. Tips for a Smooth Demonstration
10. Potential Questions and Answers

## 1. Initial Setup and Basic Overview

```bash
# Start the application with default settings (priority scheduler)
python main.py

# Clear the screen for a clean display
clear

# Show help to display available commands
help

# Get detailed help for a specific command
help_command status

# Check the initial status of the simulator
status
```

## 2. Using Preset Task Configurations and Scheduler Selection

```bash
# Start the simulation
start

# List available scheduler types
list_schedulers

# List available preset configurations
list_presets

# Load a basic preset with 3 tasks of different priorities
load_preset basic

# Show the tasks that were created
status

# Get detailed information about a specific task
task_info 1

# Show scheduler performance metrics
metrics

# Switch to a different scheduler type
select_scheduler round-robin

# Load a preset specifically designed for round-robin demonstration
load_preset round_robin_demo

# Show the tasks that were created
status

# Enable visualization to see task states
visualize

# Show the task state graph
graph

# Switch to another scheduler type
select_scheduler fcfs

# Load a mixed priority preset
load_preset mixed_priority

# Show the tasks with the new scheduler
status
graph
```

## 3. Task State Transitions Demonstration

```bash
# Switch back to priority scheduler for better demonstration
select_scheduler priority

# Load the blocking demonstration preset
load_preset blocking_demo

# Enable visualization
visualize

# Block a high-priority task (use the ID from the tasks list)
block 1

# Show status to demonstrate how blocking affects scheduling
status
graph

# Unblock the task
unblock 1

# Load the sleeping demonstration preset
load_preset sleeping_demo

# Put tasks to sleep with different durations
sleep 1 5
sleep 2 10
sleep 3 15

# Show status to see the sleeping tasks
status
graph

# Wait a few seconds and check status again to see tasks waking up
status
graph

# Change the priority of a task
priority 2 5

# Show the updated status
status
```

## 4. Memory and Register Examination

```bash
# Show register values
registers

# Show memory contents at the program location (e.g., counter program)
memory 0x1000 64

# Disassemble instructions at a program location
disassemble 0x1000 10

# Show memory where a different program is loaded
memory 0x2000 64
disassemble 0x2000 10

# Get detailed information about a task, including its registers and next instructions
task_info 1

# Clear the screen for better readability
clear
```

## 5. Aging Mechanism Demonstration

```bash
# Load the aging demonstration preset
load_preset aging_demo

# Enable visualization
visualize

# Show initial status
status

# Toggle verbose mode to see more details
verbose

# Let the system run for a while to see priority aging in action
# (You can explain the aging mechanism during this time)

# Show status again to see how priorities have changed
status

# Show the task state graph
graph

# Show scheduler metrics
metrics
```

## 6. Comprehensive Presentation Demonstration

```bash
# Reset the simulator
reset

# Start the simulation
start

# Load the comprehensive presentation preset (25 tasks)
load_preset presentation

# Enable visualization
visualize

# Show initial status
status

# Step through execution one tick at a time
step
step

# Show the updated status
status

# Continue execution
continue

# Demonstrate task state transitions with selected tasks
block 1  # Block the EmergencyHandler (highest priority)
sleep 5 10  # Put the ErrorHandler to sleep
block 8  # Block the DisplayDriver

# Show the updated status
status
graph

# Unblock tasks
unblock 1
unblock 8

# Show the final status
status
graph

# Switch to a different scheduler to compare behavior
select_scheduler round-robin
load_preset presentation
status
graph
```

## 7. Example Simulation

```bash
# Run the example simulation with priority scheduler
example priority

# While the example is running, use these commands to observe:
status  # Show current task states

# Enable visualization during the example
visualize

# Show the task state graph during the example
graph

# Show scheduler metrics
metrics

# You can also try different scheduler types with the example:
example round-robin
# or
example fcfs
```

## 8. Demonstration Script for Presentation Flow

Here is a suggested script for a smooth presentation:

1. Start with priority scheduler and clear the screen:
   ```bash
   python main.py
   clear
   start
   ```

2. Show available presets and schedulers:
   ```bash
   list_schedulers
   list_presets
   ```

3. Load the comprehensive presentation preset (25 tasks):
   ```bash
   load_preset presentation
   status
   ```

4. Enable visualization:
   ```bash
   visualize
   ```

5. Demonstrate task state transitions:
   ```bash
   block 1  # Block highest priority task
   status
   sleep 5 10  # Put a critical task to sleep
   status
   block 10  # Block a high priority task
   status
   unblock 1  # Unblock highest priority task
   status
   graph
   ```

6. Show detailed task information and memory examination:
   ```bash
   task_info 1
   memory 0x9000 32
   disassemble 0x9000 5
   registers
   ```

7. Switch to a different scheduler to compare behavior:
   ```bash
   select_scheduler round-robin
   load_preset presentation
   status
   graph
   ```

8. Switch to another scheduler:
   ```bash
   select_scheduler fcfs
   load_preset presentation   
   status
   graph
   ```

9. Show scheduler metrics:
   ```bash
   metrics
   ```

10. Run the example simulation:
    ```bash
    select_scheduler priority
    example
    ```

11. During the example, show status and graph:
    ```bash
    status
    graph
    ```

12. Conclude with a summary of the differences observed between schedulers

## 9. Tips for a Smooth Demonstration

1. **Practice the commands** beforehand to ensure you are familiar with them
2. **Use the clear command** to keep the display clean and focused
3. **Use the preset loading feature** to quickly set up specific scenarios
4. **Use the scheduler selection feature** to compare different scheduling algorithms
5. **Use the step command** to demonstrate the scheduler's decision-making process
6. **Have a cheat sheet** with the commands ready during your presentation
7. **Explain what is happening** as you execute each command
8. **Highlight key differences** between scheduling algorithms
9. **Focus on visualization** as it provides the clearest demonstration of concepts
10. **Be prepared for questions** about implementation details

## 10. Potential Questions and Answers

### Q: How does the context switching mechanism work in your implementation?
A: Context switching is implemented in the context_switch method of SchedulerBase. It saves the current task's register context, updates its state, and then restores the new task's context or initializes it if it's the first run. This simulates how a real OS would save and restore CPU state during task switching.

### Q: What are the differences between the three scheduling algorithms you've implemented?
A: The Priority Scheduler selects tasks based on priority values (lower = higher priority) and implements preemption. The Round-Robin Scheduler gives each task a fixed time slice before switching to the next one, ensuring fair CPU allocation. The FCFS Scheduler executes tasks in the order they were created without preemption.

### Q: How does your implementation prevent starvation of lower-priority tasks?
A: We implement an aging mechanism in the _apply_aging method of SchedulerBase. It gradually increases the priority of tasks that have been waiting for a long time, ensuring that even low-priority tasks eventually get CPU time.

### Q: How realistic is your RISC-V simulation compared to actual hardware?
A: Our simulation is simplified for educational purposes. It implements the core concepts of a RISC-V processor including registers, memory, and basic instruction execution, but doesn't include advanced features like pipelining, branch prediction, or memory hierarchy. It's designed to demonstrate scheduling concepts rather than accurate hardware simulation.

### Q: How would you extend this project to make it more realistic?
A: We could extend it by implementing a more complete RISC-V instruction set, adding memory management with virtual addressing, implementing a file system, adding inter-process communication mechanisms, and creating a more sophisticated interrupt handling system.

### Q: How does your implementation handle task priorities and preemption?
A: Tasks are assigned priority values (lower = higher priority). The Priority Scheduler checks for preemption in each tick by finding the highest priority ready task and comparing it to the current task. If a higher priority task becomes ready, the current task is preempted.

### Q: What are the advantages and disadvantages of the different scheduling algorithms?
A: Priority scheduling ensures critical tasks get CPU time but can lead to starvation. Round-robin ensures fairness but may not be optimal for time-critical tasks. FCFS is simple but can lead to poor response times if long-running tasks are ahead in the queue.

### Q: How does your visualization help in understanding the scheduler behavior?
A: The visualization shows task state transitions over time, making it easy to see how tasks move between READY, RUNNING, BLOCKED, SLEEPING, and TERMINATED states. This helps understand how the scheduler makes decisions and how different scheduling algorithms affect task execution patterns.

### Q: How does your system handle a large number of tasks?
A: Our system can efficiently manage a large number of tasks through its priority-based scheduling and efficient context switching. The visualization components are designed to scale and provide clear insights even with many tasks. The preset configurations allow demonstrating scenarios with up to 25 tasks to show how different schedulers handle varying workloads.

### Q: What metrics do you use to evaluate scheduler performance?
A: We track several metrics including the number of context switches, preemptions, task state transitions, and CPU utilization. The metrics command shows these statistics, allowing you to compare the efficiency of different scheduling algorithms under various workloads.
