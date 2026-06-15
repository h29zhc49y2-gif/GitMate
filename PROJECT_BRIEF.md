# GitMate 项目简报

## 项目概要

- **项目名**：GitMate
- **定位**：自动生成 Conventional Commit 提交信息与 PR 描述的 Trae Skill
- **一句话**：git add . → 自动生成符合规范的 commit message + PR 描述
- **目标用户**：所有用 Git 的开发者，尤其是团队中使用 commitlint 的项目

## 核心功能

1. 读取 git diff --staged 分析变更内容
2. 自动推断 Conventional Commit type（feat/fix/docs…含 10 种标准类型）
3. 从文件路径自动推断 scope
4. 生成完整的 commit body（按文件列变更条目）
5. 生成标准 PR 描述模板（变更概述/详细改动/自检清单/截图区）
6. 中文/英文双语言支持
7. 兼容 @commitlint/config-conventional 规范
8. 支持手动指定 type/scope/subject

## 差异化

- 不是简单的"根据描述生成 commit"（那是通用 AI 的能力）
- 而是"读了你的 git diff，自己推断 type 和 scope"
- 对于团队场景：统一整个团队的 commit 格式，不需要配 husky/commitlint
- PR 描述自动分类变更文件（组件/页面/API/样式/测试/配置/文档）

## 定价

免费。作为矩阵产品的流量入口被"Git"关键词搜索发现。

## 技术架构

```
GitMate/
├── SKILL.md
├── README.md / PROJECT_BRIEF.md
├── scripts/
│   ├── commit_generator.py   → commit message 生成
│   └── pr_generator.py       → PR 描述生成
├── references/
│   ├── conventional_commits_guide.md
│   └── edge_cases.md
└── assets/
```

## 产品矩阵

| # | 产品 | 场景 | 搜索关键词 |
|---|------|------|-----------|
| 1 | i18nFlow | 国际化翻译 | i18n/翻译 |
| 2 | ViteForge | 构建配置 | Vite/配置 |
| 3 | TypeForge | 类型推断 | TypeScript/类型/JSON |
| 4 | **GitMate** | **Git 提交流程** | **Git/Commit/PR** |
