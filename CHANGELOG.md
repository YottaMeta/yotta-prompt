# 更新日志

## v0.1.0 (2026-08-28)

初始发布：

- 定位：元引 —— 意图澄清 + 生态入口（免费开源引流，后期按情况再商业化）。
- 核心机制五步：识别意图 → 2-4 候选方向 → 选一 → 深挖（目标/范围/输出/约束）→ 串联到元阁技能输出可跑提示词。
- 引擎：零依赖（Python 3.8+ 标准库）意图澄清 CLI，十个意图域（dev/analysis/planning/memory/security/logs/learning/writing/quality/general），
  关键词加权 + 技能名锁定（yotta-* / 元X），候选不足自动补「通用引导」。
- map：方向 / 技能名 → 元阁 16 技能（中文名 / 一句话 / 安装命令）+ 可直接运行的提示词模板。
- scenarios：18 个内置场景案例，覆盖任何行业（周报 / 表格 / 学习计划 / 演讲稿 / 翻译 / 会议纪要 / 合同审阅 / 头脑风暴 / 面试准备等；完整示例见 references/scenarios.md）。
- 输出 text / JSON；退出码 0 / 1 / 4。
- 常驻注入：frontmatter always-load + SKILL.md「常驻注入（必须，勿跳过）」双栏声明。
- 自包含提示词（优雅降级）：map / 场景输出为「行为优先」提示词，目标技能未安装也能直接运行；已安装则自动增强；用户一个技能都没装也可直接用。
- 测试：41 个用例全绿；含 CLI 端到端（候选 / map / scenarios / 退出码 / JSON）。
- 文档：SKILL.md + README 中英双版 + references/scenarios.md。
