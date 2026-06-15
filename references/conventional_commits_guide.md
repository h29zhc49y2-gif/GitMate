# Conventional Commits 规范参考

## 格式

```
<type>[(scope)]: <subject>

[body]

[footer]
```

## type 列表

| type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(home): 添加用户列表` |
| `fix` | Bug 修复 | `fix(auth): 修复 token 过期未刷新` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式（不影响逻辑） | `style: 统一缩进格式` |
| `refactor` | 重构（不新增功能也不修 bug） | `refactor(utils): 提取公共方法` |
| `perf` | 性能优化 | `perf(list): 添加虚拟滚动` |
| `test` | 测试相关 | `test(auth): 添加登录单元测试` |
| `chore` | 构建/工具/依赖 | `chore: 升级 Vite 到 6.0` |
| `ci` | CI/CD 变更 | `ci: 添加 pr 预览环境` |
| `build` | 构建系统变更 | `build: 调整打包配置` |

## scope 规则

- 小写英文或中文
- 从变更文件路径自动推断
- 不写 scope 也可以：`feat: 添加暗色模式`

## subject 规则

- 不超过 50 字符
- 不以句号结尾
- 动词开头
- 英文用现在时，不加 `s`：`add` 不是 `adds`

## body 规则

- 每行不超过 72 字符
- 解释 **为什么改**，不只是改了什么
- 多条用 `- ` 开头

## footer 规则

```
BREAKING CHANGE: 描述不兼容的变更

Closes #123
Refs #456
```

## 常见错误

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| `feat: 我添加了按钮` | `feat(home): 添加按钮组件` |
| `修改了一些东西` | `fix(auth): 修复登录跳转失败` |
| `fix: fixed the bug` | `fix: correct login redirect` |
| `feat: update.` | `feat: add user profile page` |
