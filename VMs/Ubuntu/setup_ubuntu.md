# VirtualBox

## Tab 1 - Name and Operating System

* In `Name`, put something recognizable like `Test`.
* The default folder for storing VM-related data on Windows is `C:\Users\<username>\VirtualBox VMs`.
* In `ISO Image`: Supposing that we have downloaded `Ubuntu 24.04` ISO image under the Windows default download location (`Downloads`), simply select: `C:\Users\<username>\Downloads\ubuntu24_04.iso`.
* By selecting the `ISO` image of the VM, some other fields are automatically filled: `Type` = `Linux`, `Subtype` = `Ubuntu` and `Version` = `Ubuntu (64-bit)`.
* Leave the field `Skil Unattended Istllation` unselected.

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

# After the first VM's reboot


