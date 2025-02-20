import csv
import sys

# 处理不同类型的函数
def handle_mmap(row):
    print(row)
    return [f"Processed mmap: {row}"]

def handle_munmap(row):
    return [f"Processed munmap: {row}"]

def handle_malloc(row):
    return [f"Processed malloc: {row}"]

def handle_free(row):
    return [f"Processed free: {row}"]

def handle_calloc(row):
    return [f"Processed calloc: {row}"]

def handle_realloc(row):
    return [f"Processed realloc: {row}"]

def handle_memset(row):
    return [f"Processed memset: {row}"]

def handle_memcmp(row):
    return [f"Processed memcmp: {row}"]

def handle_memmove(row):
    return [f"Processed memmove: {row}"]

def handle_memcpy(row):
    return [f"Processed memcpy: {row}"]

# 根据类型选择对应的处理函数
def process_row(row):
    operation_type = row[0]
    if operation_type == 'mmap':
        return handle_mmap(row)
    elif operation_type == 'munmap':
        return handle_munmap(row)
    elif operation_type == 'malloc':
        return handle_malloc(row)
    elif operation_type == 'free':
        return handle_free(row)
    elif operation_type == 'calloc':
        return handle_calloc(row)
    elif operation_type == 'realloc':
        return handle_realloc(row)
    elif operation_type == 'memset':
        return handle_memset(row)
    elif operation_type == 'memcmp':
        return handle_memcmp(row)
    elif operation_type == 'memmove':
        return handle_memmove(row)
    elif operation_type == 'memcpy':
        return handle_memcpy(row)
    else:
        return [f"Unknown operation type: {operation_type}"]

# 主程序
def parse_csv(input_file, output_file):
    try:
        # 打开输入文件进行读取
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            # 打开输出文件进行写入
            with open(output_file, mode='w', newline='') as outfile:
                writer = csv.writer(outfile)
                for row in reader:
                    processed_row = process_row(row)
                    writer.writerow(processed_row)
        print(f"Processing completed. Results written to {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"Error: {e}")

# 获取命令行参数
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]  # 从命令行获取输入文件
    output_file = sys.argv[2]  # 从命令行获取输出文件
    parse_csv(input_file, output_file)
