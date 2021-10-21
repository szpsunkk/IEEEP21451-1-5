#!/usr/bin/env python

'Driver code of PCF8591 analog digital converter'

import i2c
import time
# This address depends on hardware configuration, specifically, 
# how pin A0, A1 and A2 are wired.
# See: https://www.nxp.com/docs/en/data-sheet/PCF8591.pdf
device_addr_list = [0x48]

read_commands_for_different_channels = [0x40, 0x41, 0x42, 0x43]

def _read_device_channel(device_addr, channel):
	i2c.i2cbus.write_byte(device_addr, read_commands_for_different_channels[channel])
	i2c.i2cbus.read_byte(device_addr)
	return i2c.i2cbus.read_byte(device_addr)

def _read_default_device_channel(channel):
	return _read_device_channel(device_addr_list[0], channel)

def read_default_device_channel0():
	return _read_default_device_channel(0)

def read_default_device_channel1():
	return _read_default_device_channel(1)

def read_default_device_channel2():
	return _read_default_device_channel(2)/5

def read_default_device_channel3():
	return 1-(_read_default_device_channel(3)/255)

if __name__ == '__main__':
	while True:
		print(read_default_device_channel0())
		print(read_default_device_channel1())
		print(read_default_device_channel2())
		print(read_default_device_channel3())
		time.sleep(1)
