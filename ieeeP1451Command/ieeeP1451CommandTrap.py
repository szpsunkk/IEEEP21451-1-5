#!/usr/bin/env python
# encoding:utf-8

import socket 
import struct


global addr1 
global addr2 
global port
addr= "192.168.31.102"  
port = 7501 # 设置

# def add_tim_address(timID, address):
# 	dict.append(timID, address)
# 	return dict

def get_int(id):
	return common(id, 0)

def set_int(id, val):
	common(id, val)

def common(id, val):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	print(type(id),type(val))
	print(addr, port)

	s.connect((addr, port))

	# id = 1
	# val = 1024

	msg_tx = struct.pack('>ii', id, val)
	s.send(msg_tx)

	msg_rx = s.recv(1024)

	val = struct.unpack('>i', msg_rx)[0]


	s.close()

	return val
# def set_channel_init(timID, channelID, val):
# 	set_channel(timID, channelID, val)

# def set_channel(timID, channelID, val):
# 	print("begin")
# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# 	if timID == 1:
# 		s.connect((addr1, port))

# 		# id = 1
# 		# val = 1024

# 		msg_tx = struct.pack('>ii', channelID, val)
# 		s.send(msg_tx)

# 		msg_rx = s.recv(1024)

# 		val = struct.unpack('>i', msg_rx)[0]

# 	if timID == 2:

# 		s.connect((addr2, port))

# 		# id = 1
# 		# val = 1024

# 		msg_tx = struct.pack('>ii', channelID, val)
# 		s.send(msg_tx)

# 		msg_rx = s.recv(1024)

# 		val = struct.unpack('>i', msg_rx)[0]

		
# 	s.close()
# 	return val
if __name__ == '__main__':
	try:
		a=set_channel(1,2,0)
		print(a)
	except keyboardInterrupt:
		s.close()		
