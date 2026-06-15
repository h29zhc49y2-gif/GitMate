# GitMate 边界情况与故障排除

## 常见边界情况

### 1. 暂存区为空

```
暂存区无变更。请先 git add 要提交的文件。
提示: 如果还没修改任何文件，先用 git status 查看状态。
```

### 2. 暂存文件过多（>50 个文件）

生成 subject 时可能过于泛化。建议：
- 拆分为多个 commit
- 或使用 `--type` 手动指定类型

### 3. 二进制文件（图片、字体等）

diff 中无法展示内容变更。生成的消息会标注：
```
chore(assets): 更新静态资源
- assets/icon.png （二进制文件，无法分析内容）
```

### 4. 超大 diff（>10000 行）

自动截断分析前 5000 行，标注：
```
（diff 超过 5000 行，已截断分析）
```

### 5. 非 Git 仓库

检测到非 Git 目录时提示：
```
当前目录不是 Git 仓库。请先运行 git init。
```

### 6. 同时有新增和删除同名文件

自动识别为重命名操作：
```
- 重命名 old_name.ts → new_name.ts
```

### 7. 只修改 package.json

如果变更内容仅涉及版本号，自动识别为依赖升级：
```
chore(deps): 升级依赖版本
- react: 18.2.0 → 18.3.0
```

### 8. PR 目标分支不存在

```
目标分支 'main' 不存在。
可用的分支: master, develop, main
请用 --base <branch> 指定正确的目标分支。
```

## 关于 Agent 的说明

GitMate 的价值不在于"替代 AI Agent"（Agent 确实也能做这些），而在于：

1. **预置规则** — 137 条 Conventional Commits 约定直接可用，不需要每次描述
2. **中文友好** — 专门优化的中文化词库和动词选择
3. **零配置** — 不需要安装 commitizen、commitlint、husky
4. **一致性** — 团队所有成员用同一个 Skill，commit 格式自动统一
