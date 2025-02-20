import sys
import re

# 每个操作类型的处理函数
def handle_malloc(line):
    # 将日志行按照逗号分割
    parts = line.split(", ")
    
    # 提取需要的部分
    operation = parts[2].split(": ")[1]  # Operation: malloc
    physical_address = parts[4].split(": ")[1]  # physical address: 0x0
    size = parts[5].split(": ")[1].split()[0]  # size: 33554432 bytes -> size: 33554432
    duration = parts[-1].split(": ")[1].split()[0]  # duration: 4278 ns -> 4278
    
    # 返回新的格式化行
    return f"{operation}, {physical_address}, {size}, {duration}"

def handle_memcpy(line):
    # 按逗号分割行
    parts = line.split(':')

    # 提取所需信息
    operation = parts[2].split(':')[1].strip()
    from_address = parts[3].split(':')[1].strip().split()[0]
    to_address = parts[4].split(':')[1].strip()
    physical_from_address = parts[5].split(':')
    print(physical_from_address)
    physical_to_address = parts[6].split(':')[1].strip().split()[0]
    size = parts[7].split(':')[1].strip().split()[0]
    duration = parts[9].split(':')[1].strip().split()[0]

    return f"{operation}, {physical_from_address}, {physical_to_address}, {size}, {duration}"



def handle_free(line):
    # 处理 free 操作
    return f"Handling free: {line}"

def handle_calloc(line):
    # 处理 calloc 操作
    return f"Handling calloc: {line}"

def handle_realloc(line):
    # 处理 realloc 操作
    return f"Handling realloc: {line}"

def handle_memset(line):
    # 处理 memset 操作
    return f"Handling memset: {line}"

def handle_memcmp(line):
    # 处理 memcmp 操作
    return f"Handling memcmp: {line}"

def handle_memmove(line):
    # 处理 memmove 操作
    return f"Handling memmove: {line}"

def handle_mmap(line):
    # 处理 mmap 操作
    return f"Handling mmap: {line}"

def handle_munmap(line):
    # 处理 munmap 操作
    return f"Handling munmap: {line}"

# 根据操作类型选择相应的处理函数
def process_line(line):
    # 解析出 operation 部分
    try:
        parts = line.split(", ")
        operation = None
        for part in parts:
            if part.startswith("Operation:"):
                operation = part.split(":")[1].strip()
                break
        
        # 根据 operation 调用不同的处理函数并返回修改后的行
        if operation == "malloc":
            return handle_malloc(line)
        elif operation == "memcpy":
            return handle_memcpy(line)
        elif operation == "free":
            return handle_free(line)
        elif operation == "calloc":
            return handle_calloc(line)
        elif operation == "realloc":
            return handle_realloc(line)
        elif operation == "memset":
            return handle_memset(line)
        elif operation == "memcmp":
            return handle_memcmp(line)
        elif operation == "memmove":
            return handle_memmove(line)
        elif operation == "mmap":
            return handle_mmap(line)
        elif operation == "munmap":
            return handle_munmap(line)
        else:
            return f"Unknown operation: {operation}"
    except Exception as e:
        return f"Error processing line: {line}, {e}"

# 主函数
def main(input_file, output_file):
    # 打开输入文件读取内容，输出文件写入结果
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            processed_line = process_line(line.strip())  # 处理每一行
            outfile.write(processed_line + "\n")  # 将处理后的行写入到输出文件

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    main(input_file, output_file)
