#!/usr/bin/env python3
"""
MyRiscvOSPy - Main Entry Point
A Python-based implementation of a multitasking scheduler for RISC-V architecture
"""

import argparse
import sys
from ui.cli import CLI
from core.simulator import RiscvSimulator
from scheduler.scheduler_factory import create_scheduler
from tasks.sample_tasks import create_sample_tasks, load_sample_programs

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='RISC-V Multitasking Scheduler in Python')
    parser.add_argument('--scheduler', type=str, default='priority',
                        choices=['priority', 'round-robin', 'fcfs'],
                        help='Scheduler algorithm to use')
    parser.add_argument('--ui', type=str, default='cli',
                        choices=['cli', 'gui', 'web'],
                        help='User interface to use')
    parser.add_argument('--tasks', type=int, default=5,
                        help='Number of sample tasks to create')
    parser.add_argument('--time-slice', type=int, default=10,
                        help='Time slice for round-robin scheduling (in ticks)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    parser.add_argument('--no-sample-tasks', action='store_true',
                        help='Do not create sample tasks')
    
    return parser.parse_args()

def main():
    """Main entry point for the application"""
    args = parse_arguments()
    
    # Initialize the RISC-V simulator
    simulator = RiscvSimulator(debug=args.debug)
    
    # Create the scheduler
    scheduler = create_scheduler(
        scheduler_type=args.scheduler,
        time_slice=args.time_slice,
        simulator=simulator
    )
    
    # Load sample programs and create sample tasks
    if not args.no_sample_tasks:
        print(f"Loading sample programs...")
        load_sample_programs(simulator)
        
        print(f"Creating {args.tasks} sample tasks...")
        task_ids = create_sample_tasks(scheduler, args.tasks)
        print(f"Created tasks: {task_ids}")
    
    # Initialize the UI
    if args.ui == 'cli':
        ui = CLI(simulator, scheduler)
    else:
        print(f"UI type '{args.ui}' not implemented yet. Using CLI.")
        ui = CLI(simulator, scheduler)
    
    print(f"Starting {scheduler.get_scheduler_type()}...")
    print("Type 'help' for a list of commands.")
    
    # Start the UI
    try:
        ui.start()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())