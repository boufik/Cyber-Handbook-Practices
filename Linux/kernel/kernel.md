# The Kernel — How It Works

A plain-language guide. Terms in **bold** are defined in `terminology.md`.

---

## The one analogy to hold onto

Think of a computer as a **nightclub**.

- The **hardware** is the building: rooms, power, plumbing.
- The **kernel** is the security staff and management. They have keys to every room, they decide who goes where, and they're the only ones allowed to touch the electrical panel.
- **Userspace** is the guests. You can dance, buy a drink, use the toilets — but you can't walk into the server room or rewire the lights.
- A **syscall** is you walking up to a staff member and asking for something. You don't go get it yourself. You ask, they check whether you're allowed, and they do it for you.

Almost everything below is a detail of how that arrangement is enforced.

---

## 1. What a kernel actually is

The kernel is the central program of an operating system. It starts at boot, stays in memory until shutdown, and sits between the hardware and everything else.

Its main jobs:

- **Scheduling** — deciding which program gets the CPU, and for how long
- **Memory** — giving each program its own private view of memory
- **Drivers** — talking to your disk, network card, keyboard, GPU
- **Filesystems** — turning "open `/home/notes.txt`" into disk operations
- **Networking** — the TCP/IP stack
- **Security** — checking who is allowed to do what

### Hardware, software, or firmware?

**Software.** Just a file on disk. On Linux it's `/boot/vmlinuz-6.x`.

People assume it's something more exotic because it runs with total power over the machine. But power and substance are different things. The kernel is privileged software, not hardware.

**Firmware** is the genuinely different one: code that ships baked into a device and usually runs *before* or *below* the operating system. Your UEFI/BIOS, the code inside your SSD's controller, the microcode inside the CPU itself. The kernel talks *to* firmware; it isn't firmware.

> **Analogy:** The kernel is the club's management team — hired staff, replaceable, they arrived with the business. Firmware is the building's own wiring and elevator controller: it was there before management, it runs whether or not the club is open, and management can only send it requests.

### What language is it written in?

Mostly **C**, plus a bit of **assembly** for the parts C can't express — the very first instructions after boot, the code that catches interrupts, the code that switches between programs.

- **Linux** — C, assembly, and since version 6.1, optional **Rust** for drivers
- **Windows NT** — C, some C++, assembly
- **macOS (XNU)** — C, C++ (for drivers), assembly

But kernel C is not normal C. There's no **libc**, so no `printf` and no `malloc` — the kernel has its own versions (`printk`, `kmalloc`). The stack is tiny (8–16 KB, versus megabytes in a normal program). Floating point is mostly banned. Code written for normal programs generally won't even compile.

> **Analogy:** It's like cooking in a submarine galley. Same skills, same ingredients — but no running water, a two-foot ceiling, and if you set off the fire alarm everyone drowns.

### Is it machine code?

The source isn't. The shipped file is.

`vmlinuz` contains a small **decompressor stub** plus a compressed blob of native **machine code** for one specific CPU architecture. That's why an x86_64 kernel won't boot on a Raspberry Pi. There's no portable "kernel bytecode" — what runs is native instructions.

---

## 2. Rings — who is allowed to do what

CPUs enforce privilege in hardware. On x86 there are four levels called **rings**, numbered 0 to 3. **Lower number = more power.**

Linux uses only two of them:

| Ring | Who | Can do |
|------|-----|--------|
| **0** | Kernel | Anything |
| 1, 2 | (unused) | — |
| **3** | Your programs | Only safe operations |

Rings 1 and 2 are skipped because other CPU families don't have four levels — ARM has EL0 (user) and EL1 (kernel) — so using the middle rings would make Linux harder to port. A few systems did use them historically: OS/2 used ring 2, and old Xen ran guest kernels in ring 1.

### Rings are NOT related to L1/L2/L3 caches

This confuses people constantly, and the two have nothing to do with each other:

| | What it is | Purpose |
|---|---|---|
| **Rings 0–3** | A 2-bit privilege setting in the CPU | Security |
| **Cache L1/L2/L3** | Physical fast memory on the CPU chip | Speed |

The numbering even runs the opposite way — ring 0 is the *most* privileged, L1 is the *smallest* cache. Caches don't care who you are; they just hold whatever was touched recently.

### Rings control both memory and execution

The privilege level gates three things at once:

1. **Which instructions you may run.** Some instructions only work in ring 0 — switching page tables, loading descriptor tables, disabling interrupts. Try one in ring 3 and the CPU faults immediately.
2. **Which memory you may touch.** Every page of memory carries a "supervisor only" flag. The **MMU** checks it on every single access, in hardware. Ring 3 touching a kernel page = page fault.
3. **Hardware ports and interrupts.** Direct device I/O is blocked from ring 3.

> **Analogy:** Rings are the difference between a guest wristband and a staff badge. The badge doesn't make you faster (that's cache); it opens doors and lets you operate equipment.

### How do you get from ring 3 to ring 0?

**The legitimate way:** you don't jump there. You trigger a hardware-defined *entry point*, and the CPU jumps to an address **the kernel chose in advance**.

- A **syscall** instruction (`syscall` on x86_64, `svc` on ARM)
- An **interrupt** from a device
- An exception, like a page fault

In all three cases you control *what you ask for*, never *where the code resumes*. That's the entire security model.

**The illegitimate way:** find a bug in the kernel and exploit it, or load your own code through an approved channel (a signed kernel module, or an **eBPF** program that passes the kernel's verifier).

> **Critical point: being `root` is NOT being in ring 0.**
> `root` (UID 0) is a *userspace* idea that the kernel enforces. A root process still runs in ring 3 and still has to ask the kernel for everything. Root means "the kernel says yes to your requests." Ring 0 means "you *are* the kernel." Getting from root to ring 0 requires a vulnerability or a module load.
>
> **Analogy:** Root is a VIP wristband — staff will unlock any door you ask about. Ring 0 is being staff. The VIP still has to ask.

---

## 3. Memory — virtual vs physical

### An address space is not RAM

When we say **address space**, we mean a *virtual* map — a made-up set of addresses that a program uses. Physical RAM is what those addresses eventually point *to*.

Every memory access goes through the **MMU**, which translates the virtual address into a real physical location using **page tables**. This happens in hardware, on every access.

Consequences worth internalizing:

- The same virtual address in two programs points to **completely different** physical memory.
- Two different virtual addresses can point to the **same** physical memory — that's how one copy of libc in RAM gets shared by hundreds of programs.
- A virtual address might point to **nothing yet** — swapped to disk, or a file not read in yet. Touching it triggers a **page fault** and the kernel fixes it up (or kills you with a segfault).
- Virtual space is far bigger than your RAM. A 64-bit process gets 128 TB of address space on a laptop with 16 GB installed. `malloc` succeeding tells you almost nothing about free memory — Linux hands out addresses freely and only finds real RAM when you actually write to it.

> **Analogy:** Everyone in the office has a desk labelled "Desk 1." Reception (the MMU) knows that *your* Desk 1 is on floor 3 and *hers* is on floor 7. You both say "Desk 1" and never learn the real location. And some desks don't exist until you actually try to sit down.

Three things to keep separate:

| Term | Meaning |
|---|---|
| **Virtual address space** | The map a program sees |
| **Physical address space** | Actual RAM chips and device registers |
| **Page tables** | The per-program translation between them |

### Where kernel space fits

**Kernel space** and **userspace** are two *regions of the same virtual address space*, separated by that supervisor flag in the page tables.

- On x86_64 the usual split is 128 TB user / 128 TB kernel.
- Each program gets its **own** user region.
- There is only **one** kernel region, mapped into every program identically.

That last point is why a syscall is relatively cheap — the kernel's code is *already mapped*, so entering it doesn't require rebuilding the memory map. Compare that to switching to a *different program*, which does require swapping page tables and is much more expensive.

(Since the Meltdown vulnerability, Linux uses **KPTI**, which stops mapping most kernel pages during ring 3 execution. This made syscalls noticeably slower — and is a big reason mechanisms that avoid syscalls entirely, like **vDSO** and **io_uring**, matter.)

### Are there other "spaces"?

Yes, and they sit *below* the kernel in privilege:

| Level | Name | Who runs there |
|---|---|---|
| Ring 3 / EL0 | Userspace | Your programs |
| Ring 0 / EL1 | Kernel space | The OS kernel |
| "Ring −1" / EL2 | Hypervisor | KVM, Hyper-V, ESXi |
| EL3 | Secure world | ARM TrustZone / TEE |
| "Ring −2" | **SMM** (System Management Mode) | Firmware — invisible to the OS |

This is why firmware-level malware is so hard to deal with: it lives beneath the layer your antivirus runs in, and the kernel cannot see or intercept it.

---

## 4. How programs talk to the kernel

### Syscalls — the front door

A **syscall** is the only sanctioned way to request kernel services:

1. Your code calls `read()` in **libc**
2. libc puts the syscall number (0 for `read`) and arguments into CPU registers
3. libc executes the `syscall` instruction
4. CPU switches to ring 0, jumps to the kernel's fixed handler
5. Kernel checks permissions, does the work
6. CPU returns to ring 3 with the result

There are roughly 350–450 syscalls depending on architecture. Run `strace ls` to watch every one a program makes.

This boundary is where **seccomp** filtering lives, and where most security monitoring is done — because *everything* a program does that matters has to cross it.

### The other paths

Syscalls are the *control* path, but not the only channel:

- **`/proc` and `/sys`** — fake filesystems exposing kernel state as readable files. `cat /proc/cpuinfo`, `cat /proc/interrupts`.
- **`ioctl`** — a catch-all "do this device-specific thing" call on an open file.
- **Netlink sockets** — how `ip`, `nftables` and `auditd` talk to the kernel.
- **eBPF** — load a small, verified program that runs *inside* the kernel at chosen **hook** points.
- **Signals** — the kernel's way of poking a program (SIGTERM, SIGSEGV).
- **Shared memory (`mmap`)** — map memory into your address space, then read and write it with **no ring transition at all**.

That last one matters more each year. **vDSO** is a kernel page mapped into every program, so `clock_gettime()` usually never enters the kernel. **io_uring** uses shared ring buffers so you can submit thousands of I/O operations with one syscall or none.

> **Analogy:** A syscall is queuing at the bar. `mmap` is management handing you your own tap.

---

## 5. Linux specifically

### Monolithic, but modular

All of Linux — drivers, filesystems, network stack — runs in one shared kernel address space at ring 0.

**Modules** (`.ko` files, loaded with `modprobe`) let you add and remove code at runtime, but they run in that *same* privileged space. This is why a buggy driver panics the whole machine, and why malicious kernel modules are such a serious class of rootkit.

Compare the alternatives:

| Design | Examples | Trade-off |
|---|---|---|
| **Monolithic** | Linux | Fast; one bug can kill everything |
| **Microkernel** | seL4, QNX, MINIX | Drivers run as normal programs; robust and verifiable, but more overhead |
| **Hybrid** | Windows NT, macOS XNU | Microkernel-ish design with services pulled back in for speed |

### Other properties worth knowing

- **GPLv2**, roughly 40 million lines, most of it in `drivers/`
- **Stable userspace ABI** — a binary from 2005 still runs today. This is a hard guarantee.
- **No stable in-kernel ABI** — internal interfaces change freely between versions. That's why out-of-tree drivers (NVIDIA) must be rebuilt for every kernel, which is what DKMS automates.

### "Linux" is only the kernel

A distribution adds everything else: bootloader (GRUB), init system (systemd), **libc** (glibc or musl), shell and coreutils, display stack (Wayland/X11), package manager, daemons.

So `OS ≈ kernel + userspace` is fair for everyday speech. But note it's not a clean split of one product — the kernel/userspace line is a *privilege boundary*, while "distribution" is a *packaging* decision. Different kinds of line.

---

## 6. Namespaces and containers

### What a namespace is

A **namespace** is a kernel object that gives a group of processes a private version of something normally global.

The classic example: inside a `net` namespace, `ip addr` shows only *that* namespace's network interfaces. Its port 80 has nothing to do with the host's port 80.

Eight types exist:

| Namespace | Gives you your own... |
|---|---|
| `mnt` | Filesystem mounts and view |
| `uts` | Hostname |
| `ipc` | Shared memory and message queues |
| `pid` | Process IDs (your first process becomes PID 1) |
| `net` | Interfaces, IPs, routes, ports, firewall rules |
| `user` | UID/GID mapping — root inside, nobody outside |
| `cgroup` | View of the cgroup tree |
| `time` | Clock offsets |

### Namespaces are not processes

A namespace is a **data structure the kernel owns**. Processes are *attached to* namespaces — they don't *contain* or *equal* them.

Three consequences:

1. **Membership is per-process AND per-type, and mixable.** A process can share the host's `pid` and `mnt` namespaces while having its own `net` namespace. This is exactly how Kubernetes pods work — containers in a pod share a network namespace so they can reach each other on `localhost`, but keep separate filesystems.
2. **A namespace can outlive its processes.** If something pins it (a bind-mount under `/var/run/netns/`, or an open file descriptor), the namespace survives with nothing running in it. That's why `ip netns exec` works on an empty namespace.
3. **Some nest, some are flat.** `pid` and `user` form a tree — a process has a *different PID* in each ancestor namespace, and the parent can see into the child. `net` is flat, with no containment.

You can inspect membership directly:

```
$ ls -l /proc/self/ns/
net -> 'net:[4026531840]'
pid -> 'pid:[4026531836]'
```

Those numbers *are* the identity. Same number = same namespace = not isolated from each other.

Tools: `lsns` lists them, `unshare` creates them, `nsenter -t <pid> -n` drops you into one.

### Containers are not a kernel thing

**The kernel has no idea containers exist.** A container is a userspace assembly of existing kernel features:

| Ingredient | Provides |
|---|---|
| **Namespaces** | Isolation — a separate view |
| **cgroups** | Limits — CPU, memory, I/O ceilings |
| **Capabilities / seccomp / LSM** | Reduced privilege |
| **overlayfs** | Layered images |

Docker and containerd just glue those together. This is why "container escape" is usually just ordinary kernel privilege escalation — there's no container wall to break, only the kernel's normal boundaries.

User namespaces in particular have a long CVE history, because they let an unprivileged user reach kernel code that was written assuming the caller was genuinely root.

> **Analogy:** A container is like a themed private room in the club. The walls are just partitions management put up. If you can pick the lock on the *building's* electrical panel, the partition never mattered.
