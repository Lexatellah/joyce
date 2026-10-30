"""Detect misconfigured framework files (Firebase, Supabase, Next.js)."""

import re
from pathlib import Path

RULE_ID = "framework/misconfig"
SEVERITY = "HIGH"

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}


def scan(root: Path):
    findings = []

    # Firebase rules left public
    for path in root.rglob("firebase.json"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if re.search(r'"public"\s*:\s*true', text):
            findings.append({
                "rule": RULE_ID,
                "severity": SEVERITY,
                "file": str(path.relative_to(root)),
                "line": 0,
                "message": 'Firebase rules set to "public": true — database is world-readable',
            })

    # Supabase RLS reminder
    for path in root.rglob("supabase/config.toml"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "rls" in text.lower() and "false" in text.lower():
            findings.append({
                "rule": RULE_ID,
                "severity": SEVERITY,
                "file": str(path.relative_to(root)),
                "line": 0,
                "message": "Row Level Security appears disabled in Supabase config",
            })

    # Next.js / Vite debug flags
    for name in ("next.config.js", "next.config.mjs", "vite.config.js"):
        for path in root.rglob(name):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(r"ignoreBuildErrors\s*:\s*true", text):
                findings.append({
                    "rule": RULE_ID,
                    "severity": "MEDIUM",
                    "file": str(path.relative_to(root)),
                    "line": 0,
                    "message": "TypeScript build errors are ignored — broken code can ship",
                })

    return findings