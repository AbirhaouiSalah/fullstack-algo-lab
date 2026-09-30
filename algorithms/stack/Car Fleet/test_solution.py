import importlib.util
from pathlib import Path
import random
import time
from fractions import Fraction

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("stack_car_fleet_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)
car_fleet = solution_module.car_fleet


def test_car_fleet_counts_merged_and_independent_cars():
    assert car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3


def test_car_fleet_handles_single_car_and_empty_input():
    assert car_fleet(10, [3], [3]) == 1
    assert solution_module.solve(10, [], []) == 0


def test_car_fleet_handles_cars_that_never_catch_up():
    assert car_fleet(100, [0, 20, 40], [1, 1, 1]) == 3


def _reference_car_fleet(target, positions, speeds):
    cars = sorted(zip(positions, speeds), reverse=True)
    fleets = 0
    latest_arrival = None
    for position, speed in cars:
        arrival = Fraction(target - position, speed)
        if latest_arrival is None or arrival > latest_arrival:
            fleets += 1
            latest_arrival = arrival
    return fleets


def test_car_fleet_seeded_random_inputs_match_exact_reference():
    rng = random.Random(991)
    for _ in range(500):
        target = rng.randint(2, 100)
        positions = sorted(rng.sample(range(target), rng.randint(0, min(target, 12))))
        speeds = [rng.randint(1, 20) for _ in positions]
        assert car_fleet(target, positions, speeds) == _reference_car_fleet(
            target, positions, speeds
        )


def run_benchmark():
    print("\nBenchmark: Car Fleet")
    print(f"{'Cars':>12} | {'Temps (ms)':>12}")
    print("-" * 28)
    for size in (1_000, 10_000, 100_000):
        positions = list(range(size))
        speeds = [(index * 17) % 97 + 1 for index in range(size)]
        started = time.perf_counter()
        result = car_fleet(size + 1, positions, speeds)
        elapsed_ms = (time.perf_counter() - started) * 1_000
        assert 1 <= result <= size
        print(f"{size:>12,} | {elapsed_ms:>12.4f}")