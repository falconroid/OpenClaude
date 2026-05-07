---
name: skill-upgrade
description: "Safely upgrade existing Claude Code skills with backup, audit, and rollback. Use when fixing a skill, improving a skill, or user points out a skill defect. Never edit a live SKILL.md without this protocol."
version: 1.0.0
---

# Skill Upgrade — Safe Upgrade Protocol

Safely modify existing skills with backup, audit, reader sync, and rollback.

**Trigger**: "upgrade skill" / "fix skill" / "skill upgrade" / "skill repair" / user points out a skill defect / old skill content was deleted / need to rollback a skill

---

## Difference from Official skill-creator

The official `skill-creator` plugin handles **creating and iterating on new skills** (eval, benchmark, description optimization). It does not address the operational problem of **changing a skill that already exists in production** — where a bad edit silently corrupts behavior across all future sessions.

This skill fills that gap: upgrade as a transaction (not an edit), mechanical audit guardrails, multi-reader consistency check, and rollback. Think of it as "git with guardrails for skill files."

---

## Core Principles

1. **Active entry point never renamed**: new version writes to the same `SKILL.md`. No `SKILL-v2.md`, no `<skill>-v2` directory — avoids index fragmentation.
2. **Upgrade is a transaction, not an edit**: preflight snapshot → incremental change → audit → sync readers → changelog → verify. Any step fails, upgrade is incomplete.
3. **Default to incremental, not rewrite**: preserve existing sections and validated flows. Insert new content at the relevant location. Deleting old sections requires explicit labeling as intentional and passing audit.
4. **Scripts do mechanical protection, LLM does semantic judgment**: line count, headings, frontmatter, hash, reader consistency checked by `upgrade-guard.py`. Whether the fix actually resolves the user's issue is judged by the executor.
5. **No rollback without backup**: must have a snapshot before touching `SKILL.md`.

---

## Preconditions

Read before starting:
- Target skill's `SKILL.md` (full text)
- Target skill's `CHANGELOG.md`, if it exists
- The issue, user correction, or incident that triggered this upgrade

Locate the canonical source first if the skill exists in multiple locations.

---

## Execution Steps

### 1. Diagnose Upgrade Type

Classify the user's correction:

- **Implementation-level**: a rule is misstated, format is wrong, command is wrong → small patch.
- **Pattern-level**: same class of problem recurs → add checkpoint, but first judge if it's an anchor problem.
- **Direction-level**: the skill's generation flow or anchor is wrong → can restructure, but must explicitly list keep/replace/remove sections.
- **Incident-level**: old content already deleted, reader drift, frontmatter corruption → rollback or restore first, then upgrade.

### 2. Create Pre-Upgrade Snapshot

```bash
python3 upgrade-guard.py preflight <skill> --reason "<one-line reason>"
```

Snapshot location: `<backup-dir>/<skill>/<YYYYMMDD-HHMMSS>/`

Contains: `SKILL.md`, `manifest.json` (sha256, line count, headings, git HEAD), `headings.txt`

Backup directory is outside the skills directory to prevent agents from loading archived copies. Default: `~/.claude/skill-backups/`.

### 3. Make Incremental Changes

- List sections to change before editing; don't rewrite the whole file.
- Insert new rules near related sections.
- Don't delete original headings; if deletion is necessary, explain in CHANGELOG why the old structure no longer holds.
- Don't compress validated flows "for brevity."
- `frontmatter name:` must match directory name; `description:` use single-line quoted string.

### 4. Post-Upgrade Audit

```bash
python3 upgrade-guard.py audit <skill>
```

Default red lines:
- Line count drops >20% → fail
- Old headings lost → fail
- Frontmatter missing or `name` mismatch → fail

For genuine restructures, explicit overrides:

```bash
python3 upgrade-guard.py audit <skill> --allow-rewrite --allow-heading-loss
```

Override is not skip-audit; still read `audit.json` and `diff.patch`, explain removed sections in CHANGELOG.

### 5. Update CHANGELOG

Every upgraded skill must have a `CHANGELOG.md`. Create if missing:

```markdown
# <Skill Name> Changelog

## YYYY-MM-DD
**Driver**: <user correction / incident / insight>
**Changes**: <added, modified, removed>
**Preserved**: <key content explicitly kept from old structure>
**Deprecated**: <old rules removed; "none" if none>
**Verified**: <audit / readers / trigger-case replay results>
```

Version numbers go in changelog entries, not in active skill filenames or directory names.

### 6. Sync & Verify Readers

If you run both Claude Code and Codex (OpenCode):

```bash
# Sync skills from CC to Codex (Codex doesn't follow symlinks)
# Use OpenClaude/skill-frontmatter/sync-skills.sh or your own rsync
python3 upgrade-guard.py readers <skill>
```

`readers=PASS` confirms all readers are in sync with the canonical source.

### 7. Trigger-Case Replay

Re-run the problem that triggered this upgrade:
- Did the missed precondition → now enforced as first step?
- Did the deleted section → caught by audit?
- Did the stale reader → caught by readers check?

Write replay results into CHANGELOG `Verified` field.

---

## Rollback

List backups:

```bash
python3 upgrade-guard.py list <skill>
```

Rollback to latest:

```bash
python3 upgrade-guard.py rollback <skill>
# Then re-sync readers if applicable
```

Rollback creates a `pre-rollback-<timestamp>` snapshot first, so even the bad version isn't irreversibly lost.

---

## Safety Rules

1. **No SKILL.md edits without a preflight snapshot.** Consequence: can't distinguish "intentional deletion" from "accidental loss."
2. **No versioned copies inside the skills directory.** Consequence: agent index may load stale skill, creating invisible fork.
3. **Never edit only `~/.codex/skills/`.** Consequence: next sync overwrites your changes from the canonical source.
4. **Never claim completion after audit failure.** Consequence: bad rules persist across sessions.
5. **Never delete old flows "for brevity."** Consequence: lose historically validated operational knowledge.

## Anti-Patterns

- "I'll just rewrite a better version" → Stop. Snapshot first, then list keep/replace/remove.
- "Git has history, no need for backup" → Stop. Git is repo-level; upgrade needs operation-level snapshot + manifest.
- "Done after editing the file" → Stop. Codex reads `~/.codex/skills/`, not where you edited.
- "Old section looks repetitive, delete it" → Stop. Prove the new anchor makes the old section automatically satisfied first.
- "Name it v2 to avoid confusion" → Stop. Version goes in changelog, not the active entry point.

---

## Post-Execution Reflection

After executing this skill, spend 30 seconds:

1. Did the audit catch real risk this time?
2. Any new mechanical checks to add to `upgrade-guard.py`?
3. Any judgment still relying on LLM subjective reading — can it be scripted?
4. Any new reader types emerged (new agent tools)?
