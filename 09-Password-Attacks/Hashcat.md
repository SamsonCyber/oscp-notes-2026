# Hashcat

See [[Hash-Identification]] to identify hash type first.

---

## Identify hash type
```bash
hashid 'HASH_HERE'
# Or: https://hashcat.net/wiki/doku.php?id=example_hashes
```

## Common modes

| Mode | Hash Type |
|------|-----------|
| 0 | MD5 |
| 100 | SHA1 |
| 1400 | SHA256 |
| 1000 | NTLM |
| 3200 | bcrypt |
| 5600 | NTLMv2 (Net-NTLMv2) |
| 13100 | Kerberoast (TGS-REP) |
| 18200 | AS-REP Roast |
| 1800 | sha512crypt ($6$) |
| 500 | md5crypt ($1$) |
| 3000 | LM |
| 22000 | WPA-PBKDF2-PMKID+EAPOL |

## Usage
```bash
hashcat -m MODE hash.txt /usr/share/wordlists/rockyou.txt
# With rules:
hashcat -m MODE hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
# Show cracked:
hashcat -m MODE hash.txt --show
```

## Common commands
```bash
# NTLM
hashcat -m 1000 ntlm.txt /usr/share/wordlists/rockyou.txt
# NTLMv2 (from Responder)
hashcat -m 5600 ntlmv2.txt /usr/share/wordlists/rockyou.txt
# Kerberoast
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt
# AS-REP
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
# Linux shadow
hashcat -m 1800 shadow.txt /usr/share/wordlists/rockyou.txt
```

See also: [[John]] for alternative cracking, [[Hydra]] for online brute force.

## From Your Boxes

> **Forest** (HTB) — AS-REP roasting with hashcat mode 18200
> - What worked: `hashcat -m 18200 svc-alfresco.kerb /usr/share/wordlists/rockyou.txt --force` cracked to `REDACTED`
> - Lesson: AS-REP roast hashes come from `impacket-GetNPUsers`. Mode 18200, no rules needed for weak passwords

> **Sauna** (HTB) — AS-REP roasting for initial access, hashcat mode 18200
> - What worked: `hashcat -m 18200 hashes.aspreroast /usr/share/wordlists/rockyou.txt --force` cracked fsmith's hash to `REDACTED`
> - Lesson: Use `impacket-getNPUsers` with `-format hashcat` flag to output directly in hashcat format

> **OSCP B — MS01** (Course) — Kerberoast hash cracked with hashcat mode 13100 + rules
> - What worked: `sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
> - Lesson: Kerberoast hashes (mode 13100) often need rules to crack. `best64.rule` is a good starting point. Save the hash from `impacket-GetUserSPNs -outputfile`

> **Course Materials — NTLM Cracking** — NTLM hash cracking with mode 1000 + rules
> - What worked: `hashcat -m 1000 nelly.hash /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
> - Lesson: Extract NTLM hashes via mimikatz (`sekurlsa::logonpasswords` or `lsadump::sam`), then crack with mode 1000. If cracking fails, try pass-the-hash instead
