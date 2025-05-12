# PMARS - Python Multitasking Archhitecture for RISCV Systems

A Python-based implementation of a multitasking scheduler for RISC-V architecture, developed for Advanced Computer Architecture (ACAD) course.

## Overview

This project implements a multitasking scheduler for RISC-V architecture in Python, inspired by [mini-riscv-os](https://github.com/cccriscv/mini-riscv-os). It simulates the behavior of a RISC-V processor and provides a framework for scheduling and executing multiple tasks.

## Features

- **Context Switching**: Save and restore task states including registers and program counters
- **Preemptive Multitasking**: Use timer interrupts to preempt running tasks
- **Priority-Based Scheduling**: Execute tasks based on their priority levels
- **Aging Mechanism**: Prevent starvation of lower-priority tasks
- **Blocking and Sleeping**: Support for tasks that voluntarily yield CPU
- **Time Slicing**: Implement round-robin scheduling for fair CPU allocation
- **Cooperative Multitasking**: Support for tasks that voluntarily yield control
- **System Calls and Interrupt Handling**: Manage tasks and respond to hardware events
- **Process State Visualization**: Monitor and visualize task states

## Project Structure

- `core/`: Core components of the RISC-V simulator
  - `simulator.py`: Main simulator implementation
  - `registers.py`: RISC-V register file implementation
  - `memory.py`: Memory model implementation
  - `interrupts.py`: Interrupt controller implementation
- `scheduler/`: Implementation of different scheduling algorithms
  - `scheduler_base.py`: Base scheduler implementation
  - `priority_scheduler.py`: Priority-based preemptive scheduler
  - `round_robin_scheduler.py`: Round-robin scheduler with time slicing
  - `fcfs_scheduler.py`: First-Come, First-Served scheduler
  - `scheduler_factory.py`: Factory for creating scheduler instances
- `tasks/`: Sample tasks and task management
  - `sample_tasks.py`: Sample task implementations for testing
- `ui/`: User interface components
  - `cli.py`: Command-line interface
  - `visualization.py`: Visualization utilities
- `utils/`: Utility functions and helpers
  - `disassembler.py`: RISC-V instruction disassembler
- `tests/`: Test cases for various components
  - `test_scheduler.py`: Tests for the scheduler
  - `test_disassembler.py`: Tests for the disassembler

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the simulator: `python main.py`

## Usage

### Running the Simulator

```bash
# Run with default settings (priority scheduler)
python main.py

# Run with round-robin scheduler
python main.py --scheduler round-robin --time-slice 10

# Run with FCFS scheduler
python main.py --scheduler fcfs

# Run with debug mode enabled
python main.py --debug

# Run without sample tasks
python main.py --no-sample-tasks
```

### Command-Line Interface

Once the simulator is running, you can use the following commands:

#### Basic Commands
- `help`: Show help message for all commands
- `help_command <command>`: Show detailed help for a specific command
- `exit`, `quit`: Exit the simulator
- `clear`: Clear the screen
- `start`: Start the simulation
- `stop`: Stop the simulation
- `status`: Show the current status of the simulator

#### Task Management
- `tasks`: List all tasks
- `task_info <task_id>`: Show detailed information about a specific task
- `create <n> <priority> <entry_point> [stack_size]`: Create a new task
- `terminate <task_id>`: Terminate a task
- `kill <task_id>`: Alias for terminate
- `block <task_id>`: Block a task
- `unblock <task_id>`: Unblock a task
- `sleep <task_id> <ticks>`: Put a task to sleep
- `priority <task_id> <new_priority>`: Change the priority of a task

#### Memory and Register Examination
- `registers`: Show register values
- `memory <address> <size>`: Show memory contents
- `disassemble <address> <count>`: Disassemble instructions in memory

#### Visualization and Monitoring
- `visualize`: Toggle task state history collection
- `graph`: Show task state graph
- `metrics`: Show scheduler performance metrics

#### Execution Control
- `step`: Execute a single tick of the scheduler
- `continue`: Resume continuous execution after stepping
- `verbose`: Toggle verbose output mode

#### Presets and Examples
- `example`: Run an example simulation with multiple tasks
- `list_schedulers`: List available scheduler types
- `select_scheduler <type>`: Switch to a different scheduler type
- `list_presets`: List available task presets
- `load_preset <name>`: Load a predefined set of tasks

### Visualization Features

The simulator includes visualization features that allow you to collect and view task state history:

- Use `visualize` to toggle task state history collection on/off
- Use `status` to see the current state of the simulator and tasks
- Use `graph` to display the task state graph based on collected history
- Use `visualize_stop` as an alias to disable history collection

When visualization data collection is enabled, the simulator records task state changes in the background without affecting the command prompt. This allows you to continue interacting with the simulator normally while data is being collected for later visualization.

### Example Simulation

The simulator includes an example simulation feature that creates and manages multiple tasks automatically:

```
riscv> example [scheduler_type]
```

This creates over 30 tasks with different priorities and behaviors, allowing you to observe the scheduler in action. The example simulation runs for approximately 30 seconds, performing various operations on tasks to demonstrate scheduling behavior.

The simulation temporarily disables the priority aging mechanism to ensure tasks maintain their original priorities throughout the demonstration.

Throughout the simulation, tasks will automatically change states (blocking, unblocking, sleeping, terminating) to demonstrate how the scheduler handles different scenarios.

The tasks are organized into priority groups:
- 5 high priority tasks (priorities 1-5)
- 10 medium priority tasks (priorities 6-15)
- 10 low priority tasks (priorities 16-25)
- 5 background tasks (priorities 26-30)
- 2 idle tasks (priorities 31-32)

The status display shows both the current priority and the original priority (in parentheses). The current priority may change due to the aging mechanism, which increases the priority of tasks that have been waiting for a long time to prevent starvation. The example simulation periodically resets priorities to their original values to better demonstrate the different priority levels.

During the simulation, various actions are performed:
- Blocking and unblocking tasks
- Putting tasks to sleep for different durations
- Terminating tasks
- Creating new high priority tasks
- Periodic status updates

While the example simulation is running, you can:
- Use `status` to see the current state of tasks
- Use `visualize` to enable task state history collection (not enabled by default)
- Use `visualize_stop` if the screen gets stuck during visualization
- Use `graph` to see the task state graph
- Continue using other commands normally

The example simulation automatically disables visualization at the start and end to prevent screen issues. You can manually enable it with the `visualize` command when needed.

You can optionally specify a scheduler type (`priority`, `round-robin`, or `fcfs`) to see how different scheduling algorithms handle the same tasks.

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test module
python -m unittest tests.test_scheduler
python -m unittest tests.test_disassembler
```

## Example: Creating and Managing Tasks

```
# Start the simulation
riscv> start

# Create a new task
riscv> create MyTask 5 0x1000 1024

# List all tasks
riscv> tasks

# Block a task
riscv> block 1

# Unblock a task
riscv> unblock 1

# Put a task to sleep
riscv> sleep 1 10

# Terminate a task
riscv> terminate 1
```

## Example: Examining Memory and Instructions

```
# View memory contents
riscv> memory 0x1000 64

# Disassemble instructions
riscv> disassemble 0x1000 10
```

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
