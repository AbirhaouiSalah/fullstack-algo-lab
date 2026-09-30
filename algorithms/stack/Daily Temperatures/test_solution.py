import importlib.util
import itertools
from pathlib import Path
import random
import time

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_daily_temperatures_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
daily_temperatures = solution_module.daily_temperatures


def test_daily_temperatures_returns_days_until_a_warmer_temperature():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_daily_temperatures_handles_equal_and_non_increasing_values():
    assert daily_temperatures([70, 70, 69]) == [0, 0, 0]
    assert solution_module.solve([30, 40, 50]) == [1, 1, 0]


def test_daily_temperatures_handles_empty_input():
    assert daily_temperatures([]) == []


def _brute_force_daily_temperatures(temperatures):
    waits = [0] * len(temperatures)
    for day, temperature in enumerate(temperatures):
        for future_day in range(day + 1, len(temperatures)):
            if temperatures[future_day] > temperature:
                waits[day] = future_day - day
                break
    return waits


def test_daily_temperatures_exhaustive_small_inputs():
    for length in range(7):
        for temperatures in itertools.product(range(3), repeat=length):
            values = list(temperatures)
            assert daily_temperatures(values) == _brute_force_daily_temperatures(values)


def test_daily_temperatures_seeded_random_inputs_match_brute_force():
    rng = random.Random(731)
    for _ in range(250):
        temperatures = [rng.randint(30, 100) for _ in range(rng.randint(0, 40))]
        assert daily_temperatures(temperatures) == _brute_force_daily_temperatures(temperatures)


def run_benchmark():
    print("\nBenchmark: Daily Temperatures")
    print(f"{'Jours':>12} | {'Temps (ms)':>12}")
    print("-" * 28)
    for size in (1_000, 10_000, 100_000):
        temperatures = [(index * 37) % 71 + 30 for index in range(size)]
        started = time.perf_counter()
        result = daily_temperatures(temperatures)
        elapsed_ms = (time.perf_counter() - started) * 1_000
        assert len(result) == size
        print(f"{size:>12,} | {elapsed_ms:>12.4f}")