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
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

// 函数指针声明
static void* (*original_mmap)(void*, size_t, int, int, int, off_t) = NULL;

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

// 连接到服务器并获取物理地址
uint64_t get_physical_address(pid_t pid, void* virtual_addr) {

    int client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd == -1) {
        perror("socket failed");
        return 0;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // 服务器地址
    server_addr.sin_port = htons(12345); // 服务器端口

    if (connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("connect failed");
        return 0;
    }

    // 将虚拟地址转换为 uintptr_t 类型以传递
    fprintf(stderr, "Sending request: PID = %d, Virtual Address = 0x%lx\n", pid, virtual_addr);
    uintptr_t addr = (uintptr_t)virtual_addr;
    fprintf(stderr, "Sending request: PID = %d, Virtual Address = 0x%lx\n", pid, addr);
    // 创建结构体并发送
    RequestData request = {pid, (void*)addr};
    write(client_fd, &request, sizeof(RequestData));

    uint64_t phys_addr;
    // 从服务器接收物理地址
    read(client_fd, &phys_addr, sizeof(uint64_t));

    close(client_fd);
    return phys_addr;
}

// 拦截 mmap 并记录日志
void* mmap(void* addr, size_t length, int prot, int flags, int fd, off_t offset) {
    pid_t pid = getpid();
    pid_t tid = get_thread_tid();
    printf("addr: %p, length: %zu, prot: %d, flags: %d, fd: %d, offset: %ld\n", addr, length, prot, flags, fd, offset);
    long start_time_ns = get_current_time_ns();
    void* result = original_mmap(addr, length, prot, flags, fd, offset);
    long end_time_ns = get_current_time_ns();
    log_message("Process PID: %d, Thread TID: %d, Operation: mmap, address: %p, size: %zu bytes, start time: %ld ns, end time: %ld ns, duration: %ld ns\n",
                pid, tid, result, length, start_time_ns, end_time_ns, end_time_ns - start_time_ns);

    // 查询物理地址并记录
    uint64_t phys_addr = get_physical_address(pid, result);
    log_message("Process PID: %d, Virtual Address: %p, Physical Address: 0x%lx\n", pid, result, phys_addr);

    return result;
}
