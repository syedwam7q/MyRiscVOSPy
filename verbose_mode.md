# Verbose Mode in PMARS

The verbose mode in PMARS provides detailed information about the internal operations of the simulator and scheduler. This is useful for debugging, understanding the system's behavior, and for educational purposes.

## Enabling Verbose Mode

To enable verbose mode, use the `verbose` command in the CLI:

```
riscv> verbose
Verbose mode enabled
```

To disable it, use the same command again:

```
riscv> verbose
Verbose mode disabled
```

## What Verbose Mode Shows

When verbose mode is enabled, the system will output detailed information about:

### 1. Task State Transitions

```
[VERBOSE] Task 1 (EmergencyHandler) state change: READY -> RUNNING
[VERBOSE] Task 2 (ErrorHandler) state change: RUNNING -> BLOCKED
```

### 2. Context Switches

```
[VERBOSE] Context switch: Task 2 (ErrorHandler) -> Task 1 (EmergencyHandler)
[VERBOSE] Saved context for Task 2 (ErrorHandler)
[VERBOSE] PC: 0x00001234, SP: 0x00010000
[VERBOSE] Restored context for Task 1 (EmergencyHandler)
[VERBOSE] PC: 0x00002000, SP: 0x00020000
[VERBOSE] Total context switches: 42
```

### 3. Scheduler Decisions

```
[VERBOSE] Found highest priority ready task: Task 1 (EmergencyHandler)
[VERBOSE] Preempting current task: Task 3 (BackgroundTask)
```

### 4. Memory Operations

```
[VERBOSE] Memory read: byte at 0x00001000 = 0x42
[VERBOSE] Memory write: byte at 0x00002000 = 0x7F (was 0x00)
```

### 5. Register Changes

```
[VERBOSE] Register changes:
[VERBOSE]   t0(x5): 0x00000000 -> 0x00000001
[VERBOSE]   a0(x10): 0x00000000 -> 0x0000000A
[VERBOSE] PC changed: 0x00001000 -> 0x00001004
```

### 6. Instruction Execution

```
[VERBOSE] Executing instruction at 0x00001000: 0x00A50533
[VERBOSE] Opcode: 0x33
[VERBOSE] Disassembly: add a0, a0, a0
```

## Benefits of Verbose Mode

1. **Educational Value**: Helps understand how the scheduler makes decisions and how tasks transition between states
2. **Debugging**: Makes it easier to identify issues in task behavior or scheduler logic
3. **Performance Analysis**: Provides insights into context switching frequency and memory access patterns
4. **System Understanding**: Gives a deeper view into the internal workings of the RISC-V simulator

## When to Use Verbose Mode

- During demonstrations to explain system behavior
- When debugging unexpected task behavior
- When teaching concepts like context switching and scheduling
- When analyzing performance bottlenecks

## When Not to Use Verbose Mode

- During normal operation as it generates a lot of output
- When running long simulations as it can slow down execution
- When the focus is on high-level task behavior rather than low-level details

## Example Use Case

```
riscv> start
Simulation started

riscv> load_preset basic
Loaded preset 'basic' with 3 tasks

riscv> verbose
Verbose mode enabled

riscv> step
[VERBOSE] Context switch: None -> Task 1 (HighPriorityTask)
[VERBOSE] Initialized new Task 1 (HighPriorityTask)
[VERBOSE] Entry point: 0x00001000, SP: 0x00010000
[VERBOSE] Task 1 (HighPriorityTask) state change: READY -> RUNNING
[VERBOSE] Run count: 1
[VERBOSE] Total context switches: 1
[VERBOSE] Executing instruction at 0x00001000: 0x00100513
[VERBOSE] Opcode: 0x13
[VERBOSE] Disassembly: addi a0, zero, 1
[VERBOSE] Register changes:
[VERBOSE]   a0(x10): 0x00000000 -> 0x00000001
[VERBOSE] PC changed: 0x00001000 -> 0x00001004

Executed one tick. Use 'step' again to continue stepping or 'continue' to resume continuous execution.

riscv> verbose
Verbose mode disabled
```
