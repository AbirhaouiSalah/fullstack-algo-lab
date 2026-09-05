#!/usr/bin/env bash

set -u

REPOSITORY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALGORITHMS_ROOT="$REPOSITORY_ROOT/algorithms"
PYTHON_BIN="${PYTHON_BIN:-$REPOSITORY_ROOT/.venv/bin/python3}"
RUNNER="$ALGORITHMS_ROOT/test-all.py"

if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi

create_test_file() {
  local problem_dir="$1"
  local test_file="$problem_dir/test_solution.py"
  local solution_file="$problem_dir/solution.py"

  cat > "$test_file" <<PYTHON
import importlib.util
import inspect
import random
import time
from pathlib import Path


solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("generated_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


def test_solution_module_loads():
    assert solution_module is not None


def _candidate_functions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_"))
    ]


def _arguments_for(function, size):
    parameters = list(inspect.signature(function).parameters.values())
    if any(parameter.kind == inspect.Parameter.VAR_POSITIONAL for parameter in parameters):
        return None
    if len(parameters) == 1:
        return ([random.randrange(-1_000_000, 1_000_001) for _ in range(size)],)
    if len(parameters) == 2:
        values = [random.randrange(-1_000_000, 1_000_001) for _ in range(size)]
        return (values, random.randrange(-1_000_000, 1_000_001))
    return None


def run_benchmark():
    sizes = [100, 1_000, 5_000, 10_000]
    repetitions = 3
    random.seed(42)
    candidates = _candidate_functions()

    print("\\nBenchmark genere automatiquement")
    print(f"{'Fonction':>24} | {'n':>8} | {'Temps moyen (ms)':>18}")
    print("-" * 58)
    for function in candidates:
        for size in sizes:
            arguments = _arguments_for(function, size)
            if arguments is None:
                print(f"{function.__name__:>24} | {'-':>8} | signature non supportee")
                break
            try:
                function(*arguments)
                start = time.perf_counter()
                for _ in range(repetitions):
                    function(*arguments)
                elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
            except Exception as error:
                print(f"{function.__name__:>24} | {size:>8,} | ignoree: {error}")
                break
            print(f"{function.__name__:>24} | {size:>8,} | {elapsed_ms:>18.4f}")

    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")
PYTHON

  echo "Created: ${test_file#$REPOSITORY_ROOT/}"
}

benchmark_count=0
while IFS= read -r -d '' solution_file; do
  problem_dir="$(dirname "$solution_file")"
  test_file="$problem_dir/test_solution.py"

  if [[ ! -f "$test_file" ]]; then
    create_test_file "$problem_dir"
  fi

  if grep -q "^def run_benchmark" "$test_file"; then
    benchmark_count=$((benchmark_count + 1))
    relative_test_file="${test_file#$REPOSITORY_ROOT/}"
    "$PYTHON_BIN" "$RUNNER" --test-file "$relative_test_file" --benchmark
  else
    echo "Skipped (no run_benchmark): ${test_file#$REPOSITORY_ROOT/}"
  fi
done < <(find "$ALGORITHMS_ROOT" -type f -name solution.py \
  ! -path '*/.venv/*' ! -path '*/__pycache__/*' -print0 | sort -z)

echo "Benchmarks launched: $benchmark_count"
