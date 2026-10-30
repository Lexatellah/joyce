#!/usr/bin/env python3
"""JOYCE - Job-Oriented Yield & Code Examiner. CLI entry point."""

import sys
from pathlib import Path

import click

from joyce.scanner import run_scan
from joyce.report import render_terminal, render_json


@click.group()
@click.version_option("0.1.0", prog_name="JOYCE")
def cli():
    """JOYCE - scan your repo before it scans you."""


@cli.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Emit JSON instead of a pretty report.")
@click.option("--out", "out_file", type=click.Path(), default=None, help="Write JSON report to a file.")
def scan(path, as_json, out_file):
    """Scan PATH and report production readiness."""
    result = run_scan(Path(path))

    if out_file:
        Path(out_file).write_text(render_json(result), encoding="utf-8")
        click.echo(f"Report written to {out_file}")

    if as_json:
        click.echo(render_json(result))
    else:
        render_terminal(result)

    sys.exit(0 if result["score"] >= 80 else 1)


if __name__ == "__main__":
    cli()
