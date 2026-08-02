# Nmap

## Quick Scans

```bash
# Initial fast scan — default scripts + version detection
nmap -sC -sV -oN nmap/initial $IP

# Full TCP port scan
nmap -p- -sC -sV -oN nmap/full $IP

# UDP top 20
sudo nmap -sU --top-ports 20 -oN nmap/udp $IP

# Vuln scan against discovered ports
nmap --script vuln -p REDACTED $IP
```

## Speed Tuning

```bash
# Fast + aggressive
nmap -T4 --min-rate 1000 -p- $IP

# Stealth SYN scan (default with sudo, half-open)
sudo nmap -sS -p- $IP

# Connect scan (no root needed, full TCP handshake)
nmap -sT -p- $IP
```

## OS Detection

```bash
sudo nmap -O $IP
sudo nmap -A $IP   # OS + version + scripts + traceroute
```

## NSE Scripts

```bash
# Find scripts by keyword
ls /usr/share/nmap/scripts/ | grep smb
ls /usr/share/nmap/scripts/ | grep http

# Script categories: auth, broadcast, brute, default, discovery, dos, exploit, external, fuzzer, intrusive, malware, safe, version, vuln

# Run all scripts in a category
nmap --script=safe -p 445 $IP

# Run specific script with args
nmap --script http-enum -p 80 $IP
nmap --script smb-enum-shares --script-args smbusername=admin,smbpassword=pass -p 445 $IP
```

## Output Formats

| Flag | Format | Use |
|------|--------|-----|
| `-oN` | Normal | Human-readable |
| `-oG` | Grepable | Parsing with grep/awk |
| `-oX` | XML | Import into other tools |
| `-oA` | All three | Best practice |

```bash
nmap -p- -sC -sV -oA nmap/full $IP
```

## Common Gotchas

- **Filtered vs Closed**: Filtered = firewall dropping packets (no response). Closed = port responds with RST (service not running).
- **SYN vs Connect**: SYN scan (`-sS`) is default with sudo, faster, stealthier. Connect scan (`-sT`) is default without sudo.
- **UDP is slow**: Always limit ports (`--top-ports 20`) or specify known UDP services.
- **Missing services**: If initial scan misses ports, always run `-p-` full scan.
- **Version detection**: `-sV` can be noisy. Use `--version-intensity 0-9` to control.

## Workflow

1. Fast scan to get quick wins: `nmap -sC -sV -oN nmap/initial $IP`
2. Full TCP in background: `nmap -p- --min-rate 1000 -oN nmap/full $IP`
3. UDP top 20: `sudo nmap -sU --top-ports 20 -oN nmap/udp $IP`
4. Targeted vuln scan on open ports: `nmap --script vuln -p REDACTED $IP`

## See Also

- [[HTTP-80-443]] | [[SMB-139-445]] | [[DNS-53]] | [[SNMP-161]]

## From Your Boxes

> **AuthBy** (PG/Windows) — Initial fast scan only showed ports 21, 242, 3145, 3389. The detailed service scan revealed port 242 was HTTP (Apache) and port 3145 was zFTPServer admin. Without `-sV`, these would have been listed as unknown services.
> - What worked: Full service scan with `-sC -sV` on all discovered ports
> - Lesson: Non-standard ports running standard services are common. Always run `-sV` — HTTP on port 242 and FTP admin on 3145 are invisible without version detection.

> **Hokkaido** (PG/Windows) — Full port scan revealed 30+ open ports including MSSQL (1433), Kerberos (88), LDAP (389), RDP (3389), WinRM (5985). The `ms-sql-ntlm-info` and `rdp-ntlm-info` scripts both leaked the domain name `hokkaido-aerospace.com` and DC info without any credentials.
> - What worked: `nmap -sC -sV -p- $IP` plus UDP scan `sudo nmap -sU --top-ports 20 $IP`
> - Lesson: NTLM info scripts on MSSQL and RDP are free domain recon. Always run `-sC` (default scripts) on Windows targets.

> **Pandora** (HTB) — TCP scan showed only SSH (22) and HTTP (80). The real breakthrough came from UDP scan finding SNMP (161), which leaked credentials in process command lines. Without the UDP scan, the box would have been a dead end.
> - What worked: `sudo nmap -sU --top-ports 20 TARGET_IP` found SNMP on port 161
> - Lesson: NEVER skip the UDP scan. SNMP (161) is the most common UDP finding and can leak entire credential chains.

> **Sorcerer** (PG/Linux) — Full scan revealed NFS (2049), HTTP on port 7742 (nginx) and 8080 (Tomcat). The non-standard HTTP port 7742 hosted a login page with downloadable zip files containing SSH keys.
> - What worked: `nmap -p- -sC -sV $IP` discovered NFS + HTTP on unusual ports
> - Lesson: Always run full `-p-` scan. Web apps on ports like 7742, 8080, 8443, 3000 are extremely common and often more vulnerable than port 80.

> **Hutch** (PG/Windows) — Nmap's `http-webdav-scan` script detected WebDAV with PUT/DELETE/MOVE methods on IIS. This was the exploitation path — upload a webshell via WebDAV.
> - What worked: Default script scan (`-sC`) auto-detected WebDAV and listed allowed methods
> - Lesson: The `-sC` default scripts catch WebDAV, exposed .git dirs, and other low-hanging fruit automatically. Don't skip them.
