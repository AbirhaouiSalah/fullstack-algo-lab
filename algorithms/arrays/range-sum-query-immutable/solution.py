class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i, n in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + n

    def sum_range(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]


def solve(nums, queries):
    na = NumArray(nums)
    return [na.sum_range(left, right) for left, right in queries]
