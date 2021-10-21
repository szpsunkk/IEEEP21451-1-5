#!/usr/bin/env python
# -*- coding: utf-8 -*-
import S71200
from time import sleep
import snap7
from snap7.util import *
import struct
# Area表示内存区。取值0x84:D区  0x83：M区  0x82：Q区  0x81：I区  0x1C:C区（16Bit）  0x1D：T区（16Bit）
# ！d 1位    !f 4位 
PLC_address_floor = 0x83   # 电梯楼层地址  M 区地址
start_address_M = 0   # 0开门  1关门   3上升  4下降  5上升P  6下降P  7停止
start_address_M = 1   # 2二楼上升  3三楼上升  4四楼上升  5五楼上升  6六楼下降
start_address_M = 2   # 1一楼上升  2二楼下降  3三楼下降  4四楼下降  5五楼下降 
start_address_M = 3   # 6上限报警  7下限报警
start_address_M = 4   # 0平层标志位  1一楼平层 2二楼平层 3三楼平层 4四楼平层 5五楼平层 6六楼平层
start_address_M = 5	  # 1一楼按钮P  ...
start_address_M = 6   # 1电梯在一楼  2电梯在二楼  3电梯在三楼 ...
start_address_M = 12  # 0 非运动状态 1上升标志位 2下降标志位  3减速标志位  6报警  7轿门关 
size = 1

PLC_address_status = 0x82  # 电梯状态   Q 区地址
start_address_staus_1 = 0
start_address_staus_2 = 1
start_address_staus_3 = 2



plc = snap7.client.Client()
plc.set_connection_type(3)
plc.connect("192.168.2.1",0,1)
print("CON STATUS: ", plc.get_connected())

def write(address, start, data, dbnumber = 0):
	value = plc.read_area(address, dbnumber, start, data)
	snap7.util.set_bool(value, dbnumber, start, 1)
	plc.write_area(address, dbnumber, start, value)


def read(address, start, data, dbnumber = 0):
	value = plc.read_area(address, dbnumber, start, data)
	data = struct.unpack('!b', value)
	struct.calcsize('!b')
	#print(data[0])


	return int(data[0])

def pow(num):
	flag = 0
	while True:
		a = num / 2
		num = a
		flag = flag + 1
		if a == 1:
			number = flag
			flag = 0
			break
	return number

def read_status(address, start, value):
	if address == 0x83:
		if start == 0:
			





while 1:
    value = read(PLC_address_M, start_address_floor, size)

    print("楼层数:{:d}".format(pow(value)))
    #value_status = read(PLC_address_floor, start_address_staus_1, size)
    #print("开始:{:d}".format(pow(value_status)))
    #print(pow(value))
    write(PLC_address, start_address, size)
    sleep(0.5)






