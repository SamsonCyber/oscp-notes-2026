# SSH Tunneling

No upload needed — just SSH access.

See also: [[Pivoting-Methodology]], [[Proxychains]]

## Local Port Forward (Access Remote Service from Kali)

```bash
# Forward INTERNAL_IP:80 to localhost:8080
ssh -N -L 8080:REDACTED:80 user@PIVOT_IP
```

Now visit `http://localhost:8080` on Kali.

```bash
# Forward internal RDP
ssh -N -L 3389:REDACTED:3389 user@PIVOT_IP
xfreerdp /v:127.0.0.1 /u:admin /p:REDACTED
```

## Remote Port Forward (Let Internal Target Reach Kali)

```bash
# Forward Kali's port 4444 through the pivot
ssh -N -R 4444:REDACTED:4444 user@PIVOT_IP
```

Now internal targets can reach PIVOT_IP:4444 which hits Kali:4444.

## Dynamic Port Forward (SOCKS Proxy)

```bash
ssh -N -D 1080 user@PIVOT_IP
```

Edit `/etc/proxychains4.conf` — add at bottom:

```
socks5 127.0.0.1 1080
```

Use with [[Proxychains]]:

```bash
proxychains nmap -sT -Pn -p REDACTED INTERNAL_IP
proxychains curl http://INTERNAL_IP
```

## sshuttle (VPN-like — Easiest)

```bash
# Requires SSH access + root on Kali
sshuttle -r user@PIVOT_IP TARGET_IP/24
```

Now access internal IPs directly — no proxychains needed:

```bash
nmap -sT -Pn 10.10.10.X
curl http://10.10.10.X
```

With SSH key:

```bash
sshuttle -r user@PIVOT_IP TARGET_IP/24 --ssh-cmd "ssh -i id_rsa"
```

## Double Pivot (Chain SSH Tunnels)

```bash
# Step 1: Forward SSH port of second pivot through first
ssh -N -L 2222:REDACTED:22 user@FIRST_PIVOT_IP

# Step 2: Use forwarded port to create tunnel to third network
ssh -N -D 1080 -p 2222 user@localhost
```

## Useful Flags

| Flag | Purpose |
|---|---|
| `-N` | No shell — tunnel only |
| `-f` | Background the connection |
| `-L` | Local port forward |
| `-R` | Remote port forward |
| `-D` | Dynamic (SOCKS) forward |
| `-i` | Specify SSH key |

## Example Combo

```bash
# Background a dynamic tunnel then use it
ssh -N -f -D 1080 user@PIVOT_IP
proxychains nmap -sT -Pn -p REDACTED INTERNAL_IP
```

## From Your Boxes

> **Pandora** (HTB) — Local port forward to access internal-only Pandora FMS console, then exploited SQLi
> - What worked: `ssh -L 9001:REDACTED:80 daniel@TARGET_IP` then visited `http://127.0.0.1:9001/pandora_console/`
> - Lesson: Internal web apps often have more vulns than external ones. Always check for services bound to localhost with `ss -tlnp`

> **Poison** (HTB) — Forwarded internal VNC port to Kali for root access
> - What worked: `ssh -N -L 34500:REDACTED:5901 charix@TARGET_IP` then `vncviewer 127.0.0.1::34500 -passwd secret`
> - Lesson: VNC running as root on localhost is a goldmine — forward it and connect with any leaked VNC password file

> **ServMon** (HTB) — Forwarded NSClient++ port restricted to localhost only
> - What worked: `ssh nadine@TARGET_IP -L 8443:REDACTED:8443` to bypass "allowed hosts = 127.0.0.1" restriction
> - Lesson: Check config files for `allowed hosts` restrictions — SSH local forward makes your traffic appear as localhost

> **Boolean** (PG/Linux) — Used SSH with uploaded authorized_keys for initial access, then local SSH with found root key for privesc
> - What worked: Uploaded SSH public key via directory traversal, then `ssh -i id_ed25519 remi@TARGET_IP`. For privesc: `ssh -i /home/remi/root root@127.0.0.1` with IdentitiesOnly config
> - Lesson: "Too many authentication failures" means SSH is trying multiple keys. Fix with `IdentitiesOnly yes` and `IdentityAgent none` in `.ssh/config`
