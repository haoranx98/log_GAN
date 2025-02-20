#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

#define MMAP_SIZE 4096  // 4KB
#define NUM_ITERATIONS 10000000  // 循环次数

// 用于读取 TSC 的内嵌汇编
static inline unsigned long long rdtsc() {
    unsigned long long int cycles;
    // 使用 rdtsc 指令读取时间戳计数器
    __asm__ volatile("rdtsc" : "=A"(cycles));
    return cycles;
}

void* mmap_memory(size_t size) {
    return mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
}

void munmap_memory(void* addr, size_t size) {
    // 使用汇编直接调用 munmap
    __asm__ volatile (
        "movq $11, %%rax;"         // syscall number for munmap
        "movq %0, %%rdi;"          // addr
        "movq %1, %%rsi;"          // size
        "syscall;"
        :
        : "r"(addr), "r"(size)
        : "%rax", "%rdi", "%rsi"
    );
}

int main() {
    // 申请内存
    void* addr = mmap_memory(MMAP_SIZE);
    if (addr == MAP_FAILED) {
        perror("mmap failed");
        return -1;
    }

    unsigned long long total_time_taken = 0;

    // 循环执行 NUM_ITERATIONS 次
    for (int i = 0; i < NUM_ITERATIONS; i++) {
        // 读取开始时的 TSC 时间戳
        unsigned long long start_cycles = rdtsc();

        // 调用 munmap 释放内存
        munmap_memory(addr, MMAP_SIZE);

        // 读取结束时的 TSC 时间戳
        unsigned long long end_cycles = rdtsc();

        // 计算时间差
        unsigned long long time_taken = end_cycles - start_cycles;
        
        // 处理 TSC 溢出情况
        if (end_cycles < start_cycles) {
            printf("TSC overflow detected\n");
            end_cycles += (1ULL << 64);  // 处理溢出
            time_taken = end_cycles - start_cycles;
        }

        total_time_taken += time_taken;
    }

    // 计算平均时间
    unsigned long long avg_time_taken = total_time_taken / NUM_ITERATIONS;

    // 输出总的和平均的时间（单位：CPU时钟周期）
    printf("Total time taken for munmap (in CPU cycles): %llu\n", total_time_taken);
    printf("Average time taken for munmap (in CPU cycles): %llu\n", avg_time_taken);

    return 0;
}

