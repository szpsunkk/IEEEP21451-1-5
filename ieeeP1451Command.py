#!/usr/bin/env python

import socket 
import struct

port = 7500
addr = "192.168.43.204"

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
if __name__ == '__main__':
	try:
		get_int(1)
	except keyboardInterrupt:
		s.close()		
