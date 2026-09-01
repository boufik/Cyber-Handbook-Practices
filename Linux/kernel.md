## What a kernel is

The kernel is the core program of an operating system. It loads at boot, stays resident in memory for the entire uptime, and sits between hardware and everything else. Its jobs:

- CPU scheduling (deciding which thread runs, and for how long)
- Memory management (virtual address spaces, paging, the MMU)
- Device drivers and hardware abstraction
- Filesystems (VFS and the concrete filesystems below it)
- The network stack
- IPC and synchronization primitives
- The system call interface
- Access control (UID/GID checks, capabilities, LSM hooks)

## Hardware, software, or firmware?

Software. Plain software, compiled from source and loaded from disk by the bootloader.

The confusion comes from privilege, not substance. The kernel runs at the CPU's highest privilege level (ring 0 on x86, EL1 on ARM), so it feels "close to the metal." But `/boot/vmlinuz-6.x` is just a file.

Firmware is different: code stored in non-volatile memory that ships *with* a device and usually runs before or below the OS. UEFI/BIOS, CPU microcode, NIC firmware, SSD controller firmware. The kernel talks *to* firmware (ACPI tables, UEFI runtime services, loading `linux-firmware` blobs into devices at probe time).

## What language

Mostly C, with assembly for the parts C can't express.

- **Linux**: C (gnu11 dialect since 5.18), assembly for boot entry, interrupt/syscall entry, context switching, atomics, per-arch primitives. Rust has been supported for drivers since 6.1.
- **Windows NT**: C, some C++, assembly.
- **macOS XNU**: C, C++ (IOKit drivers), assembly.

Kernel C is not normal C. There's no libc (the kernel has its own `printk`, `memcpy`, `kmalloc`), no floating point in most contexts, a fixed and tiny stack (8 or 16 KB per thread), compiled `-ffreestanding -fno-stack-protector` with a custom allocator. Code written for userspace generally won't compile.

## Is it machine code?

The source isn't; the shipped artifact is. `vmlinuz` is a compressed image containing a small decompressor stub plus the compiled binary for one specific architecture. That's why you need a different kernel build for x86_64, arm64, and riscv64: what executes is native machine code, not anything portable.

## The Linux kernel specifically

Monolithic but modular. All of it (drivers, filesystems, network stack) runs in a single kernel address space at ring 0. Loadable kernel modules (`.ko` files, via `modprobe`/`insmod`) let you add and remove code at runtime, but they run in that same privileged space, which is why a buggy module panics the whole machine and why LKM rootkits are so effective.

Compare:
- **Microkernel** (seL4, QNX, MINIX): drivers and filesystems run as userspace servers. More robust and easier to verify, more IPC overhead.
- **Hybrid** (Windows NT, XNU): microkernel-ish design with most services pulled back into kernel space for performance.

Other Linux properties worth knowing: GPLv2, roughly 40 million lines with `drivers/` accounting for most of it, a hard guarantee of userspace ABI stability (syscalls don't break), and deliberately *no* stable in-kernel ABI (out-of-tree modules must be rebuilt per version).

## The kernel is not the whole OS

A Linux distribution adds: bootloader (GRUB, systemd-boot), init and service manager (systemd), C library (glibc or musl), shell and coreutils, display stack (Wayland/X11), package manager, and the daemons. "Linux" strictly means the kernel; the rest is userspace.

## How the kernel is actually used

You don't call kernel functions. You cross the boundary through defined interfaces:

1. **System calls.** Your code calls `read()` in glibc, glibc puts the syscall number in a register and executes `syscall` (x86_64) or `svc` (ARM). The CPU switches to ring 0 and jumps to a fixed entry point. The kernel dispatches, does the work, and returns. Linux has roughly 350–450 syscalls depending on arch.
2. **Pseudo-filesystems**: `/proc` (process and kernel state), `/sys` (device and driver model), `/dev` (device nodes), `debugfs`.
3. **ioctl** on file descriptors, for driver-specific operations that don't fit a syscall.
4. **Netlink sockets**, used by `ip`, `nftables`, and auditd.
5. **eBPF**, which lets you load verified programs that run *inside* the kernel at attach points.
6. **mmap**, which maps kernel or device memory into your address space so you skip syscalls entirely afterward.

## Terminology

**Kernel space vs user space** — Two things at once: a split of the virtual address space, and a split of CPU privilege. Kernel space is one shared mapping visible only in privileged mode; each process gets its own private user address space. A fault in userspace kills a process. A fault in kernel space is an oops or a panic.

**Ring 0 / ring 3** — x86 privilege levels. Rings 1 and 2 exist but no mainstream OS uses them. ARM uses exception levels: EL0 (user), EL1 (kernel), EL2 (hypervisor), EL3 (secure monitor).

**Mode switch vs context switch** — A mode switch is user→kernel→user within the same process (a syscall). A context switch swaps to a different process entirely, including page tables. Mode switches are cheaper but got much more expensive after Meltdown mitigations (KPTI), which is why `vDSO` exists (a kernel page mapped into every process so calls like `clock_gettime` never trap) and why `io_uring` batches I/O submission.

**Preemption** — Whether the kernel can interrupt a task mid-execution. `PREEMPT_RT` (mainlined in 6.12) makes almost all of it preemptible for realtime workloads.

**Interrupt handling** — Hard IRQ handlers run with interrupts disabled and must be minimal; deferred work goes to softirqs, tasklets, or workqueues.

**Capabilities** — root's power split into ~40 discrete bits (`CAP_NET_ADMIN`, `CAP_SYS_ADMIN`, `CAP_BPF`). You can grant one without granting all of them.

**LSM** — Linux Security Modules: hook points where SELinux, AppArmor, or Landlock enforce policy after the standard DAC checks pass.

**seccomp** — Per-process syscall filtering, expressed as a BPF program.

**cgroups** — Resource accounting and limiting (CPU, memory, I/O, PIDs) for groups of processes.

## Namespaces

A namespace wraps a global kernel resource so that processes inside it see their own isolated instance of it. Eight types:

| Namespace | Isolates |
|---|---|
| `mnt` | Mount points, the filesystem view |
| `uts` | Hostname and NIS domain name |
| `ipc` | System V IPC, POSIX message queues |
| `pid` | Process IDs; the first process becomes PID 1 inside |
| `net` | Network devices, IP addresses, routing tables, ports, netfilter/nftables rules |
| `user` | UID/GID mappings; root inside, unprivileged outside |
| `cgroup` | The cgroup hierarchy root |
| `time` | `CLOCK_MONOTONIC` and `CLOCK_BOOTTIME` offsets |

You create them with `clone(CLONE_NEWNET|...)`, join existing ones with `setns()`, or detach from your current ones with `unshare()`. They're visible as symlinks under `/proc/<pid>/ns/`, and the CLI tools are `lsns`, `nsenter`, and `unshare`.

The key point: **containers are not a kernel object.** A container is a userspace construction made of namespaces (isolation) + cgroups (limits) + capabilities/seccomp/LSM (privilege reduction) + overlayfs (layered images). Docker and containerd assemble those pieces. The kernel has no idea "containers" exist, which is why container escapes are usually just ordinary kernel privilege escalation. User namespaces in particular have a long CVE history, because they hand unprivileged users a path to code that historically assumed a real root caller.

## Userspace

Everything that isn't the kernel: init, daemons, your shell, your browser. Runs at ring 3, each process in its own virtual address space, unable to touch hardware or another process's memory directly, and forced through syscalls for anything real.

Worth internalizing: **being UID 0 is not the same as being in kernel mode.** Root is a userspace concept the kernel enforces. A root process is still in ring 3 and still traps for every syscall. Getting from root to ring 0 requires a kernel vulnerability or a legitimate loading mechanism (a signed module, or a verified eBPF program). That syscall boundary is where practically all host-level detection instrumentation lives.