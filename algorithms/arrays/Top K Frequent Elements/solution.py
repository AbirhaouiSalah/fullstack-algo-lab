import heapq


def solve_hint_1(args0, args1):
    nums, k = args0, args1
    if not nums or k <= 0:
        return []

    frequencies = {}
    for num in nums:
        frequencies[num] = frequencies.get(num, 0) + 1

    return sorted(frequencies, key=frequencies.get, reverse=True)[:k]


def solve_hint_2(args0, args1):
    nums, k = args0, args1
    if not nums or k <= 0:
        return []

    frequencies = {}
    for num in nums:
        frequencies[num] = frequencies.get(num, 0) + 1

    return [
        num
        for _, num in heapq.nlargest(
            k, ((frequency, num) for num, frequency in frequencies.items())
        )
    ]


def solve_hint_3(args0, args1):
    nums, k = args0, args1
    if not nums or k <= 0:
        return []

    frequencies = {}
    for num in nums:
        frequencies[num] = frequencies.get(num, 0) + 1

    max_frequency = max(frequencies.values())
    buckets = [[] for _ in range(max_frequency + 1)]
    for num, frequency in frequencies.items():
        buckets[frequency].append(num)

    result = []
    for frequency in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[frequency])
        if len(result) >= k:
            return result[:k]
    return result


def solve(args0, args1, args2):
    case = args2
    if case == 0:
        return solve_hint_1(args0, args1)
    if case == 1:
        return solve_hint_2(args0, args1)
    if case == 2:
        return solve_hint_3(args0, args1)
    raise ValueError(f"Invalid case number: {case}")


def main():
    print("lancer le code pour le problème Top K Frequent Elements")
    # Analyse de complexité : O(n log n) pour le tri du dictionnaire par fréquence décroissante
    print(
        "Analyse de complexité : O(n log n) pour le tri du dictionnaire par fréquence décroissante"
    )

    print("Test case : Hint 1")
    print(solve([1, 1, 1, 2, 2, 3], 2, 0))
    print(solve([1], 1, 0))


if __name__ == "__main__":
    main()
