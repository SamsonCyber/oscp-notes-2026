# SNMP - Port 161 (UDP)

## Brute Force Community Strings

```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt $IP
```

Default strings: `public`, `private`, `manager`

## SNMPWalk

```bash
# Full walk
snmpwalk -v2c -c public $IP

# With human-readable output
snmpwalk -v2c -c public $IP -m ALL
```

## Useful OIDs

```bash
# Users
snmpwalk -v2c -c public $IP 1.3.6.1.4.1.77.1.2.25

# Running processes
snmpwalk -v2c -c public $IP 1.3.6.1.2.1.25.4.2.1.2

# TCP listening ports
snmpwalk -v2c -c public $IP 1.3.6.1.2.1.6.13.1.3

# Installed software
snmpwalk -v2c -c public $IP 1.3.6.1.2.1.25.6.3.1.2

# System info
snmpwalk -v2c -c public $IP 1.3.6.1.2.1.1

# Network interfaces
snmpwalk -v2c -c public $IP 1.3.6.1.2.1.2.2.1.2

# ARP table
snmpwalk -v2c -c public $IP 1.3.6.1.2.1.3.1.1.2
```

## Quick Enum

```bash
snmp-check $IP
snmp-check $IP -c public
```

## Nmap

```bash
nmap -sU --script snmp-brute,snmp-info,snmp-interfaces,snmp-processes,snmp-win32-users -p 161 $IP
```

## Tips

- SNMP is UDP — will not appear in TCP scans. Always run UDP scan.
- SNMP can leak usernames, running processes, and **passwords in process command-line arguments**.
- Look at process list carefully — cron jobs, scripts with hardcoded creds, internal services.
- SNMPv1/v2c send community strings in cleartext. SNMPv3 uses encryption.
- `snmpwalk` output can be huge — redirect to file and grep through it.

```bash
snmpwalk -v2c -c public $IP > snmp_full.txt
grep -i "password\|user\|login\|pass" snmp_full.txt
```

## See Also

- [[Nmap]]

## From Your Boxes

> **Pandora** (HTB) — SNMPwalk with `public` community string revealed a running process with hardcoded credentials in its command line: `/usr/bin/host_check -u daniel -p REDACTED Direct SSH access as daniel.
> - What worked: `snmpwalk -v2c -c public TARGET_IP` then grep output for passwords
> - Lesson: SNMP process lists can contain passwords as command-line arguments. Always redirect full snmpwalk to a file and grep for password/user/login.

> **Mentor** (HTB) — SNMP check with community string `public` revealed system info including hostname, OS version (Linux 5.15.0-56), and admin email. While it didn't directly leak creds, it confirmed the target OS and helped narrow the attack surface.
> - What worked: `snmp-check TARGET_IP` and `snmpwalk -v2c -c public TARGET_IP`
> - Lesson: Even when SNMP doesn't leak passwords, it reveals OS, hostname, and system architecture — useful for choosing exploits.

> **Kiero (OSCP B)** (Course) — SNMPwalk with `NET-SNMP-EXTEND-MIB` OID revealed extended SNMP data. Combined with default creds `kiero:REDACTED` found via SNMP enumeration, gained FTP access to SSH keys.
> - What worked: `snmpwalk -c public -v 2c TARGET_IP NET-SNMP-EXTEND-MIB::nsExtendObjects`
> - Lesson: Try the `NET-SNMP-EXTEND-MIB` OID specifically — it can reveal custom scripts and commands not shown in standard walks.
