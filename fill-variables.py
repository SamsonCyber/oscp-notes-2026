#!/usr/bin/env python3
"""
OSCP Notebook Variable Filler
=============================
Fill in IPs once in 00-Start-Here/Variables.md, then run:

    python3 fill-variables.py apply     # Replace placeholders with your IPs
    python3 fill-variables.py reset     # Restore all placeholders
    python3 fill-variables.py status    # Show current state (applied or placeholders)

The script keeps a backup of original placeholders so reset always works.
"""

import os
import re
import sys
import json
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).parent
VARIABLES_FILE = NOTEBOOK_DIR / "00-Start-Here" / "Variables.md"
BACKUP_FILE = NOTEBOOK_DIR / ".variables-backup.json"
# Public repo ships placeholders only. Never commit an applied backup.

# These are the placeholder tokens used throughout the notebook.
# Maps: placeholder_token -> variable_name_in_Variables.md
PLACEHOLDER_MAP = {
    "ATTACKER_IP":  "ATTACKER_IP",
    "TARGET_IP":    "STANDALONE1",   # Generic TARGET_IP maps to standalone1
    "INTERNAL_IP":  "INTERNAL_IP",
    "INTERNAL_NET": "INTERNAL_NET",
    "DC_IP":        "DC_IP",
    "MS01_IP":      "MS01_IP",
    "MS02_IP":      "MS02_IP",
    "STANDALONE1":  "STANDALONE1",
    "STANDALONE2":  "STANDALONE2",
    "STANDALONE3":  "STANDALONE3",
}

# $IP is special — it appears as a shell variable in commands.
# We handle it separately since $IP could be a legit bash variable reference.
# We replace $IP only in non-bash-variable contexts (i.e., where it's clearly a placeholder).
DOLLAR_IP_VAR = "STANDALONE1"  # $IP defaults to standalone1, but see per-file logic below

DOMAIN_PLACEHOLDER = "domain.htb"
DOMAIN_VAR = "DOMAIN"

# Files to never modify
SKIP_FILES = {"Variables.md", "fill-variables.py"}


def parse_variables() -> dict:
    """Parse Variables.md and extract key=value pairs from code blocks."""
    if not VARIABLES_FILE.exists():
        print(f"ERROR: {VARIABLES_FILE} not found!")
        print("Create it in 00-Start-Here/Variables.md with your IPs.")
        sys.exit(1)

    variables = {}
    content = VARIABLES_FILE.read_text(encoding="utf-8")

    # Match lines like: ATTACKER_IP  = 192.168.45.200
    for match in re.finditer(r"^(\w+)\s*=\s*(.+)$", content, re.MULTILINE):
        key = match.group(1).strip()
        val = match.group(2).strip()
        # Skip placeholder values (contain uppercase X, or are the default domain)
        if not val or "X" in val or val == "domain.htb":
            continue
        variables[key] = val

    return variables


def get_md_files() -> list:
    """Get all markdown files in the notebook, excluding Variables.md itself."""
    files = []
    for f in NOTEBOOK_DIR.rglob("*.md"):
        if f.name not in SKIP_FILES and ".git" not in str(f):
            files.append(f)
    return sorted(files)


def save_backup(file_contents: dict):
    """Save original file contents for reset."""
    backup = {str(k): v for k, v in file_contents.items()}
    BACKUP_FILE.write_text(json.dumps(backup, indent=2), encoding="utf-8")


def load_backup() -> dict:
    """Load original file contents from backup."""
    if not BACKUP_FILE.exists():
        return {}
    data = json.loads(BACKUP_FILE.read_text(encoding="utf-8"))
    return {Path(k): v for k, v in data.items()}


def apply_variables():
    """Replace all placeholders with actual IPs from Variables.md."""
    variables = parse_variables()

    if not variables:
        print("ERROR: No valid IPs found in Variables.md!")
        print("Fill in your IPs (replace the X placeholders with real values).")
        print()
        print("Example:")
        print("  ATTACKER_IP  = 192.168.45.200")
        print("  STANDALONE1  = 192.168.120.50")
        sys.exit(1)

    print("Variables loaded:")
    for k, v in variables.items():
        print(f"  {k:15s} = {v}")
    print()

    # Save backup of originals before any modification
    files = get_md_files()
    originals = {}
    for f in files:
        originals[f] = f.read_text(encoding="utf-8")
    save_backup(originals)

    modified_count = 0
    total_replacements = 0

    for f in files:
        content = originals[f]
        original_content = content
        replacements = 0

        # 1. Replace named placeholders (ATTACKER_IP, INTERNAL_IP, etc.)
        #    Only replace when they appear as standalone tokens, not as part of other words.
        #    But DO replace inside command strings where they're used as literal text.
        for placeholder, var_name in PLACEHOLDER_MAP.items():
            if var_name in variables and placeholder != "STANDALONE1":
                # Use word boundary to avoid partial replacements
                # But allow matches inside URLs, command args, etc.
                pattern = re.compile(r'(?<![a-zA-Z_])' + re.escape(placeholder) + r'(?![a-zA-Z_0-9])')
                new_content = pattern.sub(variables[var_name], content)
                count = len(content) - len(new_content)  # rough check
                if new_content != content:
                    replacements += len(pattern.findall(content))
                    content = new_content

        # 2. Replace $IP with the appropriate target
        #    $IP is used generically for "the current target" in enum/attack notes.
        #    We replace it contextually — but since it's a generic placeholder,
        #    map it to STANDALONE1 by default. Users can re-run with different values.
        if DOLLAR_IP_VAR in variables:
            # Match $IP but not ${IP} or $IPA etc. — must be followed by non-alphanum or EOL
            pattern = re.compile(r'\$IP(?![A-Za-z0-9_])')
            if pattern.search(content):
                new_content = pattern.sub(variables[DOLLAR_IP_VAR], content)
                replacements += len(pattern.findall(content))
                content = new_content

        # 3. Replace domain.htb with actual domain
        if DOMAIN_VAR in variables:
            if DOMAIN_PLACEHOLDER in content:
                replacements += content.count(DOMAIN_PLACEHOLDER)
                content = content.replace(DOMAIN_PLACEHOLDER, variables[DOMAIN_VAR])

        if content != original_content:
            f.write_text(content, encoding="utf-8")
            modified_count += 1
            total_replacements += replacements
            rel = f.relative_to(NOTEBOOK_DIR)
            print(f"  Updated: {rel} ({replacements} replacements)")

    print(f"\nDone! {total_replacements} replacements across {modified_count} files.")
    print("Run 'python3 fill-variables.py reset' to restore placeholders.")


def reset_variables():
    """Restore all files to their original placeholder state."""
    backup = load_backup()

    if not backup:
        print("No backup found — notes are already in placeholder state.")
        return

    restored = 0
    for filepath, original_content in backup.items():
        if filepath.exists():
            current = filepath.read_text(encoding="utf-8")
            if current != original_content:
                filepath.write_text(original_content, encoding="utf-8")
                restored += 1
                rel = filepath.relative_to(NOTEBOOK_DIR)
                print(f"  Restored: {rel}")

    # Remove backup file after successful reset
    if BACKUP_FILE.exists():
        BACKUP_FILE.unlink()

    print(f"\nDone! Restored {restored} files to placeholder state.")


def show_status():
    """Show whether notes currently have placeholders or real IPs."""
    variables = parse_variables()
    backup = load_backup()

    if backup:
        print("Status: APPLIED (real IPs are in your notes)")
        print()
        if variables:
            print("Current variables:")
            for k, v in variables.items():
                print(f"  {k:15s} = {v}")
        print()
        print(f"Backup exists with {len(backup)} files — 'reset' will restore them.")
    else:
        print("Status: PLACEHOLDERS (notes have generic placeholders)")
        print()
        if variables:
            print("Ready to apply:")
            for k, v in variables.items():
                print(f"  {k:15s} = {v}")
        else:
            print("Fill in 00-Start-Here/Variables.md first, then run 'apply'.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Usage:")
        print("  python3 fill-variables.py apply    # Fill IPs into all notes")
        print("  python3 fill-variables.py reset    # Restore placeholders")
        print("  python3 fill-variables.py status   # Check current state")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "apply":
        apply_variables()
    elif command == "reset":
        reset_variables()
    elif command == "status":
        show_status()
    else:
        print(f"Unknown command: {command}")
        print("Use: apply, reset, or status")
        sys.exit(1)


if __name__ == "__main__":
    main()
