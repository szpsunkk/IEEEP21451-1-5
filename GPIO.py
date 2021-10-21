#!/usr/bin/env python

'Driver code of GPIO'

import RPi.GPIO

#### TODO: colored led wrapper
#### TODO: configuration file or something alike
#### why word global is needed?

# data structure that stores all gpio pin instances
gpio_pin_collection	= {}

READ_ONLY		= RPi.GPIO.IN
READ_WRITE		= RPi.GPIO.OUT

def register_gpio_pin(name, pin, permission, default_val=False):
	if name in gpio_pin_collection:
		print("Name \"%s\" already exsists. The pin's information will be updated." % name)
	gpio_pin_collection[name] = GpioPin(name, pin, permission, default_val)

def print_gpio_pin_collection():
	pass # TODO:

def _convert_to_py_boolean(val):
	if val:
		return True
	else:
		return False

class GpioPin(object):
	def __init__(self, name, pin, permission, default_val=False):
		self.name	= name
		self.pin	= pin
		self.permission	= permission
		self.status	= None # later handled in _change_status()

		# let some of these attributes take effect
		self._set_permission()
		self._change_status(default_val)

	def __repr__(self):
		return "<GpioPin object named \"" + self.name +"\">"

	def __str__(self):
		return "member of Test" # TODO:

	#### Helper Functions ####

	# configure the physical pin's permission as per the value in memory (self.permission)
	def _set_permission(self):
		RPi.GPIO.setup(self.pin, self.permission)

	# update the value in memory (self.status) according to what the physical pin senses
	def _read_status(self):
		self.status = _convert_to_py_boolean(RPi.GPIO.input(self.pin))
	
	# write the value in memory (self.status) to the physical pin
	def _write_status(self):
		RPi.GPIO.output(self.pin, self.status)
	
	def _change_status(self, val):
		self.status = _convert_to_py_boolean(val)
		self._write_status()
	
	#### Read Operations ####
	def read(self):
		self._read_status()
		return self.status

	def info(self):
		self._read_status()
		print("name: %s\tpin:%d\tstatus:%s" % (self.name, self.pin, self.status)) # TODO: complete and make it return a string

	#### Write Operations ####
	def on(self):
		self._change_status(True)

	def off(self):
		self._change_status(False)

	def toggle(self):
		self._change_status(not self.read())

def init_gpio_subsystem():
	RPi.GPIO.setmode(RPi.GPIO.BCM)

def shut_down_gpio_subsystem():
	RPi.GPIO.cleanup()

def write_gpio_pin(name, val):
	if val:
		gpio_pin_collection[name].on()
	else:
		gpio_pin_collection[name].off()

def read_gpio_pin(name):
	return gpio_pin_collection[name].read()


if __name__ == '__main__':
	try:
		init_gpio_subsystem()

		#### For Demo System Ver 3.0 ####
		register_gpio_pin('relay0', 11, READ_WRITE)
		register_gpio_pin('relay1', 13, READ_WRITE)

		gpio_pin_collection['relay0'].on() # TODO: further encapsualte
		gpio_pin_collection['relay1'].on()

		while True:
			pass

	except KeyboardInterrupt:
		print("Keyboard interrupt captured. The system will be shut down.")
		shut_down_gpio_subsystem()


#### in the terminal or other scripts ####

'''
import hw.gpio as gpio
gpio.init_gpio_subsystem()
gpio.register_gpio_pin('relay0', 17, gpio.READ_WRITE)
gpio.register_gpio_pin('relay1', 27, gpio.READ_WRITE)
# lower level
gpio.gpio_pin_collection['relay0'].read()
gpio.gpio_pin_collection['relay0'].on()
# higher level
gpio.write_gpio_pin('relay0', True)
gpio.read_gpio_pin('relay0')
gpio.shut_down_gpio_subsystem()
'''