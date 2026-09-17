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

    print("\nBenchmark genere automatiquement")
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
            except (AttributeError, IndexError, TypeError, ValueError, RecursionError) as error:
                print(f"{function.__name__:>24} | {size:>8,} | ignoree: {error}")
                break
            print(f"{function.__name__:>24} | {size:>8,} | {elapsed_ms:>18.4f}")

    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")
