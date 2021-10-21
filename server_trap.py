#!/usr/bin/env python
# -*- coding: utf-8 -*-
# for command line parsing
import getopt, sys
import socket 
import threading
import struct
import GPIO as gpio
import pcf8591 as adc
import smbus
import time
import RPi.GPIO as GPIO
import dht11

bus = smbus.SMBus(0) # 查询寄存器地址sudo i2cdetect -y 0
TRIG = 17
ECHO = 27
port = 7501
pin_1 = 18
pin_2 = 23
Pin_3 = 24
pin_4 = 25
global Temp_sensor BuzzerPin
Temp_sensor=21  # 温度湿度gpio
BuzzerPin = 20 # buzzer 控制器
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

def command_handler(sock, addr, TRIG, ECHO): # TODO: function name tbd
	print()
	print("Source: %s:%s" % addr)
	msg_rx = sock.recv(2048)
	id, val = struct.unpack('>ii', msg_rx)
	if (id == 999):
		val = 1
	# if (id == 10):  # 读取seTemperature
	# 	print("read temp")
	# 	val = ReadTemperature_humidity(1)  
	# 	pass
	# elif (id == 11):  # 读取seLight
	# 	print("read light")
	# 	val = read(1, I2CAddress0)
	# 	pass
	# elif (id == 12): # 测量seHumidity
	# 	print("read humd")
	# 	val = ReadTemperature_humidity(2)
	# 	pass
	# elif (id == 13):  # 读取seDistence
	# 	print("read distence")
	# 	val = ReadDistenceHC(TRIG, ECHO)
	# 	pass
	# elif (id == 14): # 读取seAcceleration_x
	# 	print("read acceleration_x")
	# 	val = ReadAcc(I2CAddress1)
	# 	val = val[0]
	# 	pass
	# elif (id == 15):
	# 	print("read acceleration_y")
	# 	val = ReadAcc(I2CAddress1)
	# 	val = val[1]
	# 	pass
	# elif (id == 16):
	# 	print("read acceleration_z")
	# 	val = ReadAcc(I2CAddress1)
	# 	val = val[2]
	# 	pass
	# elif(id == 17): # 读取seHS
	# 	print("read HS sensor")
	# 	val = read(3, I2CAddress0)
	# 	pass
	# elif(id == 18): # 
	# 	print("read voltage")
	# 	val = 5 # V
	# 	pass
	# elif (id == 19):
	# 	print("read current")
	# 	val = 51  # mA
	# 	pass
	# elif (id == 110):
	# 	print("read power")
	# 	val = 0.25
	# 	pass
	# elif(id == 111): # 读取presure
	# 	val = 10
	# 	pass
	# elif (id == 20): # 执行 acLamp
	# 	print("write lamp %d" % val)
	# 	if val:
	# 		gpio.write_gpio_pin('relay0', True)
	# 	else:
	# 		gpio.write_gpio_pin('relay0', False)
	# elif (id == 21): # 执行 acHunidifier
	# 	print("write lamp %d" % val)
	# 	if val:
	# 		gpio.write_gpio_pin('relay1', True)
	# 	else:
	# 		gpio.write_gpio_pin('relay1', False)
	# elif (id == 22): # 执行 acbuzzer
	# 	print("write lamp %d" % val)
	# 	if val:
	# 		buzzer(val)
	# 	else:
	# 		buzzer(val)
	# elif (id == 23): # 执行 acLEDScreen
	# 	print("write lamp %d" % val)
	# 	if val:
	# 		gpio.write_gpio_pin('relay3', True)
	# 	else:
	# 		gpio.write_gpio_pin('relay3', False)


	print("id:%d\t val:%d" % (id, val))
	msg_tx = struct.pack('>i', val)
	sock.send(msg_tx)
	sock.close()

def ReadTemperature_humidity(flag):
	#define GPIO 14 as DHT11 data pin
	
	# Main program block
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
	# Initialise display
	#  lcd_init()
	instance = dht11.DHT11(pin = Temp_sensor)
	#get DHT11 sensor value
	result = instance.read()
	#print"Temperature = ",result.temperature,"C"," Humidity = ",result.humidity,"%"
	if (flag == 1):
		return result.temperature
	else:
		return result.humidity


def ReadAcc(I2CAddress): # 读取加速度信息
	data_acc_x = bus.read_byte_data(I2CAddress, 0x04)
	data_acc_y = bus.read_byte_data(I2CAddress, 0x06)
	data_acc_z = bus.read_byte_data(I2CAddress, 0x08)
	acc_x = data_acc_x / 16
	acc_y = data_acc_y / 16
	acc_z = data_acc_z / 16
	acc = [acc_x, acc_y, acc_z]
	return acc 


def ReadDistenceHC(TRIG, ECHO):  # 测距

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
	GPIO.output(TRIG, True)
	time.sleep(0.001)
	GPIO.output(TRIG, False)
	while GPIO.input(ECHO) == 0:
		pass
	pulse_start = time.time()

	while GPIO.input(ECHO) == 1:
		pass
	pulse_end = time.time()

	puluse_duration = pulse_end - pulse_start
	distence  = puluse_duration * 343 / 2 * 100
	distence = round(distence, 2)
	print("distence: {}cm".format(distence))
	GPIO.cleanup()
	return distence 


def ReadDistenceNoopLoop():
	ser = serial.Serial("/dev/ttyAMA0", 115200) # 串口操作， 加速度计
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
        			
        			p = dat[i+12]+dat[i+13]*255
        			print("strength = ")
        			
        			q = dat[i+8]+dat[i+9]*255
        			print("distence = ")

def buzzer(flag):
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    if (flag == 1):
    	GPIO.output(BuzzerPin, GPIO.LOW) # 低电平响
    else:
    	GPIO.output(BuzzerPin, GPIO.HIGH)


## delay? twice?
def read(chn, address): #channel   # 读取PCF寄存器数据
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
	global I2CAddress0
	global I2CAddress1
	I2CAddress0 = 0x48  # PCF8592地址
	I2CAddress1 = 0x23  # 加速度计地址
	####
	gpio.init_gpio_subsystem()

	gpio.register_gpio_pin('relay0', pin_1, gpio.READ_WRITE)
	gpio.register_gpio_pin('relay1', pin_2, gpio.READ_WRITE)
	gpio.register_gpio_pin('relay2', Pin_3, gpio.READ_WRITE)
	gpio.register_gpio_pin('relay3', pin_4, gpio.READ_WRITE)
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
		thread = threading.Thread(target = command_handler, args = (sock, addr, TRIG, ECHO))
		thread.start()

if __name__ == '__main__':
	main()
