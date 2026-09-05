from collections import defaultdict


def solve_hint_1(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    groups_list = defaultdict(list)
    groups_occurences = defaultdict(list)
    # strs :: ["str", ... ]
    # lets start by sorting the list
    sorted_strs = sorted(strs)
#   print(sorted_strs)
#    print(strs)
    # signature with ascii 
    for str in strs :
        codes = [ord(c) for c in str]
        if str in groups.keys():
            groups_occurences[str]+=1
        else :
            groups_occurences[str]=1
        groups[str]=sum(codes)
    # print(groups_occurences)
    # print(groups)



    # unique keys :
    # group anagram using unique keys 
    list_values = list(groups.values())
    unique = sorted(set(list_values))
    for ascci_number in unique:
        for i ,val in enumerate(groups):
    #        print(groups[val])
    #        print(ascci_number)
            if groups[val] == ascci_number :
                groups_list[ascci_number].append(val)
    # print("XXXXXXXX")
    # print(groups_list)
    for i, val in enumerate(groups):
    #    print(i,val,groups_occurences[val])
        if groups_occurences[val] < 2 : continue
        for i in range(groups_occurences[val] - 1):
            groups_list[groups[val]].append(val)
    # print(groups_list)
    return list(groups_list.values())


def solve_hint_2(strs: list[str]) -> list[list[str]]:

    groups = defaultdict(list)        # string -> ascii-sum signature
    groups_list = defaultdict(list)   # ascii-sum signature -> list of strings

    # STEP 1: signature = sum of ASCII codes, then the unique signatures
    for s in strs:
        codes = [ord(c) for c in s]
        groups[s] = sum(codes)
    unique = sorted(set(groups.values()))

    # STEP 2: group strings sharing a signature (loop over strs, not groups,
    # so repeated input strings aren't lost)
    for ascii_number in unique:
        for s in strs:
            if groups[s] == ascii_number:
                groups_list[ascii_number].append(s)

    # STEP 3
    return list(groups_list.values())


def solve_hint_3(strs: list[str]) -> list[list[str]]:
    groups = {}

    return list(groups.values())

def main():
    # expected = [["hat"], ["act", "cat"], ["pots", "stop", "tops"]]
    # input_strs = ["act", "pots", "tops", "cat", "stop", "hat"]
    # result = solve_hint_1(input_strs)
    # print(result)
    # result=solve_hint_1(["x"]) == [["x"]]
    # print(result)

#     # result = solve_hint_1([""]) == [[""]]
    # print(result)

    result = solve_hint_1(["", "", "a", "a", "aa", "a", "baa", "aba"])
    print(result)
    print(result == [["", ""], ["a", "a", "a"], ["aa"], ["aba", "baa"]])

if __name__ == "__main__":
    main()