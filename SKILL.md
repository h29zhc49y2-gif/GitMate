---
name: GitMate
description: >
  自动生成 Conventional Commit 提交信息与 PR 描述。
  读取 git diff 分析变更内容，智能推断 type/scope，
  支持中文/英文输出，兼容 commitlint 规范。
version: 1.0.0
tags: [Git, Commit, PR, 提交规范, 自动化, Conventional Commits, commitlint]
triggers:
  - 生成commit
  - 生成提交信息
  - 生成commit message
  - 写commit
  - commit message
  - 生成PR描述
  - 写PR
  - PR描述
  - 规范化提交
  - 自动提交
  - generate commit
  - git commit
  - conventional commit
---

# GitMate

## 任务目标

读取 Git 暂存区 / 分支差异，自动生成符合 Conventional Commits 规范的提交信息与 Pull Request 描述。

## 执行流程

### Step 1：读取变更

运行分析脚本获取当前变更内容：

```bash
python scripts/commit_generator.py --detect
```

输出：
- 暂存区文件列表及变更类型（新增/修改/删除）
- 每个文件的变更行数统计
- 变更内容关键词提取

### Step 2：推断提交类型

根据变更内容智能推断 Conventional Commit type：

| 变更特征 | 推断 type | 示例 |
|---------|----------|------|
| 新增文件为主 | `feat` | 新组件、新页面 |
| 修改现有文件，无新增 | `fix` | Bug 修复 |
| 仅 .md 文件 | `docs` | 文档更新 |
| 配置文件 (.eslint/.prettier) | `chore` | 工具链 |
| 测试文件 | `test` | 测试 |
| 代码重构大量修改 | `refactor` | 重构 |
| CSS/样式文件 | `style` | 样式 |
| 性能相关关键词 | `perf` | 性能优化 |

### Step 3：生成提交信息

```bash
python scripts/commit_generator.py --lang zh
```

输出完整的 commit message：
```
feat(home): 添加首页用户列表组件

- 新增 UserList 组件及样式
- 接入 /api/users 接口获取用户数据
- 实现搜索过滤和分页功能
```

### Step 4：生成 PR 描述（可选）

```bash
python scripts/pr_generator.py --base main --lang zh
```

输出标准 PR 描述：变更概述、详细改动、测试说明、截图区域。

---

## 核心规则

### 规则 1：Conventional Commits 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

必填字段：type、subject（50 字以内）
可选字段：scope、body（72 字换行）、footer（BREAKING CHANGE / Closes #123）

### 规则 2：type 推断规则

扫描变更文件路径和关键词：

```
src/components/        → 可能是 feat 或 fix
src/utils/             → 可能是 refactor
*.test.ts / *.spec.ts  → test
*.md                   → docs
*.css / *.scss         → style
package.json           → chore (依赖变更)
```

优先使用用户指定的 type。如果用户说"修复登录按钮"→ 强制 `fix`。

### 规则 3：scope 推断规则

从变更的文件路径自动推断 scope：

| 文件路径 | 推断 scope |
|---------|-----------|
| src/pages/home/ | home |
| src/components/Button/ | button |
| src/utils/auth.ts | auth |
| src/api/user.ts | user |

### 规则 4：subject 生成规则

- 动词开头：添加/修复/重构/更新/移除
- 英文：动词原形开头：add/fix/refactor/update/remove
- 不超过 50 字符
- 不以句号结尾
- 不使用"了"等语气词（中文）

### 规则 5：body 生成规则

从 git diff 中提取关键变更，生成条目列表：
- 每条一行，以 `- ` 开头
- 一行超过 72 字符自动换行
- 为什么改 > 改了什么（如果 diff 看不出，标注"建议补充原因"）

### 规则 6：commitlint 兼容

生成的格式兼容 `@commitlint/config-conventional`：
- type 必须来自标准列表
- subject 不能为空
- subject 不超过 72 字符
- body 每行不超过 100 字符

---

## 输出示例

### Commit Message（中文）

```
feat(home): 添加用户列表页面

- 新增 UserList、UserCard 组件
- 接入 /api/users 分页接口
- 实现搜索、排序、筛选功能
- 添加加载骨架屏和空状态
```

### Commit Message（英文）

```
feat(home): add user list page

- Add UserList and UserCard components
- Integrate /api/users paginated endpoint
- Implement search, sort, and filter
- Add loading skeleton and empty state
```

### PR 描述

```markdown
## 📝 变更概述

为首页添加用户列表功能，支持分页检索。

## 🔧 详细改动

- **新增**: `UserList.tsx` — 用户列表容器组件
- **新增**: `UserCard.tsx` — 用户卡片组件
- **新增**: `useUsers.ts` — 用户数据 Hook
- **修改**: `api/client.ts` — 添加通用分页参数

## ✅ 测试

- [ ] 分页加载正常
- [ ] 搜索过滤正确
- [ ] 空数据状态显示
- [ ] 接口错误处理

## 📸 截图

(待补充)
```

---

## 分支命名建议

基于 commit type 推断分支名：

```
feat    → feature/xxx
fix     → fix/xxx
refactor → refactor/xxx
```
