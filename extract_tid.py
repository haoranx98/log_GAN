import re
import argparse

def extract_pid_tid_and_operations(log_file_path):
    pid_tid_set = set()  # 用于存储唯一的 PID 和 TID 对应关系
    operations = set()   # 用于存储唯一的操作种类

    # 正则表达式匹配 PID、TID 和操作种类
    pattern_pid_tid = r"Process PID: (\d+), Thread TID: (\d+)"
    pattern_operation = r"Operation: (\w+)"

    # 打开文件读取
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            # 查找 PID 和 TID
            match_pid_tid = re.search(pattern_pid_tid, line)
            if match_pid_tid:
                pid = match_pid_tid.group(1)
                tid = match_pid_tid.group(2)
                pid_tid_set.add((pid, tid))  # 将 PID 和 TID 添加到集合中
            
            # 查找 Operation
            match_operation = re.search(pattern_operation, line)
            if match_operation:
                operation = match_operation.group(1)
                operations.add(operation)  # 将操作类型添加到集合中

    # 输出 PID 和 TID 的对应关系
    print("PID and TID Correspondences:")
    for pid, tid in pid_tid_set:
        print(f"PID: {pid}, TID: {tid}")
    
    # 输出不同的操作种类
    print("\nDifferent Operations:")
    for operation in operations:
        print(f"Operation: {operation}")

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Extract PID, TID, and Operation from a log file.")
    parser.add_argument("log_file", help="The path to the log file.")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用函数处理日志文件
    extract_pid_tid_and_operations(args.log_file)
