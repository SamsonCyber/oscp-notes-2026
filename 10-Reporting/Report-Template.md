# OSCP Exam Report

> **People who hack all the machines but write a bad report FAIL.** This is not hypothetical — it happens every exam cycle. OffSec grades your report, not your hacking. If a reader can't reproduce your steps, you get 0 for that machine.

---

## Use the Official Template

**Download the OffSec-provided report template BEFORE exam day:**
- Check the [Exam Guide](https://help.offsec.com/hc/en-us/articles/360040165632) for the current link
- It's a Word/Markdown template — fill in the blanks
- Using their template guarantees you don't miss required sections
- **Do NOT freelance the format** — use theirs

---

## Required Per Machine

### 1. Service Enumeration
- Full nmap output (paste the relevant scan)
- Any additional enumeration (gobuster, smbclient, etc.)

### 2. Vulnerability Identification
- **Name the vulnerability** (e.g., "Unauthenticated Remote Code Execution in Apache Struts 2.5.12 (CVE-2017-5638)")
- **Severity**: Critical / High / Medium / Low
- Brief description of what makes it exploitable

### 3. Exploitation / Initial Access
- **Step-by-step commands** — EVERY command, in order
- Screenshots of key output (shell obtained, first output)
- If you modified an exploit: show what you changed and why
- **local.txt proof screenshot**

### 4. Privilege Escalation
- What misconfiguration/vulnerability you found
- **Step-by-step commands** — EVERY command
- Screenshots of key steps
- **proof.txt proof screenshot**

### 5. Remediation
- How to fix each vulnerability (OffSec REQUIRES this)
- Example: "Update Apache Struts to version X.Y.Z", "Remove SUID bit from /usr/bin/find", "Disable anonymous LDAP bind"

---

## AD Set — Show the FULL Chain

The AD report must show the COMPLETE attack path as one connected narrative:

1. **Machine 1**: How you got initial foothold (web app? spray? SMB?)
2. **Credentials discovered**: What, where, how
3. **Machine 2**: How you moved laterally (PtH? cred reuse? ACL abuse?)
4. **DC compromise**: Final escalation (DCSync? secretsdump? delegation abuse?)
5. proof.txt from DC

**Every step must connect to the next.** "I found creds in a config file on Machine 1, sprayed them, and got WinRM on Machine 2" — that's the narrative OffSec wants.

---

## Proof Screenshots — EXACT Requirements

### Linux
```bash
whoami && hostname && ip addr && cat /home/user/local.txt
whoami && hostname && ip addr && cat /root/proof.txt
```

### Windows
```cmd
whoami && hostname && ipconfig && type C:\Users\user\Desktop\local.txt
whoami && hostname && ipconfig && type C:\Users\Administrator\Desktop\proof.txt
```

**Requirements:**
- Must be an **interactive shell** (not webshell, not LFI, not script output)
- All proof commands + flag visible in **one screenshot**
- Use `&&` to chain commands so they appear together
- Flag hash must be fully visible (not cut off)

---

## Report Killers (Why People Fail)

| Mistake | Consequence |
|---------|-------------|
| Missing remediation section | Machine not scored |
| Vague steps ("I ran the exploit") | Machine not scored — must be reproducible |
| Screenshot doesn't show whoami/hostname/ip | Proof not accepted |
| Proof from non-interactive shell | Proof not accepted |
| Wrong report format (not PDF) | Report rejected |
| Submitted after 24-hour deadline | Report rejected |
| Forgot to submit flags in control panel | 0 points regardless of report |
| Modified exploit without showing changes | Reviewer can't reproduce |

---

## Report Workflow During Exam

1. **As you work**: paste every command into your notes immediately
2. **After each flag**: take proof screenshot RIGHT NOW, submit flag in panel
3. **After each machine**: spend 5 minutes organizing notes while fresh
4. **After exam**: you have 24 hours — use the official template, paste your notes in, add screenshots, write remediation
5. **Before submitting**: re-read every machine section — can a stranger reproduce this?

---

## Tools

- **Official template**: Download from OffSec portal (do this before exam day)
- **Screenshots**: Flameshot (`flameshot gui`) — annotate screenshots if helpful
- **Terminal logging**: `script -a ~/oscp-exam/terminal.log` on every terminal
- **Markdown to PDF**: `pandoc report.md -o report.pdf` or export from the template
- **File name**: `OSCP-OS-XXXXX-Exam-Report.pdf` (your OS-ID)
- Upload via OffSec portal — **confirm the upload succeeded**
