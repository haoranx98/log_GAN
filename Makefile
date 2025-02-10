CC=gcc
CFLAGS=-shared -fPIC
LIBS=-ldl
TARGET=mmap_logger_multi.so
SOURCE=mmap_logger_multi.c
SCRIPT=run_python

all: $(TARGET) $(SCRIPT)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

$(SCRIPT):
	@echo "#!/bin/bash" > $(SCRIPT).sh
	@echo "export LD_PRELOAD=\"./$(TARGET)\"" >> $(SCRIPT).sh
	@echo "python tests/main_core.py 2> GAN_core.log" >> $(SCRIPT).sh
	@echo "unset LD_PRELOAD" >> $(SCRIPT).sh
	chmod +x $(SCRIPT).sh

clean:
	rm -f $(TARGET)
	rm -f $(SCRIPT).sh

run: $(SCRIPT)
	./$(SCRIPT).sh

