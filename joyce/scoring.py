"""Convert findings into a 0–100 Production Readiness Score."""

SEVERITY_WEIGHTS = {
    "CRITICAL": 25,
    "HIGH": 12,
    "MEDIUM": 5,
    "LOW": 1,
}


def compute_score(findings):
    penalty = 0
    for f in findings:
        penalty += SEVERITY_WEIGHTS.get(f["severity"], 1)
    return max(0, 100 - penalty)