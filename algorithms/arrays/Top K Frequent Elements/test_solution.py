from solution import solve_hint_1, solve_hint_2, solve_hint_3

def batch(args0, args1, args2):
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