# LDAP - Port 389 (636 for LDAPS)

## Find Base DN

```bash
ldapsearch -x -H ldap://$IP -s base namingcontexts
```

## Anonymous Bind (40% of DCs Allow It)

```bash
ldapsearch -x -H ldap://$IP -b "DC=domain,DC=local"

# Dump users
ldapsearch -x -H ldap://$IP -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName description memberOf

# Dump computers
ldapsearch -x -H ldap://$IP -b "DC=domain,DC=local" "(objectClass=computer)" name

# Dump groups
ldapsearch -x -H ldap://$IP -b "DC=domain,DC=local" "(objectClass=group)" cn member
```

## Authenticated Bind

```bash
ldapsearch -x -H ldap://$IP -D "user@domain.local" -w 'password' -b "DC=domain,DC=local"

# Dump all users with descriptions
ldapsearch -x -H ldap://$IP -D "user@domain.local" -w 'password' -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName description
```

**50% of boxes have passwords in the description field.**

## NetExec

```bash
nxc ldap $IP -u '' -p '' -M get-desc-users
nxc ldap $IP -u user -p password --users
nxc ldap $IP -u user -p password --groups
```

## Nmap

```bash
nmap --script ldap-search,ldap-brute,ldap-rootdse -p 389 $IP
```

## Windapsearch

```bash
windapsearch -d domain.local --dc $IP -U           # Enumerate users
windapsearch -d domain.local --dc $IP -G           # Enumerate groups
windapsearch -d domain.local --dc $IP -PU          # Privileged users
windapsearch -d domain.local --dc $IP --da          # Domain admins
```

## ldapdomaindump

```bash
ldapdomaindump -u 'domain\user' -p 'password' $IP -o ldap_dump/
# Outputs HTML files — open in browser
```

## Tips

- LDAP often reveals the full domain structure, usernames, group memberships.
- Always check description fields for passwords.
- Service accounts often have weak or descriptable passwords.
- If anonymous bind works, you have a goldmine of AD info.

## See Also

- [[AD-Methodology]] | [[Kerberos-88]] | [[Nmap]]

## From Your Boxes

> **Hutch** (PG/Windows) — Anonymous LDAP bind dumped all user objects. Found password in Freddy McSorley's description field: `Password set to CrabSharkJellyfish192 at user's request`. Sprayed against all LDAP-enumerated users, confirmed `fmcsorley:REDACTED`. Later used LDAP to query LAPS admin password.
> - What worked: `ldapsearch -v -x -b "DC=hutch,DC=offsec" -H "ldap://TARGET_IP" "(objectclass=*)"` then `ldapsearch -x -H 'ldap://TARGET_IP' -D 'hutch\fmcsorley' -w 'CrabSharkJellyfish192' -b 'dc=hutch,dc=offsec' "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd`
> - Lesson: LDAP description fields contain passwords more often than you'd expect. Also always check for LAPS via `ms-MCS-AdmPwd` attribute.

> **Sauna** (HTB) — Anonymous LDAP bind returned naming contexts (`DC=EGOTISTICAL-BANK,DC=LOCAL`) confirming the domain name. Didn't directly leak users in this case, but established the base DN for further authenticated queries.
> - What worked: `ldapsearch -x -h TARGET_IP -s base namingcontexts` then `ldapsearch -x -h TARGET_IP -b 'DC=EGOTISTICAL-BANK,DC=LOCAL'`
> - Lesson: Even when anonymous LDAP doesn't dump users, it confirms the domain structure needed for Kerberos and other attacks.

> **Hokkaido** (PG/Windows) — LDAP service scan in nmap revealed the full domain `hokkaido-aerospace.com` and DC FQDN `dc.hokkaido-aerospace.com` without any credentials.
> - What worked: Nmap LDAP service detection automatically exposed domain info in banner
> - Lesson: LDAP banners on port 389 always reveal the domain name — add it to /etc/hosts immediately.

> **Cascade** (HTB) — LDAP enumeration revealed user attributes containing encoded passwords. Combined with SMB share access for full credential chain.
> - What worked: Authenticated LDAP query dumping all user attributes including custom fields
> - Lesson: Dump ALL attributes, not just sAMAccountName and description. Custom attributes can hide encoded creds.
