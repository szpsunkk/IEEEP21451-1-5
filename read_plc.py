#!/usr/bin/env python
# -*- coding: utf-8 -*-
import snap7
from snap7.util import *
from snap7.snap7types import *
import time

def ReadMemory(self,byte,bit,datatype):
  result=self.read_area(0x83,0,byte,datatype)
  if datatype==S7WLBit:  #这里的datatype应该可以写数字（参照上面写入output），或者像这里直接写类型
      return get_bool(result,0,bit)
  if datatype==S7WLByte or datatype==S7WLWord:
      return int(get_int(result,0))/256
  if datatype==S7WLReal:        #elif更好
      return get_real(result,0)
  if datatype==S7WLDWord:
      return get_dword(result,0)

myplc=snap7.client.Client()
myplc.connect('192.168.2.1', rack=0,slot=1)
flag = 0
while 1:
	print('bool型',type(ReadMemory(myplc,2,0,S7WLBit))
	#print('byte型',type(ReadMemory(myplc,2,0,S7WLByte)))
	print('Word型',ReadMemory(myplc,2,0,S7WLWord))
	print('Real型',ReadMemory(myplc,2,0,S7WLReal))
	print('Dword型',ReadMemory(myplc,2,0,S7WLDWord))
	time.sleep(2)



