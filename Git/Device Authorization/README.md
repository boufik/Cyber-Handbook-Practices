# A. Prerequisites

## A1. Initial actions to verify Git is installed

```
sudo apt install git -y
git --version
```

## A2. Set up your identity

```
git config --global user.name "my_name"
git config --global user.email "my_email@example.com"
```

⚠️ About the values inside  the `""` for both `user.name` and `user.email`:
* They are NOT ABOUT REAL AUTHENTICATION - they are about our personal identity
* These values are recorded and shown in EVERY COMMIT we make
* These help GitHub and other platforms to link commits to our personal account

👉 Ideal Values:
* `user.name`: Any name we want to be displayed in the COMMIT HISTORY. It can be either our real name (`Thomas Thomas`) or our GitHub username or anything else to identify ourselves
* `user.email`: This must match to our GitHub-account associated email. If we don’t want our personal email to be exposed in commit history, GitHub provides a private noreply email like `12345678+username@users.noreply.github.com`. We can find it in GitHub under: `Settings → Emails → Keep my email address private`. If we set this as our Git email, commits still link to our profile, but don’t reveal our real email.

## 3. After filling these values, we can inspect our choices by writing:

```
git config --global user.name
git config --global user.email
```


# B. OLD METHOD

Until 2021, in order to clone our private repo from GitHub to our desired Ubuntu/Windows Host Machine, we should run:

```
git clone https://github.com/<username>/DataCamp-Git.git
```

After typing this command, the VM would instruct us to fill in the username and the password from our GitHub account. But this does NOT work now. A new method with SSH keys should be used.


# C. NEW METHOD - SSH KEY

So, now in order to connect/authenticate your machine/VM to your GitHub account, you should do this:

## C1. Go in our VM's CLI and create an SSH keys

```
which ssh-keygen		# Verify if this command is installed in Linux
ssh-keygen -t ed25519 -C "my_email@example.com"
```

After typing the command, the CLI output is:

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/linux_username/.ssh/id_ed25519)
Press Enter to accept default file location (/home/linux_username/.ssh/id_ed25519)
```

Optionally, we can set a passphrase (recommended) or we can simply leave empty by typing two `Enter` keys in the next shell prompt. After doing this, our key is generated, and the CLI prints the key fingerprint in a new line:

```
SHA256:/+.............. my_email@example.com
```

Also, the key's randomart image is also displayed.

## C2. Start the ssh-agent and add our key

```
eval "$(ssh-agent -s)"
```

CLI will print a message like: `Agent pid <number>`. Then, execute:

```
ssh-add ~/.ssh/id_ed25519
```

CLI output will be in this format:

```
Identity added: /home/linux_username/.ssh/id_ed25519 (my_email@example.com)"
```

## C3. Copy our public key and add it to GitHub

```
cat ~/.ssh/id_ed25519.pub
```

This will print one line that we need to copy in order to paste it afterwards in GitHub. The line is in this format: 

```
ssh-ed25519 <......long_random_key.......> my_email@example.com
```

We should copy the ENTIRE line.

## C4. Paste our public key in our GitHub using a browser
In GitHub, go to `Settings → SSH and GPG keys → New SSH key`. In the title section, write something like `Machine_Name_SSH_KEY`. Paste the key and then save.

## C5. Test the SSH connection from our machine/VM terminal

```
ssh -T git@github.com
```

The first time, you type this command, you will sth like this: 

```
The authenticity of host 'github.com ...' can't be established.
……………………………………………………………………………………..
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

This is super normal the first time we connect to a new host with SSH. By typing `yes`, the system will save GitHub’s fingerprint in:  `/home/linux_username/.ssh/known_hosts`. From now on, it won’t ask us again (unless the host key changes, which could indicate a man-in-the-middle attack). Finally, a greeting message will appear saying:

```
Hi <GitHub_username>! You've successfully authenticated, but GitHub does not provide shell access.
```

This means that our SSH key worked and GitHub recognized our account. The phrase `does not provide shell access` is also normal, since GitHub doesn’t give us a remote shell, it only accepts Git commands.

## C6. Clone the desired repo

After this, we can successfully `git clone` an existing GitHub repo like this:

```
git clone git@github.com:<GitHub_username>/<repo_name>.git
```

The output will be like this:

```
Cloning into '<repo_name>'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (3/3), done.
```
