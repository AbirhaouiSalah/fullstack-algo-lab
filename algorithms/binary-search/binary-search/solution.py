"""Implement Binary Search without using list.index, bisect or linear scanning."""


class binary_search:
    def __init__(self):
        pass

    # 1. Classique : fenetre fermee [l, r], boucle while
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = l + (r - l) // 2  # avoids overflow in other languages
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1

    # 2. Recursive : meme logique, la pile d'appels remplace la boucle
    def search_recursive(self, nums: list[int], target: int) -> int:
        def helper(l: int, r: int) -> int:
            if l > r:
                return -1
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                return helper(mid + 1, r)
            return helper(l, mid - 1)

        return helper(0, len(nums) - 1)

    # 3. Lower bound : fenetre semi-ouverte [l, r), une seule comparaison < par tour
    def search_lower_bound(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums)

        while l < r:
            mid = l + (r - l) // 2
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid

        return l if l < len(nums) and nums[l] == target else -1

    # 4. Sauts de puissances de 2 (Bentley) : pas de mid, pas de r
    def search_jump(self, nums: list[int], target: int) -> int:
        n = len(nums)
        if n == 0:
            return -1

        pos = -1
        step = 1 << (n.bit_length() - 1)  # plus grande puissance de 2 <= n
        while step:
            nxt = pos + step
            if nxt < n and nums[nxt] <= target:
                pos = nxt
            step >>= 1

        return pos if pos >= 0 and nums[pos] == target else -1

    # 5. Interpolation : estime la position selon la valeur (O(log log n) si donnees uniformes)
    def search_interpolation(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r and nums[l] <= target <= nums[r]:
            if nums[l] == nums[r]:  # une seule valeur restante (evite la division par 0)
                return l if nums[l] == target else -1
            pos = l + (target - nums[l]) * (r - l) // (nums[r] - nums[l])
            if nums[pos] == target:
                return pos
            if nums[pos] < target:
                l = pos + 1
            else:
                r = pos - 1

        return -1

    # 6. Exponentielle (galloping) : double la borne puis binary search dans [bound/2, bound]
    def search_exponential(self, nums: list[int], target: int) -> int:
        n = len(nums)
        if n == 0:
            return -1
        if nums[0] == target:
            return 0

        bound = 1
        while bound < n and nums[bound] < target:
            bound <<= 1

        l, r = bound >> 1, min(bound, n - 1)
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1


def solve(nums: list[int], target: int) -> int:
    searcher = binary_search()
    return searcher.search(nums, target)


def solve_recursive(nums: list[int], target: int) -> int:
    return binary_search().search_recursive(nums, target)


def solve_lower_bound(nums: list[int], target: int) -> int:
    return binary_search().search_lower_bound(nums, target)


def solve_jump(nums: list[int], target: int) -> int:
    return binary_search().search_jump(nums, target)


def solve_interpolation(nums: list[int], target: int) -> int:
    return binary_search().search_interpolation(nums, target)


def solve_exponential(nums: list[int], target: int) -> int:
    return binary_search().search_exponential(nums, target)