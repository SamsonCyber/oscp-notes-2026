# OSCP Exam Scoring & Rules

> **Verify everything here against the [official OffSec exam guide](https://help.offsec.com/hc/en-us/articles/360040165632) before exam day.** OffSec changes rules. This page is a study aid, not authority.

## Exam Structure

| Component | Points | Details |
|-----------|--------|---------|
| Standalone Machine #1 | 20 pts | 10 pts `local.txt` + 10 pts `proof.txt` |
| Standalone Machine #2 | 20 pts | 10 pts `local.txt` + 10 pts `proof.txt` |
| Standalone Machine #3 | 20 pts | 10 pts `local.txt` + 10 pts `proof.txt` |
| AD Set (3 machines) | 40 pts | 2 clients + 1 DC - **all-or-nothing** |
| **Total** | **100 pts** | |

**Passing score: 70 points**

---

## AD Set Breakdown

- 3 machines: 2 client machines + 1 Domain Controller
- You MUST get `proof.txt` from the DC to get ANY points
- **All-or-nothing** - partial AD completion = 0 points
- This is why you do AD first while fresh - see [[Exam-Day-Checklist]]

---

## Bonus Points

| Bonus | Points | Requirements |
|-------|--------|-------------|
| Lab report | 10 pts | Complete 80% of exercises in EACH topic + 10 lab machines documented |

> **WARNING**: Bonus point requirements change. Check the [official OSCP Exam Guide](https://help.offsec.com/hc/en-us/articles/360040165632) the week before your exam for current rules. OffSec updates these silently.

With bonus points, you only need 60/100 on the exam to pass.

---

## Passing Scenarios

| AD Set | Standalones | Bonus | Total | Pass? |
|--------|-------------|-------|-------|-------|
| 40 | 30 (1.5 machines) | 0 | 70 | YES |
| 40 | 20 (1 machine) | 10 | 70 | YES |
| 0 | 60 (3 machines) | 10 | 70 | YES |
| 0 | 60 (3 machines) | 0 | 60 | NO |
| 40 | 20 (1 machine) | 0 | 60 | NO |

**Takeaway**: AD + 1 standalone = pass. Without AD, you need ALL 3 standalones + bonus.

---

## Metasploit Restrictions

- Allowed on **ONE machine only** - choose wisely
- Includes: `msfconsole`, `msfvenom` payloads generated with `msfvenom` are allowed everywhere
- `msfvenom` for payload generation = UNLIMITED use (any machine)
- `multi/handler` listener = UNLIMITED use (any machine)
- Full Metasploit (exploit modules, post modules, etc.) = ONE machine only
- **Recommendation**: Save it for the hardest standalone or don't use it at all

---

## Prohibited

- Commercial exploitation tools (Canvas, Core Impact, etc.)
- Automated exploitation frameworks (besides the one Metasploit use)
- Spoofing (IP, ARP, DNS)
- Denial of Service attacks
- AI-assisted exploitation tools (ChatGPT, Claude, Copilot, etc.)
- Any tools that auto-exploit (auto-pwn type)
- SQLMap auto mode counts as automated exploitation on some interpretations - use manual SQLi first, sqlmap for confirmation/dumping only

> **ALWAYS re-read the [official exam guide](https://help.offsec.com/hc/en-us/articles/360040165632) the week before.** OffSec updates restrictions without notice. People have been failed for tools that were allowed 6 months prior.

---

## Time Limits

| Phase | Duration |
|-------|----------|
| Exam | 23 hours 45 minutes |
| Report writing | 24 hours after exam ends |

---

## Report Requirements

- **Format**: PDF
- **Must include per machine**:
 - Vulnerability identified
 - Step-by-step exploitation (reproducible by a reader)
 - All commands used with output
 - Screenshots with proof commands (see [[Exam-Day-Checklist]])
 - Remediation recommendations
- **Proof commands required in screenshots**:
 - `whoami`
 - `hostname`
 - `ip addr` (Linux) or `ipconfig` (Windows)
 - Contents of `local.txt` and/or `proof.txt`
- All proof commands must be visible in an **interactive shell** - not a webshell, not a script output
- **File name**: `OSCP-OS-XXXXX-Exam-Report.pdf` (your OS-ID)
- Upload via OffSec portal before deadline

---

## Flag Locations

```
# Standalones
local.txt → low-priv user's desktop/home directory
proof.txt → root's home or Administrator's desktop

# AD Set
proof.txt → on the Domain Controller (Administrator desktop)
```

Submit flags in the exam control panel **as soon as you find them** - do not wait.
