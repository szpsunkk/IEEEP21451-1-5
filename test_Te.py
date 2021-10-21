#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for command line parsing
import getopt, sys
import socket 
import threading
import struct
import GPIO as gpio
import pcf8591 as adc
import time

def delayMicrosecond(t):    # 微秒级延时函数
    start,end=0,0           # 声明变量
    start=time.time()       # 记录开始时间
    t=(t-3)/1000000     # 将输入t的单位转换为秒，-3是时间补偿
    while end-start<t:  # 循环至时间差值大于或等于设定值时
        end=time.time()     # 记录结束时间


def main():
    gpio.init_gpio_subsystem()
    gpio.register_gpio_pin('relay0', 17, gpio.READ_WRITE)
    
    while True:
        val = gpio.read_gpio_pin('relay0')
        print(val)
        time.sleep(2)
    


if __name__ == '__main__':
    main()