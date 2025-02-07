#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <dlfcn.h>
#include <unistd.h>
#include <time.h>
#include <stdarg.h>
#include <sys/syscall.h>
#include <pthread.h>
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>

// 函数指针声明
static void* (*original_mmap)(void*, size_t, int, int, int, off_t) = NULL;


// 定义最大日志长度
#define MAX_LOG_LENGTH 1024

// 获取当前时间（单位：纳秒）
long get_current_time_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000000000L + ts.tv_nsec;
}

// 获取当前线程的 TID
pid_t get_thread_tid() {
    return syscall(SYS_gettid); // 获取当前线程的TID
}

// 初始化函数
__attribute__((constructor))
void initialize_original_functions() {
    original_mmap = dlsym(RTLD_NEXT, "mmap");
}

// 日志输出函数，使用 write 替代 fprintf
void log_message(const char *format, ...) {
    char buffer[MAX_LOG_LENGTH];
    va_list args;
    va_start(args, format);
    int len = vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    write(STDERR_FILENO, buffer, len);
}



// 拦截 mmap 并记录日志
void* mmap(void* addr, size_t length, int prot, int flags, int fd, off_t offset) {

    pid_t pid = getpid();
    pid_t tid = get_thread_tid();

    long start_time_ns = get_current_time_ns();
    void* result = original_mmap(addr, length, prot, flags, fd, offset);
    long end_time_ns = get_current_time_ns();
    log_message("Process PID: %d, Thread TID: %d, Operation: mmap, address: %p, size: %zu bytes, start time: %ld ns, end time: %ld ns, duration: %ld ns\n",
                pid, tid, result, length, start_time_ns, end_time_ns, end_time_ns - start_time_ns);
    return result;
}



