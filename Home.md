# OSCP Field Notebook

**~70 notes. Zero fluff. Commands copy-paste ready.**

Port-indexed methodology + decision trees + lessons from practice boxes. For authorized labs only.

---

## Quick access

| Need | Go to |
|------|--------|
| Set lab IPs (optional) | [[00-Start-Here/Variables\|Variables]] + `fill-variables.py` |
| Overall attack flow | [[00-Start-Here/Methodology\|Methodology]] |
| Blocked? | [[00-Start-Here/Im-Stuck\|I'm Stuck]] |
| Exam-day ops checklist | [[00-Start-Here/Exam-Day-Checklist\|Exam Day Checklist]] |
| Scoring overview (verify with OffSec) | [[00-Start-Here/Scoring\|Scoring]] |

## Sections

### 00 - Start here
Methodology, stuck tree, variables, exam ops.

### 01 - Enumeration (by port)
[[01-Enumeration/Nmap|Nmap]] · FTP · SSH · SMTP · DNS · HTTP · SMB · SNMP · LDAP · Kerberos · MSSQL · NFS · RDP · WinRM

### 02 - Web attacks
[[02-Web-Attacks/Web-Methodology|Web Methodology]] · SQLi · command injection · LFI/RFI · XSS · SSTI · SSRF · auth bypass

### 03 - Active Directory
[[03-Active-Directory/AD-Methodology|AD Methodology]] · enum · AS-REP · Kerberoast · spray · BloodHound · lateral · DCSync · ACL · silver ticket

### 04 - Linux privesc
[[04-Linux-PrivEsc/Linux-PrivEsc-Methodology|Methodology]] · SUID · sudo · capabilities · cron · kernel · Docker/LXD

### 05 - Windows privesc
[[05-Windows-PrivEsc/Windows-PrivEsc-Methodology|Methodology]] · services · DLL · unquoted · tokens · scheduled tasks · AlwaysInstallElevated

### 06 - Pivoting
[[06-Pivoting/Pivoting-Methodology|Methodology]] · Ligolo-ng · Chisel · SSH tunnels · proxychains

### 07-10
File transfers · shells · password attacks · reporting structure

---

See [README.md](README.md) and [SCOPE.md](SCOPE.md) for public policy.
