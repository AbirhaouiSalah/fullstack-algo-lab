"""Find Minimum In Rotated Sorted Array — implement after solving the problem.

Define the signature from the official statement before writing the algorithm.
"""
"""Find Minimum in Rotated Sorted Array in O(log n), without min(nums) or a linear scan."""


class find_minimum:
    def __init__(self):
        pass

    # 1. Compare mid avec la borne droite : si nums[mid] > nums[r], le minimum est a droite de mid
    def search(self, nums: list[int]) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            mid = l + (r - l) // 2
            if nums[mid] > nums[r]:
                l = mid + 1  # mid est dans le segment gauche (trop grand), le minimum est apres
            else:
                r = mid  # mid est dans le segment droit : mid peut etre le minimum

        return nums[l]

    # 2. Style NeetCode : fenetre fermee, on garde le meilleur candidat, sortie rapide si la fenetre est triee
    def search_closed_window(self, nums: list[int]) -> int:
        l, r = 0, len(nums) - 1
        res = nums[0]

        while l <= r:
            if nums[l] < nums[r]:  # fenetre deja triee : son minimum est nums[l]
                res = min(res, nums[l])
                break
            mid = l + (r - l) // 2
            res = min(res, nums[mid])
            if nums[mid] >= nums[l]:
                l = mid + 1  # mid dans le segment gauche, le minimum est a droite
            else:
                r = mid - 1

        return res

    # 3. Compare mid avec nums[0] : predicat "mid est dans le segment gauche" (vrai...vrai faux...faux)
    def search_compare_first(self, nums: list[int]) -> int:
        if nums[0] <= nums[-1]:
            return nums[0]  # pas de rotation effective

        l, r = 1, len(nums) - 1
        while l < r:
            mid = l + (r - l) // 2
            if nums[mid] >= nums[0]:
                l = mid + 1
            else:
                r = mid

        return nums[l]

    # 4. Cherche directement le point de rupture (nums[i] > nums[i + 1]) avec les voisins de mid
    def search_pivot(self, nums: list[int]) -> int:
        n = len(nums)
        if nums[0] <= nums[-1]:
            return nums[0]

        l, r = 0, n - 1
        while l <= r:
            mid = l + (r - l) // 2
            if mid + 1 < n and nums[mid] > nums[mid + 1]:
                return nums[mid + 1]  # rupture juste apres mid
            if mid > 0 and nums[mid - 1] > nums[mid]:
                return nums[mid]  # rupture juste avant mid
            if nums[mid] > nums[0]:
                l = mid + 1
            else:
                r = mid - 1

        return nums[0]

    # 5. Sauts de puissances de 2 : dernier indice du segment gauche, le minimum est le suivant (modulo n)
    def search_jump(self, nums: list[int]) -> int:
        n = len(nums)
        first = nums[0]

        pos = 0
        step = 1 << (n.bit_length() - 1)
        while step:
            nxt = pos + step
            if nxt < n and nums[nxt] >= first:
                pos = nxt
            step >>= 1

        return nums[(pos + 1) % n]

    # 6. Diviser pour regner : une moitie est toujours triee (retour immediat), l'autre recurse -> O(log n)
    def search_divide_conquer(self, nums: list[int]) -> int:
        def helper(l: int, r: int) -> int:
            if nums[l] <= nums[r]:
                return nums[l]  # segment trie : son minimum est son premier element
            mid = l + (r - l) // 2
            return min(helper(l, mid), helper(mid + 1, r))

        return helper(0, len(nums) - 1)


def solve(nums: list[int]) -> int:
    finder = find_minimum()
    return finder.search(nums)


def solve_closed_window(nums: list[int]) -> int:
    return find_minimum().search_closed_window(nums)


def solve_compare_first(nums: list[int]) -> int:
    return find_minimum().search_compare_first(nums)


def solve_pivot(nums: list[int]) -> int:
    return find_minimum().search_pivot(nums)


def solve_jump(nums: list[int]) -> int:
    return find_minimum().search_jump(nums)


def solve_divide_conquer(nums: list[int]) -> int:
    return find_minimum().search_divide_conquer(nums)