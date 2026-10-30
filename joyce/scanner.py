"""JOYCE core scanning engine."""

from pathlib import Path
from .rules import ALL_RULES
from .scoring import compute_score


def run_scan(root: Path):
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Not a directory: {root}")

    findings = []
    for rule_module in ALL_RULES:
        try:
            findings.extend(rule_module.scan(root))
        except Exception as exc:  # a broken rule must never crash the run
            findings.append({
                "rule": "engine/error",
                "severity": "LOW",
                "file": str(rule_module.__name__),
                "line": 0,
                "message": f"Rule crashed: {exc}",
            })

    score = compute_score(findings)
    return {
        "project": root.name,
        "score": score,
        "findings": findings,
    }