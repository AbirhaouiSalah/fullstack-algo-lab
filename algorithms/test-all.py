"""Compatibility entry point for the Python algorithm test runner."""

from pathlib import Path
import runpy


RUNNER = Path(__file__).parent.parent / "scripts" / "algorithms" / "test-all.py"

runpy.run_path(str(RUNNER), run_name="__main__")