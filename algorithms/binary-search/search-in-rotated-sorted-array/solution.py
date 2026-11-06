"""Search In Rotated Sorted Array — implement after solving the problem.

Define the signature from the official statement before writing the algorithm.
"""

"""Search in Rotated Sorted Array in O(log n), without list.index, bisect or linear scanning."""


class search_rotated:
    def __init__(self):
        pass

    @staticmethod
    def find_pivot(nums: list[int]) -> int:
        """Index of the minimum (start of the right segment); 0 if the array is not rotated."""
        l, r = 0, len(nums) - 1
        while l < r:
            mid = l + (r - l) // 2
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                r = mid
        return l

    @staticmethod
    def binary_search(nums: list[int], target: int, l: int, r: int) -> int:
        """Classic binary search restricted to nums[l..r] (inclusive)."""
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return -1

    # 1. Une seule passe : a chaque tour, une moitie est triee, on regarde si target y est
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid

            if nums[l] <= nums[mid]:  # moitie gauche triee
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            else:  # moitie droite triee
                if nums[mid] < target <= nums[r]:
                    l = mid + 1
                else:
                    r = mid - 1

        return -1

    # 2. Deux passes : on trouve le pivot, on choisit le bon segment, puis binary search classique dedans
    def search_pivot_segment(self, nums: list[int], target: int) -> int:
        pivot = self.find_pivot(nums)

        if nums[pivot] <= target <= nums[-1]:
            return self.binary_search(nums, target, pivot, len(nums) - 1)
        return self.binary_search(nums, target, 0, pivot - 1)

    # 3. Deux passes : pivot, puis binary search sur le tableau "remis en ordre" virtuellement
    def search_virtual_shift(self, nums: list[int], target: int) -> int:
        n = len(nums)
        pivot = self.find_pivot(nums)

        l, r = 0, n - 1
        while l <= r:
            mid = l + (r - l) // 2
            real = (mid + pivot) % n  # position reelle de la mid-ieme valeur dans l'ordre trie
            if nums[real] == target:
                return real
            elif nums[real] < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1

    # 4. Astuce de l'infini : si mid et target sont dans des segments differents, mid vaut +inf (target a gauche) ou -inf (target a droite)
    def search_infinity_trick(self, nums: list[int], target: int) -> int:
        first = nums[0]
        target_is_left = target >= first
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = l + (r - l) // 2
            value = nums[mid]
            if (value >= first) != target_is_left:
                value = float("inf") if target_is_left else float("-inf")
            if value == target:
                return mid
            elif value < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1

    # 5. Recursive : meme logique que la version 1
    def search_recursive(self, nums: list[int], target: int) -> int:
        def helper(l: int, r: int) -> int:
            if l > r:
                return -1
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]:
                    return helper(l, mid - 1)
                return helper(mid + 1, r)
            if nums[mid] < target <= nums[r]:
                return helper(mid + 1, r)
            return helper(l, mid - 1)

        return helper(0, len(nums) - 1)


def solve(nums: list[int], target: int) -> int:
    searcher = search_rotated()
    return searcher.search(nums, target)


def solve_pivot_segment(nums: list[int], target: int) -> int:
    return search_rotated().search_pivot_segment(nums, target)


def solve_virtual_shift(nums: list[int], target: int) -> int:
    return search_rotated().search_virtual_shift(nums, target)


def solve_infinity_trick(nums: list[int], target: int) -> int:
    return search_rotated().search_infinity_trick(nums, target)


def solve_recursive(nums: list[int], target: int) -> int:
    return search_rotated().search_recursive(nums, target)
