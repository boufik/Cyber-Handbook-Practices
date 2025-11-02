# 1. VirtualBox

## Tab 1 - Name and Operating System

* In `Name`, put something recognizable like `Test`.
* The default folder for storing VM-related data on Windows is `C:\Users\<username>\VirtualBox VMs`.
* In `ISO Image`: Supposing that we have downloaded `Kali Linux 2025.2` ISO image under the Windows default download location (`Downloads`), simply select: `C:\Users\<username>\Downloads\kali_2025_2.iso`.
* By selecting the `ISO` image of the VM, fill in manually the other fields: `OS/Type` = `Linux`, `OS Distribution/Subtype` = `Debian` and `OS Version` = `Debian (64-bit)`.
* Leave the field `Skip Unattended Installation` unselected.

## Tab 2 - Unattended Install

In some `VirtualBox` versions, this tab may be intouchable, so leave the fields to their default values. In case you can play with the values:

* Put your username and password.
* `Hostname` field is usually filled in automatically, taking the value of the `Name` we defined in the previous tab, here `Test`.
* `Domain Name` is usually taken the value `myguest.virtualbox.org`.

## Tab 3 - Hardware

* Put whatever value you want in `Base Memory` (ideally, higher than `2048 MB = 2 GB`) and `Processors` (ideally, higher than 2). Make sure that sliders stay in the green color area.
* Leave the field `Enable EFI` unselected.

## Tab 4 - Hard Disk

* The `Hard Disk File Location and Size` should look like this: `C:\Users\thoma\VirtualBox VMs\Test\Test.vdi`.
* The first option `Create a Virtual Hard Disk Now` is usually automatically selected. Leave it this way. Put a value higher than `20 GB` in your VM.
* Finally, leave the field `Pre-allocate Full Size` unselected. If we select it, then the size of the VM storage will be fixed and will not be able to increase to fit our needs. We need dynamic space allocation.


# 2. Start the VM for the first time

## 2a. Loading additional components

After pressing `Finish`, the configuration of our Kali VM has been completed, so we may need to start it manually. This allows us to configure some extra settings in prior to our first VM boot. Right-click in the VM using the GUI of VirtualBox and then press `Settings`.

* In the `Display` tab, set the `Video Memory` to the highest value (typically `128 MB`) Also, we can select `Enable 3D acceleration`, but this is optional.
* If we want our VM to automatically take an IP in the range of `192.168.0.0/16`, we need to go to the `Network` tab and change the value to `Bridged Adapter`. The `Name` will be in this form `Realtek ____CE Wireless LAN 802.11__ PCI NIC` or `Realtek Gaming ____ Family Controller`, which is the NIC card.
* In any case, we can always set the `Shared Clipboard` or `Drag'n'Drop` to `Bidirectional` instead of the default value of `Disabled`. We can find these settings under the `Advanced` tab of `General`.

Manually start the VM. Press `Graphical install` and the installation will begin shortly. At this point, you only need to select your language and region. After this, you will see something like this:

![Kali First Packages](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_first.png)

## 2b. Installing the base system

The next window will prompt you to:

* Put the `Hostname` of this VM - You can either leave the default `kali` option or put something more specific or meaningful for you.
* For `Domain name`, you can leave it completely empty.
* In the next tabs, determine your username and the password of this user.
* In `Partition Disks`, select `Guided - use entire disk`.
* In the following tab, the `disk to partition` will be automatically named like this: `SCSI3 (0, 0, 0) (sda) - ___ GB ATA VBOX HARDDISK`. Press `Continue`.
* Press `All files in one partition (recommended for new users)` and `Finish partitioning and write changes to disk`.
* In the question `Write changes to disks?` --> Press `Yes`.
* Then, some minutes will pass due to the installation of the base system.

![Kali Installation of base system](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_base_install.png)

## 2c. Select and install software

* The next tab refers to the software selection process. First, we need to choose which desktop environment we will use (imagine desktop environment as a Kali Linux "skin"). The available options are `Xfce` (checked by default), `Gnome` and `KDE plasma`. We can stick with `Xfce`, which is lightweight.
* The last 3 choices are about Kali Linux tools. Let them checked, because we may need some of these tools in the future.

The desktop installation is expected to last about 15 minutes.

![Kali Installation of SW - Desktop environment and tools](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_SW_install.png)

## 2d. Boot Loader

* In the question `Install the GRUB boot loader to your primary drive?`, select `Yes`.
* Then, choose the option beginning with `/dev/sda` for the boot loader installation.

![Kali Installation of SW - Desktop environment and tools](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_finish.png)

Finally, press `Continue` to reboot.



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
