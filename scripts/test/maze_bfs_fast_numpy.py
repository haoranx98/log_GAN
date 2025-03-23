import numpy as np
from collections import deque
import time

# 生成一个 10000x10000 的随机迷宫（0是通路，1是墙）
def generate_maze(size, wall_prob=0.3, seed=None):
    if seed is not None:
        np.random.seed(seed)
    return (np.random.rand(size, size) > wall_prob).astype(np.uint8)

# BFS 搜索最短路径长度（不记录路径，节省内存）
def bfs_shortest_path(maze, start, end):
    rows, cols = maze.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque()
    queue.append((start[0], start[1], 0))  # (x, y, steps)
    visited[start] = True

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx, ny] and maze[nx, ny] == 1:
                    visited[nx, ny] = True
                    queue.append((nx, ny, steps + 1))

    return -1  # 无法到达

# 主程序
if __name__ == '__main__':
    size = 10000
    start = (0, 0)
    end = (size - 1, size - 1)

    print("正在生成迷宫...")
    maze = generate_maze(size, wall_prob=0.3, seed=42)

    # 确保起点和终点可以通行
    maze[start] = 1
    maze[end] = 1

    print("开始搜索...")
    start_time = time.time()
    steps = bfs_shortest_path(maze, start, end)
    end_time = time.time()

    if steps != -1:
        print(f"成功到达终点，最短路径步数: {steps}")
    else:
        print("无法到达终点。")

    print(f"耗时: {end_time - start_time:.2f} 秒")
