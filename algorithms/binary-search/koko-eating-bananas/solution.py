"""Koko Eating Bananas: binary search on the answer k, without scanning every k from 1 to max(piles)."""


class koko_eating_bananas:
    def __init__(self):
        pass

    @staticmethod
    def hours_needed(piles: list[int], k: int) -> int:
        """Total hours at rate k: each pile costs ceil(p / k)."""
        return sum((p + k - 1) // k for p in piles)

    @staticmethod
    def can_finish(piles: list[int], k: int, h: int) -> bool:
        """Same check, but stops as soon as the hours exceed h."""
        hours = 0
        for p in piles:
            hours += (p + k - 1) // k
            if hours > h:
                return False
        return True

    # 1. Lower bound sur k : fenetre semi-ouverte [1, max], on garde la plus petite valeur faisable
    def search(self, piles: list[int], h: int) -> int:
        l, r = 1, max(piles)

        while l < r:
            mid = l + (r - l) // 2
            if self.hours_needed(piles, mid) <= h:
                r = mid  # mid marche, la reponse est mid ou plus petit
            else:
                l = mid + 1  # mid trop lent

        return l

    # 2. Fenetre fermee [l, r] : on memorise le meilleur k trouve (meme style que Binary Search classique)
    def search_closed_window(self, piles: list[int], h: int) -> int:
        l, r = 1, max(piles)
        res = r

        while l <= r:
            mid = l + (r - l) // 2
            if self.hours_needed(piles, mid) <= h:
                res = mid
                r = mid - 1
            else:
                l = mid + 1

        return res

    # 3. Verification avec sortie anticipee : on arrete de sommer des que les heures depassent h
    def search_early_exit(self, piles: list[int], h: int) -> int:
        l, r = 1, max(piles)

        while l < r:
            mid = l + (r - l) // 2
            if self.can_finish(piles, mid, h):
                r = mid
            else:
                l = mid + 1

        return l

    # 4. Bornes resserrees : ceil(total / h) <= k <= min(max, ceil(total / (h - n + 1)))
    def search_tight_bounds(self, piles: list[int], h: int) -> int:
        n, total = len(piles), sum(piles)
        l = max(1, -(-total // h))
        r = min(max(piles), -(-total // (h - n + 1)))

        while l < r:
            mid = l + (r - l) // 2
            if self.hours_needed(piles, mid) <= h:
                r = mid
            else:
                l = mid + 1

        return l

    # 5. Bornes resserrees + sortie anticipee
    def search_tight_early_exit(self, piles: list[int], h: int) -> int:
        n, total = len(piles), sum(piles)
        l = max(1, -(-total // h))
        r = min(max(piles), -(-total // (h - n + 1)))

        while l < r:
            mid = l + (r - l) // 2
            if self.can_finish(piles, mid, h):
                r = mid
            else:
                l = mid + 1

        return l


def solve(piles: list[int], h: int) -> int:
    solver = koko_eating_bananas()
    return solver.search(piles, h)


def solve_closed_window(piles: list[int], h: int) -> int:
    return koko_eating_bananas().search_closed_window(piles, h)


def solve_early_exit(piles: list[int], h: int) -> int:
    return koko_eating_bananas().search_early_exit(piles, h)


def solve_tight_bounds(piles: list[int], h: int) -> int:
    return koko_eating_bananas().search_tight_bounds(piles, h)


def solve_tight_early_exit(piles: list[int], h: int) -> int:
    return koko_eating_bananas().search_tight_early_exit(piles, h)