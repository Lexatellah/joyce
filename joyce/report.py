"""Pretty terminal and JSON report rendering for JOYCE."""

import json
from colorama import Fore, Style, init

init(autoreset=True)

SEVERITY_COLOR = {
    "CRITICAL": Fore.RED + Style.BRIGHT,
    "HIGH": Fore.YELLOW + Style.BRIGHT,
    "MEDIUM": Fore.CYAN,
    "LOW": Fore.WHITE,
}


def render_terminal(result):
    score = result["score"]
    if score >= 80:
        verdict, color = "READY", Fore.GREEN + Style.BRIGHT
    elif score >= 50:
        verdict, color = "NEEDS WORK", Fore.YELLOW + Style.BRIGHT
    else:
        verdict, color = "NOT READY", Fore.RED + Style.BRIGHT

    bar = "═" * 52
    print(f"\n╔{bar}╗")
    print(f"║  JOYCE — Production Readiness Report{' ' * 15}║")
    print(f"╠{bar}╣")
    print(f"║  Project : {result['project']:<37}║")
    print(f"║  Score   : {score:>3} / 100   {verdict:<19}║")
    print(f"╚{bar}╝\n")

    if not result["findings"]:
        print(Fore.GREEN + "  ✨ No issues found. Ship it.\n")
        return

    by_sev = {}
    for f in result["findings"]:
        by_sev.setdefault(f["severity"], []).append(f)

    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    for sev in order:
        items = by_sev.get(sev)
        if not items:
            continue
        print(f"{SEVERITY_COLOR[sev]}[{sev}] {len(items)} finding(s)")
        for item in items:
            loc = f"{item['file']}:{item['line']}" if item["line"] else item["file"]
            print(f"  • {loc:<40} — {item['message']}")
        print()


def render_json(result):
    return json.dumps(result, indent=2)