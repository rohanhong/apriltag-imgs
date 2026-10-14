<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../.github/assets/banner-light.svg">
  <img alt="apriltag-imgs" src="../../.github/assets/banner-light.svg" width="492">
</picture>

<h1>🏷️ AprilTag-imgs（复刻）</h1>

<p><b>全部 AprilTag 3 标签族的预生成图像，可直接交给 AI 编程智能体使用</b></p>

<p>
  <a href="../../LICENSE"><img alt="License" src="https://img.shields.io/github/license/rohanhong/apriltag-imgs"></a>
  <a href="https://github.com/AprilRobotics/apriltag-imgs"><img alt="Fork of" src="https://img.shields.io/badge/fork%20of-AprilRobotics%2Fapriltag--imgs-lightgrey?logo=github"></a>
  <a href="https://github.com/rohanhong/apriltag-imgs/commits/master"><img alt="Last commit" src="https://img.shields.io/github/last-commit/rohanhong/apriltag-imgs"></a>
  <a href="https://github.com/rohanhong/apriltag-imgs/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/rohanhong/apriltag-imgs?style=flat"></a>
  <a href="https://agents.md"><img alt="AGENTS.md" src="https://img.shields.io/badge/AGENTS.md-ready-24292f"></a>
  <a href="https://agentskills.io"><img alt="Agent Skills" src="https://img.shields.io/badge/Agent%20Skills-open%20format-8250df"></a>
</p>

<p>🌐 <a href="../../README.md">English</a> | <b>简体中文</b></p>

</div>

> [!IMPORTANT]
> 本仓库是 [AprilRobotics/apriltag-imgs](https://github.com/AprilRobotics/apriltag-imgs) 的非官方复刻，与密歇根大学（University of Michigan）、APRIL 机器人实验室（APRIL Robotics Laboratory）及上游维护者均无关联，也未获其认可。标签图像和 `tag_to_svg.py` 与上游完全一致。

本仓库收录全部预生成 [AprilTag 3](https://github.com/AprilRobotics/apriltag) 标签族中每个标签的图像。如需自定义布局或标签图像，可使用 [AprilTag-generation](https://github.com/AprilRobotics/apriltag-generation) 自行生成。本复刻额外提供一套与具体工具无关的智能体指令（`AGENTS.md`）和技能（`.agents/skills`），任何 AI 编程智能体都能按同一套规则在本仓库中工作。本复刻还以 SVG 形式提供全部标签，按标签族打包在 `svg/` 中，由 `scripts/tags_to_svg.py` 生成。

## ✨ 亮点

- 🖼️ **涵盖全部预生成标签族**：八个标签族，约 159,000 张标签 PNG，每个标签族另附一张拼图和一份 PostScript 图纸。
- 📐 **按任意尺寸打印**：`tag_to_svg.py` 可将标签转换为带物理尺寸的 SVG。
- 🗜️ **全部标签的 SVG 版本**：`svg/<Family>.tar.gz` 以每个标签像素 2 mm 的尺寸收录全部 159,428 个标签的 SVG，合计约 17 MiB。
- 🤖 **面向智能体**：`AGENTS.md` 加 15 个技能，覆盖 git、文档和环境配置工作，并附带 Claude Code 适配器。
- 🛡️ **上游内容不变**：图像、脚本和 BSD-2-Clause 许可证均保持原样，本复刻通过普通合并与上游同步。

## 📦 标签族

| 目录 | 标签数 | 标签图像（像素） | SVG 边长 |
|---|---|---|---|
| `tag16h5` | 30 | 8 x 8 | 16 mm |
| `tag25h9` | 35 | 9 x 9 | 18 mm |
| `tag36h11` | 587 | 10 x 10 | 20 mm |
| `tagCircle21h7` | 38 | 9 x 9 | 18 mm |
| `tagCircle49h12` | 65,698 | 11 x 11 | 22 mm |
| `tagCustom48h12` | 42,211 | 10 x 10 | 20 mm |
| `tagStandard41h12` | 2,115 | 9 x 9 | 18 mm |
| `tagStandard52h13` | 48,714 | 10 x 10 | 20 mm |

每个标签对应一个文件，命名为 `tag<bits>_<hamming>_<id>.png`，例如 `tag36h11/tag36_11_00000.png`。每个目录还包含 `mosaic.png` 和 `alltags.ps`。

“SVG 边长”一列是 `svg/<Family>.tar.gz` 中每个标签的尺寸（每个标签像素 2 mm；条目为 `<Family>/<name>.svg`）。`scripts/tags_to_svg.py` 用 `tag_to_svg.py` 从 PNG 生成这些压缩包；解压出的 `svg/<Family>/` 目录已被 git 忽略。

## 🚀 快速开始

> [!NOTE]
> 缩放图像需要 [ImageMagick](https://imagemagick.org)。SVG 脚本需要 Python 3 和 Pillow（`pip install Pillow`）。

1. 克隆仓库：
   ```bash
   git clone https://github.com/rohanhong/apriltag-imgs.git
   ```
2. 标签图像很小（宽 8 到 11 像素），使用前请先缩放（Unix；在 ImageMagick 7 中用 `magick` 代替 `convert`）：
   ```bash
   convert <small_marker>.png -scale <scale_chosen_in_percent>% <big_marker>.png
   ```
3. 或者生成标签的 SVG（可缩放矢量图形）版本：
   ```bash
   python3 tag_to_svg.py tagStandard52h13/tag52_13_00007.png tag52_13_00007.svg --size=20mm
   ```
4. 或者解压一整个标签族的现成 SVG（Windows 10 及更高版本也自带 `tar`）：
   ```bash
   tar -xzf svg/tag36h11.tar.gz -C svg
   ```
5. 如需以其他尺寸生成全部标签，请输出到你自己的目录，以免改动 `svg/` 中受 git 跟踪的 2 mm 压缩包（约 2.5 分钟）：
   ```bash
   python3 scripts/tags_to_svg.py --cell=5mm --out <your_dir>
   ```

<details>
<summary>只克隆一个标签族</summary>

```bash
git clone --filter=blob:none --sparse https://github.com/rohanhong/apriltag-imgs.git
cd apriltag-imgs
git sparse-checkout set tag36h11
```

</details>

## 🤖 AI 智能体支持

| 路径 | 用途 |
|---|---|
| `AGENTS.md` | 智能体指令：项目信息、命令、约定和复刻规则 |
| `.agents/skills/` | 下列技能，采用开放的 Agent Skills 格式 |
| `CLAUDE.md`、`.claude/skills` | Claude Code 适配器：一行 `@AGENTS.md` 导入，以及指向 `.agents/skills` 的链接 |
| `.gitmessage` | 提交格式与工作流（`trunk-solo`，分支命名 Variant C） |
| `.gitattributes`、`.gitignore` | 换行符、二进制标记和忽略规则 |
| `.github/settings.yml` | GitHub About 面板的记录；GitHub 不读取该文件，修改后需手动应用 |

| 分组 | 技能 | 作用 |
|---|---|---|
| 🌿 Git | `git-branch-create` `git-commit` `git-fetch` `git-pull` `git-merge` `git-push` `git-tag` `git-branch-delete` | 按 `.gitmessage` 创建分支、提交、同步、合并、发布和打标签 |
| 🏗️ 配置 | `repo-init` `repo-docs` `py-env-setup` | 检查 git 配置、维护 README、创建 conda 环境 |
| 🤗 HF Hub | `hf-setup` `hf-upload` `hf-download` | 以固定且经过校验的版本托管大型产物 |

技能在执行任何难以撤销的操作前都会等待你确认。它们需要 git 2.22 或更高版本，以及 POSIX shell（Windows 上为 Git Bash）。

> [!IMPORTANT]
> 在 Windows 上，`.claude/skills` 是符号链接。克隆前请开启开发者模式并运行 `git config --global core.symlinks true`，否则 Claude Code 找不到任何技能。修复步骤见 `AGENTS.md`（Layout 一节）。

## 🔄 与上游同步

`upstream` 远程指向原始仓库：

```bash
git remote add upstream https://github.com/AprilRobotics/apriltag-imgs.git   # once
git fetch upstream
git merge upstream/master   # or run the git-merge skill with source upstream/master
```

上游处于维护模式，不接受新增功能的拉取请求。智能体工具来自维护者自己的仓库模板；如需更新，用模板的新版本替换 `.agents/skills/` 并检查差异。

## 📚 文档

| 主题 | 位置 |
|---|---|
| 智能体指令、复刻规则、目录布局、技能编写 | [`AGENTS.md`](../../AGENTS.md) |
| 提交格式、工作流变体、分支命名、标签 | [`.gitmessage`](../../.gitmessage) |
| 每个技能的流程与规则 | [`.agents/skills/<name>/SKILL.md`](../../.agents/skills) |
| SVG 转换器选项 | `python3 tag_to_svg.py --help` |
| 批量 SVG 转换器选项 | `python3 scripts/tags_to_svg.py --help` |

## 🤝 参与贡献

对标签图像或 `tag_to_svg.py` 的修改应提交到上游。欢迎就本复刻新增的内容在此提交 issue 和拉取请求；提交信息遵循 [`.gitmessage`](../../.gitmessage)。

## 🔗 相关资源

- [AprilRobotics/apriltag-imgs](https://github.com/AprilRobotics/apriltag-imgs)：上游仓库。
- [AprilTag](https://github.com/AprilRobotics/apriltag)：检测库。
- [AprilTag-generation](https://github.com/AprilRobotics/apriltag-generation)：生成自定义布局和标签图像。
- [AprilTag 项目主页](https://april.eecs.umich.edu/software/apriltag)：背景介绍与论文。
- [AGENTS.md](https://agents.md) 和 [Agent Skills](https://agentskills.io)：智能体指令与技能的开放格式。

## ⚖️ 法律信息

- **许可证**：[BSD 2-Clause](../../LICENSE)，Copyright (c) 2013-2016, The Regents of The University of Michigan。本复刻新增的内容（智能体指令、技能、文档、批量 SVG 脚本和 SVG 压缩包）按相同条款提供。
- **关联声明**：本仓库是非官方复刻。文中出现的上游名称仅用于指明原始项目，不表示任何认可。

## ⭐ Star 历史

<a href="https://www.star-history.com/#rohanhong/apriltag-imgs&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=rohanhong/apriltag-imgs&type=Date&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=rohanhong/apriltag-imgs&type=Date">
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=rohanhong/apriltag-imgs&type=Date" width="600">
  </picture>
</a>
