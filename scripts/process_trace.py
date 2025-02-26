import sys

def process_line(line, start_time):
    # 假设每行的格式是：操作类型（WRITE/READ） 地址 操作时间
    parts = line.split()
    if len(parts) == 3:
        operation = parts[0]  # WRITE/READ
        address = parts[1]    # 地址
        operation_time = int(parts[2])  # 操作时间（单位：纳秒）
        
        # 计算当前行的开始时间
        start_time += operation_time
        
        # 除以0.75并取整
        start_time = int(start_time / 0.75)
        
        # 返回格式化的字符串，包含开始时间和其他字段
        return f"{address} {operation} {start_time}\n", start_time
    return None, start_time

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            start_time = 0  # 第一行开始时间设为0
            for line in infile:
                processed_line, start_time = process_line(line.strip(), start_time)
                if processed_line:
                    outfile.write(processed_line)
        print(f"Data successfully written to {output_filename}")
    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
