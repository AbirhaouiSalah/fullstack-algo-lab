"""Run the Python algorithm assessment suite through pytest."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--test-file",
        action="append",
        default=[],
        help="Test path relative to the repository root. Repeat for multiple files.",
    )
    parser.add_argument(
        "--test-name",
        help="Run only tests matching this pytest expression.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    test_paths = args.test_file or ["algorithms"]
    command = [sys.executable, "-m", "pytest", *test_paths]

    if args.test_name:
        command.extend(["-k", args.test_name])

    print(f"Running: {' '.join(command)}")
    completed = subprocess.run(command, cwd=REPOSITORY_ROOT, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())