import re
import argparse

def handle_calloc(line):
    # 定义正则表达式来匹配calloc相关的内容
    match = re.search(r"Operation: calloc,.*nmemb: (\d+), size: (\d+) bytes", line)
    
    if match:
        nmemb = int(match.group(1))  # 提取nmemb的值
        return nmemb
    return None

def calculate_average_nmemb(input_file):
    total_nmemb = 0
    count = 0

    with open(input_file, 'r') as file:
        for line in file:
            if "Operation: calloc" in line:
                nmemb = handle_calloc(line)
                if nmemb is not None:
                    total_nmemb += nmemb
                    count += 1

    # 计算平均值
    if count > 0:
        average_nmemb = total_nmemb / count
        print(f"Average nmemb: {average_nmemb}")
    else:
        print("No calloc operations found.")

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Calculate the average nmemb from calloc operations.")
    parser.add_argument("input_file", help="Input log file containing calloc operations.")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用计算函数
    calculate_average_nmemb(args.input_file)
