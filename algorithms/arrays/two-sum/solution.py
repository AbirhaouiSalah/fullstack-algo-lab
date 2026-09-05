def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    raise ValueError("No two sum solution exists")


def two_sum_brute_force(nums, target):
    for first_index in range(len(nums)):
        for second_index in range(first_index + 1, len(nums)):
            if nums[first_index] + nums[second_index] == target:
                return [first_index, second_index]
    raise ValueError("No two sum solution exists")

def two_sum_hash_map(nums: list[int], target: int) -> list[int]:
    # build a second solution 
    i,j=0,0
    for i in range(len(nums)):
        diff = target - nums[i]
        if diff in nums:
            j = nums.index(diff)
            if i != j:
                return [i,j]
            else:
                continue
    return []
    