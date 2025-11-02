# 1. VirtualBox

## Tab 1 - Name and Operating System

* In `Name`, put something recognizable like `Test`.
* The default folder for storing VM-related data on Windows is `C:\Users\<username>\VirtualBox VMs`.
* In `ISO Image`: Supposing that we have downloaded `Ubuntu 24.04` ISO image under the Windows default download location (`Downloads`), simply select: `C:\Users\<username>\Downloads\ubuntu24_04.iso`.
* By selecting the `ISO` image of the VM, some other fields are automatically filled: `Type` = `Linux`, `Subtype` = `Ubuntu` and `Version` = `Ubuntu (64-bit)`.
* Leave the field `Skip Unattended Installation` unselected.

## Tab 2 - Unattended Install

* Put your username and password - you need to remember them, as these will be your credentials during the first reboot of the VM.
* `Hostname` field is usually filled in automatically, taking the value of the `Name` we defined in the previous tab, here `Test`.
* `Domain Name` is usually taken the value `myguest.virtualbox.org`.

## Tab 3 - Hardware

* Put whatever value you want in `Base Memory` (ideally, higher than `2048 MB = 2 GB`) and `Processors` (ideally, higher than 2).
* Leave the field `Enable EFI` unselected.

## Tab 4 - Hard Disk

* The `Hard Disk File Location and Size` should look like this: `C:\Users\thoma\VirtualBox VMs\Test\Test.vdi`.
* The first option `Create a Virtual Hard Disk Now` is usually automatically selected. Leave it this way. Put a value higher than `20 GB` in your VM.
* Finally, leave the field `Pre-allocate Full Size` unselected. If we select it, then the size of the VM storage will be fixed and will not be able to increase to fit our needs. We need dynamic space allocation.

## Next Steps

After pressing `Finish`, the VM should automatically start running and downloading the necessary packages. If we do not see anything for some time at the beginning, we can always terminate the VM session. Then, we can configure its settings. Right-click in the VM using the GUI of VirtualBox and then press `Settings`. In the `Display` tab, set the `Video Memory` to the highest value (typically `128 MB`). Also, if we want our VM to automatically take an IP in the range of `192.168.0.0/16`, we need to go to the `Network` tab and change the value to `Bridged Adapter`. The `Name` will be in this form `Realtek ____CE Wireless LAN 802.11__ PCI NIC`, which is the NIC card.

Now, if we had terminated our VM previously, we need to restart it. Press `Try or install Ubuntu` and the installation will begin shortly. If extra prompts appear next, press `Install` and `Erase disk and install Ubuntu` (do not worry - the `Erase` option does not refer to the original disk of our host machine). This may take some time. In any case, the installation process should look like this:

![Ubuntu Downloads](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Ubuntu/Images/ub24_being_installed.png)

After the installation is complete, Ubuntu prompts us to fill in some other fields like username, password, computer name and region. Leave the field `Require my password to log in` **selected**. Then, Ubuntu instructs us to restart our VM, so we ned to follow this instruction.

# 2. After the first VM's reboot

## 2a. Update and upgrade
After the reboot, Ubuntu asks us some other things like reporting problems, diagnostics, e.t.c. Then, we need to update and upgrade our system using the commands:

```
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential linux-headers-$(uname -r)
```

The system has been updated by installing the essential build tools and kernel headers on Ubuntu (Debian-based).

![Ubuntu Downloads](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Ubuntu/Images/ub24_apt_upgrade.png)

## 2b. Install Guest Additions

In the navigation bar of VM, click on `Devices` and then `Insert Guest Additions CD image`. By doing so, in the left sidebar of Ubuntu, a logo with a disk appears. Clicking the disk logo opens a directory in the form `/media/<username>/VBox_GAs_7.1.12`. Inside, we can find several folders and files, but we only care about the `autorun.sh` file though. Right-click this file and select `Run as a program`. Insert your password and then the script runs. Among the output lines of the running shell are:
```
Verifying archive integrity... 100%     MD5 checksums are OK. All good.
Uncompressing VirtualBox 7.1.12 Guest Additions for Linux    100%
VirualBox Guest Additions installer
VirualBox Guest Additions: Starting
VirualBox Guest Additions: Setting up modules
```

After the installation, we can press any key (e.g. `Enter`) in the console and then we can safely restart again our VM.

# 3. Install packages

For any package we install we can use the `sudo apt install` or `sudo snap install` command (optionally with the falg `-y`), and then we can verify if the software is installed by writing a command like `<package_name> --version` or `<package_name> -v`.

```
sudo apt install -y pip
pip --version
```
Output: `pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)`.

```
sudo apt install -y git
git --version
```
Output: `git 2.43.0`.

```
sudo apt install -y net-tools
```
Output: the command `ifconfig` should work now.

```
sudo apt install -y curl
curl --version
```
Output: `curl 8.5.0 (x86_64-pc-linux-gnu) ...`.

```
sudo snap install docker
docker --version
```
Output: `docker 28.4.0 from Canonical✅ installed`.

```
sudo apt install -y docker-compose
docker-compose --version
```
Output: `docker-compose 1.29.2, build unknown`.

Sometimes, we want to execute Docker-related commands without needing to include `sudo` in every command. For this purpose, we need to create the Docker `group` and add our user to the group:

```
sudo groupadd docker
sudo usermod -aG docker $USER
```

In order for the last command to be "registered", we need to restart our VM. So, in the next VM session, we will execute Docker commands without `sudo`.

# 4. Snapshot

Before, we turn off our VM, it is a great idea to create a snapshot of the current state.
