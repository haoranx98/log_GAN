import re
import sys

# 检查是否传入了文件名
if len(sys.argv) != 2:
    print("Usage: python script.py <log_file>")
    sys.exit(1)

log_file_path = sys.argv[1]  # 从命令行参数获取文件名

# 正则表达式来匹配 malloc, calloc, realloc, free, memset, memcpy, memmove, memcmp, mmap 和 munmap 操作
log_pattern = re.compile(
    r"Process PID: (\d+), Thread TID: (\d+), Operation: (malloc|calloc|realloc|free|memset|memcpy|memmove|memcmp|mmap|munmap), "
    r"address: (0x[0-9a-fA-F]+), physical address: (0x[0-9a-fA-F]+), "
    r"(nmemb: (\d+), )?(new size: (\d+) bytes, )?(value: (-?\d+), )?(from: (0x[0-9a-fA-F]+), )?"
    r"(to: (0x[0-9a-fA-F]+), )?(between: (0x[0-9a-fA-F]+) and: (0x[0-9a-fA-F]+), )?"
    r"size: (\d+) bytes, start time: (\d+)\.(\d+), "
    r"end time: (\d+)\.(\d+), duration: (\d+) ns"
)

# 打开日志文件
try:
    with open(log_file_path, 'r') as file:
        for line in file:
            match = log_pattern.match(line.strip())
            if match:
                # 提取字段
                pid = int(match.group(1))
                tid = int(match.group(2))
                operation = match.group(3)  # 'malloc', 'calloc', 'realloc', 'free', 'memset', 'memcpy', 'memmove', 'memcmp', 'mmap' or 'munmap'
                address = match.group(4)
                physical_address = match.group(5)
                
                # 如果是 calloc 操作，提取 nmemb
                if operation == 'calloc':
                    nmemb = int(match.group(8))
                    new_size = int(match.group(9))  # 'new size' is used in realloc and calloc
                elif operation == 'realloc':
                    nmemb = None
                    new_size = int(match.group(9))  # 'new size' for realloc
                elif operation == 'memset':
                    value = int(match.group(10))
                    size = int(match.group(13))
                    nmemb = None
                    new_size = None
                elif operation == 'memcpy':
                    from_address = match.group(12)
                    to_address = match.group(14)
                    size = int(match.group(15))
                    value = None
                    nmemb = None
                    new_size = None
                elif operation == 'memmove':
                    from_address = match.group(12)
                    to_address = match.group(14)
                    size = int(match.group(15))
                    value = None
                    nmemb = None
                    new_size = None
                elif operation == 'memcmp':
                    between_start = match.group(16)
                    between_end = match.group(17)
                    size = int(match.group(18))
                    value = None
                    nmemb = None
                    new_size = None
                    from_address = None
                    to_address = None
                elif operation == 'mmap' or operation == 'munmap':
                    size = int(match.group(19))
                    nmemb = None
                    new_size = None
                    value = None
                    from_address = None
                    to_address = None
                    between_start = None
                    between_end = None
                else:
                    nmemb = None  # 对于 malloc 和 free 操作，没有 nmemb 字段
                    new_size = None  # free 没有 new size 字段
                    value = None
                    from_address = None
                    to_address = None
                    between_start = None
                    between_end = None

                start_time_sec = int(match.group(20))
                start_time_nsec = int(match.group(21))
                end_time_sec = int(match.group(22))
                end_time_nsec = int(match.group(23))
                duration_ns = int(match.group(24))
                
                # 打印提取的信息，操作放到最前面
                if operation == 'free':
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, address: {address}, "
                          f"physical address: {physical_address}, start time: {start_time_sec}.{start_time_nsec}, "
                          f"end time: {end_time_sec}.{end_time_nsec}, duration: {duration_ns} ns")
                elif operation == 'memset':
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, address: {address}, "
                          f"physical address: {physical_address}, value: {value}, size: {size} bytes, "
                          f"start time: {start_time_sec}.{start_time_nsec}, end time: {end_time_sec}.{end_time_nsec}, "
                          f"duration: {duration_ns} ns")
                elif operation == 'memcpy':
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, from: {from_address} to: {to_address}, "
                          f"physical address from {physical_address} to {to_address}, size: {size} bytes, "
                          f"start time: {start_time_sec}.{start_time_nsec}, end time: {end_time_sec}.{end_time_nsec}, "
                          f"duration: {duration_ns} ns")
                elif operation == 'memmove':
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, from: {from_address} to: {to_address}, "
                          f"size: {size} bytes, start time: {start_time_sec}.{start_time_nsec}, "
                          f"end time: {end_time_sec}.{end_time_nsec}, duration: {duration_ns} ns")
                elif operation == 'memcmp':
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, between: {between_start} and: {between_end}, "
                          f"physical address between {physical_address} to {to_address}, size: {size} bytes, "
                          f"start time: {start_time_sec}.{start_time_nsec}, end time: {end_time_sec}.{end_time_nsec}, "
                          f"duration: {duration_ns} ns")
                elif operation == 'mmap' or operation == 'munmap':
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, address: {address}, "
                          f"physical address: {physical_address}, size: {size} bytes, "
                          f"start time: {start_time_sec}.{start_time_nsec}, end time: {end_time_sec}.{end_time_nsec}, "
                          f"duration: {duration_ns} ns")
                else:
                    print(f"Operation: {operation}, PID: {pid}, TID: {tid}, address: {address}, "
                          f"physical address: {physical_address}, nmemb: {nmemb if nmemb is not None else 'N/A'}, "
                          f"new size: {new_size if new_size is not None else 'N/A'} bytes, "
                          f"start time: {start_time_sec}.{start_time_nsec}, "
                          f"end time: {end_time_sec}.{end_time_nsec}, duration: {duration_ns} ns")
            else:
                print(f"Line does not match expected format: {line.strip()}")
except FileNotFoundError:
    print(f"Error: The file '{log_file_path}' was not found.")
    sys.exit(1)
