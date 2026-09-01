# Kernel Terminology — A to Z

Every entry: what the acronym stands for, a plain-language meaning, and where you'd actually meet it. Companion to `kernel.md`.

---

### ABI — Application Binary Interface

The agreement between compiled pieces of software about *binary* details: which CPU register holds which argument, how a struct is laid out in memory, what syscall number 257 means.

Linux promises a **stable userspace ABI** — a program compiled in 2005 still runs on today's kernel. It deliberately promises **no stable in-kernel ABI**: internal function shapes change freely between versions, which is why the NVIDIA driver has to be recompiled for every kernel update (DKMS does this automatically).

> An API is "call the function named `open`." An ABI is "put the filename pointer in register RDI." Recipe vs. exact plating instructions.

---

### Address space

The range of addresses a piece of code is allowed to use. It's **virtual** — invented — and the **MMU** translates it to real RAM on every access.

Each program gets its own. Two programs can both use address `0x7fff0000` and be pointing at entirely different physical memory. Some addresses map to nothing at all until you touch them.

> Every office desk is labelled "Desk 1." Reception knows yours is on floor 3 and hers is on floor 7. You never learn the real location.

**See also:** kernel space, page table, userspace, virtual memory.

---

### Blob — Binary Large OBject

A file of compiled bytes shipped without source code. In kernel context, usually vendor **firmware** the kernel uploads into a device before it works.

Example: `/lib/firmware/iwlwifi-*.ucode` gets pushed into an Intel Wi-Fi card at startup. Debian ships these in a separate `firmware-nonfree` package because they aren't free software.

---

### Capability

Root's all-or-nothing power, split into about 40 separate permissions the kernel can grant individually — `CAP_NET_ADMIN` (configure networking), `CAP_SYS_ADMIN` (a grab-bag of powerful things), `CAP_BPF` (load eBPF programs).

Lets you give `ping` the ability to open raw sockets without making it fully root.

> Instead of one master key, a keyring with labelled keys. Hand out only the ones needed.

---

### cgroup — Control GROUP

A kernel feature for **measuring and limiting** resources across a group of processes: CPU share, memory ceiling, disk I/O bandwidth, number of processes.

Controlled through a filesystem. Writing `500M` to `/sys/fs/cgroup/mygroup/memory.max` caps that group; going over triggers the OOM killer *inside the group only*, leaving the rest of the machine alone.

systemd puts every service in its own cgroup. So does every container runtime.

> **Namespaces decide what you can see. cgroups decide how much you can consume.** They're often confused, and they do genuinely different jobs.

---

### Context switch

Swapping the CPU from one *program* to another. Expensive, because the memory map has to be replaced (new page tables, invalidated **TLB**).

Contrast with a **mode switch**, which is just user → kernel → user *inside the same program* — a syscall. Much cheaper, since the kernel's memory is already mapped.

---

### Decompressor stub

The small uncompressed piece of code at the front of a compressed kernel image (`vmlinuz`).

The bootloader jumps to the stub, the stub inflates the real kernel into memory, then jumps to it. It has to exist because the kernel can't decompress itself before it's in memory.

---

### eBPF — extended Berkeley Packet Filter

A way to load small programs *into the running kernel* that execute at chosen **hook** points — without writing a kernel module or rebooting.

Every program is checked by a verifier first (no infinite loops, no wild memory access), so it's far safer than a module. Used heavily for observability, networking (Cilium), and security monitoring.

---

### Firmware

Code that ships baked into a device and typically runs *before* or *below* the operating system: UEFI/BIOS, CPU microcode, the controller inside your SSD, network card firmware.

The kernel *talks to* firmware — reading ACPI tables, calling UEFI runtime services, uploading **blobs** into devices. It is not firmware itself.

> Firmware is the building's wiring and elevator controller. The kernel is management, who arrived later and can only send it requests.

---

### GID — Group ID

The numeric identity of a group a process belongs to. Paired with **UID** in every permission check the kernel performs.

---

### Hook

A pre-arranged spot in kernel code where it calls out to registered functions, so subsystems can add behaviour without editing the core.

**LSM hooks** are the security ones: `security_file_open()` fires on every file open, and SELinux or AppArmor's registered function decides allow or deny. netfilter, kprobes and eBPF all use the same pattern — fixed attach point plus a callback.

> Pre-drilled screw holes. The manufacturer put them there so you can bolt accessories on without cutting into the frame.

---

### IRQ — Interrupt ReQuest

A hardware signal from a device meaning "something happened, deal with it" — a packet arrived, a key was pressed, a disk read finished.

The **IRQ handler** is the kernel function that responds. It runs under harsh restrictions (can't sleep, can't allocate freely), so it does the bare minimum — acknowledge the device, grab the data — and hands the real work to a **softirq** or **workqueue**.

Check counts with `cat /proc/interrupts`.

> The handler is the person who grabs the ringing phone, takes a name, and puts a note on someone's desk. They don't stay on the line.

---

### Kernel build

What you get from compiling kernel source with a specific config for a specific CPU architecture: a `vmlinuz` image plus a `/lib/modules/<version>/` tree of `.ko` module files.

Config options are decided at **compile time** — `y` (built in), `m` (loadable module), `n` (absent) — so two builds from identical source can have genuinely different capabilities.

---

### Kernel space

The part of the virtual **address space** that's only reachable at ring 0, holding kernel code and data.

There is **one** kernel space, shared and mapped into every program's address space (protected by a supervisor flag in the page tables). A bad pointer here causes a *panic* or *oops*, not a segfault — there's no outer layer left to catch it.

---

### KPTI — Kernel Page Table Isolation

The fix for Meltdown. Stops mapping most kernel pages while running in ring 3, so a speculative-execution attack has nothing to leak.

Cost: every syscall now has to swap page tables, making it substantially slower. This is a major reason mechanisms that *avoid* syscalls — **vDSO**, **io_uring** — became important.

---

### libc — C standard LIBrary

The userspace library implementing `printf`, `malloc`, `open`, `fopen`. Usually **glibc** (GNU) or **musl** (small; used by Alpine Linux).

It's normally the wrapper around syscalls: you call `read()`, glibc sets up registers and executes the actual `syscall` instruction.

The kernel does **not** use libc. It has its own internals (`printk` instead of `printf`, `kmalloc` instead of `malloc`), which is why kernel C looks unfamiliar.

---

### LSM — Linux Security Modules

The framework of **hook** points where SELinux, AppArmor or Landlock enforce policy — running *after* the normal owner/permission checks pass.

So a file you own by Unix rules can still be denied by SELinux policy. Two independent gates in series.

---

### Mode switch

User → kernel → user, within the same process. That's a syscall. Cheap relative to a **context switch**, because the memory map doesn't change.

---

### Module (kernel module, `.ko`)

Kernel code that can be loaded and unloaded at runtime — usually a driver. Loaded with `modprobe` or `insmod`, listed with `lsmod`.

Crucially, a module runs in **the same privileged space as the rest of the kernel**. A buggy one crashes the machine; a malicious one is a rootkit with total control.

---

### MMU — Memory Management Unit

Hardware inside the CPU that translates every virtual address to a physical one, using **page tables**, on every single access. It also enforces the supervisor flag that keeps ring 3 out of kernel memory.

> The receptionist who converts "Desk 1" into "floor 3, room 12" — and refuses if you're not cleared for that floor.

---

### Namespace

A kernel object that gives a set of processes a **private view** of something normally global.

Eight types: `mnt` (mounts), `uts` (hostname), `ipc`, `pid`, `net` (interfaces, IPs, ports, firewall rules), `user` (UID mapping), `cgroup`, `time`.

Processes are *attached to* namespaces — they don't *contain* them. One process can mix and match: host `pid` namespace but its own `net` namespace. Membership shows up as symlinks under `/proc/<pid>/ns/`; matching inode numbers mean shared, different numbers mean isolated.

Tools: `lsns`, `unshare`, `nsenter`.

> Namespaces are what make containers possible — but a container is a *userspace* assembly of namespaces + cgroups + capabilities. The kernel has no concept of a container.

---

### Page fault

What happens when a program touches a virtual address that isn't currently backed by real memory.

Often harmless and routine — the kernel loads the page from disk or allocates it fresh and lets you continue. Sometimes fatal: touching genuinely invalid memory gets you SIGSEGV.

---

### Page table

The per-process structure the **MMU** uses to translate virtual → physical addresses. On x86 the CPU finds it via register CR3.

Each entry also carries flags: writable, executable, and **user/supervisor** — the bit that enforces the kernel/user boundary in hardware.

---

### Preemption

Whether the kernel can interrupt a running task mid-execution to run something else. Full preemption (`PREEMPT_RT`, mainlined in Linux 6.12) makes almost all kernel code interruptible, which matters for realtime workloads.

---

### Privilege

Two different things people conflate:

1. **CPU privilege** — which **ring** you execute in, enforced by hardware
2. **OS privilege** — what your **UID** and **capabilities** let you ask the kernel to do

`sudo` only affects the second. It's an ordinary setuid-root program that checks `/etc/sudoers` and then runs your command as UID 0. A sudo'd process is still in ring 3 and still asks the kernel for everything.

> **Root is a VIP wristband — staff unlock doors when you ask. Ring 0 is being staff.**

---

### Rings (0–3)

x86 hardware privilege levels. **Lower number = more power.** Linux uses only ring 0 (kernel) and ring 3 (your programs); rings 1 and 2 go unused because other CPU families don't have four levels. ARM's equivalent is EL0/EL1/EL2/EL3.

The ring gates three things: which instructions you may execute, which memory you may touch, and whether you can do direct device I/O.

**Not related to L1/L2/L3 caches.** Caches are about speed (fast memory on the chip); rings are about security (a privilege setting). The numbering even runs opposite ways.

**Getting from ring 3 to ring 0 legitimately:** only through hardware entry points — a `syscall` instruction, an interrupt, or an exception — each landing at an address *the kernel picked in advance*. You choose what to ask for, never where execution resumes.

**Illegitimately:** exploit a kernel bug, or load your own code via a signed module or a verified eBPF program.

---

### Ring −1 / −2 (informal)

Levels *below* the kernel:

- **Ring −1** — hypervisor (KVM, Hyper-V, ESXi); ARM calls it EL2
- **Ring −2** — **SMM**, System Management Mode: firmware code the OS cannot see or intercept

This is why firmware implants are so hard to detect. Your antivirus runs in a layer above them.

---

### seccomp — SECure COMPuting mode

Per-process filtering of which **syscalls** are allowed, written as a small BPF program.

Lets a program voluntarily drop its own access — a PDF renderer can permit `read` and `write` while blocking `execve` and `socket` entirely, so a bug in the parser can't spawn a shell.

---

### Symlink — SYMbolic LINK

A file whose contents are a path, so opening it redirects to the target. Created with `ln -s`, inspected with `ls -l` or `readlink`.

Relevant here because `/proc/self/ns/net` is a symlink pointing at something like `net:[4026531840]` — not a real path, but a **namespace identifier**. That's how you tell whether two processes share a namespace.

---

### Syscall — SYStem CALL

The only sanctioned way userspace requests something from the kernel: put a number and arguments in CPU registers, execute the `syscall` instruction, and the CPU jumps to ring 0 at a fixed handler.

`openat` is number 257 on x86_64. Run `strace ls` to watch every syscall a program makes. There are roughly 350–450 depending on architecture.

This boundary is where **seccomp** filters, and where most security monitoring happens — because everything meaningful has to cross it.

> Ordering at the bar. You don't reach behind the counter; you ask, they check whether you're allowed, they hand it over.

---

### TLB — Translation Lookaside Buffer

A small cache of recent virtual → physical address translations, so the **MMU** doesn't have to walk the **page tables** every time.

A **context switch** invalidates much of it, which is a big part of why switching processes is expensive.

---

### UID — User ID

The numeric identity of a process's owner. The kernel compares UID and **GID** against file ownership on every access.

- **UID 0 = root.** Historically bypasses all permission checks; modern kernels break this down into **capabilities**.
- **UID 1000** is conventionally the first human account created at install. Not a kernel rule — just a distro convention.
- **UIDs 1–999** are typically system daemons.

Inside a **user namespace**, these get remapped: UID 0 inside can be UID 100000 outside. Root in the container, nobody on the host.

---

### Userspace

Everything running at ring 3, each program in its own private **address space**: your shell, systemd, sshd, browsers, plus libraries like libc.

It cannot touch hardware or another program's memory directly. Everything real goes through a **syscall**.

On whether `OS = kernel + userspace`: fair for everyday speech, but the two aren't clean halves of one circle. "Linux" strictly names the kernel; a *distribution* is kernel plus userspace. The kernel/userspace line is a **privilege boundary**, while "distribution" is a **packaging** decision — different kinds of line.

---

### vDSO — virtual Dynamic Shared Object

A small kernel-maintained page mapped into every program's address space, holding data and code for a few very common calls.

`clock_gettime()` usually reads it directly in ring 3 and **never enters the kernel at all**. Pure speed optimisation — and it matters more since **KPTI** made syscalls expensive.

> Management posts the current time on a board in the guest area, so nobody has to queue at the bar to ask.

---

### Virtual memory

The overall scheme: programs use invented addresses, the **MMU** translates them via **page tables**, and physical RAM is allocated only as actually needed.

Why virtual space can be enormously bigger than installed RAM (128 TB of address space on a 16 GB laptop), why `malloc` succeeding tells you little about free memory, and why shared libraries exist as one physical copy mapped into many programs.
