# OpenClaude — CC/Codex 工具与技能开源合集

> 从 mind skills 泛化后发布。本地 `~/vault/mind/skills/` 是 canonical 源，本项目是裁剪快照。

## 泛化规则

见 [GENERALIZATION.md](GENERALIZATION.md)。

核心原则：
- 去掉所有 `~/vault/mind/`、`/home/aegis/` 等个人路径
- 去掉 OpenClaw、soul-vault、stream capture、飞书 wiki 等个人基础设施引用
- 默认路径假设标准 CC + Codex 安装（`~/.claude/skills/`、`~/.codex/skills/`）
- 可配置的用 env var（`SKILLS_HOME`、`SKILLS_BACKUP`、`CODEX_SKILLS`）
- Codex 相关能力保留（Codex 是公开工具），仅去掉个人特定配置

## Git 边界

本项目独立 `.git`，不上溯到 `~/vault`。
