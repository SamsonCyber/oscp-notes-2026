# DNS - Port 53

## Decision Tree

### 1. Zone Transfer (Instant Win)

```bash
dig axfr @$IP domain.htb
dig axfr @$IP domain.htb +noall +answer

# Alternative
host -l domain.htb $IP
dnsrecon -d domain.htb -n $IP -t axfr
```

### 2. Basic Queries

```bash
# Any records
dig any @$IP domain.htb

# Specific record types
dig @$IP domain.htb A
dig @$IP domain.htb MX
dig @$IP domain.htb TXT
dig @$IP domain.htb NS
dig @$IP domain.htb AAAA
```

### 3. Subdomain Brute Force

```bash
gobuster dns -d domain.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -r $IP:53

# Alternative with dnsenum
dnsenum --dnsserver $IP --enum -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt domain.htb
```

### 4. Reverse Lookup

```bash
dnsrecon -r TARGET_IP/24 -n $IP
```

### 5. Add to /etc/hosts

```bash
echo "$IP domain.htb" | sudo tee -a /etc/hosts
echo "$IP sub.domain.htb" | sudo tee -a /etc/hosts
```

## Common Gotchas

- **Always add discovered hostnames to `/etc/hosts`** — vhosts may serve completely different content.
- Multiple subdomains can point to the same IP but serve different sites.
- Zone transfer failing does not mean no subdomains exist — brute force next.
- Check for both TCP and UDP on port 53. Zone transfers use TCP.
- If you find a domain name in any service banner, try DNS enumeration against it.

## Nmap

```bash
nmap --script dns-brute,dns-zone-transfer --script-args dns-brute.domain=domain.htb -p 53 $IP
```

## See Also

- [[HTTP-80-443]] | [[Nmap]]

## From Your Boxes

> **Flight** (HTB) — Subdomain fuzzing with wfuzz found `school.flight.htb` which served a completely different PHP site vulnerable to LFI/RFI. The main site was static HTML with nothing useful.
> - What worked: `wfuzz -u http://TARGET_IP -H "Host: FUZZ.flight.htb" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --hh 7069`
> - Lesson: Always fuzz for vhosts — different subdomains often serve entirely different (and more vulnerable) applications.

> **Mentor** (HTB) — Subdomain brute forcing discovered an API subdomain (`api.mentorquotes.htb`) that wasn't visible on the main site. The API had its own authentication and endpoints that led to command injection.
> - What worked: Subdomain enumeration found `api.mentorquotes.htb`
> - Lesson: APIs are often hidden behind subdomains. Always add discovered hostnames to /etc/hosts and enumerate further.

> **Multiple HTB/PG Boxes** — Adding discovered domain names to `/etc/hosts` was critical on nearly every box (Pilgrimage, Devvortex, Precious, Monitored, etc.). Sites often returned different content or redirected when accessed by hostname vs IP.
> - Lesson: If any service banner reveals a domain name, immediately add it to /etc/hosts and re-enumerate HTTP.
