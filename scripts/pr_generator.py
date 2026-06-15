#!/usr/bin/env python3
"""
GitMate - PR description generator.
Compares current branch with base branch, generates structured PR descriptions.
"""

import subprocess
import sys
import re
import argparse
from pathlib import Path
from collections import Counter


def run_git(args: list, cwd: str = ".") -> str:
    try:
        result = subprocess.run(
            ["git"] + args, cwd=cwd,
            capture_output=True, text=True, encoding="utf-8",
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"


def get_branch_diff(base: str, cwd: str = ".") -> str:
    return run_git(["diff", f"{base}..HEAD"], cwd)


def get_changed_files(base: str, cwd: str = ".") -> list:
    output = run_git(["diff", f"{base}..HEAD", "--name-status"], cwd)
    if not output:
        return []
    files = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            files.append({"status": parts[0], "path": parts[1]})
    return files


def get_commit_logs(base: str, cwd: str = ".") -> list:
    output = run_git(["log", f"{base}..HEAD", "--oneline", "--no-decorate"], cwd)
    if not output:
        return []
    return [line.strip() for line in output.split("\n") if line.strip()]


def get_branch_name(cwd: str = ".") -> str:
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)


def categorize_changes(files: list) -> dict:
    """Categorize changes by type."""
    cats = {
        "新增": [],
        "修改": [],
        "删除": [],
        "组件": [],
        "页面": [],
        "工具/API": [],
        "样式": [],
        "测试": [],
        "配置": [],
        "文档": [],
        "其他": [],
    }

    for f in files:
        path = f["path"]
        status = f["status"]

        # Status category
        if status == "A":
            cats["新增"].append(path)
        elif status == "D":
            cats["删除"].append(path)
        elif status == "M":
            cats["修改"].append(path)

        # Content category
        if "component" in path.lower() or "组件" in path:
            cats["组件"].append(path)
        elif "page" in path.lower() or "pages" in path.lower() or "页面" in path:
            cats["页面"].append(path)
        elif "api" in path.lower() or "utils" in path.lower() or "hooks" in path.lower() or "接口" in path:
            cats["工具/API"].append(path)
        elif any(ext in path.lower() for ext in [".css", ".scss", ".less", ".sass"]):
            cats["样式"].append(path)
        elif "test" in path.lower() or "spec" in path.lower() or "__tests__" in path.lower() or "测试" in path:
            cats["测试"].append(path)
        elif any(kw in path.lower() for kw in ["config", "eslint", "prettier", "package.json", "配置"]):
            cats["配置"].append(path)
        elif path.endswith(".md") or "docs" in path.lower() or "文档" in path:
            cats["文档"].append(path)
        else:
            cats["其他"].append(path)

    return cats


def detect_breaking_changes(diff_text: str) -> bool:
    """Heuristic: check if diff contains breaking change indicators."""
    indicators = [
        "BREAKING CHANGE",
        "breaking change",
        "不兼容",
        "migration",
        "deprecated",
        "移除接口",
        "remove public api",
    ]
    diff_lower = diff_text.lower()
    return any(ind.lower() in diff_lower for ind in indicators)


def generate_pr_description(
    files: list,
    commits: list,
    diff_text: str,
    branch_name: str,
    lang: str = "zh",
    title: str = "",
) -> str:
    """Generate full PR description."""

    cats = categorize_changes(files)
    has_breaking = detect_breaking_changes(diff_text)

    lines = []

    if lang == "zh":
        # Title
        if title:
            lines.append(f"## 📝 {title}")
        else:
            lines.append("## 📝 变更概述")
        lines.append("")
        lines.append("_（请在此简述本次 PR 的目的和背景）_")
        lines.append("")

        # Checklist
        lines.append("## ✅ 自检清单")
        lines.append("")
        lines.append("- [ ] 代码已在本地测试通过")
        lines.append("- [ ] 已添加必要的测试用例")
        lines.append("- [ ] 无新增 lint 警告")
        lines.append("- [ ] UI 变更已附截图")
        lines.append("- [ ] API 变更已更新文档")
        if has_breaking:
            lines.append("- [ ] 已标注 BREAKING CHANGE 并说明迁移方案")
        lines.append("")

        # Changes detail
        lines.append("## 🔧 详细改动")
        lines.append("")

        if cats["新增"]:
            lines.append("### 新增文件")
            for f in cats["新增"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if cats["修改"]:
            lines.append("### 修改文件")
            for f in cats["修改"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if cats["删除"]:
            lines.append("### 删除文件")
            for f in cats["删除"]:
                lines.append(f"- `{f}`")
            lines.append("")

        # Categorized
        for cat_name in ["组件", "页面", "工具/API", "样式", "测试", "配置", "文档"]:
            cat_files = [f for f in cats[cat_name] if f not in cats["新增"] and f not in cats["删除"]]
            if cat_files:
                lines.append(f"### {cat_name}")
                for f in cat_files:
                    lines.append(f"- `{f}`")
                lines.append("")

        # Commits
        if commits:
            lines.append("## 📋 提交记录")
            lines.append("")
            for c in commits[:10]:
                lines.append(f"- {c}")
            if len(commits) > 10:
                lines.append(f"- _...共 {len(commits)} 条提交_")
            lines.append("")

        # Breaking
        if has_breaking:
            lines.append("## ⚠️ BREAKING CHANGE")
            lines.append("")
            lines.append("> 此版本包含不兼容的变更，请查看以下迁移指南：")
            lines.append("")
            lines.append("（迁移说明待补充）")
            lines.append("")

        # Screenshots
        lines.append("## 📸 截图")
        lines.append("")
        lines.append("_（如有 UI 变更，请补充截图）_")

    else:
        # English version
        if title:
            lines.append(f"## 📝 {title}")
        else:
            lines.append("## 📝 Summary")
        lines.append("")
        lines.append("_(Briefly describe the purpose and background of this PR)_")
        lines.append("")

        lines.append("## ✅ Checklist")
        lines.append("")
        lines.append("- [ ] Code tested locally")
        lines.append("- [ ] Tests added when needed")
        lines.append("- [ ] No new lint warnings")
        lines.append("- [ ] UI changes have screenshots")
        lines.append("- [ ] API changes have updated docs")
        if has_breaking:
            lines.append("- [ ] BREAKING CHANGE noted with migration guide")
        lines.append("")

        lines.append("## 🔧 Changes")
        lines.append("")

        if cats["新增"]:
            lines.append("### Added")
            for f in cats["新增"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if cats["修改"]:
            lines.append("### Modified")
            for f in cats["修改"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if cats["删除"]:
            lines.append("### Removed")
            for f in cats["删除"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if commits:
            lines.append("## 📋 Commits")
            lines.append("")
            for c in commits[:10]:
                lines.append(f"- {c}")
            lines.append("")

        if has_breaking:
            lines.append("## ⚠️ BREAKING CHANGE")
            lines.append("")
            lines.append("> Migration guide needed.")
            lines.append("")

        lines.append("## 📸 Screenshots")
        lines.append("")
        lines.append("_(Add screenshots if applicable)_")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="GitMate - PR description generator")
    parser.add_argument("--base", default="main", help="Base branch name")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Language")
    parser.add_argument("--title", default="", help="Custom PR title")
    parser.add_argument("--cwd", default=".", help="Working directory")

    args = parser.parse_args()

    files = get_changed_files(args.base, args.cwd)
    commits = get_commit_logs(args.base, args.cwd)
    diff_text = get_branch_diff(args.base, args.cwd)
    branch_name = get_branch_name(args.cwd)

    if not files:
        print(f"当前分支 '{branch_name}' 相对于 '{args.base}' 无变更。")
        print("提示: 如果你用的是 master 分支，试试 --base master")
        sys.exit(0)

    pr_desc = generate_pr_description(
        files=files,
        commits=commits,
        diff_text=diff_text,
        branch_name=branch_name,
        lang=args.lang,
        title=args.title,
    )

    print(pr_desc)
    print()
    if args.lang == "zh":
        print(f"📊 变更统计: {len(files)} 个文件, {len(commits)} 条提交")
    else:
        print(f"📊 Stats: {len(files)} files, {len(commits)} commits")


if __name__ == "__main__":
    main()
