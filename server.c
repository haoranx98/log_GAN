#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PAGE_SIZE 4096  // 页大小，通常为 4096 字节

// 获取物理地址的函数
uint64_t get_physical_address(pid_t pid, void* virtual_addr) {
    printf("Getting physical address for PID = %d, Virtual Address = 0x%lx\n", pid, (uintptr_t)virtual_addr);
    
    // 构造 pagemap 路径
    char pagemap_path[256];
    snprintf(pagemap_path, sizeof(pagemap_path), "/proc/%d/pagemap", pid);

    // 打开 pagemap 文件
    int pagemap_fd = open(pagemap_path, O_RDONLY);
    if (pagemap_fd == -1) {
        perror("Failed to open pagemap");
        return 0;
    }

    uintptr_t addr_num = (uintptr_t)virtual_addr;
    printf("Virtual Address Number: %lu\n", addr_num);

    // 计算虚拟地址所在页面的偏移
    off_t page_offset = (addr_num / getpagesize()) * sizeof(uint64_t); 
    uint64_t frame_number = 0;

    // 定位到 pagemap 文件中对应虚拟地址的条目
    if (lseek(pagemap_fd, page_offset, SEEK_SET) == -1) {
        perror("Failed to seek in pagemap");
        close(pagemap_fd);
        return 0;
    }

    // 读取该页面的物理页框号
    ssize_t bytes_read = read(pagemap_fd, &frame_number, sizeof(uint64_t));
    if (bytes_read != sizeof(uint64_t)) {
        if (bytes_read == -1) {
            perror("Failed to read from pagemap");
        } else {
            fprintf(stderr, "Unexpected number of bytes read from pagemap: %zd\n", bytes_read);
        }
        close(pagemap_fd);
        return 0;
    }

    // 关闭文件
    close(pagemap_fd);

    // 检查该页是否有效
    if (frame_number & (1ULL << 63)) {  // 检查位 63 是否为 1，表示该页已映射
        // 计算物理地址
        uint64_t phys_addr = (frame_number & ((1ULL << 55) - 1)) * getpagesize() + (addr_num % getpagesize());
        return phys_addr;
    }

    // 如果该页未映射，返回 0
    return 0;
}

// 定义结构体
typedef struct {
    pid_t pid;
    void* virtual_addr;
} RequestData;

// 处理来自其他程序的请求
void handle_request(int client_fd) {
    RequestData request;
    
    // 从客户端读取结构体
    ssize_t bytes_read = read(client_fd, &request, sizeof(RequestData));
    if (bytes_read != sizeof(RequestData)) {
        perror("Failed to read request");
        return;
    }

    pid_t pid = request.pid;
    void* virtual_addr = request.virtual_addr;

    printf("Received request: PID = %d, Virtual Address = 0x%lx\n", pid, (uintptr_t)virtual_addr);

    // 查询物理地址
    uint64_t phys_addr = get_physical_address(pid, virtual_addr);

    // 将物理地址发送回客户端
    ssize_t bytes_written = write(client_fd, &phys_addr, sizeof(uint64_t));
    if (bytes_written != sizeof(uint64_t)) {
        perror("Failed to send physical address");
    }

    printf("Returned Physical Address: 0x%lx\n", phys_addr);
}

int main() {
    // 创建一个 TCP 套接字
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("socket failed");
        return 1;
    }

    // 设置服务器地址
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(12345);

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind failed");
        return 1;
    }

    if (listen(server_fd, 5) == -1) {
        perror("listen failed");
        return 1;
    }

    printf("Waiting for requests...\n");

    while (1) {
        // 接受客户端连接
        int client_fd = accept(server_fd, NULL, NULL);
        if (client_fd == -1) {
            perror("accept failed");
            continue;
        }

        // 处理请求
        handle_request(client_fd);

        // 关闭客户端连接
        close(client_fd);
    }

    return 0;
}
