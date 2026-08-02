# Hash Identification

---

## Quick reference

| Pattern | Likely Hash |
|---------|-------------|
| 32 hex chars | MD5 or NTLM |
| 40 hex chars | SHA1 |
| 64 hex chars | SHA256 |
| 128 hex chars | SHA512 |
| `$1$...` | md5crypt |
| `$5$...` | sha256crypt |
| `$6$...` | sha512crypt |
| `$2a$`/`$2b$`/`$2y$` | bcrypt |
| `$krb5tgs$` | Kerberoast |
| `$krb5asrep$` | AS-REP |
| LM:REDACTED format | Windows SAM dump |
| `user::domain:...` | NTLMv2 (Net-NTLMv2) |
| `aad3b435...` (LM part) | NTLM (LM part is empty/disabled) |

## Tools
```bash
hashid 'HASH'
hash-identifier  # interactive
# Or check: https://hashcat.net/wiki/doku.php?id=example_hashes
```

## Common sources to hash type

- `/etc/shadow` --> $6$ (sha512crypt) usually, [[Hashcat]] mode 1800
- Windows SAM --> NTLM, mode 1000
- Responder/relay capture --> NTLMv2, mode 5600
- Kerberoasting --> TGS-REP, mode 13100
- AS-REP roasting --> mode 18200
- KeePass database --> mode 13400
- .pfx/.p12 certificate --> pfx2john first

See also: [[Hashcat]], [[John]] for cracking.

## From Your Boxes

> **Lab AD chain** (personal lab) — SAM/SYSTEM dump producing LM:REDACTED hash pairs
> - What worked: `impacket-secretsdump -system SYSTEM -sam SAM LOCAL` dumped hashes in `uid:rid:REDACTED:nthash` format. The `NTHASH` LM portion means LM is disabled (normal)
> - Lesson: SAM dump hashes are NTLM (hashcat mode 1000). The LM part starting with `aad3b435...` is always empty/disabled on modern Windows

> **Forest** (HTB) — AS-REP hash identification (`$krb5asrep$23$`) for hashcat mode 18200
> - What worked: GetNPUsers output starts with `$krb5asrep$23$` — immediately identifiable as AS-REP roast, mode 18200
> - Lesson: `$krb5asrep$` prefix = mode 18200. `$krb5tgs$` prefix = mode 13100 (Kerberoast). Learn these prefixes — they tell you the mode instantly

> **Sauna** (HTB) — Same AS-REP pattern, secretsdump producing raw NTLM hashes for pass-the-hash
> - What worked: `impacket-secretsdump` output admin hash `NTHASH` — 32 hex chars = NTLM. When hashcat couldn't crack it, used pass-the-hash instead
> - Lesson: 32 hex chars can be MD5 or NTLM. Context matters — if it came from SAM/secretsdump/mimikatz, it's NTLM (mode 1000). If it won't crack, try PTH

> **Sunday** (HTB) — `$5$` prefix in shadow backup identified as sha256crypt
> - What worked: `$5$Ebkn8jlK$...` immediately identified as sha256crypt. John cracked it without specifying format
> - Lesson: Shadow file hash prefixes: `$5$` = sha256crypt (mode 7400 hashcat), `$6$` = sha512crypt (mode 1800), `$1$` = md5crypt (mode 500)

> **Course Materials — Hash ID Tools** — hashid and hash-identifier for unknown hashes
> - What worked: `hashcat --help | grep -i "KeePass"` to find mode numbers, `hashid 'HASH'` for quick identification
> - Lesson: When in doubt, grep hashcat help or check the example hashes wiki page: https://hashcat.net/wiki/doku.php?id=example_hashes
