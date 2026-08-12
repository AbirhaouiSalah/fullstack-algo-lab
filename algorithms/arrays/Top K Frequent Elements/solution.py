
def solve(args0, args1):
    # TODO: implement solution
    # passer en argument la liste d'entiers et k, retourner les k éléments les plus fréquents
    nums, k = args0, args1
    # genere un dictionaire qui associe chaque élément à sa fréquence
    freq_nums = []

    for num in nums:
        if num in freq_nums:
            freq_nums[num][1] += 1
        else:
            freq_nums.append([num,1])

    # trier le dictionnaire par fréquence décroissante
    freq_nums.sort(key=lambda x: x[1], reverse=True)

    # retourner les k éléments les plus fréquents
    return [num for num, freq in freq_nums[:k]]

def main():
    print(solve([1,1,1,2,2,3], 2))
    print(solve([1], 1))

if __name__ == "__main__":
    main()
