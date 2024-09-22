#!/usr/bin/env python3

"""Linting scripts for Cosmosys project."""

import subprocess
import sys

import typer

app = typer.Typer()


@app.command()
def run_pylint() -> None:
    """Run Pylint on the project."""
    result = subprocess.run(
        ["pylint", "cosmosys", "tests", "scripts"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        sys.exit(result.returncode)


@app.command()
def run_mypy() -> None:
    """Run Mypy on the project."""
    result = subprocess.run(
        ["mypy", "cosmosys", "tests", "scripts"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        sys.exit(result.returncode)


@app.command()
def run_ruff() -> None:
    """Run Ruff on the project."""
    result = subprocess.run(
        ["ruff", "cosmosys", "tests", "scripts"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        sys.exit(result.returncode)


@app.command()
def lint_all() -> None:
    """Run all linters on the project."""
    run_pylint()
    run_mypy()
    run_ruff()


def run_lint() -> None:
    """Entry point for the linting scripts."""
    if len(sys.argv) == 1:
        # No arguments were provided, default to lint_all
        lint_all()
    else:
        # Otherwise, use Typer to handle commands
        app()


if __name__ == "__main__":
    run_lint()
