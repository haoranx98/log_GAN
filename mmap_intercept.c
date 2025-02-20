#define _GNU_SOURCE
#include <sys/mman.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

void * __mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset) {
    printf("Intercepted __mmap call\n");
    
    // 你可以在这里调用原始的 __mmap 函数
    void *(*real_mmap)(void *, size_t, int, int, int, off_t);
    real_mmap = dlsym(RTLD_NEXT, "__mmap");

    // 在调用原始 __mmap 之前进行一些操作
    if (real_mmap == NULL) {
        perror("dlsym");
        exit(EXIT_FAILURE);
    }

    // 调用真实的 __mmap
    void *result = real_mmap(addr, length, prot, flags, fd, offset);

    // 在这里可以对结果进行一些操作
    printf("Original __mmap returned: %p\n", result);

    return result;
}
