#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdarg.h>
#include <unistd.h>
#include <sys/syscall.h>

// 定义原始的 syscall 函数指针
static long (*original_syscall)(long number, ...) = NULL;

// 拦截 syscall
long syscall(long number, ...) {
    if (!original_syscall) {
        // 获取原始的 syscall 函数地址
        original_syscall = dlsym(RTLD_NEXT, "syscall");
    }

    // 获取可变参数
    va_list args;
    va_start(args, number);
    
    // 打印系统调用编号和参数（这里仅展示编号，可以根据需要打印参数）
    printf("Intercepted syscall: number=%ld\n", number);

    // 这里你可以进一步处理特定的 system call，如打印详细的参数等
    // 例如，对于特定的系统调用，你可以打印其参数
    if (number == SYS_mprotect) {
        void *addr = va_arg(args, void*);
        size_t len = va_arg(args, size_t);
        int prot = va_arg(args, int);
        printf("sys_mprotect: addr=%p, len=%zu, prot=%d\n", addr, len, prot);
    }

    va_end(args);

    // 调用原始的 syscall
    return original_syscall(number, args);
}
