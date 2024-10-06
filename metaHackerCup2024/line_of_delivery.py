import bisect
from sortedcontainers import SortedList

FILE_PATH = "line_of_delivery_part_1_input.txt"


def solve_problem_1(E_i_s, G):
    N = len(E_i_s)
    E_i_s.sort()
    r_index = bisect.bisect_right(E_i_s, G)
    l_index = r_index - 1
    indexes = [r_index, l_index]
    solutions = []
    for index in indexes:
        if 0 <= index < N:
            diff = abs(G - E_i_s[index])
            rev_index = N - index  # 1 based rev_index
            solutions.append((diff, rev_index))
    return min(solutions)



def solve_problem_2_bruteforce(E_i_s):
    N = len(E_i_s)
    positions = []
    for j, e_i in enumerate(E_i_s):
        new_positions = []
        x = e_i
        # print(f"{j},{e_i}: Planning to insert {e_i=} in {positions=}")
        i = 0
        while i < len(positions):
            a = positions[i]
            if x < a:
                new_positions.append(x)
                # print(f"{j},{e_i}: Adding new stone {e_i} as {x}")
                break
            # print(f"{j},{e_i}: Adding existing stone at {a - 1}")
            new_positions.append(a - 1)
            x += 1
            # print(f"{j},{e_i}: Incremented new stone's pos {e_i} to {x=}")
            i += 1
        if i == len(positions):
            new_positions.append(x)
            # print(f"{j},{e_i}: Adding new stone {e_i} as {x}")
        new_positions.extend(positions[i:])
        positions = new_positions
        # print(f"{j},{e_i}: Post: {positions=}")
    return positions


with open(FILE_PATH) as f:
    # T = int(f.readline())
    # # for t in range(T):
    # _N, _G = map(int, f.readline().split())
    # _E_i_s = list(map(int, (f.readline() for n in range(_N))))
    _E_i_s = [4, 5, 6, 7]
    print(f"Original positions are {_E_i_s}")
    print(solve_problem_2_bruteforce(_E_i_s))
    # solution = solve_problem_2(_E_i_s, _G)
    # solution_index = solution[1]
    # solution_val = solution[0]
    # print(f"Case #{t + 1}: {solution_index} {solution_val}")




