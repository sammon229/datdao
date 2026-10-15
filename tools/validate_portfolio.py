"""Run lightweight, dependency-free integrity checks for the portfolio.

This intentionally validates structure and syntax without executing notebooks,
downloading data, calling external APIs, or modifying project artifacts.
"""

from __future__ import annotations

import ast
import csv
import json
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "node_modules"}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.references.append(value)


def files(pattern: str) -> list[Path]:
    return [p for p in ROOT.rglob(pattern) if not any(part in SKIP_DIRS for part in p.parts)]


def check_python() -> list[str]:
    problems: list[str] = []
    for path in files("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            problems.append(f"Python syntax: {path.relative_to(ROOT)}: {exc}")
    return problems


def check_javascript() -> list[str]:
    node = shutil.which("node")
    if not node:
        return ["JavaScript syntax: node was not available; check skipped"]
    problems: list[str] = []
    for path in files("*.js"):
        result = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
        if result.returncode:
            detail = (result.stderr or result.stdout).strip().splitlines()[-1]
            problems.append(f"JavaScript syntax: {path.relative_to(ROOT)}: {detail}")
    return problems


def check_notebooks() -> list[str]:
    problems: list[str] = []
    for path in files("*.ipynb"):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"Notebook JSON: {path.relative_to(ROOT)}: {exc}")
            continue
        for number, cell in enumerate(notebook.get("cells", []), 1):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            source = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith(("%", "!")))
            try:
                ast.parse(source, filename=f"{path} cell {number}")
            except SyntaxError as exc:
                problems.append(f"Notebook syntax: {path.relative_to(ROOT)} cell {number}: {exc.msg}")
    return problems


def check_markdown_links() -> list[str]:
    problems: list[str] = []
    for readme in files("README.md"):
        for match in LINK_RE.finditer(readme.read_text(encoding="utf-8")):
            target = match.group(1).strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http:", "https:", "mailto:")):
                continue
            candidate = Path(unquote(target))
            if not (readme.parent / candidate).exists():
                problems.append(f"Markdown link: {readme.relative_to(ROOT)} -> {target}")
    return problems


def check_html_assets() -> list[str]:
    problems: list[str] = []
    for html in [ROOT / "index.html", ROOT / "projects" / "bigboymission" / "showcase.html"]:
        parser = AssetParser()
        parser.feed(html.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = reference.split("?", 1)[0].split("#", 1)[0]
            if not target or target.startswith(("http:", "https:", "mailto:", "#", "/")):
                continue
            if not (html.parent / unquote(target)).exists():
                problems.append(f"HTML asset: {html.relative_to(ROOT)} -> {reference}")
    return problems


def check_csv() -> list[str]:
    problems: list[str] = []
    for path in files("*.csv"):
        try:
            with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
                sample = next(reader, [])
            if not header or not any(str(value).strip() for value in header):
                problems.append(f"CSV header: {path.relative_to(ROOT)} is empty")
            elif sample and len(sample) != len(header):
                problems.append(f"CSV shape: {path.relative_to(ROOT)} header has {len(header)} fields, sample has {len(sample)}")
        except OSError as exc:
            problems.append(f"CSV read: {path.relative_to(ROOT)}: {exc}")
    return problems


def check_binary_artifacts() -> list[str]:
    problems: list[str] = []
    for extension in ("*.docx", "*.pptx"):
        for path in files(extension):
            if not zipfile.is_zipfile(path):
                problems.append(f"Office archive: {path.relative_to(ROOT)} is not a valid ZIP package")
    for path in files("*.pdf"):
        try:
            with path.open("rb") as handle:
                if handle.read(5) != b"%PDF-":
                    problems.append(f"PDF header: {path.relative_to(ROOT)} is invalid")
        except OSError as exc:
            problems.append(f"PDF read: {path.relative_to(ROOT)}: {exc}")
    return problems


def check_r() -> list[str]:
    problems: list[str] = []
    for path in files("*.R") + files("*.r"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            problems.append(f"R source: {path.relative_to(ROOT)} is empty")
        if text.count("{") != text.count("}"):
            problems.append(f"R source: {path.relative_to(ROOT)} has unbalanced braces")
    return problems


def main() -> int:
    checks = [
        ("Python", check_python),
        ("JavaScript", check_javascript),
        ("Notebooks", check_notebooks),
        ("Markdown links", check_markdown_links),
        ("HTML assets", check_html_assets),
        ("CSV samples", check_csv),
        ("Office/PDF artifacts", check_binary_artifacts),
        ("R source", check_r),
    ]
    problems: list[str] = []
    for name, check in checks:
        found = check()
        problems.extend(found)
        print(f"{name}: {'PASS' if not found else f'{len(found)} issue(s)'}")
    if problems:
        print("\nIssues:")
        print("\n".join(f"- {problem}" for problem in problems))
        return 1
    print("\nPortfolio validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
