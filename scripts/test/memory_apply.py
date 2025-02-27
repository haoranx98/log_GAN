import threading
import time

# 模拟内存申请和释放的函数
def allocate_and_free(thread_id):
    for i in range(200):  # 执行50次内存申请和释放
        # 申请4KB内存
        memory = bytearray(4 * 1024)  # 4KB
        print(f"Thread-{thread_id}: Allocated 4KB memory, iteration {i+1}")

        # 模拟一些工作
        time.sleep(0.1)

        # 释放内存
        del memory  # 释放内存
        print(f"Thread-{thread_id}: Freed 4KB memory, iteration {i+1}")

# 创建两个线程
thread1 = threading.Thread(target=allocate_and_free, args=(1,))
thread2 = threading.Thread(target=allocate_and_free, args=(2,))

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("Both threads have completed memory allocation and deallocation.")
