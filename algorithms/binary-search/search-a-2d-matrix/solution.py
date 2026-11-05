"""Search a 2D Matrix in O(log(m * n)) without any(target in row ...) or a full linear scan."""


class search_matrix:
    def __init__(self):
        pass

    # 1. Deux binary search : d'abord la ligne (via ses bornes), puis la valeur dans la ligne
    def search(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        top, bot = 0, len(matrix) - 1
        while top <= bot:
            row = top + (bot - top) // 2
            if target > matrix[row][-1]:
                top = row + 1
            elif target < matrix[row][0]:
                bot = row - 1
            else:
                break  # target est dans [premier, dernier] de cette ligne
        else:
            return False

        l, r = 0, len(matrix[row]) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if matrix[row][mid] == target:
                return True
            elif matrix[row][mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return False

    # 2. Matrice "aplatie" virtuellement : un seul binary search sur 0..m*n-1
    def search_flat(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        n = len(matrix[0])
        l, r = 0, len(matrix) * n - 1
        while l <= r:
            mid = l + (r - l) // 2
            value = matrix[mid // n][mid % n]
            if value == target:
                return True
            elif value < target:
                l = mid + 1
            else:
                r = mid - 1
        return False

    # 3. Lower bound aplati : fenetre semi-ouverte, une comparaison < par tour
    def search_flat_lower_bound(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n
        while l < r:
            mid = l + (r - l) // 2
            if matrix[mid // n][mid % n] < target:
                l = mid + 1
            else:
                r = mid
        return l < m * n and matrix[l // n][l % n] == target

    # 4. Ligne par premier element (derniere ligne dont le debut <= target), puis lower bound dans la ligne
    def search_first_column(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        l, r = 0, len(matrix)
        while l < r:
            mid = l + (r - l) // 2
            if matrix[mid][0] <= target:
                l = mid + 1
            else:
                r = mid
        if l == 0:
            return False  # target plus petit que tout
        row = matrix[l - 1]

        l, r = 0, len(row)
        while l < r:
            mid = l + (r - l) // 2
            if row[mid] < target:
                l = mid + 1
            else:
                r = mid
        return l < len(row) and row[l] == target

    # 5. Escalier (coin haut-droit) : O(m + n), marche aussi sans la 2e contrainte (Search a 2D Matrix II)
    def search_staircase(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        r, c = 0, len(matrix[0]) - 1
        while r < len(matrix) and c >= 0:
            value = matrix[r][c]
            if value == target:
                return True
            if value > target:
                c -= 1
            else:
                r += 1
        return False


def solve(matrix: list[list[int]], target: int) -> bool:
    searcher = search_matrix()
    return searcher.search(matrix, target)


def solve_flat(matrix: list[list[int]], target: int) -> bool:
    return search_matrix().search_flat(matrix, target)


def solve_flat_lower_bound(matrix: list[list[int]], target: int) -> bool:
    return search_matrix().search_flat_lower_bound(matrix, target)


def solve_first_column(matrix: list[list[int]], target: int) -> bool:
    return search_matrix().search_first_column(matrix, target)


def solve_staircase(matrix: list[list[int]], target: int) -> bool:
    return search_matrix().search_staircase(matrix, target)