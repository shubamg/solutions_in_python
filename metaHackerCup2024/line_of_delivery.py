import bisect
from sortedcontainers import SortedList

FILE_PATH = "line_of_delivery_part_2_sample_input.txt"


def solve_problem_1(E_i_s, G):
    E_i_s.sort()
    return get_nearest_stone_from_final_pos(E_i_s, G)


def get_nearest_stone_from_final_pos(E_i_s, G):
    N = len(E_i_s)
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
    positions = []
    for j, e_i in enumerate(E_i_s):
        new_positions = []
        x = e_i
        i = 0
        while i < len(positions):
            a = positions[i]
            if x < a:
                # Simple case: Stone reaches 0 energy at x and stops without collisions
                new_positions.append(x)
                break
            # Moving Stone collides with stone at 'a'. It stops at 'a' - 1, transferring energy to stone at 'a'
            new_positions.append(a - 1)
            # Stone originally at 'a' moves with transferred energy to freely reach x + 1
            x += 1
            i += 1
        if i == len(positions):
            # Case when the rightmost stone also moves (for loop doesn't break)
            new_positions.append(x)
        # The stones on the right, which don't move retain their position
        new_positions.extend(positions[i:])
        positions = new_positions
    return get_nearest_stone_from_final_pos(positions, _G)


with open(FILE_PATH) as f:
    T = int(f.readline())
    for t in range(T):
        _N, _G = map(int, f.readline().split())
        _E_i_s = list(map(int, (f.readline() for n in range(_N))))
        # print(f"Original positions are {_E_i_s}")
        solution_val, solution_index = solve_problem_2_bruteforce(_E_i_s)
        print(f"Case #{t + 1}: {solution_index} {solution_val}")
