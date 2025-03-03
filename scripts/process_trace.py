import sys

def process_line(line):
    """ 解析一行数据并处理第三列 """
    parts = line.split()
    if len(parts) == 3:
        operation = parts[0]  # 读取操作类型（READ/WRITE）
        address = parts[1]    # 读取内存地址
        time = int(parts[2])  # 读取时间值并转换为整数
        
        # 整除 0.75 并取整
        adjusted_time = int(time // 0.75)
        
        return operation, address, adjusted_time
    return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        total_time = 0  # 第一行的时间应该是0
        first_line = True

        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                result = process_line(line.strip())
                if result:
                    operation, address, adjusted_time = result
                    
                    # 第一行时间为 0，之后每行累加
                    if first_line:
                        outfile.write(f"{address} {operation} 0\n")
                        first_line = False
                    else:
                        total_time += adjusted_time  # 累加时间
                        outfile.write(f"{address} {operation} {total_time}\n")

        print(f"Processed data successfully written to {output_filename}")
    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()