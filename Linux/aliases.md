> At first, copy `.bashrc` or `.zshrc` to another file to save your original configurations (`.bashrc.bak` or `.zshrc.bak`).

# 1. Navigation and Listing
```bash
alias ll='ls -altFh'
```

# 2. Updates
```bash
# Ubuntu
alias update='sudo apt update && sudo apt upgrade -y'
# Kali
alias update='sudo apt update && sudo apt full-upgrade -y'
```

# 3. Disk and System
```bash
alias dfh='df -h -T'
```

# 4. Ports
```bash
alias ports='ss -tulpn'
```

# 5. Search processes
```bash
alias psg='ps aux | grep -i'
```

# 6. Search history
```bash
alias h30='history | tail -30'
```
