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
To get a **200 OK (not a 403)**, the webroot must contain an `index.html` file.
nginx serves from `/usr/share/nginx/html`.
If you bind-mount an **empty** host directory over that path, you hide the image's built-in default page and nginx returns **403 Forbidden**.
It has no index to serve and directory listing is off.
So, create the host dir and drop an index file in it *before* running.

```bash
# 1. Prepare the webroot with at least an index file
mkdir -p ~/dockerhosts/nginx
echo '<h1>Thomas Boufikos Nginx Lab</h1>' > ~/dockerhosts/nginx/index.html

# 2. Run, while mounting the NON-EMPTY dir at the correct webroot path
docker run -d --name nginx \
  -p 80:80 \
  -v ~/dockerhosts/nginx:/usr/share/nginx/html \
  --restart always \
  nginx:1.10.1

# 3. Verify and expect "HTTP/1.1 200 OK" and "Server: nginx/1.10.1"
curl -sI http://<Docker_Container_IP>
```

*Note:* **Do not** mount over `/etc/nginx`, since that shadows the config and nginx won't start.

> **Note on the 403 vs 200 behaviour (and a misleading "fix").**
> An empty bind-mount over the webroot → **403**. Two ways people accidentally get a 200:
> - Run **without** the `-v` at all. nginx serves its own baked-in default page
>   (a `Last-Modified` date years in the past is the tell that it's the image's page, not yours).
> - **Misspell the mount target** (e.g. `/usr/share/ngingx/html`).
>   The volume then lands on a path nginx never reads, the real webroot is left untouched, and the default page survives → 200.
>   This *looks* like it fixed things but is a dead mount:
>   files you put in that host dir are never served. Always mount the correctly-spelled `/usr/share/nginx/html`.
>
> For a **fingerprint target**, note the 403 response still leaks `Server: nginx/1.10.1`, so a scanner reads the version regardless of status code.
>  The index file only matters if you want the page to actually load.

> **Version caveat.** Very old tags (roughly pre-2017, e.g. `nginx:1.10.0`) were published as schema-1 manifests,
> which current Docker Engine (25+) refuses with a
> "manifest version … schema 1 support has been removed" error.
> Versions `1.10.1` and `1.10.3` still pull. If a tag is rejected, step forward until one works (`1.12` → `1.14` → `1.18`).

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

## B3. `Postfix`

SMTP server on Debian 8 "Jessie" (Postfix 2.11.3). Three details make this container work, and it is useless without all three:

1. **Jessie, not older.** Squeeze and Wheezy carry glibc 2.11/2.13 and apt 0.8, which segfault on a modern host (`Method http has died unexpectedly`).
   Jessie's glibc 2.19 and apt 1.0.9 are fine. Bullseye would work too but ships Postfix 3.5, which is too recent to be interesting.
2. **The debconf preseed.** Without it, `postfix` installs under `DEBIAN_FRONTEND=noninteractive` as "No configuration" 
   and no daemon ever starts. The build still succeeds, so the failure is silent.
3. **Two parenthesised groups in the banner.** nmap only extracts a Postfix version from a banner shaped `... ESMTP Postfix (version) (distro)`.
   With a single group it falls through to a prefix-only match and reports `Postfix smtpd` with an empty version and an unversioned CPE.
   Keep `(Debian)` plain. `(Debian/GNU)` contains a slash, which falls outside nmap's character class and drops you back to the versionless match.
   `postfix start-fg` does not exist before Postfix 3.0, so 2.11.3 must start the daemon and hold the foreground separately.

**`~/dockerhosts/postfix/Dockerfile`**

```dockerfile
FROM debian/eol:jessie
ENV DEBIAN_FRONTEND=noninteractive

# Jessie is archived: pin apt at archive.debian.org, skip the expired
# Valid-Until check and accept unsigned packages.
RUN set -eux; \
    echo 'deb http://archive.debian.org/debian jessie main contrib non-free' > /etc/apt/sources.list; \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid; \
    echo 'APT::Get::AllowUnauthenticated "true";' > /etc/apt/apt.conf.d/99allow-unauth; \
    apt-get update

RUN set -eux; \
    echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections; \
    echo "postfix postfix/mailname string mail.lab.local"        | debconf-set-selections; \
    apt-get install -y --force-yes postfix rsyslog; \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    postconf -e 'smtpd_banner = $myhostname ESMTP $mail_name ($mail_version) (Debian)'; \
    postconf -e 'myhostname = mail.lab.local'; \
    postconf -e 'mydestination = mail.lab.local, localhost'; \
    postconf -e 'inet_interfaces = all'; \
    postconf -e 'inet_protocols = ipv4'; \
    postconf -e 'mynetworks = 0.0.0.0/0'; \
    newaliases; \
    touch /var/log/mail.log

EXPOSE 25
CMD ["/bin/sh","-c","rsyslogd; postfix start; sleep 3; postfix status; exec tail -f /var/log/mail.log"]
```

```bash
docker build -t postfix-image ~/dockerhosts/postfix
docker run -d --name postfix --restart always postfix-image
```

Swap to **Exim** by installing `exim4-daemon-light` and using `CMD ["exim", "-bd", "-v"]`.
That flips the fingerprint to `"Exim smtpd"`, and Exim advertises its version in the banner by default, so no `smtpd_banner` equivalent is needed.
No `-p 25:25` here: the scans target container IPs directly, and publishing the port collides with any MTA already on the host.

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

## B6 `exim`

Unlike `Postfix` which needs special tricks to advertise its version in its banner, `exim` does it by default:

```dockerfile
FROM debian/eol:jessie
ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    echo 'deb http://archive.debian.org/debian jessie main' > /etc/apt/sources.list; \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid; \
    echo 'APT::Get::AllowUnauthenticated "true";' > /etc/apt/apt.conf.d/99allow-unauth; \
    apt-get update; \
    apt-get install -y --force-yes exim4-daemon-light; \
    rm -rf /var/lib/apt/lists/*

# Debian's exim4 binds to 127.0.0.1 only by default. Empty dc_local_interfaces
# means all interfaces -- without this the container runs but the port is shut.
RUN set -eux; \
    echo 'mail.lab.local' > /etc/mailname; \
    printf "%s\n" \
      "dc_eximconfig_configtype='internet'" \
      "dc_other_hostnames='mail.lab.local'" \
      "dc_local_interfaces=''" \
      "dc_readhost=''" \
      "dc_relay_domains=''" \
      "dc_minimaldns='false'" \
      "dc_relay_nets='0.0.0.0/0'" \
      "dc_smarthost=''" \
      "CFILEMODE='644'" \
      "dc_use_split_config='false'" \
      "dc_hide_mailname=''" \
      "dc_mailname_in_oh='true'" \
      "dc_localdelivery='mail_spool'" \
      > /etc/exim4/update-exim4.conf.conf; \
    update-exim4.conf

EXPOSE 25
CMD ["/usr/sbin/exim4", "-bd", "-v"]
```

```bash
docker build -t exim-image ~/dockerhosts/exim
docker run -d --name exim --restart always exim-image
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
| exim       | `exim`      | 25/tcp       | build        | `exim-image`               |
