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



# 3. After the first VM's reboot

In case you installed the `Xfce` desktop environment, both username and password are required to log in. If you chose the `Gnome` installation, Kali prompts you to only fill in the password for the selected user.

## 3a. Update and upgrade

After the reboot, we need to update and upgrade our Kali system:

```
sudo apt update
sudo apt upgrade -y
```

The  upgrade of the system may last about 15 minutes.

![Kali - Update and Upgrade](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_upgrade.png)

Once it's done, `reboot` the system.

## 3b. Install Kernel Headers

After the reboot, type this command to install the necessary Linux kernel headers:

```
sudo apt-get install linux-headers-$(uname -r)
```

## 3c. Install Guest Additions

In the navigation bar of VM, click on `Devices` and then `Insert Guest Additions CD image`. After this mount, a file beginning with `VBox_GAs` will appear in the filesystem, or it will have been installed in Desktop.

![Kali - Update and Upgrade](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_guest_additions.png)

Open this folder with the CD icon and **copy everything** (both folders and files) inside it. Then, create a folder named `GuestAdditions` under the `Documents` directory. Paste all copied folders and files inside the newly created folder. Now, the `~/Documents/GuestAdditions` folder contains anything is inside the file beginning with `VBox_GAs`.

If we type, `ls *run`, we will detect one or two scripts with the `.run` extension. We only care about the file `VBoxLinuxAdditions.run`. Change the permissions of this file by running the command `chmod 777` and then, execute the package:

```
sudo chmod 777 VBoxLinuxAdditions.run
sudo ./VBoxLinuxAdditions.run
```

![Kali - Install Guest Additions](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_execute_run.png)

This will take about a minute to run after typing `yes` to the terminal prompt. Then, restart again your VM by typing `reboot` in order for these changes to be applied.



# 4. Install Software

## 4a. Pre-installed packages

After the restart, we can make a snapshot of our machine to be more safe. For any package we install, we can use the `sudo apt install` command (optionally with the flag `-y`), and then we can verify if the software is installed by writing a command like `<package_name> --version` or `<package_name> -v`.

By default, Kali comes with some pre-installed software and tools. Besides, we selected such a choice during the installation process. We can verify that `python3`, `pip`, `pip3`, `git` and `curl` are already installed.

## 4b. Install `docker`

As stated in the official page of Kali Linux about Docker (`https://www.kali.org/docs/containers/installing-docker-on-kali/`), Kali Linux has already a package named `docker`, so we need to install `docker-ce` from Docker repository. Run the command:

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list
```
Terminal will print this: `deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable`

Then, import the `gpg` key:

```
curl -fsSL https://download.docker.com/linux/debian/gpg |
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Finally, install the latest version of `docker-ce`:

```
sudo apt update
```
```
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

The output in the console should look like this:

![Kali - Docker](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_docker.png)

If all things were done properly, you can now see a Docker version like `28.5.1`, when typing the command"

```
docker --version
```

## 4c. Add user to the `docker` group

Sometimes, we want to execute Docker-related commands without needing to include `sudo` in every command. For this purpose, we need to create the Docker `group` and add our user to the group:

```
sudo groupadd docker
sudo usermod -aG docker $USER
```

In order for the last command to be "registered", we need to restart our VM. So, in the next VM session, we will able to execute Docker commands without `sudo`.

## 4d. Install Google Chrome

In the Firefox browser, search for `chrome`. Click on the first link `Google Chrome - The Fast $ Secure Web Browser ...` and in the next webpage, click on `64 bit .deb (For Fedora/Ubuntu)` and press `Accept and Install`. The Debian package is downloaded under the directory `~/Downloads`. So, navigate to the current directory and verify the fact that this `.deb` package is installed there:

```
cd ~/Downloads
ls
```

Terminal should print the package `google-chrome-stable_current_amd64.deb`. First, update your system through:

```
sudo apt update
```

And finally, being under the `~/Downloads` directory, install the Debian package via the command:

```
sudo apt install ./google-chrome-stable_current_amd64.deb
```

![Kali - Chrome](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_chrome.png)

Now, Google Chrome has been successfully installed in our system and we can search for it in the applications.

## 4e. Install VS Code

As above, try to manually install the `.deb` package from a web browser by navigating to `https://code.visualstudio.com` or `https://code.visualstudio.com/Download`. Download the `.deb` package and find it under the `~/Documents` directory.

```
cd ~/Downloads
ls
```

Terminal should print a package named like `code_1.105.1-1760482543_amd64.deb`. First, update your system through:

```
sudo apt update
```

And finally, being under the `~/Downloads` directory, install the Debian package via the command:

```
sudo dpkg -i code_1.105.1-1760482543_amd64.deb
```

During the installation process, whose console output looks like this:

![Kali - Installing VSCode](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_vscode.png)

a message saying `Add Microsoft apt repository for Visual Studio Code` may appear from the system. Just press `Yes` and the installation will finish successfully.

![Kali - VSCode MS apt repo message](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Kali/Images/kali_vscode_MS_apt_repo.png)

# 5. Snapshot

Before, we turn off our VM, it is a great idea to create a snapshot of the current state.
