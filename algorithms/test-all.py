"""Run the Python algorithm assessment suite through pytest."""

from __future__ import annotations

import argparse
import importlib.util
import shlex
import subprocess
import sys
import time
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ALGORITHMS_ROOT = REPOSITORY_ROOT / "algorithms"


def discover_problems() -> list[Path]:
    return sorted(
        (
            solution.parent
            for solution in ALGORITHMS_ROOT.rglob("solution.py")
            if ".venv" not in solution.parts and "__pycache__" not in solution.parts
        ),
        key=lambda path: str(path).casefold(),
    )


def print_problems() -> None:
    problems = discover_problems()
    print("Problemes disponibles :")
    for index, problem in enumerate(problems, start=1):
        test_file = problem / "test_solution.py"
        marker = "[test]" if test_file.exists() else "[sans test Python]"
        print(f"  {index:>2}. {problem.relative_to(ALGORITHMS_ROOT)} {marker}")


def select_problem(selector: str) -> Path:
    problems = discover_problems()
    if not problems:
        raise FileNotFoundError("Aucun probleme Python avec solution.py n'a ete trouve.")

    if selector.isdigit():
        index = int(selector)
        if 1 <= index <= len(problems):
            return problems[index - 1]
        raise ValueError(f"Numero de probleme invalide: {selector}")

    matches = [
        problem
        for problem in problems
        if selector.casefold() in str(problem.relative_to(ALGORITHMS_ROOT)).casefold()
    ]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise ValueError(f"Aucun probleme ne correspond a: {selector}")
    choices = ", ".join(str(path.relative_to(ALGORITHMS_ROOT)) for path in matches)
    raise ValueError(f"Selection ambigue ({choices}); utilisez le numero.")


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
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run the benchmark exposed by the selected test file after pytest.",
    )
    parser.add_argument(
        "--list-problems",
        action="store_true",
        help="List all Python problems and their numbered selections.",
    )
    parser.add_argument(
        "--problem",
        help="Select a problem by its number from --list-problems or by name.",
    )
    return parser.parse_args()


def run_benchmark(test_path: str) -> None:
    module_path = REPOSITORY_ROOT / test_path
    module_name = f"benchmark_{module_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load benchmark from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    benchmark = getattr(module, "run_benchmark", None)
    if benchmark is None:
        raise AttributeError(f"{test_path} does not define run_benchmark()")
    benchmark()


def main() -> int:
    args = parse_args()
    if args.list_problems:
        print_problems()
        return 0

    if args.test_file and args.problem:
        print("Utilisez --test-file ou --problem, pas les deux.", file=sys.stderr)
        return 2

    selected_problem = None
    if args.problem:
        try:
            selected_problem = select_problem(args.problem)
        except (FileNotFoundError, ValueError) as error:
            print(f"Erreur: {error}", file=sys.stderr)
            return 2
        selected_test = selected_problem / "test_solution.py"
        if not selected_test.exists():
            print(f"Erreur: aucun test Python dans {selected_problem}", file=sys.stderr)
            return 2
        test_paths = [str(selected_test.relative_to(REPOSITORY_ROOT))]
    else:
        test_paths = args.test_file or ["algorithms"]

    command = [sys.executable, "-m", "pytest", *test_paths]

    if args.test_name:
        command.extend(["-k", args.test_name])

    print(f"Running: {shlex.join(command)}")
    completed = subprocess.run(command, cwd=REPOSITORY_ROOT, check=False)

    if completed.returncode == 0 and args.benchmark:
        benchmark_path = test_paths[0] if selected_problem else args.test_file[0]
        if len(test_paths) != 1:
            print("--benchmark requires exactly one selected test file", file=sys.stderr)
            return 2
        started = time.perf_counter()
        run_benchmark(benchmark_path)
        print(f"Benchmark completed in {time.perf_counter() - started:.3f}s")

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())