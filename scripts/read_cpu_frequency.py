import time

def read_cpu_frequency():
    try:
        # 打开文件以读取 CPU 0 当前频率（单位：KHz）
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
            freq = int(f.read().strip())
            # 输出当前频率（单位：MHz）
            print(f"CPU 0 Current Frequency: {freq / 1000} MHz")
    except FileNotFoundError:
        print("Failed to read CPU frequency. Ensure the CPU frequency scaling driver is enabled.")

def main():
    while True:
        read_cpu_frequency()
        time.sleep(0.5)  # 每隔 500 毫秒输出一次

if __name__ == "__main__":
    main()
