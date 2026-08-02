# SSH - Port 22

## Banner Grab

```bash
nc -nv $IP 22
nmap -sV -p 22 $IP
```

## Login

```bash
# With password
ssh user@$IP

# With private key
chmod 600 id_rsa
ssh -i id_rsa user@$IP

# Specify port
ssh user@$IP -p 2222

# Force password auth (skip key)
ssh user@$IP -o PreferredAuthentications=password
```

## Brute Force (Last Resort)

```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://$IP
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://$IP -t 4
```

See [[Hydra]] for more options.

## Crack SSH Key Passphrase

```bash
ssh2john id_rsa > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

## Port Forwarding

```bash
# Local: access remote_host:REDACTED via localhost:REDACTED
ssh -L 8080:REDACTED:80 user@$IP

# Remote: expose your local_port on the target
ssh -R 8080:REDACTED:80 user@$IP

# Dynamic (SOCKS proxy)
ssh -D 1080 user@$IP
# Then configure proxychains: socks5 127.0.0.1 1080
```

See [[SSH-Tunneling]] for advanced pivoting.

## Known Vulnerabilities

| Version | Vuln | Impact |
|---------|------|--------|
| OpenSSH < 7.7 | CVE-2018-15473 | Username enumeration |
| OpenSSH < 6.6 | Weak key generation | Predictable keys |

```bash
# Username enumeration (OpenSSH < 7.7)
searchsploit openssh user enumeration
python3 45939.py $IP -U users.txt
```

## Tips

- Found `id_rsa` in loot? Try it against every discovered user on every SSH port.
- Check `authorized_keys` for other usernames.
- SSH config files (`~/.ssh/config`) may reveal internal hosts.
- Look for keys in web directories, FTP shares, SMB shares, backups.

## See Also

- [[Hydra]] | [[SSH-Tunneling]] | [[File-Transfers]]

## From Your Boxes

> **Sorcerer** (PG/Linux) - Found SSH keys in zip files on HTTP. Max's `.ssh` dir had `id_rsa` (no passphrase) but `authorized_keys` had a forced command (`scp_wrapper.sh`). Bypassed by uploading a modified `authorized_keys` file (removed the command prefix) via SCP using the existing key.
> - What worked: `scp -i id_rsa -O authorized_keys max@TARGET_IP:/home/max/.ssh/authorized_keys` then `ssh -i id_rsa max@TARGET_IP`
> - Lesson: If authorized_keys has a forced command, overwrite it via SCP using the same key.

> **Kiero (OSCP B)** (Course) - SNMP walk revealed SSH keys on FTP. Downloaded `id_rsa` (no passphrase) and `id_rsa_2` (encrypted). Used ssh2john on encrypted key, but the unencrypted key worked directly for SSH as john.
> - What worked: `ssh2john id_rsa` (confirmed no password), then `ssh -i id_rsa john@TARGET_IP`
> - Lesson: Always run ssh2john on found keys - if no passphrase, direct login. Try keys against every discovered user.

> **Fantastic** (PG/Linux) - Grafana path traversal CVE leaked the Grafana SQLite DB. Decrypted stored credentials revealed `sysadmin:REDACTED`, which worked for SSH even though it didn't work on the Grafana panel.
> - What worked: `ssh sysadmin@TARGET_IP` with password from decrypted Grafana DB
> - Lesson: Credentials found in one service often work on SSH. Always try creds everywhere.

> **Broker** (HTB) - After exploiting ActiveMQ CVE for initial shell, escalated by writing a generated SSH public key to `/root/.ssh/authorized_keys` via a sudo nginx misconfiguration with PUT/DAV enabled.
> - What worked: `curl -X PUT localhost:1338/root/.ssh/authorized_keys -d 'ssh-rsa AAAA...'` then `ssh -i evil_rsa root@TARGET_IP`
> - Lesson: Writing to authorized_keys is a reliable privesc path when you have arbitrary file write as root.

> **Pilgrimage** (HTB) - ImageMagick arbitrary file read CVE extracted SQLite DB containing `emily:REDACTED`. SSH login worked immediately.
> - What worked: `ssh emily@pilgrimage.htb` with creds from SQLite DB leaked via CVE
> - Lesson: Web app databases are goldmines for SSH creds. Always extract and inspect them.

> **Pandora** (HTB) - SNMP walk exposed a running process with hardcoded creds in the command line: `daniel:REDACTED`. Direct SSH login as daniel.
> - What worked: `ssh daniel@TARGET_IP` with creds from SNMP process list
> - Lesson: SNMP process lists can leak passwords in command-line arguments - always grep for creds.
