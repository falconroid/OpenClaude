# Skill Builder

Create well-structured Claude Code skills with required sections, quality standards, and a built-in self-improvement loop.

## vs. Official skill-creator

Claude Code ships with an official `skill-creator` plugin. Here's how they differ:

| | Official skill-creator | Skill Builder (this) |
|---|---|---|
| **Focus** | Design, test, iterate, benchmark | Structure, discipline, maintainability |
| **Process** | interview → draft → eval → grade → benchmark → repeat | 6 required sections → quality checklist → post-execution reflection |
| **Key tool** | `run_eval.py` (parallel test runs) | The 6-section template + reflection loop |
| **Output** | Quantitatively validated skill | Structurally complete, maintainable skill |
| **When to use** | You're designing a skill and want to measure if it works | You know what you want and need the right skeleton |

They're complementary. Think: official plugin = design sprint. This = coding standards.

## What This Covers

- 6 required sections every SKILL.md needs
- Quality standards (repeatable, bounded, safe, evolving, deterministic-first)
- Post-execution reflection for self-improving skills
- Codex/OpenCode compatibility notes
- Pointer to skill-upgrade for safe modification

## Install

```bash
# Ensure CC discovers this skill
mkdir -p ~/.claude/skills/skill-builder
cp SKILL.md ~/.claude/skills/skill-builder/SKILL.md
```

## Requirements

- Claude Code
