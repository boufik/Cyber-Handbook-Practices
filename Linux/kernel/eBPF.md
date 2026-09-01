## What it is

**eBPF is a revolutionary technology with origins in the Linux kernel that can run sandboxed programs in a privileged context such as the operating system kernel. It allows sandboxed programs to run within the operating system, which means that application developers can run eBPF programs to add additional capabilities to the operating system at runtime.**

eBPF lets you load small programs into the running Linux kernel and attach them to hook points — a syscall entry, a network packet arriving on a NIC, a function in a userspace binary — where they execute in a sandboxed VM every time that event fires. No kernel module, no reboot, no patching kernel source.

The critical property is safety. Before loading, a **verifier** statically analyses the bytecode and rejects anything it can't prove terminates and stays in bounds: no unbounded loops, no arbitrary memory access, bounded stack, limited instruction count. If it loads, it can't panic your kernel. After verification a JIT compiler translates the bytecode to native instructions, so it runs at near-native speed.

## The name

**BPF = Berkeley Packet Filter**, from McCanne & Jacobson's 1992/93 USENIX paper at Lawrence Berkeley National Laboratory. It was a tiny register VM for filtering packets in the kernel so `tcpdump` wouldn't have to copy every packet to userspace. That original design is now called **cBPF** (classic BPF) — still what `libpcap` filter expressions and `seccomp-bpf` compile down to.

**eBPF = extended BPF**: Alexei Starovoitov's 2013–14 rewrite that widened registers to 64-bit, added maps, helper calls, and many more attach points. Merged in **kernel 3.15 (June 2014)**; the `bpf()` syscall landed in **3.18 (Dec 2014)**.

Worth knowing for your writeup: the eBPF Foundation now treats "eBPF" as a standalone name rather than an acronym, since it long ago stopped being about Berkeley or packet filtering. Cite the expansion once, then move on.

## Core architecture

| Piece | Role |
|---|---|
| **Verifier** | Static safety proof; rejects unsafe programs at load time |
| **JIT** | Bytecode → native instructions |
| **Maps** | Typed key/value stores (hash, array, ring buffer, LRU, per-CPU) — the only way kernel programs share state with each other and with userspace |
| **Helpers** | A fixed, whitelisted API for kernel functions the program may call |
| **BTF + CO-RE** | BPF Type Format debug info enabling "Compile Once – Run Everywhere": one binary that relocates against different kernel struct layouts, instead of recompiling per kernel |
| **libbpf / bpftool** | The canonical loader library and CLI |

**Attach points** are the thing to internalise, because they define what's possible:

- **kprobes / kretprobes** — any kernel function (unstable ABI)
- **tracepoints** — stable, curated kernel events
- **fentry/fexit** — faster BTF-based function tracing (kernel 5.5+)
- **uprobes / USDT** — userspace functions, e.g. hooking `SSL_write` in OpenSSL to see plaintext before encryption
- **XDP** — earliest possible point in the RX path, sometimes in the NIC driver or offloaded to hardware; drop/redirect at line rate
- **tc (traffic control)** — ingress/egress after skb allocation, richer but slower than XDP
- **socket / cgroup hooks** — per-container network policy, `sockops`
- **LSM BPF** (kernel 5.7+) — attach to Linux Security Module hooks and *deny* operations, not just observe
- **perf events** — sampling profilers

## Timeline

- **1992** — BPF at LBNL, for `tcpdump`
- **2014** — eBPF merged (3.15); `bpf()` syscall (3.18)
- **2016** — XDP; Cilium and Facebook's Katran L4 load balancer appear
- **2017–18** — BTF, CO-RE, `libbpf` — portability finally solved
- **2020–21** — BPF LSM; **eBPF Foundation** founded under the Linux Foundation (Google, Meta, Microsoft, Isovalent, Netflix); eBPF for Windows announced
- **2023** — IETF **BPF Working Group** formed to standardise the ISA beyond Linux
- **2023–26** — Cilium graduates in CNCF; eBPF becomes default plumbing for Kubernetes networking and runtime security; OpenTelemetry work to integrate eBPF-based collection into the collector

## Application domains

**Networking** — Cilium (Kubernetes CNI, replaces kube-proxy/iptables), Katran, Cloudflare's DDoS mitigation (drop at XDP before the packet costs you an skb), service mesh without sidecars.

**Observability** — `bcc`, `bpftrace`, Pixie, Parca continuous profiling, Coroot, Grafana Beyla. The selling point is zero-instrumentation: you get HTTP/DB/DNS visibility without touching application code.

**Security** — this is your lane:
- **Falco** (CNCF) — syscall-level runtime threat detection with a rules DSL
- **Tetragon** (Isovalent) — observability *and* in-kernel enforcement via LSM BPF; can kill a process from kernel space rather than reacting after the fact
- **Tracee** (Aqua) — runtime detection and forensics
- **KubeArmor**, **Cilium network policy**, **seccomp-bpf**
- File integrity, cryptographic-material extraction (TLS plaintext via uprobes), container escape detection, provenance/data-flow graphs for APT investigation

**Performance** — `sched_ext` (pluggable schedulers, kernel 6.12+), storage and memory tuning.
