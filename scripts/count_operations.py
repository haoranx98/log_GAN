import argparse
from collections import defaultdict

def count_operations(log_file):
    operation_count = defaultdict(int)  # 使用 defaultdict 来存储每种操作的计数

    with open(log_file, 'r') as file:
        for line in file:
            # 使用简单的字符串查找来提取操作类型
            if "Operation:" in line:
                # 例如：Operation: memset
                parts = line.split("Operation:")  # 切分出 "Operation:" 后的部分
                if len(parts) > 1:
                    operation = parts[1].split(",")[0].strip()  # 提取操作类型，去掉多余的空格和逗号
                    operation_count[operation] += 1

    return operation_count

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="统计日志文件中不同操作类型的数量")
    parser.add_argument('log_file', help="日志文件路径")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 统计操作类型及其数量
    operation_count = count_operations(args.log_file)
    
    # 输出结果
    print("Operations and their counts:")
    for operation, count in operation_count.items():
        print(f"{operation}: {count}")

if __name__ == "__main__":
    main()
