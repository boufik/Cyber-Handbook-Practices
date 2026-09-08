# Deploy Vulnerable Services

A collection of 10 **deliberately outdated/misconfigured services**, each exposing a single port with a recognisable fingerprint, in order to act as **scan/detection targets**. 
The services split into two groups by how they are deployed:

1. **Run directly**: A published image already exists, so a single `docker run` is enough.
2. **Build first**: No suitable public image, so a `Dockerfile` is built into a local image (`<name>-image`) and then run.

> - Volume mounts (where meaningful) live under `~/dockerhosts/` directory.

---

# ⚠️ Exposure warning

Every command below publishes on `0.0.0.0` with `--restart always`, so each service comes back on **every interface on every boot**.
Several are genuinely dangerous if the host is routable beyond an isolated lab network:

- **telnet** is an *unauthenticated root shell*.
- **postfix / exim** is effectively an *open SMTP relay*.
- **ntpd** can be abused for *reflection/amplification*.

For a lab, bind these to loopback or your lab subnet instead. Prepend the host address to the port mapping: `-p 127.0.0.1:23:23`.
Only leave them on `0.0.0.0` if the VM is fully isolated.

---

# A. Deploy with `docker run` only

These four use published images and need nothing but the run command.

## A1. `nginx` on TCP 80

Web server with a recognisable version banner.
The volume is the webroot, which is safe to bind-mount empty. You just get an empty index, but nginx still starts.
**Do not** mount over `/etc/nginx`.

```bash
docker run -d --name nginx \
  -p 80:80 \
  -v ~/dockerhosts/nginx:/usr/share/nginx/html \
  --restart always \
  nginx:1.18
```

## A2. `pure-ftpd` on TCP 21 (+ passive range 30000–30009)

FTP server.
The passive-port publish and `PUBLICHOST` are the parts that most people forget.
Without them, the control channel connects but every `LIST`/download stalls.
Set `PUBLICHOST` to whatever address the client/scanner reaches the box on.

```bash
docker run -d --name pureftpd \
  -p 21:21 \
  -p 30000-30009:30000-30009 \
  -e PUBLICHOST=127.0.0.1 \
  -e FTP_USER_NAME=labuser \
  -e FTP_USER_PASS=labpass \
  -e FTP_USER_HOME=/home/labuser \
  -v ~/dockerhosts/pureftpd:/home/labuser \
  --restart always \
  stilliard/pure-ftpd:latest
```

## A3. `PostgreSQL` on TCP 5432

Old release with real CVEs.
Postgres will not boot without a password env.
A weak one is part of the setup.
If a bind-mounted data dir ever hits an ownership error on init, drop the `-v` line and let it use the image's own volume instead.

```bash
docker run -d --name postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -v ~/dockerhosts/postgres:/var/lib/postgresql/data \
  --restart always \
  postgres:9.6
```

## A4. `MongoDB` on TCP 27017

Old MongoDB version.
Note the **correct** `-v` syntax with the `:` separator.
A source path with no colon silently creates an *anonymous* volume instead of mounting your host folder.

```bash
docker run -d --name mongodb \
  -p 27017:27017 \
  -v ~/dockerhosts/mongodb:/data/db \
  --restart always \
  mongo:4.4.29
```

## A5. `Apache` HTTP Server on port 8080

A deliberately outdated version of Apache, version 2.4.25.

```bash
docker run -d --name apache -p 8080:80 -v ~/dockerhosts/apache:/var/www/html --restart always vulnerables/web-dvwa
```

---

# B. Deploy by building an image first with `docker build` + `Dockerfile`

No suitable public image exists for these services, so each is pinned to an old base and built into a local `<service>-image`.
For every service below, save the `Dockerfile` into
`~/dockerhosts/<service>/Dockerfile`, then build and run.

The general pattern is:

```bash
docker build -t <service>-image ~/dockerhosts/<service>
docker run -d --name <service> -p <host_port>:<container_port> --restart always <service>-image
```

---

## B1. `OpenSSH` on TCP 2222

Distros patch OpenSSH in place, so `apt install` on a current image gives you the *fixed* build.
Pinning an old base is what yields a known-vulnerable sshd. `ubuntu:16.04` ships OpenSSH 7.2p2 (CVE-2018-15473 username enumeration, etc.).
Host port is **2222** to avoid colliding with the host's own `sshd` on 22.

**`~/dockerhosts/openssh/Dockerfile`**

```dockerfile
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y openssh-server && mkdir -p /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
 && sed -i 's/#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
```

```bash
docker build -t openssh-image ~/dockerhosts/openssh
docker run -d --name openssh -p 2222:22 --restart always openssh-image
```

> No volume: SSH's only stateful dir is `/etc/ssh` (host keys), and bind-mounting an empty folder over it would clobber the baked-in config and keys so `sshd` won't start.

## B2. `ntpd` on UDP 123

The classic reflection/amplification service.
Note the port is **UDP**.
Leave off the `/udp` and a scanner sees nothing.

**`~/dockerhosts/ntpd/Dockerfile`**

```dockerfile
FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y ntp && rm -rf /var/lib/apt/lists/*
EXPOSE 123/udp
CMD ["ntpd", "-n", "-g"]
```

```bash
docker build -t ntpd-image ~/dockerhosts/ntpd
docker run -d --name ntpd -p 123:123/udp --restart always ntpd-image
```

> Verify with a UDP scan like `nmap -sU -p123 localhost`, since a plain TCP Nmap scan will never show it.

## B3. `Postfix` on TCP 25

SMTP server with a set banner.
Swap to **Exim** by installing `exim4-daemon-light` and
using `CMD ["exim", "-bd", "-v"]` instead.
That flips the fingerprint to `"Exim smtpd"`.
Watch for a local MTA already occupying host port 25.

**`~/dockerhosts/postfix/Dockerfile`**

```dockerfile
FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y postfix && rm -rf /var/lib/apt/lists/*
RUN postconf -e "myhostname = mail.lab.local" \
 && postconf -e "smtpd_banner = \$myhostname ESMTP Postfix"
EXPOSE 25
CMD ["postfix", "start-fg"]
```

```bash
docker build -t postfix-image ~/dockerhosts/postfix
docker run -d --name postfix -p 25:25 --restart always postfix-image
```

## B4. `Telnet` on TCP 23

Generic `telnetd` via busybox, which runs cleanly in the foreground (no `inetd` dance).

**`~/dockerhosts/telnet/Dockerfile`**

```dockerfile
FROM busybox:latest
EXPOSE 23
CMD ["telnetd", "-F", "-l", "/bin/sh"]
```

```bash
docker build -t telnet-image ~/dockerhosts/telnet
docker run -d --name telnet -p 23:23 --restart always telnet-image
```

> `-l /bin/sh` gives an **unauthenticated root shell over telnet**. This is the most "vulnerable" and the most dangerous box in the set. Loopback-bind this one for certain.

## B5. `rdp` on TCP 3389

`xrdp` gives a genuine RDP listener.
This is the heaviest box (~1 GB — it pulls a desktop environment).
It provides the RDP *fingerprint* only.
It is **xrdp on Linux, not Windows RDP**, so it will not reproduce BlueKeep (CVE-2019-0708) or other Microsoft-stack bugs. Two fixes from getting this stable, both baked into the CMD below:

- The original `service xrdp start && tail -f /var/log/xrdp/xrdp.log` **restart-looped**:
  this build logs to stdout/syslog, so that log file never existed, `tail` exited
  immediately, and the container died on repeat.
- The fix is to run the daemons in the **foreground** — `xrdp-sesman` for the session
  side, then `exec xrdp -n` (no-daemonize) as the process that keeps the container alive.

**`~/dockerhosts/rdp/Dockerfile`**

```dockerfile
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y xrdp xfce4 && rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password --gecos "" labuser && echo "labuser:labpass" | chpasswd
RUN echo "xfce4-session" > /home/labuser/.xsession
EXPOSE 3389
CMD ["bash", "-c", "xrdp-sesman && exec xrdp -n"]
```

```bash
docker build -t rdp-image ~/dockerhosts/rdp
docker run -d --name rdp -p 3389:3389 --restart always rdp-image
```

# Verification

```bash
# View the running containers
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Status}}"
# View the Docker-related IPs
docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)

# TCP fingerprints
sudo nmap -sV -p- localhost
# UDP-only scan for NTP
sudo nmap -sV -sU -p123 localhost
```

---


# Summary table

| Service    | Container   | Port         | Method       | Image                      |
|------------|-------------|--------------|--------------|----------------------------|
| nginx      | `nginx`     | 80/tcp       | run          | `nginx:1.18`               |
| pure-ftpd  | `pureftpd`  | 21 + 30000–9 | run          | `stilliard/pure-ftpd`      |
| postgres   | `postgres`  | 5432/tcp     | run          | `postgres:9.6`             |
| mongodb    | `mongodb`   | 27017/tcp    | run          | `mongo:4.4.29`
| apache    | `apache`     | 8080/tcp     | run          | `vulnerables/web-dvwa`
| |
| ssh        | `ssh`       | 2222→22/tcp  | build        | `ssh-image`                |
| ntpd       | `ntpd`      | 123/udp      | build        | `ntpd-image`               |
| postfix    | `postfix`   | 25/tcp       | build        | `postfix-image`            |
| telnet     | `telnet`    | 23/tcp       | build        | `telnet-image`             |
| rdp        | `rdp`       | 3389/tcp     | build        | `rdp-image`                |
