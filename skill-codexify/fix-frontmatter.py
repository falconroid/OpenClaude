#!/usr/bin/env python3
"""Fix YAML frontmatter for Codex compatibility.

Codex SKILL.md frontmatter validation is stricter than Claude Code:
- Colons/special chars in unquoted description strings → parse failure
- Double --- blocks → treated as empty frontmatter
- Multi-line descriptions (|, >) → not always handled

Usage:
    python fix-frontmatter.py ~/vault/mind/skills
    python fix-frontmatter.py ~/.codex/skills --check   # dry-run, report only
"""
import os, re, sys

def yaml_safe(s: str) -> str:
    if any(c in s for c in [':', '#', '{', '}', '[', ']', '&', '*', '!', '|', '>', '%', '@', '`']):
        return '"' + s.replace('"', '\\"') + '"'
    return s

def fix_frontmatter(filepath: str):
    skill = os.path.basename(os.path.dirname(filepath))
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix `## name:skillnamedescription:` → proper YAML
    content = re.sub(
        r'^---\s*\n\s*\n\s*## name:\s*(\S+)description:\s*(.+)',
        r'---\nname: \1\ndescription: "\2"\n---',
        content, flags=re.MULTILINE)

    # Fix bare `## name:` lines
    content = re.sub(
        r'^## name:\s*(\S+)\s*$',
        r'name: \1',
        content, flags=re.MULTILINE)

    # Fix double --- blocks
    content = re.sub(r'^---\s*\n---\s*\n(name:)', r'---\n\1', content, flags=re.MULTILINE)
    content = re.sub(r'^---\n\s*\n---\n', r'---\n', content, flags=re.MULTILINE)

    # Collapse multi-line descriptions (|, >, "|") into single quoted line
    content = re.sub(
        r'^description: "\|"\n((?:  .+\n?)+)',
        lambda m: 'description: "' + ' '.join(
            line.strip() for line in m.group(1).strip().split('\n')
        ).replace('"', '\\"')[:300] + '"',
        content, flags=re.MULTILINE)
    content = re.sub(
        r'^description: [|>]\n((?:  .+\n?)+)',
        lambda m: 'description: "' + ' '.join(
            line.strip() for line in m.group(1).strip().split('\n')
        ).replace('"', '\\"')[:500] + '"',
        content, flags=re.MULTILINE)

    # Fix unquoted description values within frontmatter
    parts = content.split('---', 2)
    if len(parts) >= 3:
        fm = parts[1]
        body = parts[2]
        new_lines = []
        for line in fm.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('description:'):
                val = line[len('description:'):].strip()
                if val.startswith('"') and val.endswith('"'):
                    new_lines.append(line)
                else:
                    new_lines.append(f'description: {yaml_safe(val)}')
            else:
                new_lines.append(line)
        content = '---\n' + '\n'.join(new_lines) + '\n---' + body
    else:
        body = content.strip()
        desc = ""
        for bline in body.split('\n'):
            if bline.startswith('# '):
                desc = bline[2:].strip()
                break
        if not desc:
            desc = body[:100].replace('\n', ' ').strip()
        content = f'---\nname: {skill}\ndescription: {yaml_safe(desc)}\n---\n\n{body}'

    if content != original:
        return 'FIXED', content
    return 'OK', None

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix-frontmatter.py <skills-dir> [--check]", file=sys.stderr)
        sys.exit(1)

    skills_dir = sys.argv[1]
    check_only = '--check' in sys.argv

    fixed = 0
    for entry in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        sf = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(sf):
            continue
        result, new_content = fix_frontmatter(sf)
        if result == 'FIXED':
            if not check_only:
                with open(sf, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            print(f'  FIXED  {entry}')
            fixed += 1

    action = "would fix" if check_only else "fixed"
    print(f'\n{action}: {fixed}')
    if check_only and fixed > 0:
        print("Run without --check to apply fixes.")

if __name__ == '__main__':
    main()
