#!/usr/bin/env python3
"""Guard rails for upgrading skills.

Active skill path stays stable:
  <skills>/<skill>/SKILL.md

Backups live outside the skill registry so agents do not load archived copies:
  <backup-dir>/<skill>/<timestamp>/

Configuration via env vars:
  SKILLS_HOME   — canonical skills directory (default: ~/.claude/skills)
  SKILLS_BACKUP — backup directory (default: ~/.claude/skill-backups)
  CODEX_SKILLS  — Codex/OpenCode skills directory (default: ~/.codex/skills)
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SKILLS_ROOT = Path(os.environ.get("SKILLS_HOME", Path.home() / ".claude" / "skills"))
BACKUPS = Path(os.environ.get("SKILLS_BACKUP", Path.home() / ".claude" / "skill-backups"))
CODEX_SKILLS = Path(os.environ.get("CODEX_SKILLS", Path.home() / ".codex" / "skills"))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def skill_dir(skill: str) -> Path:
    if "/" in skill or skill in {"", ".", ".."}:
        fail(f"invalid skill name: {skill!r}")
    return SKILLS_ROOT / skill


def skill_file(skill: str) -> Path:
    return skill_dir(skill) / "SKILL.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(text: str) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def headings(text: str) -> list[str]:
    result: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+\S", line):
            result.append(line.strip())
    return result


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    raw = text[4:end].strip()
    parsed: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip('"').strip("'")
    return parsed


def snapshot_metadata(skill: str, path: Path, reason: str) -> dict[str, object]:
    text = read_text(path)
    git_head = ""
    try:
        git_head = subprocess.check_output(
            ["git", "-C", str(path.parent.parent), "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        git_head = "unknown"

    return {
        "skill": skill,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "reason": reason,
        "source": str(path),
        "sha256": sha256(path),
        "lines": line_count(text),
        "bytes": path.stat().st_size,
        "frontmatter": frontmatter(text),
        "headings": headings(text),
        "git_head": git_head,
    }


def resolve_backup(skill: str, requested: str) -> Path:
    root = BACKUPS / skill
    if requested == "latest":
        if not root.exists():
            fail(f"no backups found for {skill}")
        candidates = sorted([p for p in root.iterdir() if p.is_dir()])
        if not candidates:
            fail(f"no backups found for {skill}")
        return candidates[-1]
    path = root / requested
    if not path.is_dir():
        fail(f"backup not found: {path}")
    return path


def command_preflight(args: argparse.Namespace) -> None:
    path = skill_file(args.skill)
    if not path.is_file():
        fail(f"active skill file not found: {path}")

    text = read_text(path)
    fm = frontmatter(text)
    if fm.get("name") != args.skill:
        fail(
            f"frontmatter name must equal directory name: "
            f"expected {args.skill!r}, got {fm.get('name')!r}"
        )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = BACKUPS / args.skill / timestamp
    dest.mkdir(parents=True, exist_ok=False)
    shutil.copy2(path, dest / "SKILL.md")

    metadata = snapshot_metadata(args.skill, path, args.reason or "")
    (dest / "manifest.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (dest / "headings.txt").write_text(
        "\n".join(metadata["headings"]) + "\n", encoding="utf-8"
    )

    print(f"backup={dest}")
    print(f"lines={metadata['lines']} sha256={metadata['sha256']}")


def write_audit_report(
    backup: Path, old_text: str, new_text: str, result: dict[str, object]
) -> None:
    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile=str(backup / "SKILL.md"),
        tofile="active/SKILL.md",
        lineterm="",
    )
    report = {
        **result,
        "audited_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    (backup / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (backup / "diff.patch").write_text("\n".join(diff) + "\n", encoding="utf-8")


def command_audit(args: argparse.Namespace) -> None:
    path = skill_file(args.skill)
    if not path.is_file():
        fail(f"active skill file not found: {path}")
    backup = resolve_backup(args.skill, args.backup)
    old_path = backup / "SKILL.md"
    if not old_path.is_file():
        fail(f"backup missing SKILL.md: {backup}")

    old_text = read_text(old_path)
    new_text = read_text(path)
    old_lines = line_count(old_text)
    new_lines = line_count(new_text)
    min_lines = int(old_lines * (1 - args.max_line_loss_pct / 100.0))
    old_headings = headings(old_text)
    new_heading_set = set(headings(new_text))
    lost_headings = [h for h in old_headings if h not in new_heading_set]
    fm = frontmatter(new_text)

    errors: list[str] = []
    warnings: list[str] = []

    if fm.get("name") != args.skill:
        errors.append(
            f"frontmatter name mismatch: expected {args.skill!r}, got {fm.get('name')!r}"
        )
    if "description" not in fm:
        errors.append("frontmatter missing description")
    if new_lines < min_lines and not args.allow_rewrite:
        errors.append(
            f"line count dropped from {old_lines} to {new_lines} "
            f"({new_lines - old_lines}); threshold allows minimum {min_lines}"
        )
    if lost_headings and not args.allow_heading_loss:
        errors.append(f"lost {len(lost_headings)} existing headings")
    elif lost_headings:
        warnings.append(f"lost headings allowed: {len(lost_headings)}")

    result = {
        "skill": args.skill,
        "backup": str(backup),
        "old_lines": old_lines,
        "new_lines": new_lines,
        "line_delta": new_lines - old_lines,
        "old_sha256": sha256(old_path),
        "new_sha256": sha256(path),
        "lost_headings": lost_headings,
        "errors": errors,
        "warnings": warnings,
    }
    write_audit_report(backup, old_text, new_text, result)

    print(f"old_lines={old_lines} new_lines={new_lines} delta={new_lines - old_lines}")
    if lost_headings:
        print("lost_headings:")
        for heading in lost_headings:
            print(f"  {heading}")
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"  {warning}")
    if errors:
        print("errors:")
        for error in errors:
            print(f"  {error}")
        print(f"audit_report={backup / 'audit.json'}")
        print(f"diff={backup / 'diff.patch'}")
        sys.exit(2)

    print("audit=PASS")
    print(f"audit_report={backup / 'audit.json'}")
    print(f"diff={backup / 'diff.patch'}")


def command_readers(args: argparse.Namespace) -> None:
    active = skill_file(args.skill)
    if not active.is_file():
        fail(f"active skill file not found: {active}")

    active_hash = sha256(active)
    errors: list[str] = []
    info: list[str] = []

    # Codex/OpenCode reader (optional — not everyone runs Codex)
    codex = CODEX_SKILLS / args.skill / "SKILL.md"
    if codex.is_file():
        if sha256(codex) != active_hash:
            errors.append(f"Codex reader stale: {codex}")
        else:
            info.append(f"Codex: OK")
    else:
        info.append(f"Codex: not present (ok if not using Codex)")

    if errors:
        for line in info:
            print(f"INFO: {line}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)

    for line in info:
        print(f"INFO: {line}")
    print("readers=PASS")


def command_rollback(args: argparse.Namespace) -> None:
    active = skill_file(args.skill)
    backup = resolve_backup(args.skill, args.backup)
    source = backup / "SKILL.md"
    if not source.is_file():
        fail(f"backup missing SKILL.md: {backup}")
    if not active.parent.is_dir():
        fail(f"active skill directory missing: {active.parent}")

    emergency = (
        BACKUPS / args.skill / f"pre-rollback-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    emergency.mkdir(parents=True, exist_ok=False)
    if active.exists():
        shutil.copy2(active, emergency / "SKILL.md")
        (emergency / "manifest.json").write_text(
            json.dumps(
                snapshot_metadata(args.skill, active, "automatic pre-rollback snapshot"),
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    shutil.copy2(source, active)
    print(f"restored={active}")
    print(f"from={source}")
    print(f"pre_rollback_snapshot={emergency}")


def command_list(args: argparse.Namespace) -> None:
    root = BACKUPS / args.skill
    if not root.exists():
        print(f"no backups for {args.skill}")
        return
    for item in sorted(root.iterdir()):
        if not item.is_dir():
            continue
        manifest = item / "manifest.json"
        reason = ""
        lines = ""
        if manifest.is_file():
            data = json.loads(read_text(manifest))
            reason = data.get("reason", "")
            lines = str(data.get("lines", ""))
        print(f"{item.name}\tlines={lines}\t{reason}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Skill upgrade guard: preflight, audit, readers, rollback."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    preflight = sub.add_parser("preflight", help="Create a pre-upgrade snapshot.")
    preflight.add_argument("skill")
    preflight.add_argument("--reason", default="")
    preflight.set_defaults(func=command_preflight)

    audit = sub.add_parser("audit", help="Audit active SKILL.md against a backup.")
    audit.add_argument("skill")
    audit.add_argument("--backup", default="latest")
    audit.add_argument("--max-line-loss-pct", type=float, default=20.0)
    audit.add_argument("--allow-rewrite", action="store_true")
    audit.add_argument("--allow-heading-loss", action="store_true")
    audit.set_defaults(func=command_audit)

    readers = sub.add_parser("readers", help="Check Codex copy matches canonical source.")
    readers.add_argument("skill")
    readers.set_defaults(func=command_readers)

    rollback = sub.add_parser("rollback", help="Restore from a backup snapshot.")
    rollback.add_argument("skill")
    rollback.add_argument("--backup", default="latest")
    rollback.set_defaults(func=command_rollback)

    list_cmd = sub.add_parser("list", help="List backups for a skill.")
    list_cmd.add_argument("skill")
    list_cmd.set_defaults(func=command_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
