#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>

#define PAGE_SIZE 4096

// 声明原始 mmap 函数指针
void* (*original_mmap)(void *addr, size_t length, int prot, int flags, int fd, off_t offset);

// 获取物理地址的函数（只有在读取 pagemap 时提升权限）
uint64_t get_physical_address(pid_t pid, void* virtual_addr) {
    // 提升权限为 root
    if (setuid(0) == -1) {
        perror("setuid failed");
        return 0;
    }

    char pagemap_path[256];
    snprintf(pagemap_path, sizeof(pagemap_path), "/proc/%d/pagemap", pid);

    // 打开 pagemap 文件
    int pagemap_fd = open(pagemap_path, O_RDONLY);
    if (pagemap_fd == -1) {
        perror("Failed to open pagemap");
        return 0;
    }

    // 获取虚拟地址的页框号
    uintptr_t addr_num = (uintptr_t)virtual_addr;
    off_t page_offset = (addr_num / PAGE_SIZE) * sizeof(uint64_t);
    uint64_t frame_number = 0;

    // 定位到页框号的位置
    if (lseek(pagemap_fd, page_offset, SEEK_SET) == -1) {
        perror("Failed to seek in pagemap");
        close(pagemap_fd);
        return 0;
    }

    // 读取页框号
    if (read(pagemap_fd, &frame_number, sizeof(uint64_t)) != sizeof(uint64_t)) {
        perror("Failed to read from pagemap");
        close(pagemap_fd);
        return 0;
    }

    close(pagemap_fd);

    // 恢复原来的权限
    if (setuid(getuid()) == -1) {
        perror("setuid to original user failed");
    }

    // 检查页框号的有效性
    if (frame_number & (1ULL << 63)) {
        // 计算物理地址
        uint64_t phys_addr = (frame_number & ((1ULL << 55) - 1)) * PAGE_SIZE + (addr_num % PAGE_SIZE);
        return phys_addr;
    }

    return 0; // 如果没有有效的物理地址
}

// 拦截 mmap 调用
void* mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset) {
    // 调用原始 mmap 函数
    void* result = original_mmap(addr, length, prot, flags, fd, offset);

    if (result == MAP_FAILED) {
        perror("mmap failed");
        return MAP_FAILED;
    }

    pid_t pid = getpid();
    
    // 获取物理地址
    uint64_t phys_addr = get_physical_address(pid, result);

    if (phys_addr) {
        fprintf(stderr, "Process PID: %d, Virtual Address: 0x%lx, Physical Address: 0x%lx\n", pid, (uintptr_t)result, phys_addr);
    } else {
        fprintf(stderr, "Process PID: %d, Virtual Address: 0x%lx, No valid frame mapped.\n", pid, (uintptr_t)result);
    }

    return result;
}

// 线程入口函数
void* thread_func(void* arg) {
    // 模拟线程操作，这里可以根据需求做相应的工作
    void* addr = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr != MAP_FAILED) {
        printf("Thread %ld mapped memory at address %p\n", pthread_self(), addr);
    } else {
        perror("mmap failed in thread");
    }

    return NULL;
}

// __attribute__((constructor)) 主要用于初始化函数，这里不需要，因为动态库会自动加载。
