"""Median of Two Sorted Arrays — implement after solving the problem.

Define the signature from the official statement before writing the algorithm.
"""
"""Median of Two Sorted Arrays in O(log(min(m, n))), without merging and sorting the full input."""


class median_finder:
    def __init__(self):
        pass

    # 1. Partition : binary search sur le nombre d'elements pris dans le plus petit tableau
    def search(self, nums1: list[int], nums2: list[int]) -> float:
        a, b = nums1, nums2
        if len(a) > len(b):
            a, b = b, a  # a est toujours le plus petit : la recherche porte sur min(m, n)

        total = len(a) + len(b)
        left_size = (total + 1) // 2  # taille de la moitie gauche (le milieu est a gauche si total impair)
        lo, hi = 0, len(a)

        while lo <= hi:
            i = lo + (hi - lo) // 2  # elements de a dans la moitie gauche
            j = left_size - i  # elements de b dans la moitie gauche

            a_left = a[i - 1] if i > 0 else float('-inf')
            a_right = a[i] if i < len(a) else float('inf')
            b_left = b[j - 1] if j > 0 else float('-inf')
            b_right = b[j] if j < len(b) else float('inf')

            if a_left <= b_right and b_left <= a_right:  # partition valide
                if total % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            elif a_left > b_right:
                hi = i - 1  # on a pris trop d'elements dans a
            else:
                lo = i + 1  # pas assez

        raise ValueError('Inputs must be sorted')

    # 2. k-ieme plus petit element : a chaque tour on elimine k/2 elements qui ne peuvent pas etre le k-ieme
    @staticmethod
    def kth_smallest(a: list[int], b: list[int], k: int) -> int:
        i = j = 0  # elements deja elimines dans a et b
        while True:
            if i >= len(a):
                return b[j + k - 1]
            if j >= len(b):
                return a[i + k - 1]
            if k == 1:
                return min(a[i], b[j])

            half = k // 2
            ni = min(i + half, len(a)) - 1  # candidat de coupe dans a
            nj = min(j + half, len(b)) - 1  # candidat de coupe dans b
            if a[ni] <= b[nj]:
                k -= ni - i + 1
                i = ni + 1
            else:
                k -= nj - j + 1
                j = nj + 1

    def search_kth(self, nums1: list[int], nums2: list[int]) -> float:
        total = len(nums1) + len(nums2)
        if total % 2:
            return float(self.kth_smallest(nums1, nums2, total // 2 + 1))
        return (self.kth_smallest(nums1, nums2, total // 2) + self.kth_smallest(nums1, nums2, total // 2 + 1)) / 2

    # 3. Binary search sur la VALEUR : plus petit x tel qu'au moins k elements sont <= x
    @staticmethod
    def count_le(arr: list[int], x: int) -> int:
        l, r = 0, len(arr)
        while l < r:
            mid = l + (r - l) // 2
            if arr[mid] <= x:
                l = mid + 1
            else:
                r = mid
        return l

    def kth_by_value(self, a: list[int], b: list[int], k: int) -> int:
        candidates_low = [arr[0] for arr in (a, b) if arr]
        candidates_high = [arr[-1] for arr in (a, b) if arr]
        lo, hi = min(candidates_low), max(candidates_high)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if self.count_le(a, mid) + self.count_le(b, mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def search_value_binary_search(self, nums1: list[int], nums2: list[int]) -> float:
        total = len(nums1) + len(nums2)
        if total % 2:
            return float(self.kth_by_value(nums1, nums2, total // 2 + 1))
        return (self.kth_by_value(nums1, nums2, total // 2) + self.kth_by_value(nums1, nums2, total // 2 + 1)) / 2

    # 4. Deux pointeurs : fusion partielle, on s'arrete a la moitie. O(m + n), O(1) espace
    def search_two_pointers(self, nums1: list[int], nums2: list[int]) -> float:
        m, n = len(nums1), len(nums2)
        total = m + n
        i = j = 0
        prev = cur = 0

        for _ in range(total // 2 + 1):
            prev = cur
            if i < m and (j >= n or nums1[i] <= nums2[j]):
                cur = nums1[i]
                i += 1
            else:
                cur = nums2[j]
                j += 1

        return float(cur) if total % 2 else (prev + cur) / 2

    # 5. Force brute : concatener et trier, O((m + n) log(m + n))
    def search_sort(self, nums1: list[int], nums2: list[int]) -> float:
        merged = sorted(nums1 + nums2)
        mid = len(merged) // 2
        return float(merged[mid]) if len(merged) % 2 else (merged[mid - 1] + merged[mid]) / 2


def solve(nums1: list[int], nums2: list[int]) -> float:
    finder = median_finder()
    return finder.search(nums1, nums2)


def solve_kth(nums1: list[int], nums2: list[int]) -> float:
    return median_finder().search_kth(nums1, nums2)


def solve_value_binary_search(nums1: list[int], nums2: list[int]) -> float:
    return median_finder().search_value_binary_search(nums1, nums2)


def solve_two_pointers(nums1: list[int], nums2: list[int]) -> float:
    return median_finder().search_two_pointers(nums1, nums2)


def solve_sort(nums1: list[int], nums2: list[int]) -> float:
    return median_finder().search_sort(nums1, nums2)