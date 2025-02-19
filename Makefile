# 编译器
CC = gcc
# 编译选项
CFLAGS = -g -Wall
PICFLAGS = -fPIC
# 链接选项
LDFLAGS = -shared

# 目录
SRC_DIR = src
LIB_DIR = $(SRC_DIR)/lib
TESTS_DIR = $(SRC_DIR)/tests
BUILD_DIR = build
BIN_DIR = bin
LIBS_DIR = libs

# 获取 lib 目录下的所有 .c 文件
LIB_SRCS = $(wildcard $(LIB_DIR)/*.c)
# 获取 tests 目录下的所有 .c 文件
TESTS_SRCS = $(wildcard $(TESTS_DIR)/*.c)
# 获取 src 目录下的所有 .c 文件（不包括 lib 和 tests 目录）
SRC_SRCS = $(filter-out $(LIB_SRCS) $(TESTS_SRCS), $(wildcard $(SRC_DIR)/*.c))

# 将 .c 文件转换为 .o 文件，并放到 build 目录
LIB_OBJS = $(patsubst $(LIB_DIR)/%.c, $(BUILD_DIR)/%.o, $(LIB_SRCS))
TESTS_OBJS = $(patsubst $(TESTS_DIR)/%.c, $(BUILD_DIR)/%.o, $(TESTS_SRCS))
SRC_OBJS = $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SRC_SRCS))

# 将 .c 文件转换为 .so 文件，并放到 libs 目录
LIB_SOS = $(patsubst $(LIB_DIR)/%.c, $(LIBS_DIR)/%.so, $(LIB_SRCS))

# 将 .c 文件转换为可执行文件，并放到 bin 目录
TESTS_BINS = $(patsubst $(TESTS_DIR)/%.c, $(BIN_DIR)/%, $(TESTS_SRCS))
SRC_BINS = $(patsubst $(SRC_DIR)/%.c, $(BIN_DIR)/%, $(SRC_SRCS))

# 默认目标
all: prepare $(LIB_SOS) $(TESTS_BINS) $(SRC_BINS)

# 创建 bin、build 和 libs 目录
prepare:
	mkdir -p $(BUILD_DIR) $(BIN_DIR) $(LIBS_DIR)

# 编译 lib 目录下的 .c 文件为 .so 文件
$(LIBS_DIR)/%.so: $(LIB_DIR)/%.c
	$(CC) $(CFLAGS) $(PICFLAGS) -c $< -o $(BUILD_DIR)/$*.o
	$(CC) $(LDFLAGS) $(BUILD_DIR)/$*.o -o $@

# 编译 tests 目录下的 .c 文件为可执行文件
$(BIN_DIR)/%: $(TESTS_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $(BUILD_DIR)/$*.o
	$(CC) $(BUILD_DIR)/$*.o -o $@

# 编译 src 目录下的 .c 文件为可执行文件
$(BIN_DIR)/%: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $(BUILD_DIR)/$*.o
	$(CC) $(BUILD_DIR)/$*.o -o $@

# 清理生成的文件
clean:
	rm -rf $(BUILD_DIR)/*.o $(LIBS_DIR)/*.so $(BIN_DIR)/*
	rmdir $(LIBS_DIR) $(BUILD_DIR) $(BIN_DIR) 2>/dev/null || true