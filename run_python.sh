#!/bin/bash
export LD_PRELOAD="./lib/mmap_logger_multi.so"
python scripts/mini_GAN_MNIST.py 2> log/mini_GAN.log
unset LD_PRELOAD
