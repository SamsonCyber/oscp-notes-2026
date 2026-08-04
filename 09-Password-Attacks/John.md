# John the Ripper

---

## Basic usage
```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
# Show cracked
john hash.txt --show
# Specific format
john --format=NT hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

## Conversion tools (hash extraction)
```bash
# SSH key
ssh2john id_rsa > hash.txt

# ZIP file
zip2john file.zip > hash.txt

# KeePass
keepass2john Database.kdbx > hash.txt

# PDF
pdf2john file.pdf > hash.txt

# Office docs
office2john file.docx > hash.txt

# 7z
7z2john file.7z > hash.txt

# Kerberos ticket
kirbi2john ticket.kirbi > hash.txt
```

Then crack:
```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

See also: [[Hashcat]] for GPU cracking, [[Hash-Identification]] to identify hash type.

## From Your Boxes

> **Active** (HTB) - john to crack Kerberoast TGS-REP hash after GetUserSPNs
> - What worked: `john GetUserSPNs.out --wordlist=/usr/share/wordlists/rockyou.txt` cracked admin's Kerberoast hash to `Ticketmaster1968`
> - Lesson: John auto-detects Kerberos hash format - no need to specify `--format`. Save GetUserSPNs output with `-outputfile` flag

> **Timelapse** (HTB) - zip2john + pfx2john chain to crack protected archive and certificate
> - What worked: `zip2john winrm_backup.zip > hash` then `john hash --wordlist=rockyou.txt` (cracked to `supremelegacy`). Then `pfx2john legacyy_dev_auth.pfx > hash` then john again (cracked to `thuglegacy`)
> - Lesson: Chain multiple john2* tools in one engagement. Zip password protects PFX, PFX contains SSL cert/key for WinRM access

> **Sunday** (HTB) - john to crack sha256crypt shadow backup hash
> - What worked: `john hash --wordlist=/usr/share/wordlists/rockyou.txt` cracked sammy's `$5$` hash to `REDACTED`
> - Lesson: Always check `/backup` directories and readable shadow files. John handles `$5$` (sha256crypt) natively

> **Nagoya** (PG/Windows) - john to crack Kerberoast hash for svc_mssql service account
> - What worked: `john kerb.txt` cracked svc_mssql SPN hash to `REDACTED` almost immediately
> - Lesson: Service account passwords are often weak. Always kerberoast with found creds: `impacket-GetUserSPNs domain/user:REDACTED -dc-ip IP -outputfile kerb.txt`

> **Course Materials - SSH Keys** - ssh2john for cracking encrypted SSH private keys
> - What worked: `ssh2john id_rsa > ssh.hash` then `john --wordlist=ssh.passwords --rules=sshRules ssh.hash`
> - Lesson: If hashcat gives "token length exception" on SSH keys, use john instead. Custom rules can be added to `/etc/john/john.conf`

> **Course Materials - KeePass** - keepass2john for cracking database passwords
> - What worked: `keepass2john Database.kdbx > keepass.hash` - remove the `Database:` prefix, then crack with hashcat `-m 13400` or john
> - Lesson: keepass2john prepends a username field that must be removed before cracking. Search Windows targets for .kdbx files with `Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue`
