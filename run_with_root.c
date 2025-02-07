#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // 设置为 root 用户执行
    if (setuid(0) < 0) {
        perror("setuid failed");
        return 1;
    }

    // 执行 Python 脚本
    system("python main_core.py 2> GAN_core.log");
    return 0;
}
