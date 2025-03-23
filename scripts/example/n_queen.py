def solve_n_queens(n):
    def is_valid(path, row, col):
        for r, c in enumerate(path):
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def dfs(row, path):
        if row == n:
            solutions.append(path[:])
            return
        for col in range(n):
            if is_valid(path, row, col):
                dfs(row + 1, path + [col])

    solutions = []
    dfs(0, [])
    return len(solutions)

import time
n = 8
start = time.time()
count = solve_n_queens(n)
end = time.time()
print(f"{n}皇后解的个数: {count}，耗时: {end - start:.2f} 秒")
