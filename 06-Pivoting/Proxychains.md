# Proxychains

Routes tool traffic through a SOCKS proxy. Combine with [[Chisel]], [[SSH-Tunneling]], or any SOCKS proxy.

See also: [[Pivoting-Methodology]]

## Config

```bash
sudo nano /etc/proxychains4.conf
```

Add at bottom:

```
socks5 127.0.0.1 1080
```

## Usage

Prefix any command with `proxychains`:

```bash
# Scanning
proxychains nmap -sT -Pn -p REDACTED INTERNAL_IP

# Web
proxychains curl http://INTERNAL_IP
proxychains firefox http://INTERNAL_IP

# Remote access
proxychains evil-winrm -i INTERNAL_IP -u user -p password
proxychains impacket-psexec domain/user:REDACTED
proxychains ssh user@INTERNAL_IP
proxychains xfreerdp /v:INTERNAL_IP /u:admin /p:REDACTED

# SMB
proxychains smbclient -L //INTERNAL_IP -U user%password
proxychains crackmapexec smb INTERNAL_IP -u user -p password
```

## Important Notes

- **nmap**: Must use `-sT` (full connect) - SYN scan (`-sS`) does not work through SOCKS
- **nmap**: Must use `-Pn` to skip ping - ICMP does not go through SOCKS
- **DNS**: May not resolve through proxy - use IPs directly or set `proxy_dns` in config
- **Speed**: It is slow - scan specific ports, not full range
- **UDP**: Does not work through SOCKS - TCP only
- **Some tools break**: If a tool does not work through proxychains, switch to [[Ligolo-ng]] which avoids this problem entirely

## Chaining Multiple Proxies

Edit `/etc/proxychains4.conf`:

```
# Change to strict_chain or dynamic_chain at top of file
dynamic_chain

# Add multiple proxies
socks5 127.0.0.1 1080
socks5 127.0.0.1 1081
```

## Quick Test

```bash
# Verify the proxy is working
proxychains curl http://INTERNAL_IP
```

If it hangs, check that your tunnel ([[Chisel]], [[SSH-Tunneling]]) is still running.

## From Your Boxes

> **Lab AD chain** (personal lab) - Proxychains + chisel SOCKS for nmap scanning and evil-winrm to internal targets
> - What worked: `proxychains nmap -sT --top-ports 100 TARGET_IP` and `proxychains evil-winrm -u celia.almeda -H HASH -i TARGET_IP`
> - Lesson: Use `--top-ports 100` through proxychains - full port scans are painfully slow through SOCKS

> **OSCP B - MS01** (Course) - Proxychains for kerberoasting, SMB enumeration, and MSSQL access against internal AD
> - What worked: `proxychains impacket-GetUserSPNs -dc-ip TARGET_IP 'OSCP.exam/web_svc:REDACTED'` and `proxychains python3 mssqlclient.py -windows-auth OSCP.exam/sql_svc:REDACTED`
> - Lesson: All impacket tools work through proxychains. crackmapexec/nxc works too for quick credential validation: `proxychains crackmapexec smb INTERNAL_IP -u user -p REDACTED

> **Nagoya** (PG/Windows) - Proxychains to access MSSQL through chisel tunnel
> - What worked: `proxychains ./mssqlclient.py svc_mssql:REDACTED -windows-auth`
> - Lesson: Use `socks5 127.0.0.1 1080` in proxychains config (chisel default). If using SSH dynamic forward, match the port you specified with `-D`
