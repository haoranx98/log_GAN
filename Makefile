CC=gcc
CFLAGS=-shared -fPIC
LIBS=-ldl
TARGET=mmap_logger_multi.so
SOURCE=src/mmap_logger_multi.c
SCRIPT=run_python
SERVER=server
SERVER_SRC=src/server.c
LOG_DIR=log
BUILD_DIR=build
BIN_DIR=bin

# 默认目标：编译共享库、脚本和server
all: $(TARGET) $(SCRIPT) $(SERVER)

# 编译共享库
$(TARGET): $(BUILD_DIR)/mmap_logger_multi.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

$(BUILD_DIR)/mmap_logger_multi.o: $(SOURCE)
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# 编译server
$(SERVER): $(BUILD_DIR)/server.o
	$(CC) -o $(BIN_DIR)/$@ $^

$(BUILD_DIR)/server.o: $(SERVER_SRC)
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $< -o $@

# 生成脚本
$(SCRIPT):
	@mkdir -p $(LOG_DIR)    # 确保log目录存在
	@echo "#!/bin/bash" > $(SCRIPT).sh
	@echo "export LD_PRELOAD=\"./$(TARGET)\"" >> $(SCRIPT).sh
	@echo "python tests/main_core.py 2> $(LOG_DIR)/GAN_core.log" >> $(SCRIPT).sh
	@echo "unset LD_PRELOAD" >> $(SCRIPT).sh
	chmod +x $(SCRIPT).sh

# 清理生成的文件，不删除log、bin、build目录
clean:
	rm -f $(TARGET)
	rm -f $(SCRIPT).sh
	rm -f $(BIN_DIR)/$(SERVER)
	rm -f $(BUILD_DIR)/*.o

# 运行脚本
run: $(SCRIPT)
	./$(SCRIPT).sh
