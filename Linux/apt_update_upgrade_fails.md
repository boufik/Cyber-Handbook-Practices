# Error

![APT error](https://github.com/boufik/Cyber-Handbook-Practices/blob/main/VMs/Images/apt_error_dependencies.png)

Whren trying to `sudo apt update && sudo apt upgrade -y`, you can sometimes take this error:

```
Installing dependencies: pyinstaller-hooks-contrib

Summary:
Upgrading: 0, Installing: 1, Removing: 0, Not Upgrading: 34
5 not fully installed or removed.
Download size: 0 B / 123 kB

Space needed: 982 kB / 6,725 MB available
Continue? [Y/n] y

(Reading database... 476999 files and directories currently installed.)
Preparing to unpack .../pyinstaller-hooks-contrib_2026.4-1_all.deb...
Unpacking pyinstaller-hooks-contrib (2026.4-1)...

dpkg: error processing archive /var/cache/apt/archives/pyinstaller-hooks-contrib_2026.4-1_all.deb (--unpack):
trying to overwrite "/usr/lib/python3/dist-packages/_pyinstaller_hooks_contrib/__init__.py', which is also in package python3-pyinstaller -hooks-contrib (2025.1-@kali1)
Errors were encountered while processing:
/var/cache/apt/archives/pyinstaller-hooks-contrib_2026.4-1_all.deb Error: Sub-process /usr/bin/dpkg returned an error code (1)
```

This isn’t a generic `apt is broken` case! The errir is very specific and fixable:
```
dpkg: trying to overwrite ... __init__.py, which is also in package python3-pyinstaller-hooks-contrib (2025.1-0kali1)
```


# Explanation

So what’s happening?
* We already have one version of `pyinstaller-hooks-contrib` installed (Kali repo version).
* `apt` is trying to install a different version `(2026.4-1)`
* Both packages contain the same files, so `dpkg` refuses to overwrite it.

This is usually caused by:
* Mixing repositories (Kali + Debian/Ubuntu or external repo) or
* A partially upgraded package set

# Clean Step-By-Step Fix

## 1. Force remove the conflicting package
```
sudo dpkg --remove --force-remove-reinstreq python3-pyinstaller-hooks-contrib
```

If that fails:
```
sudo dpkg --purge --force-all python3-pyinstaller-hooks-contrib
```

## 2. Clean package cache
```
sudo apt clean
sudo apt autoclean
```

## 3. Fix broken state
```
sudo apt --fix-broken install
```

## 4. Update again
```
sudo apt update
sudo apt upgrade
```

If it STILL fails, we need a stronger fix: a force overwrite (last resort but safe in this case):
```
sudo dpkg -i --force-overwrite /var/cache/apt/archives/pyinstaller-hooks-contrib_2026.4-1_all.deb
sudo apt --fix-broken install
```

# Error Reason

We likely had:

* Mixed repos (very common in Kali setups) or
* Manually installed a newer package

Check sources:
```
cat /etc/apt/sources.list
```

We should see the official Kali repos, so if not, that’s the root cause.

# What NOT to do
* Don’t keep retrying `apt upgrade` blindly
* Don’t ignore `dpkg` overwrite errors
* Don’t mix Debian stable + Kali rolling (breaks fast)

As a pro-level tip, to detect broken/mixed packages:
```
sudo apt policy python3-pyinstaller-hooks-contrib
```
This command shows which repo/version is being pulled.
