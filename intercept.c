#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <execinfo.h>
#include <dlfcn.h>
#include <pthread.h>

static pthread_mutex_t mprotect_mutex = PTHREAD_MUTEX_INITIALIZER;

int mprotect(void *addr, size_t len, int prot) {
    // 加锁，保证线程安全
    pthread_mutex_lock(&mprotect_mutex);
    
    // 打印调用栈
    void *buffer[10];
    int size = backtrace(buffer, 10);
    char **symbols = backtrace_symbols(buffer, size);
    
    printf("Intercepted mprotect: addr=%p, len=%zu, prot=%d\n", addr, len, prot);
    for (int i = 0; i < size; i++) {
        printf("%s\n", symbols[i]);
    }
    free(symbols);

    // 调用原始的 mprotect 函数
    int (*original_mprotect)(void*, size_t, int);
    original_mprotect = dlsym(RTLD_NEXT, "mprotect");

    // 解锁
    pthread_mutex_unlock(&mprotect_mutex);

    return original_mprotect(addr, len, prot);
}
