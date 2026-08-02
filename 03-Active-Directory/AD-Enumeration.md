# AD Enumeration

## From Linux (Kali)

```bash
# Domain info
nxc smb $DC -u user -p pass
nxc smb $DC -u user -p pass --users
nxc smb $DC -u user -p pass --groups
nxc smb $DC -u user -p pass --pass-pol
```

```bash
# LDAP — all users with descriptions and group memberships
ldapsearch -x -H ldap://$DC -D "user@domain.local" -w 'pass' -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName description memberOf
```

```bash
# Find computers
ldapsearch -x -H ldap://$DC -D "user@domain.local" -w 'pass' -b "DC=domain,DC=local" "(objectClass=computer)" dNSHostName
```

```bash
# Find SPNs (for Kerberoasting)
ldapsearch -x -H ldap://$DC -D "user@domain.local" -w 'pass' -b "DC=domain,DC=local" "(servicePrincipalName=*)" sAMAccountName servicePrincipalName
```

→ [[Kerberoasting]]

---

## From Windows (Domain-Joined Machine)

### PowerView

```powershell
Import-Module .\PowerView.ps1

Get-DomainUser | Select-Object samaccountname,description,memberof
Get-DomainGroup | Select-Object name
Get-DomainComputer | Select-Object dnshostname,operatingsystem
Find-DomainShare -CheckShareAccess

# Kerberoastable accounts
Get-DomainUser -SPN

# AS-REP roastable accounts
Get-DomainUser -PreauthNotRequired

# ACL abuse paths
Get-ObjectAcl -Identity "target" -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll|GenericWrite|WriteOwner|WriteDacl|AllExtendedRights|ForceChangePassword"}
```

→ [[ACL-Abuse]]

### .NET / ADSI

```powershell
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()

([adsisearcher]"(&(objectCategory=person)(objectClass=user))").FindAll() | %{$_.Properties.samaccountname}
```

### CMD

```cmd
net user /domain
net group /domain
net group "Domain Admins" /domain
```

---

## Checklist

- [ ] Enumerate users, groups, computers
- [ ] Check user description fields for passwords
- [ ] Identify Kerberoastable accounts (SPN set)
- [ ] Identify AS-REP roastable accounts (preauth disabled)
- [ ] Check password policy (lockout threshold)
- [ ] Enumerate shares
- [ ] Run [[BloodHound]] collection
