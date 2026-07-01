# Fix for interrupted `apt` Process: `Ctrl`+`C` or closed terminal

Happens when you kill a running `apt update`, `apt upgrade` or `apt full-upgrade` mid-way, either by pressing **`Ctrl`+`C`** or **accidentally closing the terminal**. This leaves `dpkg` locks and possibly partially installed packages behind.




## Quick Guide

For more details, scroll down to find out the logic behind each command:
```bash
ps aux | grep apt
sudo kill -9 <PID>

sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
sudo rm /var/cache/apt/archives/lock

sudo dpkg --configure -a

sudo apt --fix-broken install

sudo apt update && sudo apt upgrade         # Ubuntu
sudo apt update && sudo apt full-upgrade    # Kali
```




## Step 1: Find and kill the stuck `apt` process

First, check what's holding the lock:

```bash
ps aux | grep apt
```

Then kill this process (replace `18762` with the PID you see):

```bash
sudo kill -9 18762
```




## Step 2: Remove leftover lock files

**If and only if the process is confirmed dead**, it is safe to run:

```bash
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
sudo rm /var/cache/apt/archives/lock
```

These lock files are created while `apt` runs.
If they linger after a crash, every subsequent `apt` command will fail with a "locked" error!




## Step 3: Repair `dpkg` (very important)

This command fixes any packages that were partially installed or left in a broken state:

```bash
sudo dpkg --configure -a
```




## Step 4: Fix broken dependencies

```bash
sudo apt --fix-broken install
```

Resolves any dependency chain issues left behind by the interrupted install.




## Step 5: Finish the `upgrade` properly

```bash
sudo apt update
sudo apt upgrade        # Ubuntu
sudo apt full-upgrade   # Kali
```

*Note: Using `upgrade` on Kali Linux can leave packages held back indefinitely. Using `full-upgrade` on Ubuntu won't break things, but it's more aggressive than usually needed.*

### Kali vs Ubuntu: Which `upgrade` command to use?

| Distro | Correct command | Why |
|--------|----------------|-----|
| **Ubuntu / Debian stable** | `sudo apt upgrade` | Stable distros shouldn't remove packages during a routine upgrade, so `upgrade` is the safer default. |
| **Kali Linux** | `sudo apt full-upgrade` | Kali is a rolling release . `full-upgrade` allows package removals needed to resolve conflicts, which is expected and safe on rolling distros. |
