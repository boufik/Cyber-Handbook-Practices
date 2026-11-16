# Hypervisors: ESXi vs VirtualBox vs Hyper-V

Questions that will be answered:
* What is a hypervisor?
* How does a hypervisor differ from a VM manager?
* Why are ESXi and VirtualBox different even though both run virtual machines?


---
---


# 1. What is a Virtual Machine?

A Virtual Machine (VM) is a computer made of software.
**It has virtual CPUs, virtual RAM, a virtual disk and a virtual network card.**
A guest OS (e.g., Kali, Windows, Ubuntu) runs inside it and **believes it is running on real hardware.**
Something has to create that illusion and share the real hardware between all the VMs.
That something is the hypervisor.


---
---


# 2. Hypervisor vs VM manager

These are two different things, even though people often mix them up.

**Hypervisor:** The software that actually runs the VMs.
*It shares the physical CPU, memory, disks and network cards among the guests and keeps them isolated from each other.*

**VM manager:** The interface you use to control the hypervisor.
It is where you click `Create VM`, attach an ISO image, configure networks or take snapshots.
It does not run guest code itself.
It tells the hypervisor what to do.

| Hypervisor | Typical VM manager(s) |
|---|---|
| ESXi | ESXi Host Client (web UI), vCenter for many hosts |
| VirtualBox | VirtualBox Manager GUI, `VBoxManage` CLI |
| QEMU/KVM | virt-manager, virsh, Proxmox web UI, Cockpit |
| Hyper-V | Hyper-V Manager, Windows Admin Center |


**About VirtualBox:**
It ships both parts in *one install.*
You get the hypervisor (kernel drivers + the VM process) and the manager GUI together.
People call it a "VM manager", but it really is a hypervisor too.

**Do VirtualBox and ESXi create VMs?**
Yes, since both are hypervisors, and both come with a way to create and manage VMs.
The difference is where they sit, explained next.


# 3. Type 1 vs Type 2 hypervisors

**Type 1 (Bare-metal):**
*The hypervisor is installed directly on the hardware.*
There is no Windows or Linux underneath it.
Examples: ESXi, KVM, Hyper-V and Xen.

**Type 2 (Hosted):**
*The hypervisor is an application running on a normal OS.*
Examples: VirtualBox and VMware Workstation.

```
Type 1 (ESXi)            Type 2 (VirtualBox)
┌─────┬─────┐            ┌─────┬─────┐
│ VM  │ VM  │            │ VM  │ VM  │
├─────┴─────┤            ├─────┴─────┤
│  ESXi     │            │ VirtualBox│
├───────────┤            ├───────────┤
│ Hardware  │            │ Host OS   │
└───────────┘            ├───────────┤
                         │ Hardware  │
                         └───────────┘
```

**Type 1 hypervisor:**
Less overhead, better isolation, built to run VMs 24/7.
The trade-off is that it *takes over the whole machine.*
It is *managed remotely from a browser*, and it can be picky about supported hardware.

**Type 2 hypervisor:**
Easy, free, and you keep using your machine as a normal desktop.
The trade-off is more overhead, and *anything that happens to the host OS (updates, crashes, reboots) affects your VMs.*


---
---


# 4. How can you install something on a machine with no OS?

This is a common question after hearing `Install ESXi straight onto the server`.
If there is no OS, there is no `apt` or another package manager, so how does anything get installed?

## ESXi is an operating system, not an application

You install ESXi the same way you install Windows or Ubuntu.
Nobody installs Ubuntu with `apt`, since `apt` installs software on top of an OS that is already running.
Installing the OS itself is a lower-level process.

## A "bare-metal" machine is not completely empty

Every motherboard has **firmware** (UEFI, or BIOS on older machines) stored on a chip on the board.
It is a tiny program that runs the moment you press the power button, and it needs no OS.
It does three things:

1. It initializes the CPU, RAM and devices.
2. It looks for something bootable (USB stick, DVD, disk, network), following the boot order you set.
3. It loads that thing's first piece of code into memory and runs it.

## The installer is a temporary mini-OS

The ESXi ISO is written to a USB stick and contains a small bootable environment:
a bootloader, a kernel and an installer program.

1. You boot from the USB and the firmware hands control to it.
2. The installer runs **in RAM**, because the disk is still empty.
3. It partitions the target disk and copies the ESXi system files onto it.
4. It writes a bootloader to that disk and registers it with the firmware.
5. You reboot, remove the USB, and the firmware now boots ESXi from the disk.

This is exactly how Ubuntu, Windows and Kali installers work as well.
After installation, ESXi does have its own package-like tool for drivers and patches: `esxcli software vib install`.

## How real servers do it without a USB stick

**Out-of-band management (iDRAC, iLO, IPMI):**
A small separate computer on the server's motherboard, with its own network port.
From a browser you can see the server's screen, mount the ESXi ISO as "virtual media" and power-cycle the machine, even with no OS installed.

**PXE network boot:**
The network card's firmware requests something to boot from a server on the network and receives the installer that way.
With an answer file, the whole installation can be automated across many servers.

## The full chain

Motherboard's firmware → Boot media (USB, ISO or network) → Installer running in RAM → OS written to disk and installed → Reboot into the OS → Only now can a package manager be used


# 5. What a VM looks like?

A VM at rest is a folder of files.
On ESXi, a VM lives on a "datastore":

```
/vmfs/volumes/datastore1/kali/
  ├── kali.vmx        ← Config (CPUs, RAM, network cards)
  ├── kali.vmdk       ← Virtual disk
  ├── kali.nvram      ← The VM's own firmware settings
  └── vmware.log
```

On VirtualBox, `kali.vbox` is the VM's config and `kali.vdi` is its disk.
A running VM is a process that the hypervisor schedules and feeds with resources.
**Important:** this file model is the same in ESXi and VirtualBox, so it is not what makes them different.
Also note the wording.
A hypervisor's job is not to *install* VMs but to *run* them.
Creating a VM takes a minute.
The real work is running many VMs continuously:
scheduling their virtual CPUs on real cores, handing out RAM, and passing their disk and network traffic to the real hardware.


---
---


# 6. VirtualBox vs ESXi

**VirtualBox:**
Windows or Linux controls the hardware.
The host OS kernel decides who gets CPU time and memory, and the host's drivers talk to the network card and disks.
VirtualBox is one program among many inside that OS.
A packet from your Kali VM travels roughly:
`VM → VirtualBox → Host OS network stack → Host driver → Network card`.
Your VMs compete with the browser, the antivirus, Windows Update and everything else in the host machine.

**ESXi:**
There is no general-purpose OS in between.
The ESXi kernel, the `VMkernel`, schedules the VMs directly, manages RAM directly and has its own drivers for network cards and storage.
The path from VM to hardware is shorter, and nothing else competes for resources.

| | VirtualBox | ESXi |
|---|---|---|
| If the host reboots or crashes | A Windows Update reboot stops all your VMs | Nothing else runs there to cause that |
| What lies under your VMs | A full desktop OS | A small, purpose-built kernel |
| Disk and network I/O | Passes through the host OS, more overhead | More direct, less overhead |
| Networking | bridged, NAT, host-only adapters | Virtual switches, VLANs, port groups |
| Clustering and live migration | No | Yes, with vCenter |
| Machine still usable as a desktop | Yes | No, it is headless |

**A common misunderstanding:**
For pure CPU work, the gap is smaller than people expect.
Both use the CPU's hardware virtualization features (`Intel VT-x` / `AMD-V`), so *guest instructions run directly on the real cores in both cases.*
The difference mostly shows up in: disk, network I/O, scheduling under load, and reliability.

> **VirtualBox runs VMs as guests of your OS.**
> **ESXi is an OS whose only job is running VMs.**


---
---


# 7. ESXi: OS or hypervisor?

ESXi is both.
**`Hypervisor` is a role** that implies creating and running VMs.
**`OS` is a software** that boots on the hardware and controls it.
**ESXi is an OS whose only role is being a hypervisor.**

## Is every Type 1 hypervisor an OS?

A Type 1 hypervisor boots first and controls the CPU and memory directly.
To do that, it must do OS-kernel work: scheduling, memory management, handling interrupts.
So, **every Type 1 hypervisor is at least an OS kernel**.
What varies is how much more than a kernel it is, mainly who handles the device drivers.
There are three designs.

## Design 1: Monolithic (ESXi)

The `VMkernel` does everything itself: scheduling, memory, drivers, storage and networking.
**It is one complete, self-contained OS, specialized for running VMs.**

## Design 2: Microkernel (Hyper-V, Xen)

The hypervisor is deliberately tiny and handles mainly CPU, memory and isolation.
It has no drivers for network cards or disks.
Those live in a special privileged VM:

- In Hyper-V this is the **root partition**, which is a normal Windows installation.
- In Xen this is **dom0**, usually Linux.

So, **these hypervisors are thinner than a typical OS kernel, and they need that privileged VM to function.**

> **The Hyper-V twist:**
> When you enable Hyper-V on Windows 11 or Windows Server, the hypervisor loads first at boot and takes over the hardware.
> The Windows you are using then starts on top of it as the root partition, which is technically a privileged VM.
> It still feels like a normal desktop, but it is no longer at the bottom of the stack.
> This is why Hyper-V counts as Type 1 even though it looks like a Windows feature.
> It is also why VirtualBox and Hyper-V can conflict.
> With Hyper-V enabled, VirtualBox has to run through Hyper-V's interface instead of using the hardware directly.

## Design 3: Kernel module (KVM)

You take a general-purpose OS like Linux and load a module that adds hypervisor abilities to its kernel.
**The OS becomes the hypervisor and can still run normal applications.**
Proxmox VE works this way:
`Proxmox = Debian Linux + KVM + a web UI`

## Comparison

| | Is the hypervisor a full OS on its own? | Who drives network cards and disks? |
|---|---|---|
| ESXi | Yes, a specialized one | The `VMkernel` itself |
| KVM / Proxmox | Yes, a general-purpose one like Linux | The Linux kernel |
| Hyper-V | No, a thin layer | Windows in the **root partition** |
| Xen | No, a thin layer | Linux in **dom0** |

> **A Type 1 hypervisor is always at least an OS kernel, and sometimes the full OS too.**
> - A full OS: ESXi (specialized) and KVM (the hypervisor is Linux itself).
> - Only a thin kernel: Hyper-V and Xen.


---
---


# 8. FAQ

**(1) Is a hypervisor different from a VM manager?**
Yes.
The hypervisor runs the VMs.
The manager is the interface you use to control the hypervisor.

**(2) Can both VirtualBox and ESXi create VMs?**
Yes.
Both are hypervisors with their own management tools.
VirtualBox is a hypervisor type 2 (hosted), while ESXi is a hypervisor type 1 (bare-metal).

**(3) How do you install ESXi on hardware with no OS?**
The motherboard firmware boots an installer from USB, ISO or the network.
The installer runs in RAM and writes ESXi image to disk, just like installing Windows or Ubuntu.

**(4) Is ESXi an OS whose files are the VMs?**
Roughly yes.
VMs are folders of files on its datastore.
But VirtualBox stores VMs as files too, so that is not the difference.

**(5) Why is ESXi different from VirtualBox?**
Because of who controls the hardware.
With VirtualBox (type 2), a desktop OS sits between the VMs and the hardware.
With ESXi (type 1), the hypervisor is the OS and controls the hardware directly.

**(6) Is ESXi an OS or a hypervisor?**
Both.
ESXi is an OS with a single role, which is only being a hypervisor.

**(7) Is every Type 1 hypervisor an OS?**
Every Type 1 hypervisor is at least an OS kernel.
Some are full OSes (ESXi and KVM / Proxmox), while others are thin kernels that rely on a privileged VM for drivers (Hyper-V and Xen).
