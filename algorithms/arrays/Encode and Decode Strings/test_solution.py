import importlib.util
import inspect
import random
import string
import time
from pathlib import Path

import pytest

solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("generated_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


def test_solution_module_loads():
    assert solution_module is not None


# test the examples written int the exercice section


def test_example():

    solution = solution_module.Solution3()

    test_input = ["Hello", "World"]
    expected_output = ["Hello", "World"]

    assert solution.decode(solution.encode(test_input)) == expected_output

    test_input = [""]
    expected_output = [""]

    assert solution.decode(solution.encode(test_input)) == expected_output


# ---------------------------------------------------------------------------
# Edge cases combining length, content and separator
# ---------------------------------------------------------------------------

EDGE_CASES = [
    ("empty_list", []),
    ("single_empty_string", [""]),
    ("multiple_empty_strings", ["", "", ""]),
    ("single_char_each", ["a", "b", "c"]),
    ("contains_delimiter_char", ["a#b", "c"]),
    ("delimiter_only_strings", ["#", "##", "###"]),
    ("delimiter_at_edges", ["#abc", "abc#", "#abc#"]),
    ("consecutive_delimiters_only", ["####"]),
    ("long_single_string", ["x" * 10_000]),
    ("many_short_strings", ["s"] * 2000),
    ("unicode_content", ["héllo", "wörld", "日本語", "🙂🙃", "Ω≈ç√"]),
    # If Solution3's delimiter is a fixed character (even a "safe" unicode
    # one), this fails whenever real content contains that exact character -
    # no fixed delimiter is safe in an absolute sense, only "safe enough for
    # a given input domain". A length-prefixed encoding has no such blind spot.
    ("contains_private_use_char", ["a\ue000b", "c"]),
    ("whitespace_and_newlines", ["line1\nline2", "\t\ttabbed", "   spaced   "]),
    ("digits_that_look_like_length_prefix", ["3#abc", "0#", "10#short"]),
    ("mixed_lengths_and_empties", ["", "a", "", "bb", ""]),
    ("single_element_list", ["only one"]),
]


@pytest.mark.parametrize(
    "strs",
    [strs for _, strs in EDGE_CASES],
    ids=[case_id for case_id, _ in EDGE_CASES],
)
def test_round_trip_edge_cases(strs):
    solution = solution_module.Solution3()
    assert solution.decode(solution.encode(strs)) == strs


ALPHABETS = {
    "ascii": string.ascii_letters + string.digits + " ",
    "delimiter_heavy": "#" * 6 + string.ascii_letters[:4],
    "unicode": "héllo日本語🙂#Ω\ue000",
}


def _random_string(rng, length, alphabet):
    return "".join(rng.choice(alphabet) for _ in range(length))


def test_round_trip_random_fuzz():
    rng = random.Random(1234)
    solution = solution_module.Solution3()

    for _ in range(200):
        count = rng.choice([0, 1, 2, 5, 20])
        alphabet = ALPHABETS[rng.choice(list(ALPHABETS))]
        strs = [_random_string(rng, rng.choice([0, 1, 3, 10, 50]), alphabet) for _ in range(count)]
        assert solution.decode(solution.encode(strs)) == strs, f"round-trip failed for {strs!r}"


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


# ---------------------------------------------------------------------------
# Encode/decode specific benchmark - compares every Solution-like class found
# in the module (Solution, Solution3, ...) side by side
# ---------------------------------------------------------------------------


def _candidate_solution_classes():
    classes = [
        (name, obj)
        for name, obj in inspect.getmembers(solution_module, inspect.isclass)
        if obj.__module__ == solution_module.__name__
        and hasattr(obj, "encode")
        and hasattr(obj, "decode")
    ]
    return sorted(classes, key=lambda item: item[0])


def _generate_strings(rng, count, length, alphabet):
    return [_random_string(rng, length, alphabet) for _ in range(count)]


def run_edge_case_report():
    classes = _candidate_solution_classes()
    if not classes:
        print("Aucune classe avec encode/decode trouvee.")
        return

    print("\nRapport des cas limites (longueur / contenu / separateur)")
    header = f"{'Cas':>36} | " + " | ".join(f"{name:>10}" for name, _ in classes)
    print(header)
    print("-" * len(header))

    for case_id, strs in EDGE_CASES:
        row = [f"{case_id:>36}"]
        for _, klass in classes:
            instance = klass()
            try:
                ok = instance.decode(instance.encode(strs)) == strs
                row.append(f"{'OK' if ok else 'CASSE':>10}")
            except (AttributeError, IndexError, TypeError, ValueError, RecursionError):
                row.append(f"{'erreur':>10}")
        print(" | ".join(row))


def run_encode_decode_benchmark():
    sizes = [(10, 20), (100, 50), (1_000, 20), (1_000, 500), (10_000, 10)]
    profiles = ["ascii", "delimiter_heavy", "unicode"]
    repetitions = 3
    rng = random.Random(42)

    classes = _candidate_solution_classes()
    if not classes:
        print("Aucune classe avec encode/decode trouvee.")
        return

    print("\nBenchmark encode/decode genere automatiquement")
    header = f"{'Classe':>12} | {'profil':>16} | {'n':>7} | {'len':>6} | {'temps moyen (ms)':>18} | {'round-trip':>10}"
    print(header)
    print("-" * len(header))

    for class_name, klass in classes:
        instance = klass()
        for count, length in sizes:
            for profile in profiles:
                alphabet = ALPHABETS[profile]
                strs = _generate_strings(rng, count, length, alphabet)

                try:
                    round_trip_ok = instance.decode(instance.encode(strs)) == strs
                except (AttributeError, IndexError, TypeError, ValueError, RecursionError) as error:
                    print(
                        f"{class_name:>12} | {profile:>16} | {count:>7,} | {length:>6} | {'-':>18} | erreur: {error}"
                    )
                    continue

                start = time.perf_counter()
                for _ in range(repetitions):
                    instance.decode(instance.encode(strs))
                elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions

                status = "OK" if round_trip_ok else "CASSE"
                print(
                    f"{class_name:>12} | {profile:>16} | {count:>7,} | {length:>6} | {elapsed_ms:>18.4f} | {status:>10}"
                )


if __name__ == "__main__":
    run_benchmark()
    run_edge_case_report()
    run_encode_decode_benchmark()
