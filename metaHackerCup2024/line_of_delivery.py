import bisect

FILE_PATH = "line_of_delivery_part_1_input.txt"
with open(FILE_PATH) as f:
    T = int(f.readline())
    for t in range(T):
        N, G = map(int, f.readline().split())
        E_i_s = list(map(int, (f.readline() for n in range(N))))
        E_i_s.sort()
        r_index = bisect.bisect_right(E_i_s, G)
        l_index = r_index - 1
        indexes = [r_index, l_index]
        solutions = []
        for index in indexes:
            if 0 <= index < N:
                diff = abs(G - E_i_s[index])
                rev_index = N - index # 1 based rev_index
                solutions.append((diff, rev_index))
        solution = min(solutions)
        solution_index = solution[1]
        solution_val = solution[0]
        print(f"Case #{t + 1}: {solution_index} {solution_val}")




