Both are userspace processes. The difference you're sensing is real, but it's not the kernel/userspace line.

## The two terms

**"Userspace process"** is precise: any process running at ring 3, in its own address space, that has to use syscalls. This is a hardware-and-kernel fact about it.

**"User process"** is ambiguous and depends on who's talking:

- In OS textbooks it usually just means "userspace process," as the opposite of kernel code.
- In sysadmin conversation it usually means "process belonging to a logged-in human," as opposed to a system daemon.

So when someone says "user process," check which contrast they're drawing. The word "userspace" never has that ambiguity.

## The actual kernel/userspace line

The thing genuinely on the other side of the boundary is **kernel threads**. They appear in `ps` in square brackets:

```
$ ps -eo pid,ppid,comm | head
    1     0 systemd
    2     0 kthreadd
    3     2 rcu_gp
   14     2 ksoftirqd/0
   16     2 kworker/0:1
```

Those run *in ring 0*, have no user address space at all, and never make syscalls (they call kernel functions directly). `ksoftirqd` handles deferred interrupt work; `kworker` runs queued kernel tasks. You can spot them because their `/proc/<pid>/cmdline` is empty and their parent is PID 2 (`kthreadd`).

Everything else on the machine — NetworkManager, VSCode, sshd, systemd itself, your shell — is a userspace process.

## What actually differs between NetworkManager and VSCode

| | NetworkManager | VSCode |
|---|---|---|
| Ring | 3 | 3 |
| UID | 0 (root) | 1000 (you) |
| Started by | systemd (PID 1) | your desktop session |
| Lifetime | boot → shutdown | while you have it open |
| Interface | D-Bus, no GUI | window on your screen |
| systemd slice | `system.slice` | `user.slice` |

Four distinctions stacked on top of each other, none of which is the privilege ring:

1. **Daemon vs interactive app** — background service with no terminal, vs something with a window.
2. **Root vs unprivileged** — but remember, root is still ring 3. NetworkManager can reconfigure your network because it holds `CAP_NET_ADMIN` and the kernel says yes to its netlink requests, not because it's "more inside" the kernel.
3. **System-managed vs session-managed** — this is where modern Linux gives "user process" a genuinely precise meaning. systemd splits everything into `system.slice` (daemons) and `user.slice` (per-login-session). Check with `systemd-cgls` or:

```
$ ps -eo pid,user,comm,cgroup --no-headers | grep -E 'NetworkManager|code'
```

4. **How close they sit to hardware** — NetworkManager talks to the kernel constantly over netlink sockets to configure interfaces and routes. VSCode mostly does file I/O and draws pixels. But both are just making syscalls; NetworkManager is asking for more privileged things.

## The one that trips people up

A daemon that manages hardware *feels* like it's part of the OS core, so people assume it's kernel-side. It isn't. NetworkManager is an ordinary program that could crash and be restarted without touching the kernel — `systemctl restart NetworkManager` proves it. The code that actually moves packets lives in the kernel's network stack; NetworkManager just tells it what to do.

Same pattern elsewhere: `sshd`, `dockerd`, `systemd-udevd`, `pulseaudio` — all privileged, all essential-feeling, all plain ring 3.