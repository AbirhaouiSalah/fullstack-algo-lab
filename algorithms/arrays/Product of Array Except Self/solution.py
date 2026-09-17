def solve(list_int : list[int])->list[int]:
    prod_except_self =[]
    for elm in range(len(list_int)) :
        prod_except_self.append(1)
    for i in range(len(list_int)):
        for j in range(len(list_int)):
            if i==j : continue 
            prod_except_self[i]=prod_except_self[i]*list_int[j]
    return prod_except_self

def solve2(list_int : list[int])->list[int]:
    prod_execept_self = []
    suffix = []
    prefix = []
     
    for i in range(len(list_int)):
        prod_execept_self.append(1)
        suffix.append(1)
        prefix.append(1)

    n = len(list_int)

    for i in range(1,n):
        prefix[i]=prefix[i-1]*list_int[i-1]
    for j in range(n-2,-1,-1):
        suffix[j]=suffix[j+1]*list_int[j+1]
 
    # lets define suffix and prefix as follows 
    for i in range(n):
        prod_execept_self[i] = suffix[i] * prefix[i]

    return prod_execept_self