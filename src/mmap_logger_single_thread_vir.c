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
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>


// 函数指针声明
static void* (*original_malloc)(size_t) = NULL;
static void* (*original_calloc)(size_t, size_t) = NULL;
static void* (*original_realloc)(void*, size_t) = NULL;
static void (*original_free)(void*) = NULL;
static void* (*original_memset)(void*, int, size_t) = NULL;
static void* (*original_memcpy)(void*, const void*, size_t) = NULL;
static void* (*original_memmove)(void*, const void*, size_t) = NULL;
static int (*original_memcmp)(const void*, const void*, size_t) = NULL;
static void* (*original_mmap)(void*, size_t, int, int, int, off_t) = NULL;
static int (*original_munmap)(void*, size_t) = NULL;
static int (*original_mprotect)(void*, size_t, int) = NULL;
static int (*original_mlock)(const void*, size_t) = NULL;
static int (*original_munlock)(const void*, size_t) = NULL;
static void (*original_bzero)(void*, size_t) = NULL;
static void (*original_bcopy)(const void*, void*, size_t) = NULL;

// 定义最大日志长度
#define MAX_LOG_LENGTH 1024

// 定义结构体
typedef struct {
    pid_t pid;
    void* virtual_addr;
} RequestData;

// 获取当前时间（单位：纳秒）
long get_current_time_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000000000L + ts.tv_nsec;
}


// 初始化函数
__attribute__((constructor))
void initialize_original_functions() {
    original_malloc = dlsym(RTLD_NEXT, "malloc");
    original_calloc = dlsym(RTLD_NEXT, "calloc");
    original_realloc = dlsym(RTLD_NEXT, "realloc");
    original_free = dlsym(RTLD_NEXT, "free");
    original_memset = dlsym(RTLD_NEXT, "memset");
    original_memcpy = dlsym(RTLD_NEXT, "memcpy");
    original_memmove = dlsym(RTLD_NEXT, "memmove");
    original_memcmp = dlsym(RTLD_NEXT, "memcmp");
    original_mmap = dlsym(RTLD_NEXT, "mmap");
    original_munmap = dlsym(RTLD_NEXT, "munmap");
    original_mprotect = dlsym(RTLD_NEXT, "mprotect");
    original_mlock = dlsym(RTLD_NEXT, "mlock");
    original_munlock = dlsym(RTLD_NEXT, "munlock");
    original_bzero = dlsym(RTLD_NEXT, "bzero");
    original_bcopy = dlsym(RTLD_NEXT, "bcopy");
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

// 拦截 malloc 并记录日志
void* malloc(size_t size) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_malloc(size);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: malloc, address: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                result, size, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 calloc 并记录日志
void* calloc(size_t nmemb, size_t size) {
    
    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_calloc(nmemb, size);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);


    log_message("Operation: calloc, address: %p, nmemb: %zu, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                result, nmemb, size, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 realloc 并记录日志
void* realloc(void* ptr, size_t size) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_realloc(ptr, size);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: realloc, address: %p, new size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                result,  size, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 free 并记录日志
void free(void* ptr) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    original_free(ptr);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: free, address: %p, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                ptr, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
}

// 拦截 memset 并记录日志
void* memset(void* s, int c, size_t n) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_memset(s, c, n);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: memset, address: %p, value: %d, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                s, c, n, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 memcpy 并记录日志
void* memcpy(void* dest, const void* src, size_t n) {
    
    long start_time_ns = get_current_time_ns();

    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_memcpy(dest, src, n);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: memcpy, from: %p to: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                src, dest, n, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 memmove 并记录日志
void* memmove(void* dest, const void* src, size_t n) {


    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_memmove(dest, src, n);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: memmove, from: %p to: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                src, dest, n, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 memcmp 并记录日志
int memcmp(const void* s1, const void* s2, size_t n) {


    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    int result = original_memcmp(s1, s2, n);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: memcmp, between: %p and: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                s1, s2, n, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 mmap 并记录日志
void* mmap(void* addr, size_t length, int prot, int flags, int fd, off_t offset) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    void* result = original_mmap(addr, length, prot, flags, fd, offset);
    
    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: mmap, address: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                result, length, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 munmap 并记录日志
int munmap(void* addr, size_t length) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    int result = original_munmap(addr, length);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: munmap, address: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                addr, length, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 mprotect 并记录日志
int mprotect(void* addr, size_t len, int prot) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    int result = original_mprotect(addr, len, prot);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: mprotect, address: %p, size: %zu bytes, prot: %d, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                addr, len, prot, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 mlock 并记录日志
int mlock(const void* addr, size_t len) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    int result = original_mlock(addr, len);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: mlock, address: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                addr, len, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 munlock 并记录日志
int munlock(const void* addr, size_t len) {

    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    int result = original_munlock(addr, len);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: munlock, address: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                addr, len, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
    return result;
}

// 拦截 bzero 并记录日志
void bzero(void* s, size_t len) {
    
    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    original_bzero(s, len);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: bzero, address: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                s, len, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
}

// 拦截 bcopy 并记录日志
void bcopy(const void* src, void* dest, size_t len) {
    
    long start_time_ns = get_current_time_ns();
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    original_bcopy(src, dest, len);

    long end_time_ns = get_current_time_ns();
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    log_message("Operation: bcopy, from: %p to: %p, size: %zu bytes, start time: %ld.%09ld, end time: %ld.%09ld, duration: %ld ns\n",
                src, dest, len, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, end_time_ns - start_time_ns);
}
