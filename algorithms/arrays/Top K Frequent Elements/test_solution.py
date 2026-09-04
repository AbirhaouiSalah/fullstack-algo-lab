import importlib.util
from pathlib import Path


solution_path = Path(__file__).with_name("solution.py")
solution_spec = importlib.util.spec_from_file_location("top_k_solution", solution_path)
if solution_spec is None or solution_spec.loader is None:
    raise ImportError(f"Cannot load solution from {solution_path}")

solution_module = importlib.util.module_from_spec(solution_spec)
solution_spec.loader.exec_module(solution_module)

solve_hint_1 = solution_module.solve_hint_1
solve_hint_2 = solution_module.solve_hint_2
solve_hint_3 = solution_module.solve_hint_3

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