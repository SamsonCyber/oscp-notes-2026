# Web Application Testing Methodology

Master checklist - work through sequentially for every web target.

## 1. Technology Identification

```bash
whatweb http://$IP
```

Check response headers in Burp or:
```bash
curl -I http://$IP
```

Use Wappalyzer browser extension for CMS/framework/language detection.

## 2. Directory and File Bruteforce

```bash
# Match extensions to detected tech stack
gobuster dir -u http://$IP -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 50

feroxbuster -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -x php,asp,aspx,jsp,html,txt
```

## 3. Check Common Paths

```
/robots.txt
/sitemap.xml
/.git/
/.DS_Store
/backup/
/wp-config.php.bak
/web.config.old
/.env
```

```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/common.txt -x bak,old,zip,tar.gz,swp,txt
```

## 4. View Source on Every Page

- Read HTML comments
- Check linked JS files for endpoints, API keys, credentials
- Look for hidden form fields
- Note all URL parameters

## 5. Test Default Credentials

Google "[software name] default credentials" - always try before bruteforce.

See [[Authentication-Bypass]] for common defaults.

## 6. Identify All Input Points

- Forms (login, search, contact, file upload)
- URL parameters (?id=, ?page=, ?file=, ?user=)
- Cookies
- HTTP headers (User-Agent, Referer, X-Forwarded-For)

## 7. Test Each Input For

| Vulnerability | Link |
|---|---|
| SQL Injection | [[SQL-Injection]] |
| Command Injection | [[Command-Injection]] |
| Local/Remote File Inclusion | [[LFI-RFI]] |
| Cross-Site Scripting | [[XSS]] |
| Server-Side Template Injection | [[SSTI]] |
| Directory Traversal | [[Directory-Traversal]] |

## 8. File Upload

If file upload exists → [[File-Upload]]

## 9. SSRF

If the app makes server-side requests (URL fetch, webhooks, PDF generation) → [[SSRF]]

## 10. API Enumeration

```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
```

Check: `/api`, `/v1`, `/v2`, `/swagger`, `/swagger-ui`, `/graphql`, `/graphiql`

## 11. Cookie Analysis

- Base64 decode cookies: `echo "cookie_value" | base64 -d`
- Check for JWT: paste into jwt.io
- Look for predictable session IDs

## 12. Authentication Bypass

Try [[Authentication-Bypass]] techniques: SQLi on login, parameter manipulation, forced browsing, 403 bypass.
