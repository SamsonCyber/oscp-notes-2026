# I'm Stuck — Decision Tree

When you're spinning wheels, walk through this top-to-bottom.

---

## Can't Find an Attack Vector?

```
Did you full-port scan TCP?
├── NO → nmap -p- -sV -sC -oA full <target>
└── YES
    ├── Did you scan UDP top 100?
    │   └── NO → sudo nmap -sU --top-ports 100 -oA udp <target>
    ├── Did you try a bigger web wordlist?
    │   └── NO → gobuster dir -u http://<target> -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt
    ├── Did you check ALL versions against searchsploit?
    │   └── NO → searchsploit <service> <version>
    ├── Did you Google "<service> <version> exploit"?
    │   └── NO → Do it now. Include "RCE", "authenticated", "PoC"
    ├── Did you check for vhosts/subdomains?
    │   └── NO → gobuster vhost -u http://<target> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
    └── Did you check every port's banner/headers manually?
        └── NO → curl -v http://<target>:<port>/ and nc -nv <target> <port>
```

---

## Got Creds But Can't Use Them?

```
Try these in order:
├── Spray creds across ALL services on ALL machines
│   ├── crackmapexec smb <targets> -u <user> -p <pass>
│   ├── crackmapexec winrm <targets> -u <user> -p <pass>
│   ├── crackmapexec ssh <targets> -u <user> -p <pass>
│   ├── crackmapexec mssql <targets> -u <user> -p <pass>
│   └── hydra -l <user> -p <pass> <target> ftp
├── Try password variations
│   ├── Username as password
│   ├── Password + "1", "!", "2024", "2025"
│   └── Case variations
├── Try as hash (pass-the-hash)
│   └── crackmapexec smb <target> -u <user> -H <hash>
├── Check for password reuse in found files
│   └── grep -ri "pass\|pwd\|cred" /var/www/ /home/ /opt/
└── Try on services you haven't enumerated yet
    └── Re-run nmap on that specific target
```

---

## Have Shell But Can't PrivEsc?

```
Run automated tools AGAIN (you might have missed output):
├── Linux:
│   ├── linpeas.sh — read ALL output, especially yellow/red highlights
│   ├── sudo -l (try with found passwords too)
│   ├── find / -perm -4000 -type f 2>/dev/null (SUID)
│   ├── cat /etc/crontab && ls -la /etc/cron.*
│   ├── ls -la /opt /var/backups /tmp /dev/shm
│   ├── Check file timestamps: find / -newer /etc/passwd -not -path "/proc/*" 2>/dev/null
│   ├── ps aux — anything running as root that's unusual?
│   ├── netstat -tulnp — internal services not exposed?
│   ├── Check capabilities: getcap -r / 2>/dev/null
│   └── Password reuse: su - root with every password you've found
│
├── Windows:
│   ├── winpeas.exe — read ALL output
│   ├── whoami /all — check privileges and groups
│   ├── Check services: sc query state=all
│   ├── Scheduled tasks: schtasks /query /fo LIST /v
│   ├── Unquoted service paths
│   ├── AlwaysInstallElevated? reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
│   ├── Stored credentials: cmdkey /list
│   ├── Check for writable service binaries/paths
│   └── Token impersonation: whoami /priv → SeImpersonate? → [[Token-Impersonation]]
│
└── General:
    ├── Did you check EVERY writable file/directory?
    ├── Did you look for config files with passwords?
    ├── Did you check internal network services (127.0.0.1)?
    └── Did you try kernel exploits as LAST resort?
```

---

## AD-Specific Stuck

```
├── Run BloodHound — actually LOOK at the paths
│   └── bloodhound-python -u <user> -p <pass> -d <domain> -ns <dc-ip> -c all
├── AS-REP Roastable users?
│   └── impacket-GetNPUsers <domain>/ -no-pass -usersfile users.txt -dc-ip <dc-ip>
├── Kerberoastable accounts?
│   └── impacket-GetUserSPNs <domain>/<user>:<pass> -dc-ip <dc-ip> -request
├── Check ACLs in BloodHound
│   ├── GenericAll / GenericWrite / WriteDACL on users or groups?
│   ├── Can you add yourself to a group?
│   └── Can you reset someone's password?
├── Check for delegation
│   └── impacket-findDelegation <domain>/<user>:<pass> -dc-ip <dc-ip>
├── SMB shares on every machine
│   └── crackmapexec smb <targets> -u <user> -p <pass> --shares
├── LDAP anonymous bind?
│   └── ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local"
└── Check for LAPS, gMSA, ADCS
    └── crackmapexec ldap <dc-ip> -u <user> -p <pass> -M laps
```

See [[AD-Methodology]] for full attack chains.

---

## Web-Specific Stuck

```
├── Try a DIFFERENT wordlist
│   ├── /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt
│   ├── /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
│   └── /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
├── Check page source for EVERY page
│   └── Comments, hidden forms, JS files, API endpoints
├── Try default credentials
│   ├── admin:REDACTED, admin:REDACTED, admin:<application-name>
│   └── Check SecLists/Passwords/Default-Credentials/
├── Fuzz parameters
│   └── ffuf -u http://<target>/page?FUZZ=test -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
├── Check for API endpoints
│   ├── /api/, /v1/, /v2/, /swagger, /docs, /graphql
│   └── Fuzz file extensions: .php, .asp, .aspx, .jsp, .bak, .old, .txt
├── Check for LFI/RFI
│   └── Try ../../etc/passwd on ANY parameter
├── Check cookies and headers
│   └── JWT? Base64 decode it. Session cookie? Tamper with it.
└── Nikto it
    └── nikto -h http://<target>
```

See [[Web-Methodology]] for systematic approach.

---

## Common Traps That Waste Hours

| Trap | Fix |
|------|-----|
| Ran linpeas but didn't read ALL output | Re-run, pipe to file, `grep -i password\|suid\|root\|writable` |
| Assumed Linux when it's Windows (or vice versa) | Double-check OS from nmap |
| Forgot to add hostname to /etc/hosts | Web app returns default page instead of real content |
| Exploit needs Python 2 but you're running Python 3 | Check shebang, try `python2 exploit.py` |
| Running tools against wrong IP | Verify with `echo $IP` |
| Password has special characters, breaks your command | Wrap in single quotes: `'P@ss!w0rd'` |
| Gobuster found nothing | Wrong wordlist, missing extension flags, or need vhost scan |

## Nuclear Options (When All Else Fails)

1. **Stop and re-read every line of enumeration output** — the answer is almost always in output you already have
2. **Take a 15-minute break** — walk away from the screen completely
3. **Start a fresh terminal** and re-enumerate from scratch — fresh eyes catch things
4. **Move to another machine** — come back in 2 hours
5. **Check your assumptions** — is that really the version? Is that port actually what you think?
6. **Read the exploit code** — you may have the right exploit but are running it wrong
