import pandas as pd
import matplotlib.pyplot as plt
import argparse

# 解析命令行输入的文件名
parser = argparse.ArgumentParser(description='Plot the histograms and output frequency counts of the 4th and 5th columns.')
parser.add_argument('input_file', type=str, help='Path to the input CSV file')
parser.add_argument('output_file', type=str, help='Path to the output frequency file')
args = parser.parse_args()

# 读取 CSV 文件，假设数据以逗号分隔
df = pd.read_csv(args.input_file, header=None, names=['operation', 'address1', 'address2', 'size', 'time'])

# 筛选第四列（size）数据：去掉值为 0 的数据
filtered_size = df['size'].loc[df['size'] > 0]

# 计算第四列（size）和第五列（time）的频数
size_counts = df['size'].value_counts().sort_index()  # 不去除 0
time_counts = df['time'].value_counts().sort_index()

# 输出频数结果到文件
with open(args.output_file, 'w') as f:
    f.write('Size Frequency Counts (Including 0):\n')
    size_counts.to_csv(f, header=True)
    f.write('\nTime Frequency Counts:\n')
    time_counts.to_csv(f, header=True)

# 绘制第四列（size）的直方图，去掉 0，并且以 10 为间隔
# plt.figure(figsize=(12, 6))

# # 绘制大小的直方图（去掉 0）
# plt.subplot(1, 2, 1)
# plt.hist(filtered_size, bins=range(10, filtered_size.max() + 10, 10), edgecolor='black', alpha=0.7)
# plt.title('Histogram of Size (4th Column)')
# plt.xlabel('Size')
# plt.ylabel('Frequency')
# plt.grid(True)

# # 绘制时间的直方图，按100为间隔
# plt.subplot(1, 2, 2)
# plt.hist(df['time'], bins=range(0, df['time'].max() + 100, 100), edgecolor='black', alpha=0.7)
# plt.title('Histogram of Time (5th Column)')
# plt.xlabel('Time')
# plt.ylabel('Frequency')
# plt.grid(True)

# # 展示图表
# plt.tight_layout()
# plt.show()
