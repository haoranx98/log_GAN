CC=gcc
CFLAGS=-shared -fPIC
LIBS=-ldl
TARGET=lib/mmap_logger_multi.so
SOURCE=src/mmap_logger_multi.c
SERVER=server
SERVER_SRC=src/server.c
LOG_DIR=log
BUILD_DIR=build
BIN_DIR=bin
TEST_DIR=src/tests
BIN_TEST_DIR=bin/tests

# 默认目标：编译共享库、脚本、server
all: $(TARGET) $(SERVER)

# 编译共享库，将.so文件放到lib目录
$(TARGET): $(BUILD_DIR)/mmap_logger_multi.o
	@mkdir -p lib  # 确保lib目录存在
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

$(BUILD_DIR)/mmap_logger_multi.o: $(SOURCE)
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# 编译server，并生成到bin目录
$(SERVER): $(BUILD_DIR)/server.o
	@mkdir -p $(BIN_DIR)
	$(CC) -o $(BIN_DIR)/$@ $^

$(BUILD_DIR)/server.o: $(SERVER_SRC)
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $< -o $@

# 生成脚本，支持传入 Python 脚本和日志文件名
script:
	@mkdir -p $(LOG_DIR)    # 确保log目录存在
	@if [ -z "$(PYTHON_SCRIPT)" ]; then \
		echo "Error: PYTHON_SCRIPT must be specified"; \
		exit 1; \
	fi
	@if [ -z "$(LOG_FILE)" ]; then \
		echo "Error: LOG_FILE must be specified"; \
		exit 1; \
	fi
	@echo "#!/bin/bash" > run_python.sh
	@echo "export LD_PRELOAD=\"./$(TARGET)\"" >> run_python.sh
	@echo "python $(PYTHON_SCRIPT) 2> $(LOG_DIR)/$(LOG_FILE)" >> run_python.sh
	@echo "unset LD_PRELOAD" >> run_python.sh
	chmod +x run_python.sh

# 清理生成的文件，不删除log、bin、build目录
clean:
	rm -f $(TARGET)
	rm -f run_python.sh
	rm -f $(BIN_DIR)/$(SERVER)
	rm -f $(BUILD_DIR)/*.o
	rm -f $(BIN_TEST_DIR)/test_*

# 运行脚本
run: script
	./run_python.sh

# 编译src/tests下的所有C文件并生成对应的可执行文件
test: $(patsubst src/tests/%.c,$(BIN_TEST_DIR)/test_%, $(wildcard $(TEST_DIR)/*.c))

$(BIN_TEST_DIR)/test_%: $(TEST_DIR)/%.c
	@mkdir -p $(BIN_DIR)
	$(CC) -o $@ $<