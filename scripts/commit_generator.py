#!/usr/bin/env python3
"""
GitMate - Commit message generator.
Reads git staging area, analyzes diff, generates Conventional Commit messages.
"""

import subprocess
import sys
import re
import argparse
from pathlib import Path
from collections import Counter
from typing import Optional


# ============================================================
# Git operations
# ============================================================

def run_git(args: list, cwd: str = ".") -> str:
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"


def get_staged_files(cwd: str = ".") -> list:
    """Get list of staged files with status."""
    output = run_git(["diff", "--staged", "--name-status"], cwd)
    if not output:
        return []
    files = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            status, filepath = parts
            files.append({"status": status, "path": filepath})
    return files


def get_staged_diff(cwd: str = ".") -> str:
    """Get full diff of staged changes."""
    return run_git(["diff", "--staged"], cwd)


def get_staged_stats(cwd: str = ".") -> str:
    """Get staged changes statistics."""
    return run_git(["diff", "--staged", "--stat"], cwd)


def get_branch_diff(base: str = "main", cwd: str = ".") -> str:
    """Get diff between current branch and base branch."""
    return run_git(["diff", base + "..HEAD"], cwd)


def get_current_branch(cwd: str = ".") -> str:
    """Get current branch name."""
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)


# ============================================================
# Conventional Commit type detection
# ============================================================

CC_TYPES = {
    "feat": {"priority": 1, "keywords": ["new", "add", "create", "新增", "添加", "新建", "创建", "实现"]},
    "fix": {"priority": 2, "keywords": ["fix", "bug", "修复", "修正", "解决", "补丁"]},
    "docs": {"priority": 5, "keywords": ["doc", "readme", "文档", "说明"]},
    "style": {"priority": 6, "keywords": ["style", "css", "样式", "格式", "排版"]},
    "refactor": {"priority": 3, "keywords": ["refactor", "重构", "重写", "优化", "简化"]},
    "perf": {"priority": 3, "keywords": ["perf", "性能", "加速", "缓存", "lazy"]},
    "test": {"priority": 4, "keywords": ["test", "spec", "测试", "用例", "e2e"]},
    "chore": {"priority": 7, "keywords": ["chore", "deps", "config", "依赖", "配置", "升级"]},
    "ci": {"priority": 7, "keywords": ["ci", "pipeline", "deploy", "部署", "构建"]},
    "build": {"priority": 7, "keywords": ["build", "webpack", "vite", "打包", "编译"]},
}


def detect_type_from_files(files: list) -> tuple:
    """Detect Conventional Commit type from file changes."""
    scores = Counter()

    for f in files:
        path = f["path"].lower()
        status = f["status"]

        # File extension based
        if path.endswith(".md"):
            scores["docs"] += 3
        if any(path.endswith(ext) for ext in [".css", ".scss", ".less", ".sass"]):
            scores["style"] += 3
        if any(path.endswith(ext) for ext in [".test.", ".spec."]):
            scores["test"] += 5
        if "test" in path or "spec" in path or "__tests__" in path:
            scores["test"] += 3
        if any(name in path for name in ["eslint", "prettier", "husky", "commitlint"]):
            scores["chore"] += 4
        if "package.json" in path or "package-lock" in path or "pnpm-lock" in path:
            scores["chore"] += 3

        # Status based
        if status == "A" or status == "??":
            scores["feat"] += 2
        if status == "M":
            scores["fix"] += 1

    if not scores:
        return "chore", 0

    return scores.most_common(1)[0]


def detect_scope_from_files(files: list) -> Optional[str]:
    """Detect scope from changed file paths."""
    path_parts = Counter()

    for f in files:
        path = f["path"]
        parts = path.split("/")
        if len(parts) >= 2 and parts[0] == "src":
            scope = parts[1] if len(parts) > 1 else parts[0]
            if scope not in (".", "..", "*"):
                path_parts[scope] += 2
        elif len(parts) >= 1:
            scope = parts[0]
            if scope not in (".", "..", "*"):
                path_parts[scope] += 1

    if path_parts:
        scope, count = path_parts.most_common(1)[0]
        if count >= 2:
            return scope
    return None


# ============================================================
# Diff analysis
# ============================================================

def analyze_diff(diff_text: str) -> dict:
    """Extract meaningful info from git diff."""
    if not diff_text:
        return {"added_lines": 0, "removed_lines": 0, "file_count": 0, "keywords": []}

    lines = diff_text.split("\n")
    added = 0
    removed = 0
    file_count = 0
    keywords = []

    # Keywords to track
    interesting_words = [
        "component", "组件", "page", "页面", "api", "接口",
        "button", "按钮", "modal", "弹窗", "form", "表单",
        "table", "表格", "list", "列表", "hook", "util",
        "function", "函数", "class", "style", "样式",
        "config", "配置", "route", "路由", "auth", "认证",
        "login", "登录", "register", "注册",
    ]

    word_counts = Counter()

    for line in lines:
        if line.startswith("diff --git"):
            file_count += 1
        elif line.startswith("+") and not line.startswith("+++"):
            added += 1
            for word in interesting_words:
                if word.lower() in line.lower():
                    word_counts[word] += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1

    keywords = [w for w, _ in word_counts.most_common(8)]

    return {
        "added_lines": added,
        "removed_lines": removed,
        "file_count": file_count,
        "keywords": keywords,
    }


# ============================================================
# Commit message generation
# ============================================================

def generate_subject(cc_type: str, analysis: dict, lang: str = "zh") -> str:
    """Generate commit subject line."""
    keywords = analysis.get("keywords", [])

    if lang == "zh":
        if cc_type == "feat":
            if "组件" in keywords or "component" in keywords:
                return "添加新组件"
            elif "页面" in keywords or "page" in keywords:
                return "新增页面"
            elif "api" in keywords or "接口" in keywords:
                return "接入新接口"
            else:
                return "添加新功能"
        elif cc_type == "fix":
            if "修复" in keywords:
                return "修复问题"
            return "修复 Bug"
        elif cc_type == "docs":
            return "更新文档"
        elif cc_type == "style":
            return "调整样式"
        elif cc_type == "refactor":
            return "重构代码"
        elif cc_type == "perf":
            return "优化性能"
        elif cc_type == "test":
            return "添加测试"
        elif cc_type == "chore":
            return "更新配置/依赖"
        else:
            return "更新"
    else:
        subjects = {
            "feat": "add new feature",
            "fix": "fix bug",
            "docs": "update docs",
            "style": "update styles",
            "refactor": "refactor code",
            "perf": "improve performance",
            "test": "add tests",
            "chore": "update config/deps",
            "ci": "update CI",
            "build": "update build",
        }
        return subjects.get(cc_type, "update")


def generate_body(files: list, analysis: dict, lang: str = "zh") -> str:
    """Generate commit body from file changes."""
    body_lines = []

    if lang == "zh":
        for f in files:
            status = f["status"]
            path = f["path"]
            filename = Path(path).name

            if status == "A":
                body_lines.append(f"- 新增 {filename}")
            elif status == "D":
                body_lines.append(f"- 移除 {filename}")
            elif status == "M":
                body_lines.append(f"- 修改 {filename}")
            elif status.startswith("R"):
                body_lines.append(f"- 重命名 {filename}")
    else:
        for f in files:
            status = f["status"]
            path = f["path"]
            filename = Path(path).name

            if status == "A":
                body_lines.append(f"- Add {filename}")
            elif status == "D":
                body_lines.append(f"- Remove {filename}")
            elif status == "M":
                body_lines.append(f"- Update {filename}")
            elif status.startswith("R"):
                body_lines.append(f"- Rename {filename}")

    return "\n".join(body_lines)


def format_commit_message(
    cc_type: str,
    scope: Optional[str],
    subject: str,
    body: str,
    breaking: bool = False,
    closes: str = "",
    lang: str = "zh",
) -> str:
    """Format complete commit message."""
    scope_part = f"({scope})" if scope else ""
    header = f"{cc_type}{scope_part}: {subject}"

    parts = [header, ""]

    if body:
        parts.append(body)

    if breaking:
        if lang == "zh":
            parts.extend(["", "BREAKING CHANGE: 此版本包含不兼容的变更"])
        else:
            parts.extend(["", "BREAKING CHANGE: This version contains breaking changes"])

    if closes:
        parts.extend(["", f"Closes #{closes}"])

    return "\n".join(parts)


def generate_full_message(
    files: list,
    diff_text: str,
    lang: str = "zh",
    custom_type: str = "",
    custom_scope: str = "",
    custom_subject: str = "",
    breaking: bool = False,
    closes: str = "",
) -> dict:
    """Generate complete commit message with all metadata."""

    # Analyze diff
    analysis = analyze_diff(diff_text)

    # Detect type
    if custom_type:
        cc_type = custom_type
    else:
        cc_type, _ = detect_type_from_files(files)
        # If no files to analyze, default to chore
        if not files and cc_type == "chore":
            cc_type = "chore"

    # Detect scope
    if custom_scope:
        scope = custom_scope if custom_scope != "-" else None
    else:
        scope = detect_scope_from_files(files)

    # Generate subject
    if custom_subject:
        subject = custom_subject
    else:
        subject = generate_subject(cc_type, analysis, lang)

    # Generate body
    body = generate_body(files, analysis, lang)

    message = format_commit_message(cc_type, scope, subject, body, breaking, closes, lang)

    return {
        "type": cc_type,
        "scope": scope,
        "subject": subject,
        "body": body,
        "message": message,
        "analysis": analysis,
        "files": files,
    }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="GitMate - Commit message generator")
    parser.add_argument("--detect", action="store_true", help="Detect staged changes only")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Language (zh/en)")
    parser.add_argument("--type", default="", help="Force commit type (feat/fix/docs/...)")
    parser.add_argument("--scope", default="", help="Force commit scope")
    parser.add_argument("--subject", default="", help="Custom subject line")
    parser.add_argument("--breaking", action="store_true", help="Mark as breaking change")
    parser.add_argument("--closes", default="", help="Issue number to close")
    parser.add_argument("--cwd", default=".", help="Working directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Get staged files
    files = get_staged_files(args.cwd)

    # Get diff
    diff_text = get_staged_diff(args.cwd)

    if args.detect:
        analysis = analyze_diff(diff_text)
        print(f"暂存文件数: {len(files)}")
        print(f"新增行: {analysis['added_lines']}")
        print(f"移除行: {analysis['removed_lines']}")
        print(f"关键词: {', '.join(analysis['keywords'])}")
        print()
        for f in files:
            print(f"  {f['status']}\t{f['path']}")
        return

    # Generate
    result = generate_full_message(
        files=files,
        diff_text=diff_text,
        lang=args.lang,
        custom_type=args.type,
        custom_scope=args.scope,
        custom_subject=args.subject,
        breaking=args.breaking,
        closes=args.closes,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, default=str))
        return

    # Output
    if args.lang == "zh":
        print(f"类型: {result['type']} | 范围: {result['scope'] or '无'}")
        print(f"变更文件: {len(result['files'])} 个")
        print("=" * 50)
        print(result["message"])
        print("=" * 50)
        print()
        print("📋 可直接运行:")
        print(f'  git commit -m "{result["message"].split(chr(10))[0]}"')
        print("或复制上方完整 message 到编辑器中提交。")
    else:
        print(f"Type: {result['type']} | Scope: {result['scope'] or 'none'}")
        print(f"Changed files: {len(result['files'])}")
        print("=" * 50)
        print(result["message"])
        print("=" * 50)


if __name__ == "__main__":
    import json
    main()
