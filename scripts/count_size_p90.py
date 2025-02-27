import pandas as pd
import argparse

# 解析命令行输入的文件名
def calculate_80_percent(input_file):
    # 读取文件，假设文件数据是用逗号分隔
    df = pd.read_csv(input_file, header=None, names=['size', 'frequency'], sep=',')

    # 确保 'frequency' 列是数字类型，处理非数字值（如字符串或空值）
    df['frequency'] = pd.to_numeric(df['frequency'], errors='coerce').fillna(0).astype(int)

    # 计算总的频数和
    total_count = df['frequency'].sum()

    # 计算目标值：总频数的 80%
    target_count = total_count * 0.99

    # 计算累计频数并找到达到 80% 的大小值
    cumulative_count = 0
    result = []

    for index, row in df.iterrows():
        cumulative_count += row['frequency']
        result.append(row)
        if cumulative_count >= target_count:
            break

    # 输出结果
    print(f"Total count of operations: {total_count}")
    print(f"99% of total count: {target_count}")
    print("\nThe sizes whose cumulative frequency covers 80% of total operations:")
    for r in result:
        print(f"Size: {r['size']}, Frequency: {r['frequency']}")

# 解析命令行参数
parser = argparse.ArgumentParser(description='Calculate and display the sizes whose cumulative frequency covers 80% of the total operations.')
parser.add_argument('input_file', type=str, help='Path to the frequency file')
args = parser.parse_args()

# 调用函数，传递命令行输入的文件路径
calculate_80_percent(args.input_file)
