def solve_naive(nums):
    if len(nums) <= 1:
        return False

    n = len(nums)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if nums[i] == nums[j]:
                return True

    return False


def _contains_value_from(nums, target, j):
    if j >= len(nums):
        return False
    if nums[j] == target:
        return True
    return _contains_value_from(nums, target, j + 1)


def _has_duplicate_from(nums, i):
    if i >= len(nums):
        return False
    if _contains_value_from(nums, nums[i], i + 1):
        return True
    return _has_duplicate_from(nums, i + 1)


def solve_recursive(nums):
    if len(nums) <= 1:
        return False
    return _has_duplicate_from(nums, 0)


def solve_hash_set(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def solve(nums):
    return solve_hash_set(nums)
