#!/usr/bin/env python

# for command line parsing
import getopt, sys
import socket 
import threading
import struct
import GPIO as gpio
import pcf8591 as adc
import smbus
import time

bus = smbus.SMBus(0) # 查询寄存器地址sudo i2cdetect -y 0

port = 7500

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'p:h', ['port=', 'help'])

for opt, arg in options:
	if opt in ('-p', '--port'):
		port = int(arg)
	elif opt in ('-h', '--help'):
		print arg
		print "Transducer interface module (TIM) daemon"
		print "-TBD-"
		exit() # TODO: is it a good practice

# TODO: hardware auto config
# - I2C
# - GPIO

ip = "0.0.0.0"

# listen_num 5 = # TODO:

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def command_handler(sock, addr): # TODO: function name tbd
	print()
	print("Source: %s:%s" % addr)
	msg_rx = sock.recv(2048)
	id, val = struct.unpack('>ii', msg_rx)

	if (id == 0):
		print("read temp")
		val = adc.read_default_device_channel2()
		pass
	elif (id == 1):
		print("read light")
		val = adc.read_default_device_channel3()
	elif (id == 2):
		print("read lamp")
		
		val = gpio.read_gpio_pin('relay1')
		pass
	elif (id == 3):
		print("read humd")

		val = gpio.read_gpio_pin('relay0')
		pass
	elif (id == 4):
		print("write lamp %d" % val)
		if val:
			gpio.write_gpio_pin('relay1', True)
		else:
			gpio.write_gpio_pin('relay1', False)

	elif (id == 5):
		print("write humd %d" % val)
		if val:
			gpio.write_gpio_pin('relay0', True)
		else:
			gpio.write_gpio_pin('relay0', False)

	print("id:%d\t val:%d" % (id, val))
	msg_tx = struct.pack('>i', val)
	sock.send(msg_tx)
	sock.close()

## delay? twice?
def read(chn, address): #channel
    if chn == 0:
        bus.write_byte(address,0x40)   #发送一个控制字节到设备
    if chn == 1:
        bus.write_byte(address,0x41)
    if chn == 2:
        bus.write_byte(address,0x42)
    if chn == 3:
        bus.write_byte(address,0x43)
    bus.read_byte(address)             #从设备读取单个字节，而不指定设备寄存器。
    return bus.read_byte(address)      #返回某通道输入的模拟值A/D转换后的数字值

def write(val):
    temp = val  # 将字符串值移动到temp
    temp = int(temp) # 将字符串改为整数类型
    # print temp to see on terminal else comment out
    bus.write_byte_data(address, 0x40, temp) 
    #写入字节数据，将数字值转化成模拟值从AOUT输出

def Ac_Setup(address):
    bus.write_byte_data(address, 0x22)
    bus.write_byte_data(address, 0x20)
    bus.write_byte_data(address, 0x00)
    bus.write_byte_data(address, 0x05)

def main():
	global address0
	global address1
	address0 = 0x48
	address1 = 0x0a
	####
	gpio.init_gpio_subsystem()

	gpio.register_gpio_pin('relay0', 17, gpio.READ_WRITE)
	gpio.register_gpio_pin('relay1', 27, gpio.READ_WRITE)
	val = gpio.read_gpio_pin('relay0')
	print(val)

	####
	s.bind((ip, port))
	print("Listenning to: %s:%d" % (ip, port))
	s.listen(5) # TODO:
	connection_cnt = 0
	while True:  
		sock, addr = s.accept() 
		connection_cnt += 1
		print("Count: %d" % connection_cnt)
		thread = threading.Thread(target = command_handler, args = (sock, addr))
		thread.start()

if __name__ == '__main__':
	main()
