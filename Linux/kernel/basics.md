# 1. The thick layer between apps and hardware

On top, you have the programs you launch (e.g, VS Code, Firefox, Chrome, OBS, Audacity, VLC, GIMP). At the bottom, you have physical parts (network card, GPU, CPU, RAM, keyboard, mouse). They never talk directly! Between them sits a **large, complex software layer**,
and **only one part of that layer is the kernel**.

```bash
    +-------------------------------------------------------------+
    |  USER APPLICATIONS                                          |
    |      [VSCode]  [Firefox]  [Chrome]  [OBS]  [VLC]  [GIMP]    |
    +-------------------------------------------------------------+
                                |
    #===========================================================#
    #                 A COMPLEX SOFTWARE LAYER                  #
    #   ......................................................  #
    #   :                    KERNEL                          :  #   <-- only one OS part
    #   :....................................................:  #       
    #===========================================================#
                                |
    +-------------------------------------------------------------+
    |  HARDWARE                                                  |
    |  [NIC]   [GPU]   [CPU]   [RAM]   [Keyboard]   [Mouse]      |
    +-------------------------------------------------------------+
```

> Key idea: "kernel" and "operating system" are NOT synonyms. The kernel is a component of the OS.

---

# 2. CPU modes: The hardware reason the kernel exists

A modern CPU can run in (at least) two modes. The mode decides **which machine
instructions are allowed**.

```
                        +---------------------+
                        |         CPU         |
                        +---------------------+
                       /                       \
        (1) PRIVILEGED MODE                      (2) RESTRICTED MODE
        FULL instruction set                     SAFE subset only
        --------------------------               --------------------
        - Move data                              - Move data
        - Copy data                              - Copy data
        - Math                                   - Math
        - Conditions                             - Conditions
        - Loop                                   - Loop
        - Manage CPU mode                        - Nothing that can touch
        - Manage memory boundaries                 hardware or other processes
        - Talk to I/O devices
```

* **Privileged mode**: Essentially every instruction, including managing memory
  pages and communicating with other devices.
* **Restricted mode**: A safe subset that *cannot interfere directly with the hardware* or with other programs.

---

# 3. Kernel Space vs User Space

There are two separate names for those two CPU modes: 
```bash
    KERNEL SPACE   ==  CPU Privileged Mode   ==  where the kernel runs
      USER SPACE   ==  CPU Restricted Mode   ==  where user apps live
```

So. **user space** and **kernel space** are just software words for the CPU's hardware-enforced privilege levels. The CPU itself keeps the two apart.

---

# 4. System call: How user space crosses the line

A restricted-mode program (e.g., user application) cannot touch the hardware (e.g., network card) by itself. When it needs to use hardware, it performs a **system call**, a controlled trap that switches the CPU into privileged mode and hands control to the kernel.

```
      User Application  (RESTRICTED mode)
            |
            |   System Call   (trap: switch CPU to PRIVILEGED mode)
            v
    +------------------- KERNEL -------------------+
    |   System Call Interface                      |
    |          |                                   |
    |          v                                   |
    |   Subsystem  -->  Device Driver              |
    +---------------------------------------------+
            |
            v
        Hardware (e.g. network card)
```

The system call is the **only sanctioned doorway** from user space into kernel
space.

---

# 5 Inside the kernel: A stack of subsystems

The kernel is not one binary large object (blob). It is a set of **subsystems**, each managing one resource or providing one service, as shown below:

```bash
    +------------------------------- KERNEL -------------------------------+
    |                       System Call Interface                          |  <-- closest part
    +----------------------------------------------------------------------+      to user apps
    | Device  | I/O     | Virtual   | CPU       | Memory      | Interrupt  |
    | Drivers | Subsys  | File Sys  | Scheduler | Management  | Exceptions |
    +---------+---------+----------+-----------+-------------+-------------+
    | Networking Stack  |    IPC Mechanisms    |    Security & Access      |
    +----------------------------------------------------------------------+
```

| Subsystem | Job |
|---|---|
| **System Call Interface** | The entry point. It lets user space request kernel services. The closest layer to user apps. |
| **Device Drivers** | Kernel modules that control and talk to specific hardware devices. |
| **I/O Subsystem** | Manages input/output between hardware devices and the system. |
| **Virtual File System** | One unified interface over many different filesystem implementations. |
| **CPU Scheduler** | Decides which process/thread runs on the CPU and for how long. |
| **Memory Management** | RAM allocation, virtual memory, paging and memory protection. |
| **Interrupt & Exception Handler** | Responds to hardware interrupts and CPU exceptions. |
| **Networking Stack** | Low-level protocols (TCP/IP) and socket communication. |
| **IPC Mechanisms** | Channels between processes like pipes, shared memory, signals and sockets. |
| **Security & Access Control** | Enforces permissions, isolation and privilege boundaries between processes and users. |

---

# 6. Bootstrapping: The kernel is loaded into memory

When the machine powers on, the kernel's own executable code has to be copied into RAM before it can run anything. That load step is called **bootstrapping**. Its code sits in a protected region, the **kernel memory**.

```bash
     MEMORY
    +-------------------------+   High addresses
    |      KERNEL MEMORY      |   <-- Kernel image is loaded here during bootstrapping 
    |           ...           |    
    |    10110101 01011010    |
    |    01101001 11010110    |
    |           ...           |
    +-------------------------+
    |           ...           |
    |           ...           |
    +-------------------------+   Low addresses
```

---

# 7. `init`: the ONE user process that is created by kernel

Once all critical subsystems are up, the kernel starts **one** user-space
process and hands over. That process is called **`init`** and it always gets **PID = 1**.

```bash
     MEMORY
    +---------------------------+   High addresses
    |       KERNEL MEMORY       |
    |            ...            |
    |            ...            |
    +---------------------------+
    |       init  (pid = 1)     |   <- the ONLY user process created BY the kernel
    |  process's address space  |
    +----------------------------+
```

`init` is a very special process, because **no other user process has created it**. The kernel did and it acts as the ancestor of every other user process that will spawn.


# 8. Every other user process descends from `init`

Run `pstree` and see a single tree. On a typical Ubuntu box, the root is named `systemd`. It is essentially symbolic link to `init`. Every other daemon and app hangs off it.

```bash
    systemd(1)
      |-- ModemManager
      |-- NetworkManager
      |-- gdm3 --- gdm-session-wor --- gdm-wayland-ses --- gnome-session-b
      |-- cron
      |-- cups-browsed
      |-- snapd
      |-- systemd --(sd-pam)
      |             |-- dbus-daemon
      |             |-- gnome-keyring-d
      |             \-- gnome-session-b --- ...
      |-- ...
```

Given that a user process can only be created by another user process (`fork`), the chain has to start *somewhere*. There is **exactly one ancestor user process** that, directly or indirectly, started them all.

```bash
                (kernel)
                   |
        creates ONE user process
                   |
                   v
            +------------------+
            |  init (pid = 1)  |           <-- The ancestor user process
            +------------------+
                /   |   \
             ...   ...   ...               <-- Every other user process is a
            /  \        /   \                  child of another user process
          ...  ...    ...   ...
```

Regarding the borderline:

* Everything that happens **before** the ancestor user process is the **kernel**.
* The **ancestor** user process is **`init`** and **everything it spawns is user space.**
* The **kernel space vs user space boundary** is NOT a folder or a file. It is **"before `init`" vs "`init` and after"**.

---

# 9. `init` is protected and must never die

Try to kill PID 1 by hand:

```bash
user@pc:~$ kill -9 1
user@pc:~$ # Nothing happens
```

`SIGKILL` (signal #9) normally cannot be caught, blocked or ignored. **Except** for PID 1. The kernel refuses to let userland kill `init`. Why so strict? There are two reasons:

**1. Orphan adoption.** Linux dislikes orphaned processes, it is, running processes whose parent has exited. If a parent dies, the kernel **reparents** its children user processes to `init`:

```bash
    Before:   parent(87) ---> child(89)
    
              # parent(87) exits
              # init(1) adopts the orphan user process

    After:       init(1) ---> child(89)
```

`init` also *reaps* these adopted children so they don't become zombies.

**2. If `init` itself crashes or exits, the system is over.** From `linux/kernel/exit.c` code:

```bash
    if (group_dead) {
        /*
         * If the last thread of global init has exited, panic
         * immediately to get a useable coredump.
         */
        if (unlikely(is_global_init(tsk)))
            panic("Attempted to kill init! exitcode=0x%08x\n",
                  tsk->signal->group_exit_code ?: (int)code);
    }
```

> Even if nothing inside the kernel is broken, **`init` crashing = kernel panic**.

---

# 10. Where does the kernel find `init`?

The kernel tries a fixed list of paths, in order. From `linux/init/main.c` code:

```bash
    if (!try_to_run_init_process("/sbin/init") ||
        !try_to_run_init_process("/etc/init")  ||
        !try_to_run_init_process("/bin/init")  ||
        !try_to_run_init_process("/bin/sh"))
            return 0;

    panic("No working init found.  Try passing init= option to kernel. "
          "See Linux Documentation/admin-guide/init.rst for guidance.");
```

Path lists:

```
    /sbin/init    - Traditional and most common location for the init binary
    /etc/init     - Older fallback used by some legacy systems
    /bin/init     - Another common path, lightweight init variants
    /bin/sh       - Final emergency fallback: just run a shell
    (none works)  - Panic!
```

Under the hood `try_to_run_init_process()` calls `run_init_process()`, which ends in `kernel_execve(init_filename, argv_init, envp_init)`.
The kernel literally `exec`s that file as PID 1. You can override the list with the `init=` kernel command-line parameter.

---

# 11. `init` is a role, NOT a fixed program

Several different programs can play the `init` role:

```bash
    SysVinit      OpenRC      runit      systemd
```

Run `pstree` on different distros and PID 1 has different names:

```bash
    Ubuntu / Fedora       -->   systemd
    Slackware (SysVinit)  -->   init
    Artix (runit)         -->   runit
```

How each one gets found by the kernel:

```bash
    SysVinit.c \
    OpenRC.c    |--> Compiled --> Real binary installed at /sbin/init
    runit.c    /

    systemd.c -----> Compiled --> /lib/systemd/systemd
                                        ^
                                        |
                   /sbin/init  ---------+   (symbolic link = a shortcut to the actual executable)                     
```

Proof with `ls -l /sbin`:

```bash
lrwxrwxrwx  1  root  root  <DATE_AND_TIME>  init  --> ../lib/systemd/systemd
```

So on a **`systemd`** machine, the kernel still opens `/sbin/init`. That path is just a symlink pointing at `systemd`. The **mechanism** (kernel executes `/sbin/init` as PID 1) never changes. Only the target binary does.

---

# 12. The kernel's responsibility stops at launching `init`

The kernel only cares about launching `init`. What other processes `init` spawns is NOT the kernel's concern. `init` alone is enough to bootstrap the **entire** user-space process tree seen back in section 8.

```bash
                        +--------+
                        |  init  |
                        +--------+
                        /        \
              (Display Server)   (Session Manager)
                 /     \              /     \
              app1    app2          app3    app4    <-- Kernel does not track any of this
             /  \     /  \                                
           ...  ... ...  ...
```

---

# 13. The rest of the OS: Essential, but still user space

Around the kernel sit many components that applications depend on to actually be usable. The following are **NOT part of the kernel**:

```bash
    Job Scheduler        Task Manager         Terminal Emulator      Desktop Environment
    File Explorer        Standard Library     Settings Manager       Firewall Manager
    Shell                SSH Server           Device Manager         Display Server
    Session Manager      Package Manager      Network Manager        Multimedia Stack
```

Usage examples of the aforementioned user space applications:

| Component | What it does | Examples |
|---|---|---|
| Shell | Reads commands, executes programs | `bash`, `zsh`, `fish`, PowerShell |
| Terminal Emulator | GUI window around a shell | GNOME Terminal, Konsole, Alacritty |
| Desktop Environment | Complete graphical desktop | GNOME, KDE Plasma, Cosmic, XFCE |
| Display Server | Manages graphical buffers, draws to screen | Xorg, Wayland, DWM |
| Standard Library | High-level APIs that *wrap* system calls | `glibc`, `musl` (C libraries) |
| Session Manager | Login sessions and seat management | `systemd-logind`, ConsoleKit |
| Package Manager | Install/update/ remove software | `apt`, `snap`, `dnf`, `pacman`, `Homebrew` |
| Device Manager | Detects and configures devices dynamically | `udev` |
| Task Manager | Shows and manages running processes | `top`, `htop`, GNOME System Monitor |
| Firewall Manager | Configures kernel firewall rules | `ufw`, `firewalld` |

> Note on **Standard Library**: Apps mostly call `glibc`, and then`glibc` makes the actual system calls.

Example flow:

```bash
    Desktop Environment
          |  (uses)
          v
     Display Server
          |  (uses)
          v
    System Call Interface  ===== Borderline =====
          |
          v
        KERNEL
```

---

# 14. The user-space part of the OS

In practice, there is **no clean definition** of which user-space programs are "the OS". Candidate rules, all leaky:

```bash
    - Every program that ships with the OS?
    - Every program that has no lower-level alternative?
    - Every program started automatically by init?
```

Counter-examples include the **GNU coreutils** (`ls`, `cp`, `mv`, `cat`, `chmod`, `rm`, `echo`, `kill`, `true`, `false`, `sleep`) and ~100 other tiny programs.

```bash
    arch   base64   basename   cat     chcon   chgrp   chmod   cp     csplit   cut
    dd     df       echo       env     expr    false   fmt     fold   head     id
    kill   ln       ls         mkdir   mv      nice    od      pwd    rm       rmdir
    seq    sleep    sort       stat    tail    tee     test    touch  tr       true
    ...
```

They obviously belong to "The operating System", yet **most of them are never started by `init`**. They run only when you type them. So the "started by init" claim is not the boundary either.

> **Conclusion: The user-space side of the OS is fuzzy and partly a matter of convention. The *kernel* side, by contrast, has a hard edge.**

---

# 15. The full picture

```bash
    =================    USER SPACE  (CPU restricted mode)    =================

    ---------------------------------------------------------------------------
      Firefox    GIMP    VLC    VS Code    OBS    Audacity
    ---------------------------------------------------------------------------
      Shell  Terminal  Display Server  Desktop Env  Package Manager
      Task Mgr  Network Mgr  CoreUtils  Standard Library  SSH Server
    ---------------------------------------------------------------------------
                          init   (pid = 1)    <-- The first user process
    ---------------------------------------------------------------------------
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <== THE BORDERLINE
    
    =================    KERNEL SPACE  (CPU privileged mode)    ===============

    ---------------------------------------------------------------------------
                        System Call Interface
    ---------------------------------------------------------------------------
      Device Drivers   | I/O Subsystem     | Virtual File System
      CPU Scheduler    | Memory Management | Interrupt & Exception Handler
      Networking Stack | IPC Mechanisms    | Security & Access Control
    ---------------------------------------------------------------------------

    ===========================================================================
                              HARDWARE
```

Same idea drawn as concentric rings:

```bash
      .-------------------  USER APPLICATIONS  --------------------.
     /  Firefox  VLC  GIMP  VS Code  OBS  Chromium  Audacity       \
    |     .--------------- OPERATING SYSTEM ---------------.         |
    |    /  Shell  CoreUtils  Display Server  init          \        |
    |   |   Package Mgr  Task Mgr  Terminal  Standard Lib    |       |
    |   |      .------------- KERNEL -------------.          |       |
    |   |     /  System Call Interface            \          |       |
    |   |    |  CPU Scheduler   Memory Mgmt   VFS  |         |       |
    |   |    |  Device Drivers  Networking   IPC   |         |       |
    |   |    |  Interrupts   Security & Access     |         |       |
    |   |     \                                   /          |       |
    |   |      '---------------------------------'           |       |
    |    \                                                  /        |
    |     '----------------------------------------------'          |
     \                                                             /
      '---------------------------------------------------------'
```

---

# Takeaways

```
    1. Kernel != OS. The kernel is one component of the operating system.

    2. The boundary is enforced by CPU hardware:
       kernel space = CPU privileged mode  |  user space = CPU restricted mode

    3. User space can enter the kernel only through system calls.
       The System Call Interface is the outermost kernel layer.

    4. The kernel is a stack of subsystems: scheduler, memory mgmt, VFS,
       drivers, networking, IPC, interrupts, security, syscall interface.

    5. The kernel creates only ONE user process: init (PID 1).
       Every other user process is a descendant/child of init.

    6. THE BORDERLINE:
         Everything before init   -->  kernel space
         init and its descendants -->  user space

    7. init is a role.
       /sbin/init may be SysVinit, OpenRC, runit, or a symlink to systemd.
       The kernel just executes /sbin/init or /etc/init or /bin/init or /bin/sh.
       Otherwise, it panics.

    8. init is protected: SIGKILL to PID 1 is ignored.
       If init ever exits, the kernel panics ("Attempted to kill init!").
       Orphans are reparented to init.

    9. The user-space "OS" (shell, coreutils, display server, package manager, ...) is essential.
       But it has NO crisp definition...
       Only the kernel-space "OS" has a hard edge and a clear definition.
```

---

# References

Kernel source references:
* `linux/init/main.c` (init path list, `run_init_process`,
`try_to_run_init_process`)
* `linux/kernel/exit.c` (`panic("Attempted to kill
init!")`).

YouTube video:
* "The Question Nobody Ever Explains: Where Does the Kernel End?" from Core Dumped's channel.
