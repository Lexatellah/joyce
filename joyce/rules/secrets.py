"""Detect hardcoded API keys and secrets in source files."""

import re
from pathlib import Path

RULE_ID = "secrets/api_keys"
SEVERITY = "CRITICAL"

# Patterns are intentionally conservative to avoid false positives.
PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI-style key"),
    (re.compile(r"sk_live_[A-Za-z0-9]{20,}"), "Stripe live key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\."), "JWT-looking string"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
]

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}
SCAN_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".py", ".env", ".json", ".yaml", ".yml", ".md"}


def scan(root: Path):
    findings = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS and path.name != ".env":
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
                        "message": f"{label} hardcoded in source",
                    })
                    break  # one finding per line is enough
    return findings