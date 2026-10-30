"""Detect patterns known to cause data leaks or security incidents."""

import re
from pathlib import Path

RULE_ID = "code/dangerous_patterns"
SEVERITY = "HIGH"

PATTERNS = [
    (re.compile(r"verify\s*=\s*False"), "TLS verification disabled"),
    (re.compile(r"dangerouslySetInnerHTML"), "Unescaped HTML injection in React"),
    (re.compile(r"eval\s*\("), "Use of eval()"),
    (re.compile(r"exec\s*\("), "Use of exec()"),
    (re.compile(r"subprocess\.[a-z]+\([^)]*shell\s*=\s*True"), "Shell injection risk"),
]

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}
SCAN_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".py"}


def scan(root: Path):
    findings = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern, label in PATTERNS:
                if pattern.search(line):
                    findings.append({
                        "rule": RULE_ID,
                        "severity": SEVERITY,
                        "file": str(path.relative_to(root)),
                        "line": lineno,
                        "message": label,
                    })
    return findings