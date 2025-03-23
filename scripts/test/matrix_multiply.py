import torch
import time

# 设置使用 CPU
device = torch.device('cpu')

# 创建两个 1000x1000 的矩阵，使用 float32 类型
a = torch.randn(1000, 1000, device=device, dtype=torch.float32)
b = torch.randn(1000, 1000, device=device, dtype=torch.float32)

# 记录开始时间
start = time.time()

# 执行矩阵乘法
c = torch.matmul(a, b)

# 记录结束时间
end = time.time()

# 打印结果信息
print("矩阵乘法完成")
print("结果矩阵 c 的形状:", c.shape)
print(f"耗时: {end - start:.6f} 秒")
