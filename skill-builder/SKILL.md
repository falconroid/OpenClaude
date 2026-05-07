---
name: skill-builder
description: "Create new Claude Code skills with proper structure, required sections, and quality standards. Use when user wants to create a skill, document a workflow, or turn a repeated process into a skill."
version: 1.0.0
---

# Skill Builder — Structure Standards for New Skills

Create well-structured skills that are repeatable, safe, and self-evolving.

**Trigger**: "create skill" / "new skill" / "build a skill" / "turn this into a skill" / "document this workflow"

---

## Difference from Official skill-creator

The official `skill-creator` plugin focuses on **design + iterate + benchmark**: draft a skill, run evals, grade outputs, optimize the description for trigger accuracy, package as `.skill` file. It helps you answer "is this skill good enough?"

This skill focuses on **structure + discipline**: what sections every skill must have, how to write them so a fresh CC session can execute correctly, and how to build in a self-improvement loop. It helps you answer "is this skill complete and maintainable?"

They're complementary. Use official skill-creator to iterate and test; use this to ensure the skeleton is solid and the skill won't rot.

---

## File Structure

```
<skill-name>/
├── SKILL.md          # Required — complete skill definition
├── CHANGELOG.md      # Created on first upgrade
└── scripts/          # Optional — bundled scripts
```

## Required Sections (All 6)

Every skill must include these six sections. They can be merged but not omitted.

### 1. Title + One-Liner

```markdown
# Skill Name — what it does in one sentence
```

### 2. Trigger

When CC should activate this skill:

```markdown
**Trigger**: "keyword" / "keyword" / condition
```

### 3. Core Principles

3-5 non-negotiable rules that define how this skill operates.

### 4. Execution Steps

Concrete, repeatable sequence. Scripts can be referenced but steps must be described in the doc. Another CC session reading only this SKILL.md should be able to execute.

### 5. Safety Rules

What must never happen. Format: `N. Rule — consequence of violation.`

### 6. Post-Execution Reflection

```markdown
## Post-Execution Reflection

After executing this skill, spend 30 seconds asking:

1. Any pitfalls this run? Steps more complex or error-prone than expected?
2. Any new edge cases? Scenarios not previously considered?
3. Can the flow be smoother? Any repeated operations that could be scripted?
4. Any safety rules to add? Moments where we almost violated a safety rule?

If findings → update this SKILL.md (use skill-upgrade for safe edits).
Not every run has findings, but every run asks the questions.
```

## Optional Sections

| Section | When |
|---------|------|
| Input/Output format | Structured data |
| Relationship to other skills | Upstream/downstream dependencies |
| Fault recovery | External systems or irreversible operations |
| State files | Persistent state |
| Cron/scheduled triggers | Timer-based execution |

## Quality Standards

- **Repeatable**: a fresh CC session reading only SKILL.md can execute correctly
- **Bounded**: explicitly states what is NOT this skill's job
- **Safe**: lists iron rules, errs on the side of listing more
- **Evolving**: improves via post-execution reflection
- **Deterministic-first**: scripts/hooks over LLM judgment for mechanical checks. LLM only for semantic understanding

## Codex / OpenCode Users

If you share skills between Claude Code and Codex (OpenCode):

- Codex YAML parser is stricter: special characters in `description:` must be quoted, multi-line descriptions collapsed, double `---` blocks removed. See `skill-frontmatter` package for a fixer script.
- Codex does not follow symlinks (issue [#8943](https://github.com/anthropics/codex/issues/8943)). Copy skills as real files or rsync.
- After creating a skill, run `skill-frontmatter/fix-frontmatter.py` on the Codex copy.

## Creating a Skill

1. Confirm single responsibility — one skill, one job
2. Write SKILL.md with all 6 required sections
3. Place in `~/.claude/skills/<name>/SKILL.md`
4. If using Codex, sync with rsync + fix frontmatter
5. Test: simulate trigger, verify CC activates and executes
6. Run post-execution reflection after first real use

## Upgrading an Existing Skill → Use skill-upgrade

Creating is different from modifying. When you need to change an existing skill, use the **skill-upgrade** package: preflight snapshot → incremental edit → audit → reader sync → changelog → rollback safety net. Never edit a live SKILL.md without a backup snapshot.
