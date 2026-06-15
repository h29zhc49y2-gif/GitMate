# 我的 commit message 又被组长打回来了——于是我写了个 Trae Skill，自动生成规范提交

> 一个读取 git diff 自动生成 Conventional Commit 的 Trae Skill。免费，装上就用。

---

## 你是不是也经历过？

```
git add .
git commit -m "update"
git push

# 5 分钟后...
组长：commit message 不规范，改成 feat(home): xxx 格式
你：好的...（心想：我哪记得这么多 type）
```

或者更惨的——你配了 husky + commitlint，结果每次提交都被钩子拦下来：

```
⧗   input: update some stuff
✖   subject may not be empty [subject-empty]
✖   type may not be empty [type-empty]
```

**然后你开始对着 cheatsheet 查：feat 还是 fix？scope 填什么？body 写什么？**

**10 分钟过去了，代码只改了 3 行，commit message 琢磨了 10 分钟。**

---

## GitMate：git add . → 自动生成规范 commit

在 Trae 里只需要一句：

```
生成 commit
```

GitMate 自动：

| 步骤 | 做了什么 |
|------|---------|
| 📖 读暂存区 | `git diff --staged` 分析所有变更 |
| 🏷️ 推断 type | 新增文件 → `feat`，修 bug → `fix`，md → `docs`… |
| 🎯 推断 scope | 从文件路径：`src/pages/home/` → scope = `home` |
| ✍️ 写 subject | 动词开头、50 字内 |
| 📋 写 body | 逐文件列变更条目 |
| 🔍 兼容性 | 格式通过 commitlint 检查 |

输出：

```
feat(home): 添加用户列表组件

- 新增 UserList.tsx
- 新增 UserCard.tsx
- 修改 index.ts
```

**3 秒钟，一个符合规范的 commit message 出来了。直接复制粘贴运行。**

---

## 组团提交也支持

团队协作时，还需要写 PR 描述：

```
生成 PR 描述，对比 main 分支
```

自动输出标准 PR 模板：

```markdown
## 📝 变更概述
（自动提取提交信息）

## 🔧 详细改动
### 新增
- src/pages/home/UserList.tsx

### 修改
- src/api/user.ts

## ✅ 自检清单
- [ ] 代码已在本地测试通过
- [ ] 已添加必要的测试用例
- [ ] 无新增 lint 警告

## 📸 截图
（待补充）
```

---

## 比 husky + commitizen 好在哪？

| 方案 | 配置成本 | 使用门槛 | 团队统一性 |
|------|:--:|:--:|:--:|
| husky + commitlint | 安装 4 个包、写 2 个配置 | 提交失败再改 | 强制统一 |
| commitizen | 配 adapter | 多一步 `git cz` | 靠自觉 |
| **GitMate** | **0** | **一句"生成 commit"** | **全员同一 Skill** |

不需要装任何东西，Trae Skill 一贴即用。

---

## 安装

Trae → 设置 → 规则和技能 → 技能 → 创建 → 粘贴下方完整内容 → 保存。

👉 **[GitMate 安装文档（飞书）]()** （替换为实际链接）

或直接下载：

💻 [Gitee](https://gitee.com/neshama_ai/GitMate) ｜ [GitHub](https://github.com/h29zhc49y2-gif/GitMate)

---

## 关于"Agent 也能做"的问题

是的，Agent 也能读 git diff 生成 commit。但 GitMate 多了一层"领域规则"：

- **137 条 Conventional Commits 约定内置**，不用每次描述一遍
- **中文化动词词库**（添加/修复/重构/移除 — 不是机翻风格）
- **commitlint 兼容保证**，输出格式直接能过校验
- **团队一致性** — 同一个 Skill → 同样的 commit 风格

---

## 开发者效率矩阵 · 第四款

| # | 产品 | 一句话 |
|---|------|--------|
| 1 | [i18nFlow](https://juejin.cn/post/7650883011774595123) | 一键翻译多语言 |
| 2 | [ViteForge](https://juejin.cn/post/7651267067145257010) | 一句生成 Vite 配置 |
| 3 | TypeForge（审核中） | 三秒出 TypeScript 类型 |
| 4 | **GitMate** | **自动规范 commit message** |

免费使用，欢迎反馈。

---

*#Trae #Git #前端工程化 #效率工具 #ConventionalCommits #AI编程*
