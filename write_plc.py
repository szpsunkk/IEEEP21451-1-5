#!/usr/bin/env python
# -*- coding: utf-8 -*-
import snap7
from snap7.util import *
from snap7.snap7types import *

areas = ADict({
  'PE': 0x81,  #input 输入区
  'PA': 0x82,  #output 输出区
  'MK': 0x83,  #bit memory 中间存储区（M区）
  'DB': 0x84,  #DB区
  'CT': 0x1C,  #counters
  'TM': 0x1D,  #Timers
})


def WriteMemory(self, byte, bit, datatype, value):   # 例如M2.0  ： byte 为2    bit 为0      datatype类型选择S7WLBit  value（True or False）
	result = self.read_area(0x83, 0, byte, datatype)
	if datatype  == S7WLBit:
		set_bool(result, 0, bit, value)
	if datatype == S7WLByte or datatype == S7WLWord:
		set_int(result, 0, value)
	if datatype == S7WLReal:
		set_real(result, 0, value)
	if datatype == S7WLWord:
		set_dword(result, 0, value)
	self.write_area(0x83, 0, byte, result)

plc = snap7.client.Client()
plc.connect('192.168.2.1', rack = 0, slot = 1)

WriteMemory(plc, 5, 3, S7WLBit, True)
# WriteMemory(plc, 1, 2, S7WLBit, True)
# WriteMemory(plc, 11, 0, S7WLByte, 2048)
# WriteMemory(plc,12,0,S7WLWord,32)
# WriteMemory(plc,14,0,S7WLReal,3.14159)
# WriteMemory(plc,18,0,S7WLDWord,1132818)