import importlib.util
import inspect
import random
import time
from pathlib import Path

import pytest


solution_path = Path(__file__).with_name("solution.py")
spec = importlib.util.spec_from_file_location("valid_anagram_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution_module)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        # --- Provided examples ---
        ("racecar", "carrace", True),
        ("jar", "jam", False),
        ("x", "x", True),

        # --- Single character ---
        ("a", "b", False),
        ("a", "a", True),

        # --- Different lengths ---
        ("ab", "abc", False),
        ("abc", "ab", False),
        ("a", "aa", False),
        ("a" * 10, "a" * 11, False),

        # --- Same length, different content ---
        ("ab", "cd", False),
        ("abcd", "abce", False),
        ("abc", "abd", False),

        # --- Same characters, different order ---
        ("listen", "silent", True),
        ("evil", "vile", True),
        ("anagram", "nagaram", True),
        ("triangle", "integral", True),

        # --- Repeated characters ---
        ("aabbcc", "abcabc", True),
        ("aabbcc", "aabbcd", False),
        ("aaab", "baaa", True),
        ("aaa", "aaaa", False),

        # --- All same character ---
        ("aaaa", "aaaa", True),
        ("aaaa", "aaab", False),
        ("zzzzz", "zzzzz", True),

        # --- Same total count, different distribution ---
        ("aabb", "abab", True),
        ("aabb", "abbb", False),
        ("aabbcc", "aabccd", False),

        # --- Prefix / suffix traps ---
        ("abcdef", "fabcde", True),
        ("abcdef", "abcde", False),
        ("abc", "cba", True),

        # --- Palindromes ---
        ("racecar", "racecar", True),
        ("abba", "baab", True),
        ("abcba", "abcba", True),

        # --- Boundary: max length 50_000 ---
        ("a" * 50_000, "a" * 50_000, True),
        ("a" * 50_000, "a" * 49_999 + "b", False),
        ("ab" * 25_000, "ba" * 25_000, True),
        ("ab" * 25_000, "ab" * 24_999 + "aa", False),

        # ---------------------------------------------------------------
        # Sum-of-ord() collisions.
        # Same character sum, different content. MUST return False.
        # Any solution based on ord sums, XOR of chars, or char products
        # will fail these.
        # ---------------------------------------------------------------
        ("ad", "bc", False),       # 97+100  == 98+99    == 197
        ("ae", "bd", False),       # 97+101  == 98+100   == 198
        ("af", "be", False),       # 97+102  == 98+101   == 199
        ("af", "cd", False),       # 97+102  == 99+100   == 199
        ("az", "mn", False),       # 97+122  == 109+110  == 219
        ("abcd", "aadd", False),   # 394 == 394
        ("aabb", "aaac", False),   # 390 == 390
        ("ad" * 500, "bc" * 500, False),     # 500*197 == 500*197
        ("af" * 1000, "be" * 1000, False),   # 1000*199 == 1000*199
        ("az" * 500, "mn" * 500, False),     # 500*219 == 500*219

        # --- Sanity: XOR-equal AND anagram ---
        ("ab", "ba", True),
        ("aabb", "bbaa", True),
    ],
)
def test_is_anagram_returns_expected(s, t, expected):
    assert solution_module.solve(s, t) is expected


def test_is_anagram_is_symmetric():
    """If s and t are anagrams, then t and s must also be anagrams."""
    cases = [
        ("racecar", "carrace"),
        ("listen", "silent"),
        ("anagram", "nagaram"),
        ("aabbcc", "abcabc"),
        ("a" * 1000, "a" * 1000),
    ]
    for s, t in cases:
        assert solution_module.solve(s, t) == solution_module.solve(t, s)


def test_is_anagram_returns_bool():
    """The solution must return an actual bool, not a truthy/falsy value."""
    assert isinstance(solution_module.solve("abc", "cba"), bool)
    assert isinstance(solution_module.solve("abc", "abd"), bool)


def test_is_anagram_reflexive():
    """Every string is an anagram of itself."""
    for s in ["a", "ab", "abc", "aabbcc", "racecar", "a" * 1000]:
        assert solution_module.solve(s, s) is True


# ---------------------------------------------------------------------------
# Benchmark (required by algorithms/test-all.py)
# ---------------------------------------------------------------------------

def _candidate_functions():
    return [
        function
        for name, function in inspect.getmembers(solution_module, inspect.isfunction)
        if function.__module__ == solution_module.__name__
        and (name == "solve" or name.startswith("solve_"))
    ]


def _build_pairs(size):
    """Return {case_name: (s, t)} pairs of the given size.

    - "anagram"   : t is a shuffled copy of s (no early-exit possible)
    - "non-anag"  : t is s with one character changed (same length)
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    s = "".join(random.choice(alphabet) for _ in range(size))

    shuffled = list(s)
    random.shuffle(shuffled)
    t_anagram = "".join(shuffled)

    changed = list(s)
    changed[0] = "z" if changed[0] != "z" else "y"
    t_not_anagram = "".join(changed)

    return {
        "anagram": (s, t_anagram),
        "non-anag": (s, t_not_anagram),
    }


def run_benchmark():
    sizes = [100, 1_000, 5_000, 10_000]
    repetitions = 3
    random.seed(42)
    candidates = _candidate_functions()

    print("\nBenchmark genere automatiquement (Valid Anagram)")
    print(f"{'Fonction':>24} | {'n':>8} | {'cas':>10} | {'Temps moyen (ms)':>18}")
    print("-" * 74)

    for function in candidates:
        for size in sizes:
            pairs = _build_pairs(size)
            for case_name, (s, t) in pairs.items():
                try:
                    function(s, t)  # warm-up
                    start = time.perf_counter()
                    for _ in range(repetitions):
                        function(s, t)
                    elapsed_ms = (time.perf_counter() - start) * 1_000 / repetitions
                except (AttributeError, IndexError, TypeError, ValueError, RecursionError) as error:
                    print(f"{function.__name__:>24} | {size:>8,} | {case_name:>10} | ignoree: {error}")
                    continue
                print(f"{function.__name__:>24} | {size:>8,} | {case_name:>10} | {elapsed_ms:>18.4f}")

    if not candidates:
        print("Aucune fonction solve ou solve_* trouvee.")