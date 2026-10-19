# Day 01 — Linux & DevOps Foundations

## Experiment 1 — Program vs Process

### Program

`app.py` is a Python program stored as a file on disk.

### Process

When I execute:

`python app.py`

the operating system starts a Python process that executes the program.

### Observation

I used:

`Get-Process python`

to inspect running Python processes.

Each process had its own Process ID (PID).

Example:

- PID 3920
- PID 24384
- PID 2704

The process created by my experiment was PID 2704.

After pressing `Ctrl+C`, PID 2704 disappeared from the list of running Python processes.

### Key Learning

A program is code stored on disk.

A process is a running instance of a program managed by the operating system.

A process has resources such as:

- PID
- CPU time
- Memory
- Process state

## Experiment 1 — Program vs Process

### Objective

Understand the difference between a program stored on disk and a running process.

### Program

`app.py` is a Python program stored as a file.

### Process

When I execute:

```powershell
python app.py