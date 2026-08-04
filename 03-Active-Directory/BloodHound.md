# BloodHound

## Collection

From Linux (with creds):
```bash
bloodhound-python -c All -u user -p password -d domain.local -ns $DC --zip
```

From Windows:
```powershell
.\SharpHound.exe -c All --zip
```

```powershell
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -ZipFileName loot.zip
```

---

## Start BloodHound

### BloodHound Legacy (neo4j-based - what OSCP labs use)
```bash
sudo neo4j start
bloodhound
# Upload the zip file via GUI
```

### BloodHound CE (newer, Docker-based)
```bash
# If your Kali has BloodHound CE instead:
# Check with: bloodhound --version
# CE uses a web UI at https://localhost:8080
# Collection is the same - just the UI is different
```

> **Know which version your Kali has BEFORE exam day.** Test it during lab practice so you're not debugging BloodHound during the exam.

---

## Key Queries (Analysis Tab)

1. **Find all Domain Admins**
2. **Shortest Paths to Domain Admins from Owned Principals** - MOST USEFUL
3. **Find Kerberoastable Users with paths to DA**
4. **Find AS-REP Roastable Users**
5. **Shortest Paths from Owned Principals**

---

## Workflow

1. Upload data
2. **Mark compromised users as Owned**: right-click node → Mark User as Owned
3. Run query #2 - shortest paths from owned to DA
4. Follow the path - each edge tells you the attack

---

## Edges to Look For

| Edge | Meaning | Exploit |
|------|---------|---------|
| GenericAll | Full control | Change password, add to group |
| GenericWrite | Write properties | Set SPN → Kerberoast |
| ForceChangePassword | Reset password | Reset without knowing current |
| WriteDACL | Modify permissions | Grant yourself DCSync |
| WriteOwner | Take ownership | Own → WriteDACL → DCSync |
| AllExtendedRights | Read LAPS, DCSync | Read LAPS password |
| ReadLAPSPassword | Read local admin pass | Get local admin |

→ [[ACL-Abuse]] for exploiting these paths

## From Your Boxes

> **Forest** (HTB) - SharpHound collection from compromised user, shortest path to DA
> - What worked: `invoke-bloodhound -collectionmethod all -domain htb.local -ldapuser svc-alfresco -ldappass REDACTED`
> - BloodHound showed: svc-alfresco -> Service Accounts -> Privileged IT -> Account Operators -> GenericAll on Exchange Windows Permissions -> DCSync
> - Lesson: "Shortest Paths to Domain Admin" query is the first thing to check after importing data

> **Vault** (PG) - Remote BloodHound-python collection without a foothold
> - What worked: `bloodhound-python -u anirudh -p REDACTED -d vault.offsec -c All -ns TARGET`
> - Revealed direct GPO write access on Default Domain Policy
> - Lesson: Use bloodhound-python from Kali when you have creds but no shell - no need for SharpHound

> **Hokkaido** (PG) - BloodHound CE revealing GenericWrite chain to admin
> - What worked: `bloodhound-ce-python -u "hrapp-service" -p 'REDACTED' -d hokkaido-aerospace.com -c all --zip -ns TARGET`
> - Chain: hrapp-service GenericWrite -> Hazel.Green -> IT Group -> ForceChangePassword on T1 admin
> - Lesson: Follow the full chain in BloodHound - one hop isn't always enough, check 2-3 hops deep

> **Resourced** (PG) - BloodHound showing GenericAll on DC for RBCD attack
> - BloodHound revealed GenericAll on the DC computer object, but no trusted computer to delegate
> - Solution: Create a fake computer object with impacket-addcomputer, then RBCD attack
> - Lesson: GenericAll on a computer object = resource-based constrained delegation attack

> **Heist** (PG) - BloodHound revealing gMSA password readable by current user
> - Shortest paths to high value targets showed svc_apache as a gMSA account
> - Current user (enox) was in Web Admins group, which could read the gMSA password
> - Lesson: Check for gMSA accounts in BloodHound - if you can read their password, you get their hash

> **Sauna** (HTB) - BloodHound first degree object control revealing DCSync rights
> - First degree object control showed svc_loanmgr had GetChanges + GetChangesAll on the domain
> - Lesson: Check "First Degree Object Control" for each compromised user - DCSync rights are the jackpot
