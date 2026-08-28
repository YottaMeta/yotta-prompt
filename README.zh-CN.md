<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-prompt banner" width="100%" />
</p>

<h1 align="center">yotta-prompt · 元引 (YuanYin)</h1>

<p align="center">YottaMeta 的 <b>意图澄清 + 生态入口</b> 技能：用户输入一句模糊的话 / 一个词时，识别意图、
给出 <b>2-4 个候选方向</b>、深挖（目标 / 范围 / 输出 / 约束），再串联到对应元阁技能，
输出<b>可直接运行的提示词</b>。</p>
<p align="center">触发场景：用户不知道怎么提问、不知道想要什么、输入模糊的一句话 / 一个词时 —
<b>每次新会话开始自动注入（always-load）</b>，接住「不会用 AI」的用户。</p>
<p align="center">零外部依赖（Python 3.8+ 标准库）；Windows + Linux + macOS；纯本地离线，不联网、不调外部服务。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-prompt"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

很多人不会跟 AI 说话：打一句模糊的话、一个词，期待被帮助，却说不清自己到底想要什么。
元引是元阁技能家族的<b>门</b>——把「不知道怎么问」变成「能直接跑的任务」。

它走五步流程：**① 识别意图 → ② 给 2-4 个候选方向 → ③ 确认 → ④ 深挖（目标 / 范围 / 输出 / 约束）→
⑤ 串联到对应元阁技能，输出能直接运行的提示词。**

它不是 prompt 美化器。提示词润色是红海；元引只做「把模糊的话补全成可执行任务」这一件事。

## 核心价值

- **意图澄清，不做 prompt 美化**——把模糊词变成可执行任务，第一步绝不替用户下结论。
- **十个意图域**——开发 / 数据 / 计划 / 记忆 / 安全 / 日志 / 学习 / 写作 / 质量 / 通用，中文 + 英文关键词加权（纯本地）。行业无关：写周报、做表格、定计划、写演讲稿、翻译、会议纪要、审合同、头脑风暴、面试准备等都能接。
- **技能名锁定**——输入提到 `yotta-*` 或家族中文名（元忆 / 元安 / …）时，立即锁定到对应方向。
- **生态入口**——每个方向映射到对应元阁技能，带中文名、一句话说明与安装命令。
- **可跑提示词**——每个方向内置一条提示词模板，填上信息即可运行。
- **场景案例库**——18 个完整走查、覆盖任何行业（模糊输入 → 候选 → 深挖 → 串联），见 `references/scenarios.md`。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **常驻注入** | `always-load: true`，会话开始即生效；接住「永远不会主动加载技能」的用户 |
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 数据库 / 联网；Windows + Linux + macOS |
| **一个技能都没装也能用** | 提示词是自包含的行为描述；元阁技能是可选加速器，不是硬依赖 |
| **纯本地离线** | 意图分类与映射全部本地完成，不调外部服务 |
| **边界诚实** | 只澄清意图——不预设立场、不做安全评审；提示词不人为设限（不违规 / 不犯法 / 不越狱） |
| **生态分发** | GitHub + npm + ClawHub 三源同步；npx / install.sh / 手动复制均可安装 |

## 命令一览

| 命令 | 说明 |
|---|---|
| clarify | 一句话 / 一个词 → 2-4 个候选方向（各带中文说明） |
| clarify --json | 结构化候选，供程序消费 |
| clarify --top N | 控制候选数量（2-4，默认 4） |
| map | 方向 / 技能名 → 元阁技能 + 安装命令 + 可跑提示词 |
| map --json | 结构化映射结果 |
| scenarios | 列出内置场景案例 |
| --version | 显示版本 |

## 使用示例

Windows 用 python，Linux/macOS 用 python3。

```bash
# 意图澄清：一句话 / 一个词 → 2-4 个候选方向
python3 scripts/yotta_prompt.py clarify "帮我写一封邮件"

# JSON 输出（供程序消费）
python3 scripts/yotta_prompt.py clarify "记一下这个" --json

# 控制候选数量
python3 scripts/yotta_prompt.py clarify "怎么学 python" --top 3

# 方向 / 技能名 → 元阁技能 + 安装命令 + 可跑提示词
python3 scripts/yotta_prompt.py map 写作
python3 scripts/yotta_prompt.py map yotta-humanize --json

# 内置场景案例
python3 scripts/yotta_prompt.py scenarios
```

退出码：**0** = 成功；**1** = 未识别（已给引导）；**4** = 用法或读取错误。

示例输出：

```
元引 yotta-prompt v0.1.0 —— 意图澄清
输入：「帮我写一封邮件」

我猜你想做这几件事（回复数字选择，或直接说出你的选择）：

1. 写作与语言（writing）
   · 命中关键词：邮件
   · 可串联：元真 yotta-humanize
2. 通用与入门（general）
   · 还没想清楚，先从通用引导开始
```

## 安装

三种方式任选；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm（推荐，一行装）
```bash
# 可选国内镜像：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-prompt -g
npx -y @yottameta/yotta-prompt --dir <你的技能目录>   # 任意智能体：装到自定义目录
```
> 预设列表里没有你的智能体？用 `--dir` 指向它的技能目录，或手动复制（方式三）。`--list` 可查看各智能体默认目录。

### 方式二：install.sh
拿到技能目录后（`npm pack` 解包或 `git clone`），进入目录：
```bash
bash install.sh -g    # 用户级；bash install.sh --list 查看全部目录
bash install.sh --agent codex   # 指定智能体（见 --list）
bash install.sh       # 项目级：自动检测已存在的技能目录
bash install.sh --dir /path/to/skills
```
> 覆盖 17 类智能体，含 Trae / Qwen / Comate / CodeBuddy / Kimi。

### 方式三：手动复制
把整个 `yotta-prompt` 文件夹复制到目标智能体的 skills 目录。常见用户级位置（Windows 用 `%USERPROFILE%`，Linux/macOS 用 `~`）：

| 智能体 | 用户级目录 | 项目级目录 |
|---|---|---|
| Codex | `%USERPROFILE%\.codex\skills\yotta-prompt\` | `.codex\skills\` |
| Claude Code | `%USERPROFILE%\.claude\skills\yotta-prompt\` | `.claude\skills\` |
| Cursor | `%USERPROFILE%\.cursor\skills\yotta-prompt\` | `.cursor\skills\` |
| Windsurf | `%USERPROFILE%\.codeium\windsurf\skills\yotta-prompt\` | `.windsurf\skills\` |
| opencode | `%USERPROFILE%\.config\opencode\skills\yotta-prompt\` | `.opencode\skills\` |
| Gemini | `%USERPROFILE%\.gemini\skills\yotta-prompt\` | `.gemini\skills\` |
| Goose | `%USERPROFILE%\.config\goose\skills\yotta-prompt\` | `.goose\skills\` |
| Amp | `%USERPROFILE%\.config\agents\skills\yotta-prompt\` | `.agents\skills\` |
| Kiro | `%USERPROFILE%\.kiro\skills\yotta-prompt\` | `.kiro\skills\` |
| WorkBuddy | `%USERPROFILE%\.workbuddy\skills\yotta-prompt\` | `.workbuddy\skills\` |
| Trae Code CLI | `%USERPROFILE%\.traecli\skills\yotta-prompt\` | `.traecli\skills\` |
| Trae IDE (国内) | `%USERPROFILE%\.trae-cn\skills\yotta-prompt\` | `.trae\skills\` |
| Qwen Code | `%USERPROFILE%\.qwen\skills\yotta-prompt\` | `.qwen\skills\` |
| Comate | `%USERPROFILE%\.comate\skills\yotta-prompt\` | `.comate\skills\` |
| CodeBuddy | `%USERPROFILE%\.codebuddy\skills\yotta-prompt\` | `.codebuddy\skills\` |
| Kimi | `%USERPROFILE%\.kimi\skills\yotta-prompt\` | `.kimi\skills\` |
| 通用 AGENTS.md | `%USERPROFILE%\.agents\skills\yotta-prompt\` | `.agents\skills\` |

> 若设置了 Codex 的 `CODEX_HOME`、opencode 的 `XDG_CONFIG_HOME`，安装会自动以该变量为准。
> `.agents\skills` 不是通用目录——只有 OpenCode / Cursor / Cline / Amp / Kimi / Gemini CLI / GitHub Copilot 等读取；
> **Claude Code 与 Codex 默认不读**。不确定时用 `--dir` 或让智能体自己装。

## 开发与校验

技能包自带测试脚本（随发布包一起分发）：

```bash
# 在技能目录内跑全量用例（41 个）
python scripts/test_yotta_prompt.py
```

场景走查见 `references/scenarios.md`。

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
