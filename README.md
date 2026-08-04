# OSCP Field Notebook

![oscp-notes-2026 banner](banner.jpg)

Port-indexed pentest methodology notebook: decision trees, copy-paste command patterns, and **lessons from real practice boxes** (HTB / PG / personal labs). Built for exam pace and real engagements.

A **workflow** you can run under time pressure. Commands and decision trees first. Not a payload dump or a library of full machine writeups.

> Public study notes for authorized practice only (your labs, HTB/PG, courses you own). No exam keys, no live engagement dumps, no OffSec course content dump.

**Live:** https://github.com/SamsonCyber/oscp-notes

---

## What makes this different

| Feature | Why it matters |
|---------|----------------|
| **Port â†’ note map** | Service open? Open the matching note. No hunting a 400-page PDF. |
| **I'm Stuck trees** | Decision trees for â€œno vectorâ€, â€œcreds but no shellâ€, â€œshell but no rootâ€. |
| **From Your Boxes** | Technique notes end with *what actually worked* on named public boxes (creds redacted). |
| **One-shot IP fill** | Set IPs once in `Variables.md`, run `fill-variables.py apply`, every note gets your lab IPs. |
| **Zero fluff** | ~70 notes. Commands first. Theory only when it changes the next command. |

## Quick start

```bash
git clone https://github.com/SamsonCyber/oscp-notes.git
cd oscp-notes

# optional: bind placeholders to your lab IPs

![oscp-notes-2026 banner](banner.jpg)
# edit 00-Start-Here/Variables.md

![oscp-notes-2026 banner](banner.jpg)
python3 fill-variables.py apply
python3 fill-variables.py status
python3 fill-variables.py reset # restore placeholders
```

Open `Home.md` in Obsidian, VS Code, or any markdown reader. Wikilinks work best in Obsidian.

## Layout

```
00-Start-Here/ methodology, I'm Stuck, exam-day ops, variables, scoring overview
01-Enumeration/ nmap + one note per common port/service
02-Web-Attacks/ injection, LFI, auth bypass, web methodology
03-Active-Directory/ no-creds â†’ DA chain, roasting, BloodHound, lateral, DCSync
04-Linux-PrivEsc/ ordered checklist + technique cards
05-Windows-PrivEsc/
06-Pivoting/ Ligolo-ng first, then Chisel / SSH / proxychains
07-File-Transfers/
08-Shells/
09-Password-Attacks/
10-Reporting/ structure reminders (use OffSec's official template for the real exam)
fill-variables.py placeholder IP binder
```

## Scope (what is / is not here)

**In scope for this repo**

- General offensive methodology aligned with OSCP-style learning
- Public-box lessons (HTB, Proving Grounds, personal labs) with secrets redacted
- Tooling patterns (nmap, nxc, impacket, evil-winrm, ligolo, hashcat, â€¦)

**Out of scope (deliberately)**

- Exam answers, exam host notes, VPN configs, proof flags
- Full machine writeup libraries
- Copyrighted OffSec PDF / course text
- Live client or employer engagement data

Verify current exam rules on [OffSecâ€™s exam guide](https://help.offsec.com/hc/en-us/articles/360040165632). Scoring tables here are study aids and can go stale.

## Variable filler

Placeholders used across notes: `ATTACKER_IP`, `TARGET_IP`, `DC_IP`, `MS01_IP`, `MS02_IP`, `STANDALONE1..3`, `INTERNAL_IP`, `INTERNAL_NET`, `DOMAIN`.

```bash
python3 fill-variables.py apply # write your IPs into every .md
python3 fill-variables.py reset # restore tokens (uses .variables-backup.json)
```

Do not commit applied IPs. Keep `Variables.md` as placeholders in git.

## Author

SamsonCyber. Built while grinding OSCP-style labs. Consolidated from a larger private vault into a public, scrubbed field notebook.

## License

MIT for original structure, scripts, and original prose. Technique knowledge is public security tradecraft. Box names refer to public HTB/PG machines; respect each platformâ€™s rules.
