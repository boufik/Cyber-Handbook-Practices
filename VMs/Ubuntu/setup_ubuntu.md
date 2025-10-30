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
* Finally, leave the field `[re-allocate Full Size` unselected.

## Next Steps

After configuring all these tabs, our VM will automatically start running and downloading the necessary packages. This may take some time. In any case, the output should look like this:

![Ubuntu Downloads]()
