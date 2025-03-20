1. 首先执行

```shell
make all
```

 来编译src/lib中的syscall_logger_phy.c和src中的server.c

2. 新建两个终端，其中一个先执行

```
sudo ./bin/server
```

，另一个执行

```shell
LD_PRELOAD=./libs/syscall_logger_phy.so python scripts/test/mini_GAN_MNIST_single_core.py > ./log/phy_ddr4_2666_32G.log 
```



3.将log文件转换为csv格式

```shell
 python scripts/log2csv.py ./log/phy_ddr4_2666_32G.log ./csv/phy_ddr4_2666_32G.csv
```

4.处理csv文件，提取需要的系统调用,生成trace文件

```
python scripts/csv2trace.py ./csv/phy_ddr4_2666_32G.csv ./trace/phy_ddr4_2666_32G.trace
```

5.处理trace文件，将trace中的每次访存操作的执行时间转换为时间戳

```
python scripts/process_trace.py ./trace/phy_ddr4_2666_32G.trace ./trace/phy_ddr4_2666_32G_0.trace
```

