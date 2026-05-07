# Session Log — OpenClaude

## 2026-05-07
- **做了什么**：初始化 OpenClaude 项目。从 cc-maintain 提取 statusline、skill-frontmatter、skill-builder、skill-upgrade 四个包
- **决策**：mind skills 保持 canonical 源不变，本项目是泛化快照；skill-builder 和 skill-upgrade 分开（不是合并）；泛化规则写入 GENERALIZATION.md
- **教训**：skill-tools 合并后在触发精确度和 context 效率上不如分开；官方 skill-creator 与我们的 builder 是互补关系（创建→维护）
- **下一步**：无
- **阻塞项**：无
