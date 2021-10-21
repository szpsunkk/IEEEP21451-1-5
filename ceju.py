#!/usr/bin/env python
# -*- coding: utf-8 -*

import serial

import time

# 打开串口

ser = serial.Serial("/dev/ttyAMA0", 115200)

def main():

    while True:

        # 获得接收缓冲区字符

        count = ser.inWaiting()
        if count >=32:
        	dat = ser.read(count)
			print(dat)
            for i in range(16):
        		if dat[i] == 0x57 and dat[i+1] == 0xff and dat[i+2] == 0 :
        			if dat[i+12]+dat[i+13]*255==0 :
        				print("out of range!")
        			else:
        				z=dat[i+11]
        				print("status = ")
        				print(z)
        				p = dat[i+12]+dat[i+13]*255
        				print("strength = ")
        				print(p)
        				q = dat[i+8]+dat[i+9]*255
        				print("distence = ")
        				print(q)	

        if count != 0:

            # 读取内容并回显

            recv = ser.read(count)

            ser.write(recv)
	    print("%s" %(recv))

        # 清空接收缓冲区

        ser.flushInput()

        # 必要的软件延时

        time.sleep(1)

    

if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:

        if ser != None:

            ser.close()
