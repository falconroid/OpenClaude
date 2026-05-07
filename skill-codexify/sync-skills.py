#!/usr/bin/env python3
"""Sync skills between directories — cross-platform replacement for rsync.

Codex/OpenCode doesn't follow symlinks (issue #8943), so this copies real files.
Equivalent to: rsync -avL --delete --exclude='.system' <source>/ <target>/

Usage:
    python3 sync-skills.py ~/vault/mind/skills ~/.codex/skills
    python3 sync-skills.py ~/.claude/skills ~/.codex/skills --dry-run
    SOURCE=~/mind/skills TARGET=~/.codex/skills python3 sync-skills.py

Env vars: SOURCE, TARGET (overridden by CLI args)
"""
import os
import shutil
import sys
from pathlib import Path


EXCLUDE_DIRS = {".system", ".git", "__pycache__"}


def sync(source: Path, target: Path, dry_run: bool = False) -> tuple[int, int, int]:
    """Sync files from source to target. Returns (copied, deleted, skipped)."""
    if not source.is_dir():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        sys.exit(1)

    copied, deleted, skipped = 0, 0, 0

    # ── Copy / update files ──
    for src_path in source.rglob("*"):
        # Skip excluded directories
        if any(p.name in EXCLUDE_DIRS for p in src_path.parents):
            continue
        if src_path.name in EXCLUDE_DIRS:
            continue

        rel = src_path.relative_to(source)
        dst_path = target / rel

        if src_path.is_dir():
            if not dry_run:
                dst_path.mkdir(parents=True, exist_ok=True)
            continue

        # Resolve symlinks — Codex needs real files (equivalent to rsync -L)
        try:
            real_src = src_path.resolve(strict=True)
        except (FileNotFoundError, RuntimeError):
            print(f"  SKIP (broken symlink): {rel}")
            skipped += 1
            continue

        # Check if copy is needed
        if dst_path.exists():
            src_stat = real_src.stat()
            dst_stat = dst_path.stat()
            if src_stat.st_size == dst_stat.st_size and src_stat.st_mtime == dst_stat.st_mtime:
                skipped += 1
                continue

        if dry_run:
            action = "UPDATE" if dst_path.exists() else "NEW"
            print(f"  [{action}] {rel}")
            copied += 1
        else:
            action = "UPDATE" if dst_path.exists() else "NEW"
            print(f"  [{action}] {rel}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(real_src, dst_path)
            copied += 1

    # ── Delete stale files in target (equivalent to rsync --delete) ──
    if target.is_dir():
        for dst_path in target.rglob("*"):
            if any(p.name in EXCLUDE_DIRS for p in dst_path.parents):
                continue
            if dst_path.name in EXCLUDE_DIRS:
                continue

            rel = dst_path.relative_to(target)
            src_path = source / rel

            if not src_path.exists() and not src_path.is_symlink():
                if dst_path.is_dir():
                    if not dry_run and not any(dst_path.iterdir()):
                        dst_path.rmdir()
                        print(f"  [DEL] {rel}/")
                        deleted += 1
                else:
                    if not dry_run:
                        dst_path.unlink()
                    print(f"  [DEL] {rel}")
                    deleted += 1

    return copied, deleted, skipped


def count_skills(target: Path) -> int:
    if not target.is_dir():
        return 0
    return len(list(target.glob("*/SKILL.md")))


def list_skills(target: Path) -> list[str]:
    if not target.is_dir():
        return []
    skills = []
    for sf in sorted(target.glob("*/SKILL.md")):
        skills.append(sf.parent.name)
    return skills


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry_run = "--dry-run" in sys.argv[1:]

    source = Path(args[0]) if len(args) >= 1 else Path(
        os.environ.get("SOURCE", str(Path.home() / ".claude" / "skills"))
    )
    target = Path(args[1]) if len(args) >= 2 else Path(
        os.environ.get("TARGET", str(Path.home() / ".codex" / "skills"))
    )

    print(f"→ Syncing skills from {source} to {target}")
    if dry_run:
        print("  (dry-run, no changes)")
    print()

    copied, deleted, skipped = sync(source, target, dry_run=dry_run)

    print()
    if dry_run:
        print(f"Would copy: {copied} | Would delete: {deleted} | Unchanged: {skipped}")
    else:
        print(f"Copied: {copied} | Deleted: {deleted} | Skipped: {skipped}")

    skill_count = count_skills(target)
    print(f"\n→ Skill count: {skill_count}")

    skills = list_skills(target)
    if skills:
        print("→ Skills:")
        for s in skills:
            print(f"    {s}")


if __name__ == "__main__":
    main()
