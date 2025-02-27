import argparse

def check_time_overlap(log_file):
    previous_end_time = None  # 上一行的结束时间
    previous_log = None  # 上一行的完整日志
    
    with open(log_file, 'r') as file:
        # 逐行读取日志
        for line_num, line in enumerate(file, start=1):
            # 如果是第一行，不进行重叠检查
            if line_num == 1:
                previous_log = line
                continue

            # 提取每行的日志时间戳和其他信息
            parts = line.split(", ")
            if len(parts) >= 6:
                try:
                    # 提取时间
                    start_time_str = parts[4].split(": ")
                    end_time_str = parts[5].split(": ")
                    
                    # 检查是否能正确提取出 start time 和 end time
                    if len(start_time_str) > 1 and len(end_time_str) > 1:
                        start_time = float(start_time_str[1])  # start time
                        end_time = float(end_time_str[1])    # end time
                    
                        # 如果上一行的结束时间大于当前行的开始时间，说明有重叠
                        if previous_end_time is not None and start_time < previous_end_time:
                            print(f"Time overlap detected between the previous line and current line:")
                            print(f"Previous log: {previous_log.strip()}")
                            print(f"Previous end time: {previous_end_time}, Current start time: {start_time}")
                            print(f"Current log: {line.strip()}")  # 输出时间重叠的日志行
                    
                        # 更新 previous_end_time 为当前行的结束时间
                        previous_end_time = end_time
                        # 更新 previous_log 为当前行的完整日志
                        previous_log = line
                except ValueError:
                    # 跳过格式不符合的行
                    continue

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="检查日志文件中是否有时间重叠")
    parser.add_argument('log_file', help="日志文件路径")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 检查时间重叠
    check_time_overlap(args.log_file)

if __name__ == "__main__":
    main()
