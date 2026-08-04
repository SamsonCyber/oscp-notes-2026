# Exam Day Checklist

## Pre-Exam Setup (30 min before)

```bash
# Connect VPN
sudo openvpn --config exam.ovpn

# Verify connectivity
ip a
ping <target-network-gateway>

# Start terminal logging (EVERY terminal)
script -a ~/oscp-exam/terminal-$(date +%Y%m%d-%H%M%S).log

# Create working directories
mkdir -p REDACTED
mkdir -p REDACTED

# Start screenshot tool
flameshot &

# Sync clock
sudo ntpdate pool.ntp.org
```

- [ ] Webcam + screen share working (test BEFORE exam starts)
- [ ] VPN connected, targets reachable
- [ ] Terminal logging active on ALL terminals
- [ ] Note-taking ready (this notebook open)
- [ ] **Exam control panel open in browser - keep it open the entire exam**
- [ ] Water, food, caffeine prepared
- [ ] Phone on silent
- [ ] Downloaded the [official OffSec report template](https://help.offsec.com/hc/en-us/articles/360040165632) already
- [ ] Tools pre-staged in ~/tools/ (linpeas, winpeas, pspy, chisel, ligolo, nc, PrintSpoofer, GodPotato, SharpHound, Rubeus, PowerView, kerbrute)

---

## Time Management

**Recommended order: AD set FIRST (40 points)**

| Block | Time | Target | Goal |
|-------|------|--------|------|
| 1 | 0:00 - 3:00 | AD Set | 40 pts - all-or-nothing, do this fresh |
| 2 | 3:00 - 5:00 | Standalone #1 | 20 pts - pick the easiest looking |
| 3 | 5:00 - 5:30 | BREAK | Eat, walk, decompress |
| 4 | 5:30 - 7:30 | Standalone #2 | 20 pts |
| 5 | 7:30 - 9:30 | Standalone #3 | 20 pts |
| 6 | 9:30+ | Rotate back | Hit anything you missed |

If AD stalls at 2 hours, pivot to standalones. Come back to AD later.

---

## Per-Machine Workflow

1. **Enumerate** → Full port scan, service versions, scripts
2. **Research** → Version-specific vulns, searchsploit, Google
3. **Exploit** → Gain initial foothold
4. **Grab local flag** → `local.txt`
5. **Privilege Escalation** → [[Linux-PrivEsc-Methodology]] or [[Windows-PrivEsc-Methodology]]
6. **Grab proof flag** → `proof.txt`
7. **Screenshot** → Proof commands in interactive shell
8. **Document** → Commands used, output, screenshots - for report

---

## Stuck Protocol

> If stuck for **1 hour** on any single phase - STOP. Rotate to another machine. Come back fresh.

1. Re-read your enumeration output - something is there
2. Try a different wordlist or tool
3. Check for rabbit holes - are you chasing something unlikely?
4. Take a 5-minute walk
5. See [[Im-Stuck]] for the full decision tree

---

## Flag Submission & Proof Requirements

**Every flag requires a screenshot with an interactive shell showing:**

```bash
# Linux proof
cat /path/to/local.txt
cat /root/proof.txt
whoami
hostname
ip addr
```

```powershell
# Windows proof
type C:\Users\<user>\Desktop\local.txt
type C:\Users\Administrator\Desktop\proof.txt
whoami
hostname
ipconfig
```

**Requirements:**
- Must be an **interactive shell** (not a webshell output, not a file read via LFI, not a script output)
- All proof commands visible in **one screenshot** (scroll up if needed, or use `&&`)
- Submit flags in the control panel **IMMEDIATELY** after capturing - do not wait
- **THE #1 STUPID WAY TO FAIL**: forgetting to submit flags in the control panel. A perfect report with no submitted flags = 0 points
- If your shell dies and you can't get it back, at least you submitted the flag

---

## Screenshot Checklist Per Machine

- [ ] `whoami` output visible
- [ ] `hostname` output visible
- [ ] `ip addr` / `ipconfig` output visible
- [ ] Flag contents visible (`local.txt` and/or `proof.txt`)
- [ ] All in ONE screenshot from an interactive shell
- [ ] Flag submitted in exam control panel

---

## Break Schedule

| Time Into Exam | Action |
|----------------|--------|
| 3:00 | 15-min break - eat something real |
| 5:30 | 30-min break - meal + walk |
| 8:00 | 10-min break - stretch, eyes off screen |
| 12:00 | Consider sleeping 2-3 hours if ahead |

Dehydration and fatigue cause more failures than skill gaps.

---

## Post-Exam: Report

- **Deadline**: 24 hours after exam ends to upload report
- **Format**: PDF only, following OffSec template
- **Include per machine**:
 - All vulnerabilities discovered
 - Step-by-step exploitation walkthrough
 - Screenshots with proof commands
 - Remediation recommendations
- **Naming**: `OSCP-OS-XXXXX-Exam-Report.pdf`
- Use the OffSec-provided report template or a markdown-to-PDF pipeline
- Double-check every screenshot is included before submission
- Upload via the OffSec portal - confirm upload success
