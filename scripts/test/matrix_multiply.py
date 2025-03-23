import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

import numpy as np
import time

a = np.random.randint(0, 100, (1000, 1000), dtype=np.int32)
b = np.random.randint(0, 100, (1000, 1000), dtype=np.int32)

start = time.time()
c = np.matmul(a, b)
end = time.time()

print("矩阵乘法完成")
print("结果矩阵 c 的形状:", c.shape)
print(f"耗时: {end - start:.6f} 秒")
