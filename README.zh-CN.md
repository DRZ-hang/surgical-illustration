<div align="center">

# 🔬 手术解剖插图 · Surgical Anatomy Illustration

**给 AI 手术/解剖插图加一层科学性把关:出图前约束 prompt,出图后查解剖错误。**

[English](README.md) · **简体中文**

<!-- 放一张 hero 成品图后取消注释:  ![hero](docs/images/hero.png)  -->

</div>

> ⚠️ 仅供教育与出版示意,非临床依据;请对照权威来源核实解剖。

---

`surgical-anatomy-illustration` 是一个面向 **Claude Code、Codex** 的手术与解剖插图 skill。
它**本身不出图**:在你出图前,把这台手术不可妥协的解剖规则与安全地标写进 prompt;在你出图后,
审查图里的解剖对错。它在意的不是"画得像",而是"画得对"——确定的它判,不确定的它标出来交给你定。

## 仓库结构

```text
surgical-anatomy-illustration/   # 可安装的 skill
├─ SKILL.md            # 行为定义:问诊 → 简报 → 审查
├─ knowledge/          # 各术式的解剖约束(JSON 种子条目)
├─ scripts/            # 纯标准库引擎(无第三方依赖)
├─ references/         # 风格、解剖、构图、期刊规范
└─ assets/examples/    # 一个完整的闭环示例
docs/                  # 设计说明与 README 配图
```

## 快速安装

把 skill 文件夹复制进 Claude Code 的 skills 目录,即可使用:

```powershell
# Windows PowerShell(在仓库目录里执行)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force surgical-anatomy-illustration "$env:USERPROFILE\.claude\skills\"
```

```bash
# macOS / Linux(在仓库目录里执行)
mkdir -p ~/.claude/skills
cp -r surgical-anatomy-illustration ~/.claude/skills/
```

重启 Claude Code,之后**直接用自然语言(中英文皆可)**向它提需求即可,不用敲命令。

## 手动安装

1. 确认 skills 目录存在:`~/.claude/skills/`(Windows 为 `C:\Users\<用户名>\.claude\skills\`),没有就新建一个。
2. 把整个 `surgical-anatomy-illustration` 文件夹放进去,保持 `SKILL.md`、`scripts/`、`knowledge/`、`references/` 原样不动。
3. 重启 Claude Code。它会自动发现这个 skill;当你提到"手术插图 / 解剖图"时就会被触发。

## 平台差异

这个 skill 只是一组文件,凡是能加载 skill 的宿主都能用,但**各家表现不同**:

| 宿主 | 怎么装 | 入口 | 表现 |
| --- | --- | --- | --- |
| **Claude Code**(推荐) | 复制到 `~/.claude/skills/` | 用自然语言提需求 | **完整**:会停下来问诊、含体位/入路、输出最学术严谨 |
| **Codex** | 在仓库目录内运行,它会读取 skill | 直接提需求 | **较简略**:不会停下来问、可能跳过细节规则,适合出草稿 |
| **OpenClaw 等 Claude Code 兼容运行时** | 同 Claude Code | 同 Claude Code | 取决于其对 skill 的支持,通常与 Claude Code 一致 |

> 一句话:**要完整、严谨的结果,用 Claude Code;Codex 当快速草稿用。**

## 主工作流

两条平级主流程,直接用自然语言说就行(中英文皆可):

1. **创作** —— 给它一个手术名,它先问你几个决定对错的选择(侧别、入路、教学重点),再返回三件套:**概述 → 出图 Prompt → 质检清单**。
   > 例:"给我回肠袢式造口术的 prompt 和质检。"
2. **检测** —— 给它任意一张手术/解剖图,它逐条审查并给出手改清单。
   > 例:"帮我看看这张手术图哪儿画错了。"(附上图)

中间的"出图"由你拿 Prompt 到自己惯用的工具(ChatGPT、即梦、Gemini…)完成,再把图带回来审查。

## 范围

本仓库是一个**单一、聚焦**的 skill,只做手术与解剖插图,**没有主控/分支结构**。
其它医学可视化方向(分子机制/通路图、论文 abstract-to-figure)规划为**独立的兄弟 skill**,不在此仓库内。

## 关键产物

- **概述**:这台手术是什么、适应证、关键解剖、核心安全点,并给出该核对的权威出处。
- **出图 Prompt**:一份约束好的、可复制到任意工具的提示词。
- **质检清单**:中英双语、四档评分(✅ 对 / ❌ 错 / ⚠️ 需核 / ❓ 看不准),跟具体病例相关的点一律标 ⚠️ 交给你定。
- 用脚本时还会落盘 `*_job.json`、`*_prompt.txt`、`*_review.json`。

## 命令

平时直接说话就能用;想用脚本生成或核对产物时:

```bash
cd surgical-anatomy-illustration
python scripts/knowledge.py list                 # 列出已有的术式种子条目
python scripts/workflow.py "回肠袢式造口术" --output-dir outputs
```

## 它试图避免的问题

- 画错侧别(左右、上下、前后)。
- 血管、导管、神经接到错误的结构上。
- 把这台手术其实**不固定**的范围/做法画死——应标出来交给医生判断,而不是替你猜。
- 手术流程图跳过患者体位与入路(开腹切口 / 腔镜戳卡)。
- 把未经核验的内容当作已核验的呈现。

## 诚实的边界

- AI 出图画不准精细解剖。可靠的交付物是**草稿 + 精确审查**,而不是一张完美的图;几何精修仍由插画师收尾。
- 知识条目默认标 `model_generated`(尚未经临床核验),除非另行注明。
- 不用于临床决策,仅供教育与出版示意。

## 许可证

[MIT](LICENSE)。
