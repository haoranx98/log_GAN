#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#define PAGE_SIZE 4096  // 页大小，通常为 4096 字节

int main() {
    // 1. 使用 mmap 映射内存
    // 使用 MAP_PRIVATE 和 MAP_ANONYMOUS 映射匿名内存（不与文件关联）
    void *addr = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr == MAP_FAILED) {
        perror("mmap failed");
        return -1;
    }

    // 2. 在映射的内存中写入数据
    const char *message = "Hello from mmap!";
    strcpy((char *)addr, message);
    printf("Data written to mapped memory: %s\n", (char *)addr);

    // 3. 读取映射内存中的数据
    printf("Data read from mapped memory: %s\n", (char *)addr);

    // 4. 解除映射
    if (munmap(addr, PAGE_SIZE) == -1) {
        perror("munmap failed");
        return -1;
    }

    printf("Memory unmapped successfully.\n");

    return 0;
}
