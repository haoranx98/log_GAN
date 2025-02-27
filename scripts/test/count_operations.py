import argparse
import re
from collections import Counter, defaultdict

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='统计日志文件中的 PID/TID 对和操作类型数量')
    parser.add_argument('log_file', help='日志文件的路径')
    return parser.parse_args()

# 统计 PID 和 TID 对
def count_pid_tid_pairs(log_file):
    log_pattern = re.compile(r"Process PID: (\d+), Thread TID: (\d+)")
    pid_tid_pairs = []

    with open(log_file, 'r') as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                pid = match.group(1)
                tid = match.group(2)
                pid_tid_pairs.append((pid, tid))

    counter = Counter(pid_tid_pairs)
    return counter

# 统计操作类型数量
def count_operations(log_file):
    operation_count = defaultdict(int)

    with open(log_file, 'r') as file:
        for line in file:
            if "Operation:" in line:
                parts = line.split("Operation:")  # 切分出 "Operation:" 后的部分
                if len(parts) > 1:
                    operation = parts[1].split(",")[0].strip()  # 提取操作类型，去掉多余的空格和逗号
                    operation_count[operation] += 1

    return operation_count

# 主函数
def main():
    # 获取命令行参数
    args = parse_args()

    # 统计 (PID, TID) 对
    pid_tid_counter = count_pid_tid_pairs(args.log_file)
    print(f"\nTotal unique (PID, TID) pairs: {len(pid_tid_counter)}")
    for (pid, tid), count in pid_tid_counter.items():
        print(f"PID: {pid}, TID: {tid} - {count} times")

    # 统计操作类型及其数量
    operation_count = count_operations(args.log_file)
    print("\nOperations and their counts:")
    for operation, count in operation_count.items():
        print(f"{operation}: {count}")

# 运行主函数
if __name__ == '__main__':
    main()
