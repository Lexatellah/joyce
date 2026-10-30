"""Detect committed .env files and secret-bearing filenames."""

from pathlib import Path

RULE_ID = "env/committed"
SEVERITY = "CRITICAL"

SUSPICIOUS_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".env.prod",
    "secrets.json",
    "credentials.json",
}

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}


def scan(root: Path):
    findings = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SUSPICIOUS_NAMES:
            findings.append({
                "rule": RULE_ID,
                "severity": SEVERITY,
                "file": str(path.relative_to(root)),
                "line": 0,
                "message": f"{path.name} is present in the repository — likely a leaked secret file",
            })
    return findings