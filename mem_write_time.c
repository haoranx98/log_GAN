#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static inline uint64_t rdtsc(void) {
    uint32_t low, high;
    // 使用 rdtsc 指令获取时间戳计数器的值
    __asm__ volatile("rdtsc" : "=a"(low), "=d"(high));
    return ((uint64_t)high << 32) | low;
}

int main() {
    uint64_t start, end;
    int *p;
    int value = 42;
    int num_iterations = 1000;

    // 反复申请、写入、释放内存 1000 次
    for (int i = 0; i < num_iterations; i++) {
        

        // 使用 malloc 分配一块内存
        p = (int *)malloc(512*sizeof(int));
        if (p == NULL) {
            printf("Memory allocation failed\n");
            return 1;
        }

        start = rdtsc();  // 获取开始时间
        // 写入内存操作
        __asm__ volatile("mov %1, %0" : "=m"(*p) : "r"(value)); // 将 value 的值写入 malloc 分配的内存

        end = rdtsc();    // 获取结束时间
        printf("Iteration %d - Time taken to write to memory: %llu CPU cycles\n", i + 1, end - start);

        // 释放内存
        free(p);
    }

    return 0;
}
