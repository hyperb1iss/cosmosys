#!/usr/bin/env python3

"""Lint script for the Cosmosys project."""

import subprocess
import sys
from typing import List, Tuple


def run_command(command: List[str]) -> Tuple[int, str]:
    """Run a command and return its exit code and output."""
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout


def run_lint() -> None:
    """Run linting checks on the project using pylint, mypy, and ruff."""
    print("Running linting checks...")

    linters = [
        ("Pylint", ["pylint", "cosmosys", "tests", "scripts"]),
        ("Mypy", ["mypy", "cosmosys", "tests", "scripts"]),
        ("Ruff", ["ruff", "check", "cosmosys", "tests", "scripts"]),
    ]

    exit_code = 0

    for linter_name, command in linters:
        print(f"\nRunning {linter_name}...")
        returncode, output = run_command(command)

        if returncode != 0:
            print(f"{linter_name} issues found:")
            print(output)
            exit_code = 1
        else:
            print(f"{linter_name} checks passed.")

    if exit_code == 0:
        print("\nAll linting checks passed!")
    else:
        print("\nLinting checks failed. Please fix the issues and try again.")

    sys.exit(exit_code)


if __name__ == "__main__":
    run_lint()
