# SMTP - Port 25 (also 465, 587)

## User Enumeration

```bash
# VRFY method
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/Names/names.txt -t $IP

# RCPT method (if VRFY disabled)
smtp-user-enum -M RCPT -U /usr/share/seclists/Usernames/Names/names.txt -t $IP

# EXPN method
smtp-user-enum -M EXPN -U /usr/share/seclists/Usernames/Names/names.txt -t $IP
```

## Nmap Scripts

```bash
nmap --script smtp-commands,smtp-enum-users,smtp-vuln-cve2010-4344,smtp-open-relay -p 25 $IP
```

## Manual Enumeration

```bash
telnet $IP 25
# or
nc -nv $IP 25

HELO test
VRFY root
VRFY admin
MAIL FROM: attacker@test.com
RCPT TO: user@domain.htb # 250 = exists, 550 = doesn't
```

## Send Email (Client-Side Attacks)

```bash
# Using swaks
swaks --to victim@domain.htb --from attacker@test.com --server $IP --header "Subject: Important" --body "Click here" --attach @malicious.pdf

# Simple send
sendemail -f attacker@test.com -t victim@domain.htb -s $IP -u "Subject" -m "Body" -a attachment.pdf
```

## POP3 - Port 110

```bash
telnet $IP 110
USER admin
PASS admin
LIST # List messages
RETR 1 # Read message 1
```

## IMAP - Port 143

```bash
telnet $IP 143
a1 LOGIN user password
a2 LIST "" "*" # List mailboxes
a3 SELECT INBOX
a4 FETCH 1 BODY[] # Read message 1
```

## Tips

- SMTP user enumeration can reveal valid system usernames for SSH/other brute force.
- Check for open relay - can send emails as anyone.
- Read all emails - they often contain passwords or hints.

## See Also

- [[Hydra]] | [[Nmap]]

## From Your Boxes

> **PostFish** (PG/Linux) - SMTP user enum with a CeWL-generated wordlist found users `Sales` and `Legal`. Logged into POP3 as `sales:REDACTED` and read an email from IT about password resets. Sent a phishing email via SMTP as IT to `brian.moore@postfish.off` with a link to Kali. Caught Brian's creds (`brian.moore:REDACTED`) via nc listener when he clicked the link. SSH as brian for initial access.
> - What worked: `nc -v postfish.off 25` then `MAIL FROM: it@postfish.off` / `RCPT TO: brian.moore@postfish.off` with phishing body pointing to Kali IP
> - Lesson: SMTP + POP3 open = read emails for context, then phish users by impersonating internal senders. Always check for open relay.

> **PostFish** (PG/Linux) - Privesc also used SMTP: the postfix disclaimer script ran on every email. As user filter (with write access to the script), injected a reverse shell into `/etc/postfix/disclaimer`, then sent another email via SMTP to trigger it. Got shell as filter, then `sudo mail --exec='!/bin/sh'` for root.
> - What worked: Injected reverse shell into `/etc/postfix/disclaimer`, triggered by sending email via `nc -v postfish.off 25`
> - Lesson: Postfix disclaimer scripts execute on email delivery - if writable, instant code execution.

> **SolidState** (HTB) - Port 25 (SMTP) open alongside POP3 (110) and NNTP (119). The SMTP/POP3 combo indicated a mail server worth enumerating for user emails containing creds or hints.
