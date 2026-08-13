
def solve_hint_1(args0, args1):
    # TODO: implement solution
    # passer en argument la liste d'entiers et k, retourner les k éléments les plus fréquents
    nums, k = args0, args1
    # genere un dictionaire qui associe chaque élément à sa fréquence
    freq_nums = {}

    if not nums:
        return []

    elif k <= 0:
        return []

    elif len(nums) < 2:
        return nums

    freq_nums = {num: freq_nums.get(num, 0) + 1 for num in nums}

    for elm in freq_nums:
        print(f"elm: {elm} freq: {freq_nums[elm]}")
        for number in nums:
            if number == elm:
                print(f"number: {number} is equal to elm: {elm}")
                freq_nums[elm] = freq_nums.get(elm, 0) + 1
        if freq_nums[elm] == 1:
            print(f"elm: {elm} is not already in freq_nums")
            freq_nums[elm] = 1
        elif freq_nums[elm] > 1:
            print(f"elm: {elm} is already in freq_nums")
            freq_nums[elm] -= 1

    for num, freq in freq_nums.items():
        num_freq = 0
        print(f"num: {num} freq: {freq}")

    # for num in nums:
    #     if num in freq_nums:
    #         print(f"num: {num} is already in freq_nums")    
    #         print(f"num: {freq_nums[num]} is already in freq_nums")    
    #         freq_nums[num] += 1
    #     else:
    #         print(f"num: {num} is not already in freq_nums")    
    #         print(f"num: {freq_nums[num]} is already in freq_nums")    
    #         freq_nums.append([num,1])
    # 
    # trier le dictionnaire par fréquence décroissante
    # freq_nums.sort(key=lambda x: x[1], reverse=True)

    # retourner les k éléments les plus fréquents
    # return [num for num, freq in freq_nums[:k]]
    return sorted(freq_nums, key=freq_nums.get, reverse=False)[:k]

def solve_hint_2(args0, args1):
    # TODO: implement solution
    pass

def solve_hint_3(args0, args1):
    # TODO: implement solution
    pass

def solve(args0, args1, args2):
    # generate a case statet and define serveral solver for each case
    case = args2
    try :
        if case == 0:
            return solve_hint_1(args0, args1)
        if case == 1:
            return solve_hint_2(args0, args1)
        if case == 2:
            return solve_hint_3(args0, args1)
    except:
        return print("Error: invalid case number")

def main():
    print("lancer le code pour le problème Top K Frequent Elements")
    # Analyse de complexité : O(n log n) pour le tri du dictionnaire par fréquence décroissante
    print("Analyse de complexité : O(n log n) pour le tri du dictionnaire par fréquence décroissante")

    print("Test case : Hint 1")
    try:
        print(solve([1,1,1,2,2,3], 2, 0))
        print(solve([1], 1, 0))
    except Exception as e:
        print(f"Error: {e}")

    
#    print("Test case : Hint 2")
#    print(solve([1], 2, 1))
#
#    print("Test case : Hint 3")
#    print(solve([9,4,-4,-2,-2,4,4,9,9,9], 3, 2))
#

if __name__ == "__main__":
    main()
