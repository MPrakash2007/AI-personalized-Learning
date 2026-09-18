"""
Generates complete, exam-oriented academic dataset for all 11 Operating Systems (OS) topics.
Saves to backend/curriculum/data/os.json.
"""
import os
import json

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "os.json"))

OS_TOPICS = {
    "os-fundamentals": {
        "title": "OS Fundamentals",
        "subject": "os",
        "exam_definition": (
            "An Operating System (OS) is system software that acts as an intermediary interface between computer hardware "
            "and user applications, providing hardware abstraction, resource management (CPU, memory, I/O, storage), "
            "and execution environment control."
        ),
        "remember": "Dual Mode Operation: User Mode (Ring 3, unprivileged) and Kernel Mode (Ring 0, privileged) separated by Hardware Mode Bit.",
        "core_concept": (
            "Without an operating system, every application would require direct machine code control over physical device registers, "
            "causing catastrophic crashes, security vulnerabilities, and zero resource sharing. The OS implements virtualization, "
            "concurrency, and persistence. The kernel is the core program that remains in RAM continuously, managing hardware "
            "through system calls (syscalls)."
        ),
        "key_points": [
            "Kernel: Core component loaded into memory at boot that manages hardware and system execution.",
            "Dual-Mode Operation: Hardware mode bit (0 = Kernel Mode, 1 = User Mode) prevents user code from accessing privileged instructions.",
            "System Calls: Software interrupts providing an interface to request privileged OS kernel services (e.g. fork(), read(), write()).",
            "Monolithic vs Microkernel: Monolithic runs all services in kernel space; Microkernel runs minimum services in kernel space and remainder in user space.",
            "Bootstrapping: Bootstrap loader in ROM/BIOS/UEFI initializes hardware and loads the OS kernel into memory."
        ],
        "classification": {
            "title": "Types of Operating Systems",
            "items": [
                {"name": "Batch OS", "desc": "Jobs with similar requirements are batched together and executed sequentially without user interaction."},
                {"name": "Time-Sharing (Multitasking) OS", "desc": "CPU time is divided into slices (quanta) among multiple processes to provide rapid interactive response."},
                {"name": "Distributed OS", "desc": "Manages a collection of independent networked computers presenting them as a single coherent system."},
                {"name": "Real-Time OS (RTOS)", "desc": "Guarantees strict deterministic timing constraints (Hard RTOS: missing deadline is system failure; Soft RTOS: quality degrades)."},
                {"name": "Clustered OS", "desc": "Combines multiple physical CPUs or server nodes sharing storage for high availability and load balancing."}
            ]
        },
        "how_it_works": {
            "title": "System Call Execution Flow & Mode Switch",
            "steps": [
                "1. User application executes a library wrapper (e.g. POSIX read() or Windows ReadFile).",
                "2. Wrapper places the system call number and parameters in designated CPU registers.",
                "3. Trap instruction (software interrupt) is executed, transitioning the CPU from User Mode (bit 1) to Kernel Mode (bit 0).",
                "4. CPU hardware looks up the interrupt vector table to invoke the OS System Call Handler.",
                "5. Kernel verifies parameters, executes the privileged service, and stores the return value in a register.",
                "6. Return-from-interrupt (sysret/iret) instruction resets mode bit to 1 and returns control to user program."
            ],
            "diagram": "User Application (User Mode) → TRAP Instruction → System Call Handler (Kernel Mode) → Hardware Access → Return to User Mode"
        },
        "example": {
            "title": "Linux System Call Invocation via C",
            "scenario": "A program reads data from standard input using the low-level `read` system call, invoking kernel trap 0x80 or syscall assembly instruction.",
            "code": (
                "#include <unistd.h>\n"
                "#include <stdio.h>\n\n"
                "int main() {\n"
                "    char buffer[128];\n"
                "    // syscall: 0 = stdin, buffer = target memory, 128 = max bytes\n"
                "    ssize_t bytes_read = read(0, buffer, sizeof(buffer) - 1);\n"
                "    if (bytes_read > 0) {\n"
                "        buffer[bytes_read] = '\\0';\n"
                "        write(1, buffer, bytes_read); // syscall: 1 = stdout\n"
                "    }\n"
                "    return 0;\n"
                "}"
            )
        },
        "comparison": {
            "title": "Monolithic Kernel vs Microkernel Architecture",
            "headers": ["Parameter", "Monolithic Kernel", "Microkernel"],
            "rows": [
                ["Architecture", "All OS services (VFS, IPC, Drivers, Scheduler) reside in single kernel address space", "Only fundamental mechanisms (IPC, basic scheduling, memory mapping) reside in kernel space; servers run in user space"],
                ["Performance", "Very High — direct function calls without context switching", "Lower — requires frequent IPC message passing and context switches"],
                ["Reliability", "Low — a bug in any device driver can crash the entire system", "High — crashed driver or user-space server can be restarted without kernel panic"],
                ["Extensibility", "Difficult — adding new services requires recompiling or inserting kernel modules", "Easy — new services added as independent user-space daemons"],
                ["Examples", "Linux, Traditional UNIX, Windows NT kernel core", "Mach, QNX, L4, MINIX"]
            ]
        },
        "formulas": [
            {"name": "Dual Mode Switch Invariant", "formula": "Mode Bit: 1 (User Mode) -> [TRAP] -> 0 (Kernel Mode) -> [IRET] -> 1 (User Mode)", "explanation": "Ensures unprivileged code cannot execute privileged CPU instructions (CLI, HLT, LGDT)."}
        ],
        "exam_tip": "Always mention the 'Mode Bit' when explaining user mode vs kernel mode transitions. In university exams, draw the 2-ring diagram showing Ring 0 (Kernel) and Ring 3 (User).",
        "common_confusion": {
            "wrong": "System calls and library functions (like printf or malloc) are the exact same thing.",
            "correct": "Library functions are user-space helper functions. Some (like strcpy, strlen) run entirely in user mode; others (like printf, fopen) wrap underlying OS system calls (write, open) via traps.",
            "explanation": "Calling `strlen()` triggers zero context switches; calling `write()` transitions the CPU to Ring 0."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the primary function of the OS Kernel?",
                "a": "The kernel is the core, resident component of the operating system that directly interfaces with hardware. Its primary functions are process management, CPU scheduling, memory allocation, virtual file system management, and I/O device control."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Dual-Mode Operation in modern Operating Systems. Why is it essential for system protection?",
                "a": "1. Definition: Dual-mode operation separates CPU execution into User Mode (unprivileged, mode bit = 1) and Kernel/Supervisor Mode (privileged, mode bit = 0).\n2. Protection Mechanism: Privileged instructions (such as I/O instructions, halt, memory management register modification) can only be executed in Kernel Mode. If an application attempts a privileged instruction in User Mode, hardware generates a trap/exception.\n3. Transition: Transitions occur via System Calls, Hardware Interrupts, or Exceptions.\n4. Importance: Prevents erroneous or malicious user programs from overwriting OS memory, corrupting file systems, or monopolizing the CPU."
            },
            {
                "marks": "10-Mark Question",
                "q": "Compare Monolithic and Microkernel architectures with diagrams, highlighting advantages, disadvantages, and real-world examples.",
                "a": "1. Monolithic Architecture: All operating system components (File System, Virtual Memory, IPC, Network Stack, Device Drivers) execute within a single unified address space in Kernel Mode. Advantages: Maximum speed and throughput due to zero IPC overhead. Disadvantages: Poor fault isolation; a single buggy driver crashes the kernel. Examples: Linux, FreeBSD.\n2. Microkernel Architecture: Strips the kernel down to essential primitives: minimal process scheduling, memory mapping, and IPC. High-level services (Device Drivers, File Systems, Networking) run as autonomous servers in User Mode. Advantages: Highly modular, secure, fault-tolerant; failing server restarts seamlessly. Disadvantages: Performance penalty due to continuous IPC message copying and context switching. Examples: QNX, Minix, Mach.\n3. Hybrid Systems: Modern systems like Windows NT and macOS incorporate microkernel modularity with monolithic performance paths."
            }
        ],
        "revision_60s": [
            "OS acts as resource manager and extended machine hardware abstractor.",
            "Kernel stays in RAM permanently; shell/GUI are user-space utilities.",
            "Mode Bit 0 = Kernel/Privileged; Mode Bit 1 = User/Restricted.",
            "System Call = software trap requesting kernel service.",
            "Monolithic = all services in kernel; Microkernel = minimal core, rest in user space."
        ]
    },

    "processes": {
        "title": "Processes & Process Management",
        "subject": "os",
        "exam_definition": (
            "A Process is a program in execution, represented in the operating system by a Process Control Block (PCB) "
            "containing its execution state, Program Counter (PC), CPU registers, memory limits, and open file descriptors."
        ),
        "remember": "Process Address Space: Text (Code) -> Data (Init Globals) -> BSS (Uninit Globals) -> Heap (Grows Up) -> Stack (Grows Down).",
        "core_concept": (
            "A program is a passive entity stored on disk (executable file), whereas a process is an active entity loaded "
            "into memory with assigned resources and execution state. Operating systems support multiprogramming by maintaining "
            "isolated address spaces for each process, managed through a 5-state or 7-state lifecycle model."
        ),
        "key_points": [
            "Process Control Block (PCB): Kernel data structure storing PID, State, Program Counter, CPU Registers, Memory Limits, and Open File List.",
            "Process States: New (created), Ready (waiting for CPU), Running (executing on CPU), Waiting/Blocked (waiting for I/O or event), Terminated (finished).",
            "Context Switching: Saving the state of the currently running process into its PCB and restoring the state of the next scheduled process.",
            "Process Creation: UNIX uses fork() to duplicate the parent process and exec() to overwrite the address space with a new binary.",
            "Zombie vs Orphan: Zombie has terminated but parent has not read exit status with wait(); Orphan's parent terminated before it, adopted by init/systemd (PID 1)."
        ],
        "classification": {
            "title": "Process States (5-State Model)",
            "items": [
                {"name": "New", "desc": "The process is being created and its PCB allocated in memory."},
                {"name": "Ready", "desc": "The process is loaded in RAM and waiting to be assigned to a CPU core by the scheduler."},
                {"name": "Running", "desc": "Instructions are actively being executed on the CPU core."},
                {"name": "Waiting (Blocked)", "desc": "The process cannot run until an I/O operation completes or a signal is received."},
                {"name": "Terminated", "desc": "The process has finished execution; OS deallocates resources while retaining exit status."}
            ]
        },
        "how_it_works": {
            "title": "Process Context Switch Mechanics",
            "steps": [
                "1. Hardware timer interrupt or system call triggers a transition to kernel mode.",
                "2. Current process P0's CPU registers (PC, SP, general registers) are saved into its PCB0 in memory.",
                "3. CPU Scheduler selects the next candidate process P1 from the Ready Queue.",
                "4. Kernel updates memory management registers (CR3 / page tables) to point to P1's virtual address space.",
                "5. Saved registers and Program Counter from PCB1 are loaded into the physical CPU hardware registers.",
                "6. CPU returns to user mode, resuming P1 at its saved Program Counter."
            ],
            "diagram": "Process P0 Running → Interrupt → Save State to PCB0 → Scheduler selects P1 → Reload State from PCB1 → Process P1 Running"
        },
        "example": {
            "title": "Process Creation with fork() and wait() in C",
            "scenario": "A parent process forks an exact duplicate child process. The child replaces its binary with `ls` using execvp, while the parent waits.",
            "code": (
                "#include <stdio.h>\n"
                "#include <unistd.h>\n"
                "#include <sys/wait.h>\n\n"
                "int main() {\n"
                "    pid_t pid = fork(); // Duplicates calling process\n\n"
                "    if (pid < 0) {\n"
                "        perror(\"Fork failed\");\n"
                "    } else if (pid == 0) {\n"
                "        // Child process: pid is 0\n"
                "        printf(\"Child process PID: %d, Parent PID: %d\\n\", getpid(), getppid());\n"
                "        char *args[] = {\"ls\", \"-l\", NULL};\n"
                "        execvp(args[0], args); // Overwrite with new program\n"
                "    } else {\n"
                "        // Parent process: pid holds child PID\n"
                "        wait(NULL); // Block until child terminates (prevents Zombie)\n"
                "        printf(\"Parent process resumed after child completed\\n\");\n"
                "    }\n"
                "    return 0;\n"
                "}"
            )
        },
        "comparison": {
            "title": "Program vs Process vs Thread",
            "headers": ["Feature", "Program", "Process", "Thread"],
            "rows": [
                ["Nature", "Passive binary entity stored on non-volatile disk", "Active instance of program executing in dedicated memory", "Lightweight unit of execution within a parent process"],
                ["Memory Space", "Stored on disk filesystem", "Independent isolated virtual address space (PCB, Heap, Stack)", "Shares parent process's Text, Data, and Heap; private Stack & PC"],
                ["Creation Overhead", "None (static file)", "High (allocates PCB, page tables, memory regions)", "Low (shares address space; allocates small stack & TCB)"],
                ["Communication", "N/A", "Inter-Process Communication (IPC): pipes, sockets, shared memory", "Direct memory access via shared global/heap variables"]
            ]
        },
        "formulas": [
            {"name": "Context Switch Overhead Cost", "formula": "T_overhead = T_save_PCB + T_scheduler_select + T_flush_TLB + T_load_PCB", "explanation": "Context switching is pure overhead during which the CPU performs no productive user work."}
        ],
        "exam_tip": "In questions on fork(), remember that fork() returns 0 to the child process and returns the positive child PID to the parent process. If fork() is called in a loop $n$ times, it creates $2^n - 1$ child processes.",
        "common_confusion": {
            "wrong": "Zombie processes consume heavy CPU and RAM until they are rebooted.",
            "correct": "Zombie processes consume zero CPU and zero memory. They only occupy an entry in the OS Process Table so the parent can read their exit status.",
            "explanation": "If the parent dies without wait(), init (PID 1) reaps the zombie automatically."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the difference between a Zombie Process and an Orphan Process?",
                "a": "An Orphan process is a running child whose parent terminated before calling wait(); it is adopted by init/systemd (PID 1). A Zombie process has completed execution but retains an entry in the process table because its parent has not yet read its exit code via wait()."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the structure and components of a Process Control Block (PCB).",
                "a": "The PCB is the kernel data structure representing a process. Key components include:\n1. Process ID (PID): Unique integer identifier.\n2. Process State: Current status (Ready, Running, Waiting, Terminated).\n3. Program Counter (PC): Memory address of next instruction to execute.\n4. CPU Registers: Accumulators, index registers, stack pointers saved during context switches.\n5. CPU Scheduling Info: Process priority and scheduling queue pointers.\n6. Memory Management Info: Page tables, segment tables, and base/limit registers.\n7. Accounting & I/O Status: CPU time used, open file descriptors, allocated I/O devices."
            },
            {
                "marks": "10-Mark Question",
                "q": "Describe the 5-state process lifecycle model with a state transition diagram and detail each state transition trigger.",
                "a": "1. Five States: New, Ready, Running, Waiting (Blocked), Terminated.\n2. State Transitions:\n   - New to Ready: OS admits the process into RAM and creates its PCB.\n   - Ready to Running: The Short-Term Scheduler dispatches the process to an available CPU core.\n   - Running to Ready: Time slice expiration (Timer Interrupt in preemptive scheduling) or higher-priority process preemption.\n   - Running to Waiting: Process requests I/O or waits for an event/signal (e.g. read(), wait()).\n   - Waiting to Ready: I/O completion interrupt or event occurrence.\n   - Running to Terminated: Process completes normal execution (exit()) or is killed by an unhandled signal/exception.\n3. Diagram and Context Switch impact: Explain how PCB is swapped during each transition."
            }
        ],
        "revision_60s": [
            "Process = active program in execution with PCB.",
            "PCB contains PID, PC, Registers, Memory Limits, Open Files.",
            "Address space: Text (Code), Data/BSS (Globals), Heap (Dynamic), Stack (Frames).",
            "fork() duplicates process: returns 0 to child, child PID to parent.",
            "Zombie = finished but unread exit status; Orphan = running without parent (adopted by init)."
        ]
    },

    "threads": {
        "title": "Threads & Concurrency",
        "subject": "os",
        "exam_definition": (
            "A Thread is a lightweight unit of CPU execution within a process that possesses its own Thread ID, Program Counter (PC), "
            "register set, and stack, while sharing the code section, data section, and OS resources with peer threads in the same process."
        ),
        "remember": "Thread Shares: Code, Global Data, Heap, Open Files. Thread Keeps Private: Thread ID, PC, Registers, Stack Space.",
        "core_concept": (
            "Creating separate processes for concurrent tasks introduces massive overhead in memory allocation and IPC. "
            "Multithreading allows multiple flows of control within the exact same virtual address space. Multithreaded applications "
            "exploit modern multi-core architectures to achieve true hardware parallelism."
        ),
        "key_points": [
            "Lightweight: Thread creation and context switching require orders of magnitude fewer CPU cycles than processes.",
            "Shared vs Private: Threads share Code, Data, Heap, and File Descriptors, but maintain independent Stacks and Registers.",
            "User-Level Threads (ULT): Managed entirely by user-space runtime libraries without kernel awareness (fast switching, but one blocking call blocks entire process).",
            "Kernel-Level Threads (KLT): Managed directly by the OS kernel (true multicore parallelism; slightly higher context switch overhead).",
            "Multithreading Models: Many-to-One (ULTs mapped to single KLT), One-to-One (each ULT mapped to one KLT — standard in Linux/Windows), Many-to-Many."
        ],
        "classification": {
            "title": "Multithreading Architecture Models",
            "items": [
                {"name": "Many-to-One Model", "desc": "Multiple user threads mapped to single kernel thread. Fast switching, but zero multicore parallelism and one blocking call blocks all."},
                {"name": "One-to-One Model", "desc": "Each user thread maps to an independent kernel thread (e.g. Linux NPTL, Windows threads). Supports true multicore parallelism."},
                {"name": "Many-to-Many Model", "desc": "Multiplexes $M$ user threads over $N$ kernel threads ($M \\ge N$). Optimal resource utilization with tunable concurrency."}
            ]
        },
        "how_it_works": {
            "title": "Multicore Thread Parallelism vs Concurrent Interleaving",
            "steps": [
                "1. Application creates worker threads via POSIX pthread_create() or language thread primitives.",
                "2. OS allocates Thread Control Block (TCB) and allocates a thread-private stack in the process address space.",
                "3. On a single core CPU, threads execute concurrently via time-sliced round-robin interleaving.",
                "4. On a multicore CPU, the kernel dispatches different KLTs to physical Core 0 and Core 1 simultaneously.",
                "5. When thread finishes, pthread_join() synchronizes termination and reclaims thread stack resources."
            ],
            "diagram": "Process Address Space [Code | Data | Heap] ──┬── Thread 1 (Stack 1 + PC 1) ── Core 0\n                                             └── Thread 2 (Stack 2 + PC 2) ── Core 1"
        },
        "example": {
            "title": "POSIX Threads (pthreads) in C",
            "scenario": "Two concurrent threads increment a shared counter using pthreads on Linux.",
            "code": (
                "#include <pthread.h>\n"
                "#include <stdio.h>\n\n"
                "long counter = 0; // Shared resource in Data segment\n\n"
                "void* worker(void* arg) {\n"
                "    for (int i = 0; i < 100000; i++) {\n"
                "        counter++; // Warning: Race condition without mutex!\n"
                "    }\n"
                "    return NULL;\n"
                "}\n\n"
                "int main() {\n"
                "    pthread_t t1, t2;\n"
                "    pthread_create(&t1, NULL, worker, NULL); // Launch thread 1\n"
                "    pthread_create(&t2, NULL, worker, NULL); // Launch thread 2\n"
                "    pthread_join(t1, NULL); // Await completion\n"
                "    pthread_join(t2, NULL);\n"
                "    printf(\"Final counter: %ld\\n\", counter);\n"
                "    return 0;\n"
                "}"
            )
        },
        "comparison": {
            "title": "User-Level Threads (ULT) vs Kernel-Level Threads (KLT)",
            "headers": ["Attribute", "User-Level Threads (ULT)", "Kernel-Level Threads (KLT)"],
            "rows": [
                ["Management", "User-space thread library (e.g. Green Threads)", "Operating System Kernel"],
                ["Kernel Awareness", "Kernel sees only 1 single-threaded process", "Kernel is directly aware of each individual thread"],
                ["Context Switch Overhead", "Extremely low (no mode switch to Ring 0)", "Moderate (requires transition to Kernel Mode)"],
                ["Multicore Execution", "Cannot run on multiple physical CPU cores simultaneously", "True hardware parallelism across multiple cores"],
                ["Blocking System Call", "If one thread makes a blocking call, entire process blocks", "One thread blocking does not affect other threads in the process"]
            ]
        },
        "formulas": [
            {"name": "Amdahl's Law (Speedup with Parallelism)", "formula": "Speedup = 1 / ((1 - P) + (P / S))", "explanation": "Where P is the parallel proportion of the program and S is the number of processing cores."}
        ],
        "exam_tip": "In exams, remember Amdahl's Law formula! If 40% of an application is strictly serial ($1-P = 0.40$), the maximum theoretical speedup is $1 / 0.40 = 2.5\\times$, regardless of having 100 CPU cores.",
        "common_confusion": {
            "wrong": "Concurrency and Parallelism are identical terms.",
            "correct": "Concurrency is about dealing with lots of things at once (structure/interleaving on single or multi-core); Parallelism is about doing lots of things at once (simultaneous execution on multiple physical cores).",
            "explanation": "A single-core system can have concurrency via time-slicing, but zero hardware parallelism."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What resources are shared between threads of the same process?",
                "a": "Threads of the same process share the Text (Code) segment, Data segment (global variables), Heap (dynamically allocated memory), and OS resources (open file descriptors, signals, sockets). Each thread maintains its own Program Counter, register set, and private Stack."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the One-to-One and Many-to-One multithreading models with their trade-offs.",
                "a": "1. Many-to-One Model: Maps multiple user-level threads to a single kernel thread. Advantages: Thread management is handled in user space, so thread creation and switching are fast with zero kernel intervention. Disadvantages: If a thread executes a blocking system call, the entire process halts; cannot utilize multiple CPU cores.\n2. One-to-One Model: Maps each user thread directly to an independent kernel thread (e.g. modern Linux and Windows). Advantages: True multicore parallel execution; one thread blocking does not stall peer threads. Disadvantages: Creating user threads incurs kernel resource allocation overhead."
            },
            {
                "marks": "10-Mark Question",
                "q": "State and derive Amdahl's Law. Calculate the speedup obtained on a 16-core system if 80% of the program can be parallelized.",
                "a": "1. Amdahl's Law Definition: Predicts the theoretical maximum speedup latency of an execution task at fixed workload that can be expected of a system whose resources are improved.\n2. Formula: Speedup = 1 / ((1 - P) + (P / N)), where P is the parallel fraction and N is the number of cores.\n3. Calculation:\n   - Given P = 0.80, Serial fraction (1 - P) = 0.20, N = 16 cores.\n   - Speedup = 1 / (0.20 + (0.80 / 16)) = 1 / (0.20 + 0.05) = 1 / 0.25 = 4.0x.\n4. Implication: Even with 16 cores, the speedup is capped at 4x due to the 20% serial bottleneck. As N approaches infinity, maximum speedup = 1 / 0.20 = 5.0x."
            }
        ],
        "revision_60s": [
            "Thread = lightweight execution unit within a process.",
            "Threads share: Code, Data, Heap, Files. Threads keep private: TCB, PC, Registers, Stack.",
            "ULT = managed by library (fast, but one blocking call blocks all).",
            "KLT = managed by kernel (true multicore parallelism).",
            "Amdahl's Law: Speedup = 1 / ((1-P) + P/N)."
        ]
    },

    "cpu-scheduling": {
        "title": "CPU Scheduling Algorithms",
        "subject": "os",
        "exam_definition": (
            "CPU Scheduling is the process by which the OS short-term scheduler selects an executable process from the Ready Queue "
            "and allocates the CPU to it, optimizing criteria such as CPU utilization, throughput, turnaround time, waiting time, and response time."
        ),
        "remember": "TAT = Completion Time - Arrival Time | Waiting Time = Turnaround Time - Burst Time | Response Time = First CPU Time - Arrival Time.",
        "core_concept": (
            "In a multiprogrammed system, the CPU switches between processes whenever the active process yields or waits for I/O, "
            "keeping CPU utilization close to 100%. Scheduling algorithms can be Preemptive (OS forcibly interrupts a running process, "
            "e.g. Round Robin, SRTF) or Non-Preemptive (process holds CPU until it voluntarily terminates or blocks, e.g. FCFS, SJF)."
        ),
        "key_points": [
            "Scheduling Criteria: CPU Utilization (max), Throughput (max), Turnaround Time (min), Waiting Time (min), Response Time (min).",
            "Preemptive vs Non-Preemptive: Preemptive preempts when higher priority arrives or quantum expires; Non-preemptive runs until completion/yield.",
            "FCFS (First-Come, First-Served): Simple, non-preemptive, suffers from Convoy Effect (short processes delayed behind long processes).",
            "SJF / SRTF (Shortest Job First / Shortest Remaining Time First): Mathematically optimal for minimum average waiting time; causes starvation for long processes.",
            "Round Robin (RR): Preemptive algorithm using fixed time quantum $q$; standard for time-sharing systems.",
            "Priority Scheduling: CPU allocated based on priority integer; solved starvation using Aging technique."
        ],
        "classification": {
            "title": "CPU Scheduling Algorithms",
            "items": [
                {"name": "FCFS (First-Come, First-Served)", "desc": "Non-preemptive algorithm servicing processes strictly in arrival order via FIFO queue."},
                {"name": "SJF (Shortest Job First)", "desc": "Non-preemptive algorithm selecting process with shortest CPU burst time. Optimal average waiting time."},
                {"name": "SRTF (Shortest Remaining Time First)", "desc": "Preemptive SJF; preempts running process if a new process arrives with shorter remaining burst."},
                {"name": "Round Robin (RR)", "desc": "Preemptive time-sliced algorithm cycling through Ready Queue with quantum $q$."},
                {"name": "Priority Scheduling", "desc": "Allocates CPU based on priority levels; can be preemptive or non-preemptive. Requires Aging to prevent starvation."},
                {"name": "Multilevel Feedback Queue (MLFQ)", "desc": "Multiple priority queues with varying time quanta; processes dynamically move between queues based on CPU-burst behavior."}
            ]
        },
        "how_it_works": {
            "title": "Gantt Chart Evaluation Flow",
            "steps": [
                "1. Sort ready processes by Arrival Time (AT).",
                "2. Maintain Ready Queue and track current time $T$.",
                "3. Select next process based on algorithm criteria (e.g. smallest burst for SJF, head of queue for FCFS/RR).",
                "4. Execute process until completion (non-preemptive) or until quantum/preemption condition (preemptive).",
                "5. Calculate Completion Time (CT), Turnaround Time ($TAT = CT - AT$), and Waiting Time ($WT = TAT - BT$).",
                "6. Compute average TAT and average WT across all $N$ processes."
            ],
            "diagram": "Ready Queue → Dispatcher → CPU Execution [Gantt Chart Timeline] → CT Calculation → TAT & WT Metrics"
        },
        "example": {
            "title": "Round Robin Scheduling Gantt Chart Calculation",
            "scenario": "Processes P1 (BT=5), P2 (BT=3), P3 (BT=1) all arrive at AT=0 with Time Quantum $q=2$.",
            "code": (
                "Processes: P1(5), P2(3), P3(1) | Quantum q = 2\n\n"
                "Gantt Chart:\n"
                "|  P1  |  P2  |  P3  |  P1  |  P2  |  P1  |\n"
                "0      2      4      5      7      8      9\n\n"
                "Completion Times (CT):\n"
                "P3 completes at 5\n"
                "P2 completes at 8\n"
                "P1 completes at 9\n\n"
                "Turnaround Time (TAT = CT - AT):\n"
                "P1 = 9 - 0 = 9 | P2 = 8 - 0 = 8 | P3 = 5 - 0 = 5\n"
                "Avg TAT = (9 + 8 + 5) / 3 = 22 / 3 = 7.33\n\n"
                "Waiting Time (WT = TAT - BT):\n"
                "P1 = 9 - 5 = 4 | P2 = 8 - 3 = 5 | P3 = 5 - 1 = 4\n"
                "Avg WT = (4 + 5 + 4) / 3 = 13 / 3 = 4.33"
            )
        },
        "comparison": {
            "title": "Preemptive vs Non-Preemptive Scheduling",
            "headers": ["Parameter", "Preemptive Scheduling", "Non-Preemptive Scheduling"],
            "rows": [
                ["CPU Release", "OS can forcibly interrupt running process and reclaim CPU", "Process voluntarily relinquishes CPU (termination or I/O wait)"],
                ["Overhead", "High — frequent context switching and state saving", "Low — context switch occurs only at natural process boundaries"],
                ["Starvation", "Possible for lower priority processes (mitigated via Aging)", "Possible (Convoy effect if long process monopolizes CPU)"],
                ["Responsiveness", "High — essential for interactive and real-time systems", "Poor — interactive tasks can freeze waiting behind batch jobs"],
                ["Examples", "Round Robin, SRTF, Preemptive Priority", "FCFS, Non-preemptive SJF"]
            ]
        },
        "formulas": [
            {"name": "Turnaround Time (TAT)", "formula": "TAT = Completion Time (CT) - Arrival Time (AT)", "explanation": "Total elapsed time from process submission to complete termination."},
            {"name": "Waiting Time (WT)", "formula": "WT = Turnaround Time (TAT) - Burst Time (BT)", "explanation": "Total time spent sitting in the Ready Queue awaiting CPU allocation."}
        ],
        "exam_tip": "Always write down the two core formulas first: $TAT = CT - AT$ and $WT = TAT - BT$. Check your arithmetic: for non-preemptive FCFS with all $AT=0$, the first process always has $WT = 0$.",
        "common_confusion": {
            "wrong": "In Round Robin, setting the time quantum as small as possible (e.g. 1 microsecond) maximizes system throughput.",
            "correct": "If the quantum is too small, context switch overhead dominates CPU execution time, destroying overall throughput.",
            "explanation": "If quantum $q = 10\\mu s$ and context switch takes $10\\mu s$, 50% of total CPU time is wasted on switching."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the Convoy Effect in CPU scheduling?",
                "a": "The Convoy Effect occurs in FCFS scheduling when a large CPU-bound process monopolizes the processor, forcing numerous short I/O-bound processes to wait in the Ready Queue, resulting in poor CPU and device utilization and high average waiting times."
            },
            {
                "marks": "5-Mark Question",
                "q": "What is Aging in CPU scheduling, and which problem does it solve?",
                "a": "1. Problem: In Priority Scheduling and SJF, low-priority or long-burst processes can suffer from Starvation (indefinite postponement) if a continuous stream of higher-priority processes enters the Ready Queue.\n2. Solution (Aging): Aging is a dynamic technique where the operating system gradually increases the priority of processes that wait in the Ready Queue for extended durations.\n3. Result: Eventually, an aging process's priority rises high enough that it is guaranteed to acquire the CPU and execute, completely eliminating starvation."
            },
            {
                "marks": "10-Mark Question",
                "q": "Given processes P1 (AT=0, BT=8), P2 (AT=1, BT=4), P3 (AT=2, BT=9), P4 (AT=3, BT=5), draw Gantt charts and compute average Waiting Time for FCFS and Preemptive SJF (SRTF).",
                "a": "1. SRTF Execution Breakdown:\n   - T=0: P1 arrives (BT=8). Runs until T=1.\n   - T=1: P2 arrives (BT=4, P1 rem=7). P2 preempts P1! Runs until T=5.\n   - T=2: P3 arrives (BT=9). P2 still has smaller burst.\n   - T=3: P4 arrives (BT=5). P2 still smallest.\n   - T=5: P2 finishes! Ready queue: P4 (5), P1 (7), P3 (9). P4 runs until T=10.\n   - T=10: P4 finishes! P1 runs until T=17.\n   - T=17: P1 finishes! P3 runs until T=26.\n2. Completion Times (CT): P2=5, P4=10, P1=17, P3=26.\n3. Metrics Calculation:\n   - P1: TAT = 17 - 0 = 17, WT = 17 - 8 = 9\n   - P2: TAT = 5 - 1 = 4, WT = 4 - 4 = 0\n   - P3: TAT = 26 - 2 = 24, WT = 24 - 9 = 15\n   - P4: TAT = 10 - 3 = 7, WT = 7 - 5 = 2\n4. Average Waiting Time: (9 + 0 + 15 + 2) / 4 = 26 / 4 = 6.5 ms."
            }
        ],
        "revision_60s": [
            "TAT = Completion Time - Arrival Time.",
            "Waiting Time = TAT - Burst Time.",
            "FCFS: Non-preemptive, simple, suffers from Convoy Effect.",
            "SJF/SRTF: Mathematically optimal average WT, but causes starvation.",
            "Round Robin: Preemptive with quantum q; optimal for time-sharing.",
            "Aging prevents starvation in priority scheduling."
        ]
    },

    "process-synchronization": {
        "title": "Process Synchronization & Concurrency Control",
        "subject": "os",
        "exam_definition": (
            "Process Synchronization is the coordination of concurrent processes or threads accessing shared data to eliminate "
            "race conditions and enforce mutual exclusion in the Critical Section, satisfying Mutual Exclusion, Progress, and Bounded Waiting."
        ),
        "remember": "Critical Section Requirements: 1) Mutual Exclusion (only 1 inside), 2) Progress (no deadlock on entry), 3) Bounded Waiting (no starvation).",
        "core_concept": (
            "When multiple concurrent threads read and modify shared memory without synchronization, the final output depends on "
            "the arbitrary interleaving order of execution. This is a Race Condition. A Critical Section is the block of code accessing "
            "shared resources. Synchronization primitives (Mutexes, Semaphores, Monitors) enforce atomicity to ensure data consistency."
        ),
        "key_points": [
            "Race Condition: A flaw where concurrent execution outcomes depend on uncontrolled timing/interleaving.",
            "Critical Section Problem Criteria: Mutual Exclusion (mandatory), Progress (mandatory), Bounded Waiting (mandatory).",
            "Peterson's Algorithm: Software solution for two processes using `turn` and `flag[]` array satisfying all 3 criteria.",
            "Hardware Primitives: Atomic instructions TestAndSet() and CompareAndSwap() provide lock foundations.",
            "Counting Semaphore vs Binary Semaphore: Binary acts as mutex (0 or 1); Counting tracks integer count of available resource instances.",
            "Classic Problems: Producer-Consumer (Bounded Buffer), Readers-Writers (Reader Preference vs Writer Starvation), Dining Philosophers."
        ],
        "classification": {
            "title": "Synchronization Primitives",
            "items": [
                {"name": "Mutex (Mutual Exclusion Lock)", "desc": "Binary locking mechanism with ownership: only the thread that acquired the mutex can release it."},
                {"name": "Counting Semaphore", "desc": "Integer variable accessed only via atomic wait() (P) and signal() (V) operations to manage pools of resources."},
                {"name": "Binary Semaphore", "desc": "Integer semaphore restricted to values 0 and 1; lacks ownership requirement (unlike mutex)."},
                {"name": "Spinlock", "desc": "Lock where waiting threads loop continuously (busy-waiting) testing the lock; efficient only for extremely short critical sections."},
                {"name": "Monitors", "desc": "High-level language synchronization construct encapsulating shared variables and procedures with implicit mutual exclusion."}
            ]
        },
        "how_it_works": {
            "title": "Semaphore Operations (wait / signal)",
            "steps": [
                "1. wait(S) [also known as P()]: Decrements semaphore value S.",
                "2. If S < 0, the calling process is suspended and added to semaphore's waiting queue.",
                "3. Process enters critical section and modifies shared resource safely.",
                "4. signal(S) [also known as V()]: Increments semaphore value S.",
                "5. If S <= 0, an asleep process from the waiting queue is woken up and moved to the Ready queue."
            ],
            "diagram": "Process → wait(S) [S > 0 ? Decrement : Sleep] → Critical Section → signal(S) [Increment & Wake Next Process]"
        },
        "example": {
            "title": "Producer-Consumer Solution Using Semaphores in C",
            "scenario": "A bounded buffer of size N synchronized with mutex, empty (init N), and full (init 0) semaphores.",
            "code": (
                "#include <semaphore.h>\n"
                "#include <pthread.h>\n\n"
                "#define N 5\n"
                "int buffer[N];\n"
                "int in = 0, out = 0;\n\n"
                "sem_t mutex; // Binary semaphore for buffer access\n"
                "sem_t empty; // Counting semaphore: empty slots (init N)\n"
                "sem_t full;  // Counting semaphore: full slots (init 0)\n\n"
                "void* producer(void* arg) {\n"
                "    int item = 42;\n"
                "    sem_wait(&empty); // Decrement empty slots (blocks if buffer full)\n"
                "    sem_wait(&mutex); // Lock buffer\n"
                "    buffer[in] = item;\n"
                "    in = (in + 1) % N;\n"
                "    sem_post(&mutex); // Unlock buffer\n"
                "    sem_post(&full);  // Increment filled slots\n"
                "    return NULL;\n"
                "}\n\n"
                "void* consumer(void* arg) {\n"
                "    sem_wait(&full);  // Decrement filled slots (blocks if buffer empty)\n"
                "    sem_wait(&mutex); // Lock buffer\n"
                "    int item = buffer[out];\n"
                "    out = (out + 1) % N;\n"
                "    sem_post(&mutex); // Unlock buffer\n"
                "    sem_post(&empty); // Increment empty slots\n"
                "    return NULL;\n"
                "}"
            )
        },
        "comparison": {
            "title": "Mutex vs Semaphore",
            "headers": ["Feature", "Mutex", "Semaphore"],
            "rows": [
                ["Nature", "Locking mechanism with ownership attribute", "Signaling mechanism using integer counter"],
                ["Ownership", "Strict ownership: only the thread that locks can unlock", "No ownership: any thread or interrupt handler can call signal()"],
                ["Values", "Binary only (0 or 1 / Locked or Unlocked)", "Integer values (0, 1 for Binary; $\\ge 0$ for Counting)"],
                ["Use Case", "Mutual exclusion for single critical section", "Resource management across multiple units or task coordination"],
                ["Deadlock Risk", "High if lock ordering is violated", "High if wait/signal order is inverted"]
            ]
        },
        "formulas": [
            {"name": "Counting Semaphore Invariant", "formula": "S_current = S_initial + #signal(S) - #wait(S)", "explanation": "If S < 0, |S| represents the exact number of processes currently blocked in the queue."}
        ],
        "exam_tip": "If an exam question asks for the three mandatory conditions to solve the Critical Section problem, write: 1) Mutual Exclusion, 2) Progress, and 3) Bounded Waiting. Never omit Bounded Waiting!",
        "common_confusion": {
            "wrong": "Busy waiting (spinlocks) should always be avoided because it is inefficient.",
            "correct": "Busy waiting is inefficient on single-core systems, but spinlocks are heavily used in multicore OS kernels when the critical section is shorter than two context switches.",
            "explanation": "Sleeping and waking a thread costs hundreds of clock cycles; a spinlock for 5 cycles is vastly faster."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What are the three mandatory requirements for a valid solution to the Critical Section problem?",
                "a": "1. Mutual Exclusion: If process Pi is executing in its critical section, no other processes can be executing in their critical sections.\n2. Progress: If no process is executing in its critical section and some wish to enter, only those not in their remainder section can participate in deciding who enters next, and selection cannot be postponed indefinitely.\n3. Bounded Waiting: There must be a limit on the number of times other processes are allowed to enter their critical sections after a process has requested entry."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Peterson's Algorithm for two processes. How does it guarantee mutual exclusion?",
                "a": "1. Data Structures: `boolean flag[2]` (flag[i] = true indicates Pi is ready to enter) and `int turn` (indicates whose turn it is to enter).\n2. Entry Section for Pi:\n   - `flag[i] = true;`\n   - `turn = j;`\n   - `while (flag[j] && turn == j); // busy wait`\n3. Mutual Exclusion Guarantee: For both processes to enter simultaneously, both `turn == 0` and `turn == 1` must hold true at the same instant, which is physically impossible on shared memory architecture. Thus, Mutual Exclusion is strictly preserved."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the Classical Readers-Writers Problem. Provide a semaphore-based solution and analyze the Writer Starvation issue.",
                "a": "1. Problem Definition: Multiple concurrent readers can read shared data simultaneously without conflict. However, if a writer accesses the data, no other reader or writer may access it.\n2. Semaphore Solution:\n   - Semaphores: `mutex` (protects read_count, init 1), `wrt` (mutual exclusion for writing, init 1).\n   - Reader Logic:\n     - wait(mutex); read_count++; if (read_count == 1) wait(wrt); signal(mutex);\n     - // Reading shared data\n     - wait(mutex); read_count--; if (read_count == 0) signal(wrt); signal(mutex);\n   - Writer Logic:\n     - wait(wrt);\n     - // Writing shared data\n     - signal(wrt);\n3. Writer Starvation: In this reader-preference solution, as long as at least one reader remains active, read_count never reaches zero, keeping wrt held. A steady stream of incoming readers will starve writers indefinitely."
            }
        ],
        "revision_60s": [
            "Race condition: output depends on arbitrary thread execution timing.",
            "Critical Section rules: Mutual Exclusion, Progress, Bounded Waiting.",
            "Peterson's algorithm: software 2-process solution using flag[] and turn.",
            "Mutex = lock with ownership; Semaphore = signaling counter without ownership.",
            "wait(S) decrements; signal(S) increments.",
            "Reader-preference causes Writer Starvation; solved using fair queues."
        ]
    },

    "deadlocks": {
        "title": "Deadlocks: Detection, Prevention & Avoidance",
        "subject": "os",
        "exam_definition": (
            "A Deadlock is a permanent state where a set of processes are blocked because each process holds at least one resource "
            "and is waiting to acquire another resource currently held by another process in the same set."
        ),
        "remember": "Coffman Conditions: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, 4) Circular Wait. All 4 must hold simultaneously.",
        "core_concept": (
            "A deadlock cannot occur if even one of the four Coffman conditions is broken. Operating systems deal with deadlocks using "
            "four fundamental strategies: Deadlock Ignorance (Ostrich Algorithm, used in Linux/Windows), Deadlock Prevention (restricting "
            "resource request methods), Deadlock Avoidance (dynamic safety checking via Banker's Algorithm), and Deadlock Detection & Recovery."
        ),
        "key_points": [
            "Coffman Conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.",
            "Resource Allocation Graph (RAG): Request edges ($P \\to R$) and Assignment edges ($R \\to P$). Cycle implies deadlock if single instance per resource type.",
            "Deadlock Prevention: Invalidate at least one Coffman condition (e.g. impose strict total ordering on resources to eliminate Circular Wait).",
            "Deadlock Avoidance: System examines dynamic state before granting resource. Safe State guarantees an execution sequence that avoids deadlock.",
            "Banker's Algorithm: Tests if granting request leaves system in a Safe State using vectors: Available, Max, Allocation, Need ($Need = Max - Allocation$).",
            "Recovery Strategies: Process Termination (abort all or abort one-by-one) or Resource Preemption (rollback to checkpoint)."
        ],
        "classification": {
            "title": "Deadlock Handling Strategies",
            "items": [
                {"name": "Deadlock Ignorance (Ostrich Algorithm)", "desc": "Ignore the problem completely under the assumption deadlocks occur rarely. Common in general-purpose OS (Linux, Windows)."},
                {"name": "Deadlock Prevention", "desc": "Design system protocols to structurally eliminate at least one of the four Coffman conditions."},
                {"name": "Deadlock Avoidance", "desc": "Dynamically evaluate resource allocation requests against current state to ensure the system remains in a Safe State (Banker's Algorithm)."},
                {"name": "Deadlock Detection & Recovery", "desc": "Periodically run wait-for graph cycle detection and recover via process termination or resource preemption."}
            ]
        },
        "how_it_works": {
            "title": "Banker's Algorithm Safety Test Flow",
            "steps": [
                "1. Initialize Work vector = Available, and Finish[i] = false for all processes $i = 0 \\dots n-1$.",
                "2. Find an index $i$ such that: Finish[i] == false AND Need[i] <= Work. If no such $i$ exists, go to Step 4.",
                "3. Work = Work + Allocation[i]; Finish[i] = true; Go back to Step 2.",
                "4. If Finish[i] == true for all $i$, the system is in a Safe State and the execution order forms a Safe Sequence. Otherwise, Unsafe (potential deadlock)."
            ],
            "diagram": "Check Request <= Need → Request <= Available → Pretend Allocate → Run Safety Algorithm → Safe ? Grant : Rollback & Wait"
        },
        "example": {
            "title": "Banker's Algorithm Numerical Matrix Calculation",
            "scenario": "3 processes (P0, P1, P2) and 3 resource types (A, B, C). Available = [3, 3, 2].",
            "code": (
                "Processes: P0, P1, P2 | Available = [3, 3, 2]\n\n"
                "Allocation Matrix:      Max Matrix:         Need Matrix (Max - Alloc):\n"
                "P0: [0, 1, 0]           P0: [7, 5, 3]       P0: [7, 4, 3]\n"
                "P1: [2, 0, 0]           P1: [3, 2, 2]       P1: [1, 2, 2]\n"
                "P2: [3, 0, 2]           P2: [9, 0, 2]       P2: [6, 0, 0]\n\n"
                "Safety Check:\n"
                "1. Work = [3, 3, 2]\n"
                "2. P1 Need [1, 2, 2] <= Work [3, 3, 2] -> TRUE!\n"
                "   P1 finishes: Work = [3,3,2] + [2,0,0] = [5, 3, 2]\n"
                "3. P2 Need [6, 0, 0] <= Work [5, 3, 2] -> FALSE\n"
                "   P0 Need [7, 4, 3] <= Work [5, 3, 2] -> FALSE\n"
                "Wait! Can any process run? If Work [5, 3, 2] cannot satisfy P0 or P2, system is UNSAFE."
            )
        },
        "comparison": {
            "title": "Deadlock Prevention vs Deadlock Avoidance",
            "headers": ["Attribute", "Deadlock Prevention", "Deadlock Avoidance"],
            "rows": [
                ["Mechanism", "Static design rules preventing at least 1 Coffman condition", "Dynamic runtime evaluation of resource safety state"],
                ["Information Required", "No prior knowledge of resource requests", "Requires processes to declare maximum resource needs in advance"],
                ["Resource Utilization", "Low — overly conservative restrictions cause poor utilization", "Higher than prevention, but restricted to safe state paths"],
                ["Overhead", "Zero runtime overhead (enforced at design time)", "High runtime overhead (computes safety matrix on every request)"],
                ["Algorithms", "Total Resource Ordering, All-or-Nothing allocation", "Banker's Algorithm, Resource Allocation Graph cycle avoidance"]
            ]
        },
        "formulas": [
            {"name": "Need Matrix Formula", "formula": "Need[i][j] = Max[i][j] - Allocation[i][j]", "explanation": "Remaining resources process Pi may request to finish execution."},
            {"name": "Deadlock Condition with N processes and R single instances", "formula": "Total Resources R >= N * (Max_Need - 1) + 1", "explanation": "Minimum resources required to guarantee deadlock-free execution."}
        ],
        "exam_tip": "In RAG diagrams: A cycle guarantees deadlock ONLY if every resource type has exactly 1 instance. If resource types have multiple instances, a cycle indicates potential deadlock, but NOT guaranteed deadlock.",
        "common_confusion": {
            "wrong": "An Unsafe State in Banker's Algorithm means the system is currently deadlocked.",
            "correct": "An Unsafe State is not a deadlock; it is a state that MAY lead to deadlock if all processes simultaneously request their maximum declared resources.",
            "explanation": "Deadlock is a subset of Unsafe states: Safe States -> Unsafe States -> Deadlocked States."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "State the four Coffman conditions necessary for a deadlock to occur.",
                "a": "1. Mutual Exclusion: At least one resource must be held in a non-shareable mode.\n2. Hold and Wait: A process must hold at least one resource and be waiting to acquire another.\n3. No Preemption: Resources cannot be forcibly preempted; they must be released voluntarily.\n4. Circular Wait: A closed chain of processes exists such that each process holds a resource needed by the next."
            },
            {
                "marks": "5-Mark Question",
                "q": "How can the Circular Wait condition be prevented in an operating system?",
                "a": "1. Mechanism: Impose a strict global total ordering function $F: R \\to \\mathbb{N}$ on all resource types.\n2. Protocol: Require that each process can only request resources in strictly increasing numerical order of enumeration.\n3. Proof: If a process holds resource $R_i$, it can only request $R_j$ if $F(R_j) > F(R_i)$. This mathematical ordering prevents a closed cycle from ever forming in the Resource Allocation Graph, completely eliminating Circular Wait."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the Banker's Algorithm for Deadlock Avoidance. Given 5 processes (P0-P4) and 3 resources (A=10, B=5, C=7), demonstrate how the safety algorithm computes a safe sequence.",
                "a": "1. Purpose: Banker's Algorithm prevents deadlocks by testing whether granting a resource request will leave the system in a 'Safe State' (where there exists an order in which all processes can finish).\n2. Matrices: Available ($1 \\times m$), Max ($n \\times m$), Allocation ($n \\times m$), Need ($Need = Max - Alloc$).\n3. Safety Algorithm Steps:\n   - Let Work = Available, Finish[i] = false for all $i$.\n   - Find $i$ where Finish[i] == false and Need[i] <= Work. If none, evaluate.\n   - Work = Work + Allocation[i]; Finish[i] = true; repeat.\n   - If all Finish[i] == true, system is in Safe State; sequence of executed $i$ is the Safe Sequence.\n4. Resource-Request Algorithm: Verifies Request <= Need and Request <= Available, pretends allocation, tests safety, and rolls back if unsafe."
            }
        ],
        "revision_60s": [
            "Deadlock = set of processes permanently blocked waiting for each other's held resources.",
            "4 Coffman conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.",
            "Break ANY 1 condition to prevent deadlock entirely.",
            "Safe State != Deadlock (Unsafe means potential deadlock).",
            "Banker's Algorithm: Need = Max - Allocation; grants request only if safe sequence exists."
        ]
    },

    "memory-management": {
        "title": "Main Memory Management & Paging",
        "subject": "os",
        "exam_definition": (
            "Memory Management is the operating system mechanism that tracks physical RAM allocation, maps logical process addresses "
            "to physical memory frames, and mitigates internal and external fragmentation via contiguous and non-contiguous schemes (Paging & Segmentation)."
        ),
        "remember": "Logical Address = Page Number (p) + Page Offset (d) | Physical Address = Frame Number (f) + Page Offset (d). Offset d never changes!",
        "core_concept": (
            "Early systems used contiguous memory allocation, which led to severe External Fragmentation (free memory exists but is broken "
            "into unusable small non-contiguous blocks). Modern operating systems eliminate external fragmentation by implementing Paging: "
            "dividing physical memory into fixed-size Frames and logical memory into identical-size Pages, mapped dynamically via Page Tables."
        ),
        "key_points": [
            "Internal Fragmentation: Allocated memory block is larger than requested data (unusable slack space inside allocated block).",
            "External Fragmentation: Total free memory is sufficient to satisfy a request, but it is split into non-contiguous fragments.",
            "Paging Architecture: Hardware Memory Management Unit (MMU) translates logical address $(p, d)$ to physical address $(f, d)$ using Page Table.",
            "Translation Lookaside Buffer (TLB): High-speed associative cache on CPU chip that caches recent page-to-frame translations to eliminate memory lookup latency.",
            "Effective Memory Access Time (EMAT): $EMAT = h \\cdot (t + m) + (1 - h) \\cdot (t + 2m)$, where $h$ is TLB hit ratio, $t$ is TLB lookup, $m$ is RAM access time.",
            "Hierarchical Paging: Multi-level page tables (e.g. 2-level, 4-level on x86-64) reduce page table memory overhead."
        ],
        "classification": {
            "title": "Memory Allocation Schemes",
            "items": [
                {"name": "Fixed Partitioning", "desc": "RAM divided into static fixed-size slots at boot. Suffers from severe internal fragmentation."},
                {"name": "Dynamic Partitioning", "desc": "Partitions allocated dynamically to fit process size. Eliminates internal fragmentation but creates external fragmentation (requires compaction)."},
                {"name": "Paging (Non-contiguous)", "desc": "Fixed-size logical pages mapped to fixed-size physical frames. Eliminates external fragmentation."},
                {"name": "Segmentation", "desc": "Logical memory divided into variable-size semantic segments (Code, Stack, Heap, Data). Can suffer from external fragmentation."}
            ]
        },
        "how_it_works": {
            "title": "Hardware Address Translation via MMU and TLB",
            "steps": [
                "1. CPU generates logical address consisting of Page Number $p$ and Offset $d$.",
                "2. MMU checks high-speed hardware associative TLB cache for page number $p$.",
                "3. TLB Hit: Frame number $f$ is retrieved in ~1 ns; physical address $(f \\times \\text{PageSize}) + d$ is sent to memory.",
                "4. TLB Miss: MMU queries Page Table in RAM (costs memory access penalty $m$), loads $f$, and updates TLB.",
                "5. Physical RAM executes read/write at calculated physical address."
            ],
            "diagram": "CPU [p | d] ──> TLB Check ──┬──[HIT]──> Frame f + Offset d ──> Physical RAM\n                             └──[MISS]─> Page Table in RAM ──> Update TLB ──> Frame f + Offset d"
        },
        "example": {
            "title": "Logical to Physical Address Translation Calculation",
            "scenario": "Page size is 4 KB ($2^{12}$ bytes). Logical address generated is 13320.",
            "code": (
                "Given: Page Size = 4 KB = 4096 bytes = 2^12 (Offset uses 12 bits)\n"
                "Logical Address = 13320\n\n"
                "1. Calculate Page Number (p):\n"
                "   p = 13320 / 4096 = 3  (integer division)\n\n"
                "2. Calculate Page Offset (d):\n"
                "   d = 13320 % 4096 = 1032\n\n"
                "3. Lookup Page Table for Page 3:\n"
                "   Suppose PageTable[3] = Frame 7\n\n"
                "4. Calculate Physical Address:\n"
                "   Physical Address = (Frame Number * Page Size) + Offset\n"
                "   Physical Address = (7 * 4096) + 1032 = 28672 + 1032 = 29704"
            )
        },
        "comparison": {
            "title": "Paging vs Segmentation",
            "headers": ["Feature", "Paging", "Segmentation"],
            "rows": [
                ["Block Size", "Fixed size (e.g. 4 KB, determined by hardware architecture)", "Variable size (determined by user/compiler based on logical units)"],
                ["Fragmentation", "Suffers from Internal Fragmentation; Zero External Fragmentation", "Suffers from External Fragmentation; Zero Internal Fragmentation"],
                ["Visibility", "Invisible to programmer; handled entirely by hardware/OS", "Visible to programmer/compiler (reflects code, stack, heap segments)"],
                ["Address Structure", "Single linear address divided into [Page # | Offset]", "Two components: [Segment # | Segment Limit + Base]"],
                ["Memory Table", "Page Table maps Page $\\to$ Frame", "Segment Table maps Segment $\\to$ Base Address and Limit"]
            ]
        },
        "formulas": [
            {"name": "Effective Memory Access Time (EMAT)", "formula": "EMAT = h * (t_TLB + t_RAM) + (1 - h) * (t_TLB + 2 * t_RAM)", "explanation": "Where h is TLB hit ratio, t_TLB is TLB access time, t_RAM is main memory access time."},
            {"name": "Address Partitioning Invariant", "formula": "Logical Address = p * PageSize + d", "explanation": "d = Logical Address % PageSize, p = Logical Address // PageSize."}
        ],
        "exam_tip": "In numerical problems: Page Offset $d$ NEVER changes during address translation! $d$ is directly copied from the logical address to the physical address. Only Page Number $p$ is replaced by Frame Number $f$.",
        "common_confusion": {
            "wrong": "Paging has zero fragmentation.",
            "correct": "Paging has zero EXTERNAL fragmentation, but it still suffers from INTERNAL fragmentation on the final page of each process.",
            "explanation": "If process requires 5 KB and page size is 4 KB, it gets 2 pages (8 KB). The last 3 KB is wasted internal fragmentation."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the difference between Internal and External Fragmentation?",
                "a": "Internal fragmentation occurs when memory is allocated in fixed-size blocks and a process does not use the entire block, leaving wasted space inside the partition. External fragmentation occurs in variable partitioning when free memory is broken into many small, non-contiguous blocks that cannot satisfy a request even though total free memory is sufficient."
            },
            {
                "marks": "5-Mark Question",
                "q": "What is a Translation Lookaside Buffer (TLB), and how does it improve Effective Memory Access Time?",
                "a": "1. Definition: A TLB is a high-speed associative hardware cache located directly on the CPU Memory Management Unit (MMU) that stores recent Page-to-Frame translations.\n2. Problem it solves: Without TLB, every memory read/write requires two physical RAM accesses (one to read the Page Table entry, and one to read the actual data), cutting memory performance in half.\n3. Improvement: With TLB hit ratio $h \\approx 98\\%$, the MMU translates addresses in ~1 ns, reducing Effective Memory Access Time formula: $EMAT = h(t + m) + (1-h)(t + 2m)$ to nearly that of a single memory access."
            },
            {
                "marks": "10-Mark Question",
                "q": "A system has a TLB hit ratio of 90%. Access time to TLB is 20 ns and to main memory is 100 ns. Calculate the Effective Memory Access Time (EMAT). Explain how multi-level paging impacts this.",
                "a": "1. Given:\n   - TLB hit ratio $h = 0.90$\n   - TLB access time $t = 20$ ns\n   - Memory access time $m = 100$ ns\n2. Calculation:\n   - EMAT = $h \\cdot (t + m) + (1 - h) \\cdot (t + 2m)$\n   - Hit Time = $20 + 100 = 120$ ns\n   - Miss Time = $20 + 100 + 100 = 220$ ns\n   - EMAT = $0.90 \\cdot (120) + 0.10 \\cdot (220) = 108 + 22 = 130$ ns.\n3. Impact of Multi-level Paging: In a $k$-level page table, a TLB miss requires $k$ memory accesses for the page tables plus 1 for the data: Miss Time = $t + (k + 1)m$. For a 4-level table on x86-64, a TLB miss costs $20 + 500 = 520$ ns, making high TLB hit rates absolutely critical."
            }
        ],
        "revision_60s": [
            "Paging eliminates External Fragmentation; still has minor Internal Fragmentation.",
            "Page = logical block; Frame = physical block (both exact same size).",
            "Offset d never changes during address translation.",
            "TLB is associative MMU cache storing page-to-frame mappings.",
            "EMAT = h*(t + m) + (1 - h)*(t + 2m)."
        ]
    },

    "virtual-memory": {
        "title": "Virtual Memory & Page Replacement",
        "subject": "os",
        "exam_definition": (
            "Virtual Memory is a storage allocation technique that provides an idealized, uniform abstraction of large continuous memory "
            "to processes, allowing execution of processes whose address spaces exceed physical RAM through Demand Paging and Page Replacement."
        ),
        "remember": "Bélády's Anomaly: Increasing physical page frames can paradoxically increase page faults in FIFO (never happens in LRU or Optimal).",
        "core_concept": (
            "Most programs execute only a fraction of their code at any given time (error handlers, uncommon branches). Demand Paging loads pages "
            "into RAM only when accessed. When a process references an unmapped page, hardware triggers a Page Fault. If physical RAM is full, "
            "a Page Replacement Algorithm (FIFO, Optimal, LRU) selects a victim page to swap out to disk."
        ),
        "key_points": [
            "Demand Paging: Pages are loaded into RAM lazily on first access ('swap in'), minimizing memory footprint and startup time.",
            "Page Fault: Hardware interrupt generated when a process accesses a page marked invalid (not resident in physical RAM).",
            "Page Replacement Algorithms: FIFO (First-In-First-Out), Optimal (replaces page not used for longest future duration — impossible to implement, used as benchmark), LRU (Least Recently Used).",
            "Bélády's Anomaly: FIFO replacement algorithm anomaly where allocating more page frames leads to more page faults for certain reference strings.",
            "Thrashing: Severe system state where CPU spends virtually 100% of time swapping pages in/out of disk rather than executing user instructions.",
            "Working Set Model: Allocates each process enough frames to hold its active working set $W(t, \\Delta)$ based on principle of locality."
        ],
        "classification": {
            "title": "Page Replacement Algorithms",
            "items": [
                {"name": "FIFO (First-In, First-Out)", "desc": "Replaces the oldest loaded page. Simple queue implementation, but suffers from Bélády's Anomaly."},
                {"name": "Optimal Page Replacement (OPT)", "desc": "Replaces page that will not be used for longest time in future. Guaranteed minimum page faults; impossible in practice without future knowledge."},
                {"name": "LRU (Least Recently Used)", "desc": "Replaces page that has not been accessed for longest time in past. Approximates OPT using stack or counter; immune to Bélády's Anomaly."},
                {"name": "Clock / Second-Chance Algorithm", "desc": "Practical LRU approximation using circular queue and 1-bit reference flag per frame."}
            ]
        },
        "how_it_works": {
            "title": "Page Fault Handling Sequence",
            "steps": [
                "1. CPU attempts to access logical address; MMU detects valid/invalid bit is '0' (Invalid/Not in RAM).",
                "2. Hardware generates Page Fault Trap to the operating system kernel.",
                "3. OS saves process registers and state, checking internal tables to confirm valid reference vs segmentation fault.",
                "4. OS locates the required page in swap backing store on disk.",
                "5. OS finds a free physical frame (or executes Page Replacement algorithm to evict a victim frame, writing to disk if dirty).",
                "6. OS issues disk I/O to read required page into allocated frame, updates Page Table valid bit to '1', and restarts the faulting CPU instruction."
            ],
            "diagram": "Memory Reference → Invalid Bit (0) → TRAP (Page Fault) → Locate on Disk → Find Free Frame (Evict if Full) → Read Page from Disk → Update Table (1) → Restart Instruction"
        },
        "example": {
            "title": "LRU vs FIFO Page Replacement Trace",
            "scenario": "Reference String: 7, 0, 1, 2, 0, 3 with 3 available frames.",
            "code": (
                "Reference String: 7, 0, 1, 2, 0, 3 | Frames: 3\n\n"
                "FIFO Algorithm Trace:\n"
                "Ref 7: [7]       - Fault 1\n"
                "Ref 0: [7, 0]    - Fault 2\n"
                "Ref 1: [7, 0, 1] - Fault 3\n"
                "Ref 2: [2, 0, 1] - Fault 4 (Evicts oldest: 7)\n"
                "Ref 0: [2, 0, 1] - HIT (0 already present)\n"
                "Ref 3: [2, 3, 1] - Fault 5 (Evicts oldest: 0)\n"
                "Total FIFO Faults = 5\n\n"
                "LRU Algorithm Trace:\n"
                "Ref 7: [7]       - Fault 1\n"
                "Ref 0: [7, 0]    - Fault 2\n"
                "Ref 1: [7, 0, 1] - Fault 3\n"
                "Ref 2: [2, 0, 1] - Fault 4 (7 used least recently)\n"
                "Ref 0: [2, 0, 1] - HIT (0 accessed, moves to most recent)\n"
                "Ref 3: [2, 0, 3] - Fault 5 (1 used least recently, evicts 1!)\n"
                "Total LRU Faults = 5"
            )
        },
        "comparison": {
            "title": "FIFO vs LRU vs Optimal Page Replacement",
            "headers": ["Parameter", "FIFO", "LRU", "Optimal (OPT)"],
            "rows": [
                ["Selection Policy", "Replaces oldest resident page", "Replaces page unreferenced for longest past period", "Replaces page unreferenced for longest future period"],
                ["Hardware Support", "Minimal (simple FIFO pointer or queue)", "High (hardware timestamps, stack, or reference bits)", "Impossible (requires clairvoyance of future program execution)"],
                ["Bélády's Anomaly", "Vulnerable (anomaly can occur)", "Immune (satisfies stack algorithm property)", "Immune (satisfies stack algorithm property)"],
                ["Page Fault Rate", "Sub-optimal / Poor", "Near-optimal in practical workloads", "Mathematically minimal possible page fault rate"]
            ]
        },
        "formulas": [
            {"name": "Effective Access Time with Demand Paging", "formula": "EAT = (1 - p) * m + p * t_fault", "explanation": "Where p is page fault probability, m is RAM access time (~100 ns), t_fault is page fault service time (~10 ms)."}
        ],
        "exam_tip": "If asked to demonstrate Bélády's Anomaly in an exam, use the classic reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5. With 3 frames it generates 9 page faults; with 4 frames it generates 10 page faults!",
        "common_confusion": {
            "wrong": "Thrashing is caused by low CPU capacity.",
            "correct": "Thrashing is caused by insufficient physical RAM allocated to processes relative to their combined working set sizes.",
            "explanation": "Adding a faster CPU makes thrashing worse because the CPU sits idle waiting on slow disk swap I/O."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is Thrashing and what causes it in an operating system?",
                "a": "Thrashing is a state of severe performance degradation where the system spends significantly more time swapping pages between RAM and disk than executing instructions. It is caused by overcommitting memory: when the sum of the working sets of all running processes exceeds physical RAM capacity."
            },
            {
                "marks": "5-Mark Question",
                "q": "What is Bélády's Anomaly? Which page replacement algorithms are susceptible or immune to it?",
                "a": "1. Definition: Bélády's Anomaly is the counter-intuitive phenomenon where allocating more physical page frames to a process results in an increased number of page faults for a given reference string.\n2. Susceptible: FIFO algorithm is vulnerable because it evicts pages strictly based on residency age rather than access recency.\n3. Immune: Stack Algorithms (such as LRU and Optimal) are mathematically immune because the set of pages in an $N$-frame system is always a strict subset of the pages in an $(N+1)$-frame system."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain Demand Paging and detail the 6 steps performed by the OS upon a Page Fault. If memory access time is 200 ns and page fault service time is 8 ms, calculate maximum acceptable page fault rate for 10% performance degradation.",
                "a": "1. Demand Paging: Bringing execution pages into physical memory only when referenced during execution.\n2. 6 Steps: 1) Hardware trap on invalid bit; 2) OS verifies valid logical address; 3) Find free frame in RAM; 4) Schedule disk I/O to swap page in; 5) Update page table valid bit to 1; 6) Restart original CPU instruction.\n3. Numerical Calculation:\n   - $EAT = (1 - p) \\cdot m + p \\cdot t_{\\text{fault}}$\n   - $m = 200\\text{ ns} = 0.2\\ \\mu\\text{s}$, $t_{\\text{fault}} = 8\\text{ ms} = 8,000,000\\text{ ns}$\n   - Target EAT = $200 + 10\\% = 220$ ns\n   - $220 = (1 - p)(200) + p(8,000,000) = 200 - 200p + 8,000,000p$\n   - $20 = p(7,999,800) \\implies p = 20 / 7,999,800 \\approx 2.5 \\times 10^{-6}$ (less than 1 fault per 400,000 accesses!)."
            }
        ],
        "revision_60s": [
            "Demand Paging: Load pages into RAM only when demanded.",
            "Page Fault occurs when referenced page has valid bit 0 (not in RAM).",
            "Optimal replacement: lowest fault rate, requires future knowledge.",
            "LRU: replaces page unreferenced longest in past (stack algorithm).",
            "FIFO suffers from Bélády's Anomaly (more frames -> more faults).",
            "Thrashing occurs when sum of working sets exceeds physical RAM."
        ]
    },

    "file-systems": {
        "title": "File Systems & Disk Allocation",
        "subject": "os",
        "exam_definition": (
            "A File System is an operating system mechanism that structures, names, stores, retrieves, and protects persistent data "
            "on non-volatile storage, organized via directory structures and implemented through disk block allocation methods (Contiguous, Linked, Indexed/Inode)."
        ),
        "remember": "UNIX Inode Structure: Direct Pointers (direct blocks) + Single Indirect + Double Indirect + Triple Indirect Pointers.",
        "core_concept": (
            "Disks are organized into linear arrays of 512-byte or 4 KB physical blocks. The file system abstracts these raw blocks into "
            "human-readable files and hierarchical directory trees. The file allocation strategy determines read/write performance, "
            "random access capabilities, and external disk fragmentation."
        ),
        "key_points": [
            "Contiguous Allocation: Files occupy consecutive disk blocks. Fastest sequential and direct access, but suffers from external fragmentation and unknown file growth.",
            "Linked Allocation: Each block contains a pointer to the next block. Zero external fragmentation, but slow random access and pointer reliability risk.",
            "File Allocation Table (FAT): Linked allocation where pointers are stored centrally in a cached table in RAM.",
            "Indexed Allocation: Each file has an Index Block containing pointers to all its data blocks. Supports fast direct access without external fragmentation.",
            "UNIX Inode: Hybrid multi-level index structure containing metadata and direct, single indirect, double indirect, and triple indirect pointers.",
            "Directory Implementations: Linear List (simple, slow $O(N)$ search) vs Hash Table (fast $O(1)$ search, collision handling needed)."
        ],
        "classification": {
            "title": "Disk Block Allocation Methods",
            "items": [
                {"name": "Contiguous Allocation", "desc": "File blocks allocated in consecutive sequence. Optimal for sequential access, but causes severe external fragmentation."},
                {"name": "Linked Allocation", "desc": "Blocks linked via disk pointers. Eliminates fragmentation, but random access requires traversal from block 0."},
                {"name": "FAT (File Allocation Table)", "desc": "Pointers stored in central memory table. Improves linked allocation random access speed."},
                {"name": "Indexed Allocation / Inode", "desc": "Index block stores array of disk block addresses. Allows direct $O(1)$ access to any block."}
            ]
        },
        "how_it_works": {
            "title": "UNIX Inode Multi-Level Block Resolution",
            "steps": [
                "1. User requests file offset $K$. File system looks up file's Inode using directory path traversal.",
                "2. Direct Pointers (typically 12 pointers): Directly address blocks 0 through 11 (covers small files instantly).",
                "3. Single Indirect Pointer: Points to an index block containing pointers to data blocks (e.g. 1024 blocks of 4 KB = 4 MB).",
                "4. Double Indirect Pointer: Points to an index block of index blocks ($1024 \\times 1024 \\times 4\\text{ KB} = 4\\text{ GB}$).",
                "5. Triple Indirect Pointer: Points to 3 levels of indexing ($1024^3 \\times 4\\text{ KB} = 4\\text{ TB}$ file support)."
            ],
            "diagram": "Inode ──┬── Direct Pointers (12) ──> Data Blocks\n          ├── Single Indirect ──> Index Block ──> Data Blocks\n          ├── Double Indirect ──> Index Block ──> Index Block ──> Data Blocks\n          └── Triple Indirect ──> 3-tier Index Tree ──> Data Blocks"
        },
        "example": {
            "title": "UNIX Inode Maximum File Size Calculation",
            "scenario": "Block size = 4 KB ($2^{12}$ bytes), disk address = 4 bytes ($2^2$ bytes). Inode has 12 direct, 1 single indirect, 1 double indirect, 1 triple indirect pointer.",
            "code": (
                "Given:\n"
                "Block size = 4 KB = 4096 bytes\n"
                "Disk address pointer = 4 bytes\n"
                "Pointers per index block = 4096 / 4 = 1024 = 2^10\n\n"
                "1. Direct Blocks:\n"
                "   12 pointers * 4 KB = 48 KB\n\n"
                "2. Single Indirect:\n"
                "   1024 pointers * 4 KB = 4,096 KB = 4 MB\n\n"
                "3. Double Indirect:\n"
                "   1024 * 1024 pointers * 4 KB = 1,048,576 * 4 KB = 4 GB\n\n"
                "4. Triple Indirect:\n"
                "   1024 * 1024 * 1024 * 4 KB = 1,073,741,824 * 4 KB = 4 TB\n\n"
                "Max File Size = 48 KB + 4 MB + 4 GB + 4 TB ≈ 4.004 TB"
            )
        },
        "comparison": {
            "title": "Contiguous vs Linked vs Indexed Allocation",
            "headers": ["Feature", "Contiguous Allocation", "Linked Allocation", "Indexed Allocation (Inode)"],
            "rows": [
                ["Sequential Access", "Extremely fast", "Good", "Good"],
                ["Random / Direct Access", "Instant $O(1)$", "Very Slow $O(N)$ (must traverse pointers)", "Fast $O(1)$ via index table"],
                ["External Fragmentation", "Severe (requires periodic compaction)", "Zero external fragmentation", "Zero external fragmentation"],
                ["File Size Growth", "Difficult (must know max size in advance)", "Dynamic and seamless", "Dynamic and seamless"],
                ["Pointer Overhead", "Zero pointer overhead", "4-8 bytes per data block lost to pointer", "Dedicated index blocks required"]
            ]
        },
        "formulas": [
            {"name": "Pointers per Index Block", "formula": "N_ptrs = Block_Size / Pointer_Size", "explanation": "Determines fan-out capacity of indirect blocks."},
            {"name": "Max Double Indirect Capacity", "formula": "Capacity = (Block_Size / Pointer_Size)^2 * Block_Size", "explanation": "Maximum byte capacity accessible via double indirect node."}
        ],
        "exam_tip": "In Inode numerical questions, always calculate the number of pointers per block first: $N = \\text{Block Size} / \\text{Pointer Size}$. Then systematically calculate Direct, Single, Double, and Triple capacities before summing.",
        "common_confusion": {
            "wrong": "Deleting a file on Linux immediately erases its data blocks on disk.",
            "correct": "Deleting a file (unlink) simply decrements the Inode hard-link reference counter. Data blocks are freed only when the link count reaches zero AND no open file handles exist.",
            "explanation": "If a running process has the file open, data remains accessible until process terminates."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is an Inode in UNIX-like file systems?",
                "a": "An Inode (index node) is a filesystem data structure on disk that stores all metadata about a file (file type, permissions, owner, size, access/modification timestamps, and link count) along with pointers to the physical data blocks storing the file's actual contents."
            },
            {
                "marks": "5-Mark Question",
                "q": "Compare Hard Links and Soft (Symbolic) Links in Linux file systems.",
                "a": "1. Hard Link: An additional directory entry pointing directly to the existing file's Inode number. Both entries share identical permissions and data. If the original filename is deleted, data remains accessible through the hard link. Cannot link across different filesystems or directories.\n2. Soft Link (Symlink): A distinct independent file whose data block contains the pathname string to the target file. Possesses its own unique Inode. If the target file is deleted, the symlink becomes 'dangling' (broken). Can link across different filesystems and directories."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain Contiguous, Linked, and Indexed allocation methods with diagrams, comparing advantages, disadvantages, and suitability for sequential vs direct access.",
                "a": "1. Contiguous Allocation: Files allocated in consecutive blocks. Pros: Simple directory entry (start block + length), maximum I/O transfer speed. Cons: External fragmentation, pre-allocation sizing difficulty. Best for read-only CD-ROMs and sequential media.\n2. Linked Allocation: Files stored in scattered blocks linked via pointers. Pros: No external fragmentation, dynamic growth. Cons: No direct access (seeking byte $N$ requires traversing $N$ disk blocks), losing one pointer corrupts entire file. FAT solves this by caching pointers in memory.\n3. Indexed Allocation: Central index block holds pointers to all distributed data blocks. Pros: Supports both rapid sequential and random direct access without external fragmentation. Cons: Index block overhead for tiny files; solved by UNIX multi-level hybrid Inode architecture."
            }
        ],
        "revision_60s": [
            "Contiguous allocation: fast direct access, severe external fragmentation.",
            "Linked allocation: zero fragmentation, terrible random access.",
            "Indexed allocation: index block stores direct block pointers.",
            "UNIX Inode: 12 direct + single + double + triple indirect pointers.",
            "Hard link points to same Inode; Soft link points to pathname string."
        ]
    },

    "io-systems": {
        "title": "I/O Hardware & Disk Scheduling",
        "subject": "os",
        "exam_definition": (
            "I/O Management is the operating system layer that bridges physical peripheral devices and the kernel via Device Drivers, "
            "Direct Memory Access (DMA), interrupt-driven I/O, and Disk Scheduling algorithms (FCFS, SSTF, SCAN, C-SCAN, LOOK)."
        ),
        "remember": "Disk Seek Time = Time to move disk arm to target cylinder (dominant mechanical latency). Rotational Latency = Time for sector to spin under head.",
        "core_concept": (
            "CPUs operate at nanosecond speeds, while magnetic and mechanical hard drives operate at millisecond speeds ($10^6$ times slower). "
            "To bridge this immense gap, operating systems use DMA controllers to transfer bulk data directly between I/O devices and RAM "
            "without CPU intervention. Disk scheduling algorithms reorder I/O read/write requests to minimize mechanical arm head movement."
        ),
        "key_points": [
            "Polling vs Interrupts: Polling consumes 100% CPU in busy-wait loops; Interrupt-driven I/O frees CPU until device signals completion.",
            "Direct Memory Access (DMA): Dedicated hardware controller transfers data blocks between device buffer and RAM with only one interrupt per block/burst.",
            "Disk Access Latency: Seek Time (largest mechanical delay) + Rotational Latency + Transfer Time.",
            "FCFS: Services disk track requests in arrival order; high total head movement.",
            "SSTF (Shortest Seek Time First): Selects request closest to current head position; minimizes seek time but causes starvation for distant tracks.",
            "SCAN (Elevator Algorithm): Arm moves in one direction servicing all requests until end of disk, then reverses.",
            "C-SCAN (Circular SCAN): Moves in one direction servicing requests; upon reaching end, immediately returns to start without servicing requests on return trip."
        ],
        "classification": {
            "title": "Disk Scheduling Algorithms",
            "items": [
                {"name": "FCFS Disk Scheduling", "desc": "Processes disk track requests strictly in order of arrival. Fair but mechanically inefficient."},
                {"name": "SSTF (Shortest Seek Time First)", "desc": "Selects track with minimum seek distance from current head. Prone to starvation."},
                {"name": "SCAN (Elevator)", "desc": "Arm sweeps across disk servicing requests until reaching physical boundary, then reverses direction."},
                {"name": "C-SCAN (Circular SCAN)", "desc": "Provides more uniform wait time by sweeping in one direction only; jumps back to track 0 without servicing."},
                {"name": "LOOK / C-LOOK", "desc": "Optimized SCAN/C-SCAN variant that reverses or jumps upon servicing the last request in that direction, without traveling to disk boundary."}
            ]
        },
        "how_it_works": {
            "title": "Direct Memory Access (DMA) Transfer Process",
            "steps": [
                "1. Device driver configures DMA controller registers with: memory address pointer, byte count, and transfer direction (Read/Write).",
                "2. DMA controller requests bus mastership from CPU (via Bus Request / Bus Grant).",
                "3. DMA transfers data words directly between device buffer and RAM across system bus, bypassing CPU registers.",
                "4. DMA controller decrements byte counter and increments memory pointer after each word.",
                "5. When byte counter reaches zero, DMA controller raises a hardware interrupt to signal transfer completion to the CPU."
            ],
            "diagram": "CPU configures DMA Controller → DMA acquires Bus Mastership → Data transfers Device <──> RAM directly → DMA sends Interrupt to CPU"
        },
        "example": {
            "title": "SSTF vs SCAN Disk Scheduling Head Movement Calculation",
            "scenario": "Track requests: 98, 183, 37, 122, 14, 124, 65, 67. Initial head at track 53.",
            "code": (
                "Queue: 98, 183, 37, 122, 14, 124, 65, 67 | Head = 53\n\n"
                "SSTF Calculation (Closest track next):\n"
                "53 -> 65 (dist 12)\n"
                "65 -> 67 (dist 2)\n"
                "67 -> 37 (dist 30)\n"
                "37 -> 14 (dist 23)\n"
                "14 -> 98 (dist 84)\n"
                "98 -> 122 (dist 24)\n"
                "122 -> 124 (dist 2)\n"
                "124 -> 183 (dist 59)\n"
                "Total Head Movement = 12 + 2 + 30 + 23 + 84 + 24 + 2 + 59 = 236 cylinders\n\n"
                "SCAN Calculation (Moving toward 199 end first):\n"
                "53 -> 65 -> 67 -> 98 -> 122 -> 124 -> 183 -> 199 (end)\n"
                "Reverses: 199 -> 37 -> 14\n"
                "Total Head Movement = (199 - 53) + (199 - 14) = 146 + 185 = 331 cylinders"
            )
        },
        "comparison": {
            "title": "SCAN vs C-SCAN Disk Scheduling",
            "headers": ["Feature", "SCAN (Elevator)", "C-SCAN (Circular SCAN)"],
            "rows": [
                ["Direction of Service", "Services requests in both forward and reverse directions", "Services requests in one direction only; returns to start without servicing"],
                ["Waiting Time Uniformity", "Biased: tracks near turnaround boundaries get faster service than tracks in center", "Uniform: all tracks experience consistent wait times"],
                ["Boundary Travel", "Travels all the way to physical disk boundary (track 0 or max track)", "Travels to boundary (or furthest request in C-LOOK) then resets to track 0"],
                ["Head Movement", "Slightly lower total cylinder distance than C-SCAN", "Slightly higher total cylinder distance due to fast return jump"],
                ["Starvation Risk", "Low, but newly arrived tracks behind head wait for full double sweep", "Extremely low, fair distribution across entire disk platter"]
            ]
        },
        "formulas": [
            {"name": "Total Disk Access Time", "formula": "T_access = T_seek + T_rotational + T_transfer", "explanation": "Average rotational latency = 1 / (2 * RPM) converted to seconds."},
            {"name": "Head Movement Distance", "formula": "Total Cylinders = SUM |Track_current - Track_next|", "explanation": "Absolute sum of track transitions across entire servicing sequence."}
        ],
        "exam_tip": "In LOOK and C-LOOK questions: The disk arm stops at the highest or lowest REQUESTED track — it does NOT travel to the physical disk limits (0 or 199) like SCAN and C-SCAN do!",
        "common_confusion": {
            "wrong": "Direct Memory Access (DMA) completely eliminates the CPU from I/O handling.",
            "correct": "The CPU is still required to initiate the transfer (writing base address and byte count to DMA registers) and service the completion interrupt.",
            "explanation": "DMA only frees the CPU during the actual bulk byte-by-byte data transfer phase."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is Direct Memory Access (DMA) and why is it needed?",
                "a": "DMA is a hardware mechanism that allows high-speed I/O devices (like disk controllers and network cards) to transfer data blocks directly to and from system RAM without passing through CPU registers, freeing the processor to perform computational tasks."
            },
            {
                "marks": "5-Mark Question",
                "q": "Differentiate between Polling and Interrupt-Driven I/O.",
                "a": "1. Polling (Programmed I/O): The CPU continuously checks the device status register in a tight loop until the device is ready. Highly inefficient because it wastes millions of CPU cycles in busy-waiting.\n2. Interrupt-Driven I/O: The CPU issues an I/O command and immediately switches to executing other processes. When the I/O device finishes, it asserts a hardware interrupt line, prompting the CPU to execute the Interrupt Service Routine (ISR). Highly efficient."
            },
            {
                "marks": "10-Mark Question",
                "q": "A magnetic disk has 200 tracks (0 to 199). The request queue contains: 82, 170, 43, 140, 24, 16, 190. Current head is at track 50. Calculate total head movement for FCFS, SSTF, and SCAN (moving toward 199).",
                "a": "1. FCFS:\n   - Order: 50 -> 82 -> 170 -> 43 -> 140 -> 24 -> 16 -> 190\n   - Distances: |82-50| + |170-82| + |43-170| + |140-43| + |24-140| + |16-24| + |190-16|\n   - Sum = 32 + 88 + 127 + 97 + 116 + 8 + 174 = 642 cylinders.\n2. SSTF:\n   - Nearest selection from 50: 43 -> 24 -> 16 -> 82 -> 140 -> 170 -> 190\n   - Distances: |43-50| (7) + |24-43| (19) + |16-24| (8) + |82-16| (66) + |140-82| (58) + |170-140| (30) + |190-170| (20)\n   - Sum = 7 + 19 + 8 + 66 + 58 + 30 + 20 = 208 cylinders.\n3. SCAN (moving toward 199):\n   - Order: 50 -> 82 -> 140 -> 170 -> 190 -> 199 (boundary) -> 43 -> 24 -> 16\n   - Distance = (199 - 50) + (199 - 16) = 149 + 183 = 332 cylinders."
            }
        ],
        "revision_60s": [
            "Disk Access = Seek Time (largest mechanical delay) + Rotational Latency + Transfer Time.",
            "DMA transfers data directly between device buffer and RAM.",
            "FCFS disk scheduling: fair, but high head travel distance.",
            "SSTF: selects closest track next; causes starvation for distant tracks.",
            "SCAN (Elevator): sweeps across disk to boundary, then reverses.",
            "LOOK/C-LOOK: reverses at furthest requested track rather than disk boundary."
        ]
    },

    "protection-and-security": {
        "title": "Protection, Security & Access Control",
        "subject": "os",
        "exam_definition": (
            "Protection is an internal operating system mechanism that controls access of processes and users to system resources, "
            "while Security is the defense against external threats, attacks, and unauthorized data breaches, enforced via Access Control Matrices, "
            "Access Control Lists (ACLs), Capabilities, and Cryptography."
        ),
        "remember": "Protection vs Security: Protection is internal resource access control; Security is defense against external attacks/threats.",
        "core_concept": (
            "An operating system must enforce the Principle of Least Privilege: every program and user should operate with the minimum "
            "set of privileges necessary to complete its task. The protection model specifies access rights across Protection Domains. "
            "Access Control can be modeled as a two-dimensional Access Matrix where rows represent Domains and columns represent Objects."
        ),
        "key_points": [
            "Principle of Least Privilege (PoLP): Minimizes damage from faults or malware by restricting access rights strictly to what is required.",
            "Protection Domain: A collection of access rights, each specifying an object and the operations permitted on it (e.g. read, write, execute).",
            "Access Control Matrix: Abstract table of Domains (rows) $\\times$ Objects (columns). Sparsely populated in practice.",
            "Access Control List (ACL): Column-oriented decomposition of the access matrix; each object stores a list of domains and allowed operations.",
            "Capability List: Row-oriented decomposition of the access matrix; each domain holds an unforgeable token/ticket listing accessible objects.",
            "User Authentication: Passwords, Multi-Factor Authentication (MFA), biometric authentication.",
            "Program Threats: Trojan Horses, Trapdoors/Backdoors, Buffer Overflows, Viruses, Worms."
        ],
        "classification": {
            "title": "Access Matrix Implementations",
            "items": [
                {"name": "Access Control Lists (ACLs)", "desc": "Stored with the object. Lists which domains/users can perform operations (e.g. POSIX file permissions rwxr-xr-x)."},
                {"name": "Capability Lists", "desc": "Stored with the domain/process. Unforgeable cryptographically signed tokens detailing permissible object operations."},
                {"name": "Role-Based Access Control (RBAC)", "desc": "Privileges assigned to organizational roles; users dynamically inherit privileges by assuming roles."},
                {"name": "Mandatory Access Control (MAC)", "desc": "System-enforced security classification levels (e.g. Top Secret, Secret, Unclassified via Bell-LaPadula model)."}
            ]
        },
        "how_it_works": {
            "title": "Buffer Overflow Attack & Stack Smashing Defense",
            "steps": [
                "1. Vulnerable C program uses unsafe function like strcpy() or gets() without bounds checking on stack buffer.",
                "2. Attacker provides input string larger than allocated buffer array.",
                "3. Excessive bytes overflow the local buffer, corrupting the saved frame pointer (EBP) and Return Address on stack.",
                "4. Overwritten Return Address points to injected malicious shellcode located in the buffer.",
                "5. When function returns (ret instruction), CPU jumps to shellcode executing arbitrary attacker commands.",
                "6. OS Defenses: Stack Canaries, Non-Executable Stack (NX/DEP bit), and Address Space Layout Randomization (ASLR)."
            ],
            "diagram": "Stack: [Local Buffer | Stack Canary | Saved Frame Pointer | Return Address (Overwritten!)] ──> Malicious Shellcode Jump"
        },
        "example": {
            "title": "UNIX File Permissions & Access Control List (ACL)",
            "scenario": "Inspecting standard octal file permissions and advanced POSIX ACLs on Linux.",
            "code": (
                "# 1. Standard UNIX 3-tier permissions (User, Group, Others)\n"
                "$ ls -l exam_grades.txt\n"
                "-rw-r----- 1 professor faculty 4096 Sep 18 exam_grades.txt\n"
                "# Explanation: User (professor) has rw-, Group (faculty) has r--, Others have ---\n\n"
                "# 2. Octal representation:\n"
                "# rw- (6) | r-- (4) | --- (0) => chmod 640 exam_grades.txt\n\n"
                "# 3. Advanced POSIX ACL: Grant teaching assistant (ta_john) read-only access\n"
                "$ setfacl -m u:ta_john:r exam_grades.txt\n"
                "$ getfacl exam_grades.txt\n"
                "# file: exam_grades.txt\n"
                "# owner: professor\n"
                "# group: faculty\n"
                "user::rw-\n"
                "user:ta_john:r--  <-- Specific fine-grained ACL entry\n"
                "group::r--\n"
                "mask::r--\n"
                "other::---"
            )
        },
        "comparison": {
            "title": "Access Control Lists (ACLs) vs Capability Lists",
            "headers": ["Feature", "Access Control Lists (ACLs)", "Capability Lists"],
            "rows": [
                ["Storage Location", "Stored on/with the Object (column-wise matrix slice)", "Stored with the Subject/Process/Domain (row-wise matrix slice)"],
                ["Analogy", "Guest list at a door (bouncer checks if your name is on list)", "Ticket or key card held in your pocket"],
                ["Revocation", "Easy: simply remove the domain name from the object's ACL", "Difficult: finding and revoking distributed capabilities is complex"],
                ["Delegation", "Difficult: requires modifying object permissions", "Easy: process can pass its capability token to another process"],
                ["Examples", "POSIX file permissions, Windows NTFS ACLs", "POSIX file descriptors, capability-based microkernels (seL4)"]
            ]
        },
        "formulas": [
            {"name": "Octal Permission Calculation", "formula": "Permission = (Read * 4) + (Write * 2) + (Execute * 1)", "explanation": "Calculated independently for User, Group, and Other (e.g. 755 = rwxr-xr-x)."}
        ],
        "exam_tip": "Remember the distinction between Protection and Security: Protection is internal resource access control mechanisms within the OS. Security is defenses against unauthorized external entities, viruses, network intruders, and hardware sabotage.",
        "common_confusion": {
            "wrong": "chmod 777 is a safe way to fix file permission denied errors.",
            "correct": "chmod 777 grants universal Read, Write, and Execute permissions to everyone on the system, creating a catastrophic security hole.",
            "explanation": "Any local user or compromised service can overwrite or execute malicious code in the file."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the Principle of Least Privilege in computer security?",
                "a": "The Principle of Least Privilege states that every program, process, and user in a computing system must operate using only the minimal set of privileges, permissions, and resources strictly necessary to perform its legitimate job function, minimizing potential attack surface and damage."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the structure and operation of an Access Control Matrix.",
                "a": "1. Structure: A conceptual two-dimensional table where rows represent Protection Domains (users or processes) and columns represent System Objects (files, devices, memory regions).\n2. Matrix Elements: Entry $M[D_i, O_j]$ specifies the set of access rights domain $D_i$ holds on object $O_j$ (e.g. {read, write, execute}).\n3. Practical Implementation: Because the matrix is vast and mostly empty (sparse), real operating systems decompose it into Access Control Lists (by column, attached to objects) or Capability Lists (by row, attached to processes)."
            },
            {
                "marks": "10-Mark Question",
                "q": "What is a Buffer Overflow attack? Explain how stack smashing corrupts the execution flow and discuss modern operating system countermeasures.",
                "a": "1. Definition: A buffer overflow occurs when a program writes data beyond the allocated boundary of a fixed-size buffer on the call stack, overwriting adjacent memory locations.\n2. Attack Mechanics:\n   - Call Stack Layout: Local variables, saved EBP/frame pointer, Return Address.\n   - Unchecked functions (strcpy, gets) allow input to spill past the buffer.\n   - The attacker overwrites the Return Address with the memory address of malicious injected shellcode.\n   - When the function executes ret, CPU jumps to attacker shellcode with the program's privileges.\n3. Countermeasures:\n   - Stack Canaries: Random integer placed before return address; verified before returning. If corrupted, kernel aborts process.\n   - Non-Executable Stack (NX / DEP): Marks stack pages non-executable, preventing CPU from executing code in stack memory.\n   - Address Space Layout Randomization (ASLR): Randomizes memory offsets of stack, heap, and libraries at boot, making shellcode addresses unpredictable."
            }
        ],
        "revision_60s": [
            "Protection = internal resource access control; Security = external defense against threats.",
            "Principle of Least Privilege: minimum privileges needed to do the job.",
            "Access Matrix: rows = domains, columns = objects.",
            "ACL = stored with object (column-slice); Capability = stored with process (row-slice).",
            "Buffer overflow overwrites stack return address; defeated by Canaries, NX, and ASLR."
        ]
    }
}

def generate():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(OS_TOPICS, f, indent=2, ensure_ascii=False)
    print(f"Generated complete OS dataset with {len(OS_TOPICS)} topics at: {DATA_PATH}")

if __name__ == "__main__":
    generate()
