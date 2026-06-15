# GitMate 📝

> Trae Skill — 自动生成 Conventional Commit 提交信息与 PR 描述。

[![Trae Skill](https://img.shields.io/badge/Trae-Skill-blue)](https://trae.com.cn)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()

## 这是什么？

GitMate 是一个 Trae Skill，读你的 git diff，自动生成符合 Conventional Commits 规范的 commit message 和 PR 描述。

「git add .」→「生成 commit」→ 输出 `feat(home): 添加用户列表组件` — 不用自己想 type 和 scope。

## 核心能力

- ✅ 读取 git diff --staged 分析变更
- ✅ 自动推断 Conventional Commit type（feat/fix/docs/…）
- ✅ 从文件路径自动推断 scope
- ✅ 中文/英文双语言支持
- ✅ 生成完整 commit body（变更条目列表）
- ✅ 生成标准 PR 描述模板
- ✅ 兼容 commitlint 规范
- ✅ 支持自定义 type/scope/subject

## 快速开始

### 安装

Trae 设置 → 规则和技能 → 技能 → 创建 → 粘贴 SKILL.md

### 使用

```
git add .
生成 commit
```

GitMate 分析暂存区 → 输出完整的 commit message → 你确认后粘贴运行。

或者生成 PR 描述：

```
生成 PR 描述，对比 main 分支
```

## 效果示例

```
类型: feat | 范围: home
变更文件: 3 个
========================================
feat(home): 添加用户列表组件

- 新增 UserList.tsx
- 新增 UserCard.tsx
- 修改 index.ts

========================================
```

## 定价

GitMate 完全免费。它是"开发者效率工具矩阵"的第四个产品。
