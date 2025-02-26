import csv
import sys

# 处理不同类型的函数
def handle_mmap(row):
    
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
    # print(row)
    address = int(row[1], 16)
    length = int(row[3])
    # print(length)
    line = []

    ops = 0

    if(length != 0):
        # print(length)
        if(length <= 8):
            ops += length
        else:
            ops = length // 8 + length % 8

        time = int(row[4]) // ops
        # print(time)

        if(length <= 8):
            for i in range(length):
                address += 1
                line.append(f"WRITE 0x{address:010X} {time}\n")
        else:
            num = length // 8
            # print(f"num: {num}")
            for i in range(num):
                address += 8
                line.append(f"WRITE 0x{address:010X} {time}\n")

            if length % 8 != 0:
                # print(f"length % 8: {length % 8}")
                num = length % 8

                for i in range(num):
                    address += 1
                    line.append(f"WRITE 0x{address:010X} {time}\n")
    else:
        print("length is 0")

    return line

def handle_memcmp(row):
    # print(row)
    src = int(row[1], 16)
    dst = int(row[2], 16)
    length = int(row[3])
    line = []
    ops = 0

    if(length != 0):
        length_16 = length // 16
        ops += length_16 * 4
        length_8 = length % 16 // 8
        ops += length_8 * 2
        length_4 = length % 8 // 4
        ops += length_4 * 2
        length_1 = length % 4
        ops += length_1

        time = int(row[4]) // ops


        for i in range(length_16):
            for i in range(2):
                src += 8
                dst += 8
                line.append(f"READ 0x{src:010X} {time}\n")
                line.append(f"READ 0x{dst:010X} {time}\n")
        
        for i in range(length_8):
            src += 8
            dst += 8
            line.append(f"READ 0x{src:010X} {time}\n")
            line.append(f"READ 0x{dst:010X} {time}\n")
        
        for i in range(length_4):
            src += 4
            dst += 4
            line.append(f"READ 0x{src:010X} {time}\n") 
            line.append(f"READ 0x{dst:010X} {time}\n")
        
        for i in range(length_1):
            src += 1
            dst += 1
            line.append(f"READ 0x{src:010X} {time}\n")
            line.append(f"READ 0x{dst:010X} {time}\n")

    return line
def handle_memmove(row):
    # print(row)
    src = int(row[1], 16)
    dst = int(row[2], 16)
    length = int(row[3])
    line = []
    ops = 0

    if(length != 0):
        if length <= 8:
            time = int(row[4]) // length
            for i in range(length):
                src += 1
                dst += 1
                line.append(f"READ 0x{src:010X} {time}\n")
                line.append(f"WRITE 0x{dst:010X} {time}\n")
        else:
            num = length // 8
            ops = num + length % 8
            time = int(row[4]) // ops

            for i in range(num):
                src += 8
                dst += 8
                line.append(f"READ 0x{src:010X} {time}\n")
                line.append(f"WRITE 0x{dst:010X} {time}\n")

            if length % 8 != 0:
                num = length % 8

                for i in range(num):
                    src += 1
                    dst += 1
                    line.append(f"READ 0x{src:010X} {time}\n")
                    line.append(f"WRITE 0x{dst:010X} {time}\n")
    return line


# 根据类型选择对应的处理函数
def process_row(row):
    operation_type = row[0]
    if operation_type == 'mmap':
        # return handle_mmap(row)
        return []
    elif operation_type == 'munmap':
        # return handle_munmap(row)
        return []
    elif operation_type == 'malloc':
        # return handle_malloc(row)
        return []
    elif operation_type == 'free':
        # return handle_free(row)
        return []
    elif operation_type == 'calloc':
        # return handle_calloc(row)
        return []
    elif operation_type == 'realloc':
        # return handle_realloc(row)
        return []
    elif operation_type == 'memset':
        return handle_memset(row)
    elif operation_type == 'memcmp':
        return handle_memcmp(row)
    elif operation_type == 'memmove':
        return handle_memmove(row)
    elif operation_type == 'memcpy':
        return handle_memmove(row)
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
                # writer = csv.writer(outfile)
                num = 0
                for row in reader:
                    processed_row = process_row(row)
                    if len(processed_row) == 0:
                        continue
                    num += 1
                    for line in processed_row:
                        outfile.write(line)
                print(f"Processing row {num}")
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
